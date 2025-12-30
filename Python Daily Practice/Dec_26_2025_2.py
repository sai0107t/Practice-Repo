# Ask the user for a positive integer and print the sum of its digits
# Requirements: if the user enters anything that is not a positive integer, print invalid input
# Donot use shortcuts - don't use strings to sum digits. do it with Math(% and //)

sum_digits=0

while True:
    s=input("Enter a positive integer (or 'done'):")

    # validate input

    if s.lower()=='done':
        break
    try:
        n=int(s)
    except:
        print("Invalid Input")
        continue
    
    if n<=0:
        print("Invalid Input")
        
    else:
        break

x=n

# logic of the program

while x>0:
    digit=x%10 # last digit
    sum_digits+=digit
    x //=10 # remove last digit

print("Sum of digits:",sum_digits)
