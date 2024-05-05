import diskcache as dc

cache=dc.Cache('tmp')

iterkeys = [k for k in cache.iterkeys()]
print('iterkeys:')
print(iterkeys)
print(cache._sql('SELECT key, value FROM Cache').fetchall())

for key in cache:
    try:
        print(key+':'+cache[key])
    except KeyError:
        print(key+' expired')