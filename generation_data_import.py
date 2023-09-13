import random, string

def get_names_list():
    f = open('names.txt', encoding='utf-8')
    arr = []
    for line in f:
        added_line = line.replace('\n','')
        arr.append(added_line)
    return arr

def get_random_string():
    length = random.randint(3,15)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_long_string():
    length = random.randint(10, 100)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_date():
    return f"{random.randint(2000, 2023)}-{random.randint(1, 13)}-{random.randint(1, 30)}"