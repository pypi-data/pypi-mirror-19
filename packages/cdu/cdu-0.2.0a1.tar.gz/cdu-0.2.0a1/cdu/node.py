from .pathinfo import PathInfo


class Node:
    def __init__(self, bucket, prefix, s3_client, progress_bar, include_files=False):
        self.bucket = bucket
        self.prefix = prefix
        self.s3_client = s3_client
        self.include_files = include_files
        self.files = []
        self.nodes = []
        self.progress_bar = progress_bar
        self.data = None

    @classmethod
    def from_dict(cls, obj):
        result = Node()
        self.prefix = obj['Key']


    @property
    def list(self):
        first = True
        result = {}
        while first or 'NextContinuationToken' in result:
            if first:
                result = self.s3_client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=self.prefix,
                    Delimiter='/'
                )
            else:
                result = self.s3_client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=self.prefix,
                    Delimiter='/',
                    ContinuationToken=result['NextContinuationToken']
                )
            first = False
            for prefix in result.get('CommonPrefixes', []):
                yield prefix

            for content in result.get('Contents', []):
                yield content

    def disk_usage(self):
        """ Recursively compute disk usage for all children
        """
        # one key/value for each storage class
        self.data = PathInfo(self.prefix)

        self.progress_bar.update("s3://%s/%s" % (self.bucket, self.prefix))
        for key in self.list:
            if 'Prefix' in key:
                # this is a subdirectory, going deeper
                node = Node(self.bucket, key['Prefix'], self.s3_client, self.progress_bar, self.include_files)
                last_item = None
                for item in node.disk_usage():
                    last_item = item
                    yield item
                if last_item:
                    # only add the last item in a directory to the total count
                    self.data.add_directory(last_item)
            else:
                path_info = PathInfo(key['Key'])
                path_info.add_file(key)
                self.data.add_file(key)
                if self.include_files:
                    yield path_info

        yield self.data

    def __repr__(self):
        return 's3://%s/%s' % (self.bucket, self.prefix)
