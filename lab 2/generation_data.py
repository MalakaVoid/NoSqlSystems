import random, string, datetime
def get_random_string():
    length = random.randint(3,15)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_email():
    length = random.randint(3,15)
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    result += "@mail.ru"
    return result

def get_random_long_text():
    length = random.randint(20, 50)
    letters = "zyxwvutsrqponmlkjihgfedcba.,/78!&"
    result = ''.join(random.choice(letters) for i in range(length))
    result += '\n'
    result += ''.join(random.choice(letters) for i in range(length))
    return result

def get_random_date():
    return datetime.date(year=random.randint(1980, 2023),
                         month=random.randint(1, 12),
                         day=random.randint(1, 28)).strftime("%Y-%m-%d")

def get_random_long_string():
    length = random.randint(10, 100)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))