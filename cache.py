import redis

client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

def set_cache(key, value, ttl):
    client.set(key, value, ex=ttl)

def get_cache(key):
    return  client.get(key)