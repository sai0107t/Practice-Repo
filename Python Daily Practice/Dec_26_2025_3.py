# problem 3- Count the words
#ask the user to enter a sentence, then print how many words it contains
#Requirements:
#    count workds separted by sapces
#    ignore extra sapces
#    if the user just presses enter(empty input), print 0
#Dont use advanced stuff like regex, list of comprehensions, external libraries
#stick to simple string methods and loops


while True:
    n=input("Please Enter a Sentence: ")

    # validate input

    if n=="":
        print("0")

        continue
    try:
        n=
    except:
        print("Invalid Input - Please enter only words")

        continue

    # formatting the input

    sentence=n.strip()

    # logic of the program

    words=sentence.split()
    print(len(words))

