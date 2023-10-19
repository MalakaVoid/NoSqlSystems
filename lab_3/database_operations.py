import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_user_existance(username):
    return r.exists(f'user:{username}')

def add_new_user(username, password):
    try:
        if r.exists(f'user:{username}'):
            return 501
        else:
            r.hset(f'user:{username}', 'username', username)
            r.hset(f'user:{username}', 'passwd', password)
    except Exception as e:
        return 404
    return 200

def auth_usr_checker(username, password):
    code = 404
    if r.exists(f'user:{username}'):
        if r.hget(f'user:{username}', 'passwd') == password:
            code = 200
        else:
            code = 501
    else:
        code = 404
    return code