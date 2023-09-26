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

def get_random_long_text():
    length = random.randint(20, 50)
    letters = "zyxwvutsrqponmlkjihgfedcba.,/78!&"
    result = ''.join(random.choice(letters) for i in range(length))
    result += '\n'
    result += ''.join(random.choice(letters) for i in range(length))
    return result

def get_random_date():
    return f"{random.randint(1990, 2023)}-{random.randint(1, 12)}-{random.randint(1, 28)}"

def get_random_long_string():
    length = random.randint(10, 100)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))