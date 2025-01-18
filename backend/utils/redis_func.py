import redis

def create_redis_client():
    connect_string = 'redis://default:VXBhCLDuIQmAbzuQdfNxMZhedkGQTPvw@monorail.proxy.rlwy.net:26453'
    client = redis.from_url(connect_string)
    return client
