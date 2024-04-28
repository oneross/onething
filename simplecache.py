import diskcache as dc

class SimpleCache(dc.Cache):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return None
