from collections import defaultdict
from time import mktime


class PathInfo:
    def __init__(self, key):
        if key and key[-1] == '/':
            key = key[:-1]
        self.key = key
        self.storage_classes = defaultdict(StorageClassInfo)

    def __repr__(self):
        return '<PathInfo: %s, %d bytes, %d files>' % (
            self.key,
            self.size,
            self.file_count,
        )

    @property
    def file_count(self):
        return sum([x.file_count for x in self.storage_classes.values()])

    @property
    def size(self):
        return sum([x.size for x in self.storage_classes.values()])

    @property
    def ts_min(self):
        return min([x.ts_min for x in self.storage_classes.values()])

    @property
    def ts_max(self):
        return max([x.ts_max for x in self.storage_classes.values()])

    def add_file(self, file):
        self.storage_classes[file['StorageClass']].add_file(file)

    def add_directory(self, directory):
        for storage_class, info in directory.storage_classes.items():
            self.storage_classes[storage_class].add(info)

    @property
    def parent(self):
        # reverse the string, split it by / once, grab the second segment
        # and reverse again
        print([self.key])
        if not self.key:
            return None
        if "/" not in self.key:
            return ""
        return self.key[::-1].split('/', 1)[1][::-1]

    def to_json(self):
        return {
            'key': self.key,
            'data': dict((x[0], x[1].to_json()) for x in self.storage_classes.items())
        }


class StorageClassInfo:
    def __init__(self):
        self.file_count = 0
        self.size = 0
        self.ts_min = None
        self.ts_max = None

    @staticmethod
    def __timestamp_from_datetime(dt):
        """Python 2.7 doesn't have a datetime.timestamp method"""
        return mktime(dt.timetuple())

    @staticmethod
    def __func_none(f, a, b):
        """Return f(a,b), unless a or b are None, in which case return the other one.
        Usefull for min/max"""
        if a is None:
            return b
        elif b is None:
            return a
        return f(a, b)

    def add(self, new):
        self.file_count += new.file_count
        self.size += new.size
        self.ts_min = StorageClassInfo.__func_none(min, self.ts_min, new.ts_min)
        self.ts_max = StorageClassInfo.__func_none(max, self.ts_max, new.ts_max)

    def add_file(self, new_file):
        self.file_count += 1
        self.size += new_file['Size']
        self.ts_min = StorageClassInfo.__func_none(
            min, self.ts_min,
            StorageClassInfo.__timestamp_from_datetime(new_file['LastModified'])
        )
        self.ts_max = StorageClassInfo.__func_none(
            max, self.ts_max,
            StorageClassInfo.__timestamp_from_datetime(new_file['LastModified'])
        )

    def __repr__(self):
        return '<StorageClassInfo: %d, %d>' % (
            self.file_count,
            self.size,
        )

    def to_json(self):
        return {
            'file_count': self.file_count,
            'size': self.size,
            'ts_min': int(self.ts_min),
            'ts_max': int(self.ts_max),
        }
