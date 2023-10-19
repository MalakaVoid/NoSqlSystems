import database_operations
def entered_user_cli(current_user):
    flag_of_ending_user_cli = True
    while flag_of_ending_user_cli:


def authorization():
    print('Enter username: ', end="")
    username = input()
    print('Enter a password: ', end="")
    password = input()

    code = database_operations.auth_usr_checker(username, password)
    if code == 200:
        entered_user_cli(username)
    elif code == 501:
        print('Wrong password. Try again.')
        authorization()
    elif code == 404:
        print(f"No user '{username}' found. Try again.")
        authorization()
    else:
        print("Something went wrong. Try again.")
        authorization()

def registration():
    print('Enter username: ', end="")
    username = input()
    print('Enter a password: ', end="")
    password = input()
    print('Enter a password again: ', end="")
    password_checker = input()
    code = 0
    if password == password_checker:
        code = database_operations.add_new_user(username, password)

    if code == 200:
        print('New user successfully added.')
        authorization()
    elif code == 501:
        print("Username is already taken. Try again.")
        registration()
    else:
        print('Something went wrong. Try again.')
        registration()