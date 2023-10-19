import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def test():
    # print(r.keys('*:SleepWalker'))
    r.lpush('test', '123')
    r.lpush('test', '123')

def add_user_to_chat(username, chat_title):
    r.lpush(f"chat:{chat_title}:users", username)
    r.lpush(f"user:chats:{username}", chat_title)

def create_chat(username, title, description, users):
    r.hset(f'chat:{title}', "title", title)
    r.hset(f'chat:{title}', "description", description)
    r.hset(f'chat:{title}', "creator", username)
    add_user_to_chat(username, title)
    for each in users:
        add_user_to_chat(each, title)

def get_all_user_chats_titles(username):
    chats = []
    if r.exists(f'user:chats:{username}'):
        chats = r.lrange(f'user:chats:{username}',0, -1)
    else:
        r.lpush(f'user:chats:{username}', "o")
        r.lpop(f'user:chats:{username}', 1)
        chats = r.get(f'user:chats:{username}')
    return chats

def check_title_chat_existence(title):
    return r.exists(f'chat:{title}')
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