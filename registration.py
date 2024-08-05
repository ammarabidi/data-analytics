print("Rgistration Applicatrion=>")
username = input('Enter your username=>')
email = input('Enter your email=>')
password = input('Enter your password=>')
cpassword = input('confirm your password=>')
gender = input("Gender (F/M/O) =>")

if username and email and password and cpassword and gender:
    if username.isalnum():
        if '@' in email and email.endswith('.com'):
            if password == cpassword:
                if len(password) >=8:
                    print("Registraton Complete")
                    print("🌍🌍🌍🌍")
                else:
                    print('Password too small')
            else:
                print('Password does not match')
        else:
            print('Invalid email')
    else:
        print('Invalid username')
else:
    print('All fields are required')