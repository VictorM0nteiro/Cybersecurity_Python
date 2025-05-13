with open('login_attempts.txt', 'r') as file:
    file_text = file.read()
usernamames = file_text.split()

def login_check(login_list, current_user):
    counter = 0
    for i in login_list:
        if i == current_user:
            counter += 1
    if(counter > 3):
        return "you have tried to login more than 3 times. Your account is locked."
    else:
        return "You may access."


resultado = login_check(usernamames, 'admin')
print(resultado)