import json
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def send_message_to_chat(username, text):
    id_m = r.get('chat:messages:id')
    message_ex = {
        "message_id": int(id_m)+1,
        "user_name": username,
        "text": text
    }
    r.lpush('chat:messages', json.dumps(message_ex))
    r.publish('reset_hndl', 'start')
    r.set('chat:messages:id', int(id_m)+1)


def get_all_chat_messages():
    messages_str = r.lrange('chat:messages', 0, -1)
    messages_json = []
    for each in reversed(messages_str):
        messages_json.append(json.loads(each))
    return messages_json

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


#------------------- USELESS FOR NOW ------------------

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