# write a program that keeps asking the user for numbers untill they type done.
# then print: count of numbers, total sum & Average.
# Ignore invalid inputs instead of crashing


total=0
count=0

#use underscores in variable names, not spaces

even_count=0 
odd_count=0
largest=None
smallest=None

while True:
    s=input("Enter the number (or 'done'):")

    if s.lower()=='done':
        break
    try:
        n=float(s)
    except:
        print('Invalid Input')
        continue

    total+=n
    count+=1

    if largest is None or n>largest:
        largest=n

    if smallest is None or n<smallest:
        smallest=n

# even/odd only if integer
    if int(n)%2 ==0:
        even_count+=1

    else:
        odd_count+=1

    
print("Total:", total)
print("Count:", count)
print("Even Count:", even_count)
print("Odd Count:", odd_count)

if count>0:
      print("Average:", total/count)
      print("Max:", largest)
      print("Min:", smallest)

else:
    print("No valid numbers entered")

    
