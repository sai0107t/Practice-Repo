##Sum positive numbers only:
##Rules:
##    1. Keep reading integers from the user
##    2. Maintain a running sum of only positive numbers
##    3. If the user enters a negative number, stop the loop immediately and print the sum
##    4. Ignore blank input using continue
##    5. Handle invlaid input with try/except
##
##


sum_positive = 0
while True:
    inp=input("Enter a number: ").strip()  #using strip also in case only spaces
    # validating blank input and input for an integer
    if inp=="":
        continue
    try:
        n=int(inp)
    except ValueError:
        print("Invalid Input")
        continue
    # check for negative numbers
    if n>=0:
        sum_positive+=n
        continue
    break
print(sum_positive)
        
