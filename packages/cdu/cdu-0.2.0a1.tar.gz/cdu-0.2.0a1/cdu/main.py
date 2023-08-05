"""Utility to calculate disk usage on cloud services"""

import sys
import argparse
from six.moves.urllib.parse import urlparse
import boto3
import json
from .node import Node
from .progress import Progress
import time
import gzip
import sqlite3
from datetime import datetime
import os.path

FORMAT_VERSION = 1


def main():
    """Entry-point when running the module as an executable"""

    parser = argparse.ArgumentParser(
        description="Utility to calculate disk usage on cloud services"
    )
    parser.add_argument('--include-files', dest='include_files', action='store_true')
    parser.add_argument('-p', metavar='aws_profile_name', type=str,
                        help='The name of the aws profile, defined in ~/.aws/credentials',
                        default=None, required=False)
    parser.add_argument('url', type=str, help="S3 URL to process")
    parser.set_defaults(include_files=False)
    args = parser.parse_args()

    url = urlparse(args.url)

    if url.scheme == 's3':
        session = boto3.Session(profile_name=args.p)
        s3_client = session.client('s3')

        bucket = url.netloc
        # remove the first slash
        prefix = url.path[1:]
        if prefix == '/':
            # remove the last slash as well if present
            prefix = prefix[:-1]

        output_filename = '%s_%s.cdu' % (
            bucket,
            datetime.now().strftime('%Y-%m-%d_%H-%M')
        )
        if os.path.exists(output_filename):
            raise Exception("File already exists")
        
        db = sqlite3.connect(output_filename)

        cursor = db.cursor()
        cursor.execute("CREATE table metadata (key TEXT, value TEXT)")
        cursor.executemany("INSERT INTO metadata VALUES (?,?)", (
            ('version', 1),
            ('bucket', bucket),
            ('prefix', prefix),
            ('timestamp', int(time.time()))
        ))

        cursor.execute("CREATE TABLE pathinfo (parent TEXT, info TEXT)")
        cursor.execute("CREATE INDEX parent ON pathinfo(parent)")

        node = Node(bucket, prefix, s3_client, progress_bar=Progress(sys.stderr), include_files=args.include_files)
        cursor.executemany(
            "INSERT INTO pathinfo VALUES (?,?)",
            (
                (x.parent, json.dumps(x.to_json())) for x in node.disk_usage()
            )
        )

        db.commit()
        db.close()

    else:
        raise Exception('Unsupported url: "%s". At the moment only s3:// is supported' % args.url)


if __name__ == "__main__":
    main()
