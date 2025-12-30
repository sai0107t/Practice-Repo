# Practice
count = 0
while True:
    password=input("Enter the password: ")

    if password=="python123":
        print("Access granted")
        break
    else:
        print("Wrong password")
        count += 1
        if count >= 3:
            print("Account locked. Too many failed attempts.")
            break
        
        
        
        
    
    
