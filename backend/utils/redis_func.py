import redis

def create_redis_client():
    connect_string = 'redis://default:VXBhCLDuIQmAbzuQdfNxMZhedkGQTPvw@monorail.proxy.rlwy.net:26453'
    client = redis.from_url(connect_string)
    return client

def get_code_from_redis(user_type, user_id):
    redis_client = create_redis_client()
    new_code = redis_client.hget(f'{user_type}:{user_id}', 'code').decode('utf-8')
    return new_code