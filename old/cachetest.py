import diskcache as dc

cache=dc.Cache('tmp')

cache.set('to_expire', 'this-is-value', expire=20)
cache.set('not_expire', 'this-is-value')

for key in cache:
    print(key+':'+cache[key])