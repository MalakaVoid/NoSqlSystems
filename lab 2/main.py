import json
import random
from jsonschema import validate
from globals import CHAT_TYPES, SEXES
import generation_data as g_d
chat_ids = 0
user_ids = 0
mes_ids = 0

def create_a_main_data() -> dict:
    main_dict = dict()
    main_dict['chats'] = []
    for i in range(0, random.randint(1, 3)):
        main_dict['chats'].append(create_chat_exmp())
    return main_dict


def create_chat_exmp() -> dict:
    global chat_ids
    chat = dict()
    chat['chat_id'] = chat_ids
    chat_ids += 1
    chat['chat_type'] = random.choice(CHAT_TYPES)
    chat['title'] = g_d.get_random_string()
    chat['description'] = g_d.get_random_long_text()
    chat['users'] = []
    chat['message_history'] = []

    for i in range(0, random.randint(2, 5)):
        chat['users'].append(create_user_exmp())
    for i in range(0, random.randint(0, 5)):
        chat['message_history'].append(create_message_exmp())

    return chat


def create_user_exmp() -> dict:
    global user_ids
    user = dict()
    user['user_id'] = user_ids
    user_ids += 1
    user['username'] = g_d.get_random_string()
    user['first_name'] = g_d.get_random_string()
    user['last_name'] = g_d.get_random_string()
    user['registration_date'] = g_d.get_random_date()
    user['sex'] = random.choice(SEXES)
    user['mail'] = []

    for i in range(0, random.randint(0, 3)):
        user['mail'].append(g_d.get_random_email())

    return user


def create_message_exmp() -> dict:
    global mes_ids
    message = dict()
    message['message_id'] = mes_ids
    mes_ids += 1
    message['date'] = g_d.get_random_date()
    message['user_id'] = 0 #IDK HOW TO DO IT NOW, THINK LATER!!!!
    message['text'] = g_d.get_random_long_text()
    message['has_photo'] = random.choice([True, False])

    if message['has_photo']:
        message['photo'] = g_d.get_random_string()
        message['caption'] = g_d.get_random_string()
    else:
        message['photo'] = None
        message['caption'] = None

    return message


def create_correct_json_file():
    result_dict = create_a_main_data()
    f = open("1-c.json", "w")
    json.dump(result_dict, f, indent=4)
    result_dict = create_a_main_data()
    f = open("2-c.json", "w")
    json.dump(result_dict, f, indent=4)
    result_dict = create_a_main_data()
    f = open("3-c.json", "w")
    json.dump(result_dict, f, indent=4)

def validate_data():
    f = open("1-c.json")
    data_1_c = json.load(f)
    f = open("2-c.json")
    data_2_c = json.load(f)
    f = open("3-c.json")
    data_3_c = json.load(f)
    f = open("json-schema.json")
    schema = json.load(f)
    try:
        validate(data_1_c, schema)
    except Exception as e:
        print("Ошибка при валидации 1-c.json. ", e)
    else:
        print("Файл 1-c.json прошел валидацию!")
    try:
        validate(data_2_c, schema)
    except Exception as e:
        print("Ошибка при валидации 2-c.json. ", e)
    else:
        print("Файл 2-c.json прошел валидацию!")
    try:
        validate(data_2_c, schema)
    except Exception as e:
        print("Ошибка при валидации 3-c.json. ", e)
    else:
        print("Файл 3-c.json прошел валидацию!")




#create_correct_json_file()
validate_data()
# f = open("example.json")
# data = json.load(f)
# f = open("json-schema.json")
# schema = json.load(f)
#
# print(validate(data, schema))