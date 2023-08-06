from rmtest.disposableredis import DisposableRedis


def testme():

    dr = DisposableRedis()

    with dr as r:

        r.set('foo', 'bar')

        for _ in r.retry_with_rdb_reload():
            
            print r.get('foo')

testme()