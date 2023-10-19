import redis
import client_ui

if __name__ == '__main__':
    print("Enter r - for registration, a - for authorization: ", end="")
    start_input = input()
    if start_input == 'r':
        client_ui.registration()
    elif start_input == 'a':
        client_ui.authorization()