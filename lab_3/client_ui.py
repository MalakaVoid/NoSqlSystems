import database_operations
def go_to_chat_actions(current_user, chat_title):
    print("SUCCESS")
def create_chat_dialog(current_user):
    while True:
        print("Enter a title of chat.")
        title = input(f'{current_user}/chat>')
        if database_operations.check_title_chat_existence(title):
            print('Title is already taken. Choose different title. ')
        else:
            break
    print("Enter a description.")
    description = input(f'{current_user}/chat>')
    if description == None:
        description = ""
    users = []
    flag = True
    print("Enter usernames of invited users. Enter /q to stop.")
    while flag:
        user = input(f'{current_user}/chat>')
        if user == '/q':
            break
        if database_operations.check_user_existance(user):
            users.append(user)
        else:
            print(f"No user '{user}' found.")
    database_operations.create_chat(current_user, title, description, users)
    print(f'Chat {title} has done successfully.')

def entered_user_cli(current_user):
    flag_of_ending_user_cli = True
    print("Control system: \n"
          "Show all chats - chats\n"
          "Go to chat - /chat {title}\n"
          "Create chat - create chat\n"
          "Change user - /change\n"
          "Show commands - --help\n"
          "Stop program - /q")
    while flag_of_ending_user_cli:
        command = input(f'{current_user}> ')

        if command == "chats":
            chats = database_operations.get_all_user_chats_titles(current_user)
            if chats is None:
                print("You have no chats.")
            else:
                for each in chats:
                    print(each)

        tmp = command.split(' ')
        if  tmp[0] == '/chat':
            if tmp[1] in database_operations.get_all_user_chats_titles(current_user):
                go_to_chat_actions(current_user, tmp[1])
            else:
                print(f"No chat '{tmp[1]}' was founded.")

        if command == 'create chat':
            create_chat_dialog(current_user)

        if command == '--help':
            print("Control system: \n"
                  "Show all chats - chats\n"
                  "Go to chat - chat {title}\n"
                  "Create chat - create chat {title}\n"
                  "Change user - /change\n"
                  "Show commands - --help\n"
                  "Stop program - /q")

        if command == '/change':
            authorization()
            break

        if command == "/q":
            flag_of_ending_user_cli = False

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
        entered_user_cli(username)
    elif code == 501:
        print("Username is already taken. Try again.")
        registration()
    else:
        print('Something went wrong. Try again.')
        registration()

def start_program():
    print("Enter r - for registration, a - for authorization: ", end="")
    start_input = input()
    if start_input == 'r':
        registration()
    elif start_input == 'a':
        authorization()