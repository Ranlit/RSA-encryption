

# Yiran Li 1630286
# Final Project: RSA encryption using Python
# Goal of the program:
""" The goal of this program is to allow the user to encrypt and decrypt messages using RSA two letters
at a time. It also allows the user to set up RSA either by themselves or by randomly generating numbers. """

from Help import *
import random 

# Purpose: this function makes sure the user enters an integer when an integer is needed (robustess)
# Contract:
    # Input: nothing
    # Output: this function returns an integer (or "end" if the message has ended), or an error
def get_integer():
    while True:
        answer = (input("Enter an integer! \n"))
        try: # This makes sure the input is an integer, otherwise we output an error
            A = int(answer)
            if int(answer) == -1:
                return "end"
            return A
        except ValueError:
            print(answer, "is not an integer!")


# Purpose: this function makes sure the user enters a letter when a letter is needed (robustess)
# Contract:
    # Input: nothing
    # Output: this function returns a string (or 1 if the message ended)
def get_letter():
    while True: # this while loop keeps on looping until all conditions are satisfied
        answer = str(input("Enter your letter: \n"))
        if answer == "1": # this if statement for when the user wants to end their message, they need to enter 1
            return 1
        if answer == " ": # this if statement allows the user to enter spaces when entering their message
            return answer
        elif not answer.isalpha(): # this part makes sure the user entered a letter, otherwise it asks again
            print("You must enter a letter!!!")
            return get_letter()
        elif not len(answer) == 1: # this part makes sure the user enters letters one at time
            print("You should only put one letter at a time!")
            return get_letter()
        else:
            return answer

# 1.Setting up RSA

# Purpose: this function lets the user choose 2 primes by themselves for setting up the RSA
# Contract:
    # Input: nothing
    # Output: the function returns a tuple containing the two primes chosen by the user
def pick_primes():
    print("Hi! Please enter a lower bound and an upper bound \n"
          "for the two primes you would like to use for your RSA encryption! \n")
    print("What is your minimum? ")
    m = get_integer()
    print("What is your maximum? ")
    M = get_integer()
    if M < m: # This if statement prevents the user from choosing their bounds incorrectly
        print("Your upper bound cannot be smaller than your lower bound! ")
        return pick_primes()
    primes = list_primes(m, M)
    if len(primes) < 2: # This if statement prevents the user from choosing bounds too close to each other
        print("The difference between your bounds was not large enough! ")
        return pick_primes()
    print("So here is the list of all primes between the bounds you picked: ")
    print(primes)
    while True: # This while loop keeps on running until the user has selected two primes
                # that correspond to the conditions
        print("Please choose two different primes from the list I just gave you. ")
        print("Your first prime: ")
        p = get_integer()
        print("Your second prime: ")
        q = get_integer()
        if p == q: # This if statement prevents the user from choosing 2 primes that are the same
            print("You need to choose two different primes!!! \n"
                  "Time to restart!")
        elif p not in primes: # This if statement prevents the user from choosing a prime that isn't in the given list
            print("The first prime you chose is not in the list of primes!!! \n"
                  "Time to restart!")
        elif q not in primes: # This if statement prevents the user from choosing a prime that isn't in the given list
            print("The second prime you chose is not in the list of primes!!! \n"
                  "Time to restart!")
        else:
            return (p, q)

# Purpose: this function lets the user randomly generate 2 primes for setting up the RSA
# Contract:
    # Input: nothing
    # Output: the function returns a tuple containing the two primes chosen by the rng
def random_pick_primes():
    print("Hi! Please enter a lower bound and an upper bound \n"
          "for the two primes you would like to use for your RSA encryption! \n")
    print("What is your minimum? ")
    m = get_integer()
    print("What is your maximum? ")
    M = get_integer()
    if M < m: # This if statement prevents the user from choosing their bounds incorrectly
        print("Your upper bound cannot be smaller than your lower bound! ")
        return random_pick_primes()
    primes = list_primes(m, M)
    length = len(primes)
    if length < 2: # This if statement prevents the user from choosing bounds too close to each other
        print("The difference between your bounds was not large enough! ")
        return random_pick_primes()
    while True: # This while loop makes the computer choose two primes
                # from the list until it has chosen two different ones
        p = list_primes(m, M)[(random.randint(0, length-1))] # we use the random function here
        q = list_primes(m, M)[(random.randint(0, length-1))]
        if p is not q: # This if statement represents the condition for breaking the while loop:
                    # the 2 primes are different
            return(p, q)

# Purpose: this function is the global function that lets the user set up RSA by using one of two methods
# Contract:
    # Input: nothing
    # Output: the function returns a tuple containing the modulo n, the power e and d the inverse modulo
    # phi(n) of e, those are all important components of RSA
def set_up():
    print("Type 1 if you want to choose the primes by yourself \n"
          "or type 2 if you want to pick random primes. ")
    a = get_integer()
    if a == 1:
        p = pick_primes()
    elif a == 2:
        p = random_pick_primes()
    else: # This prevents the user from typing anything that isn't 1 or 2
        print("You need to type either 1 or 2!")
        return set_up()
    if p[0] < 2627 or p[1] < 2627: # This checks that Check that p and q are at least 2627
                                 # so that we can encrypt using two-letter blocks
        print("We really want p and q to be both at least 2627, so could you please do me a favor \n"
              "and set up your boundaries such that the two primes chosen can be at least 2627?")
        return set_up()
    n = p[0] * p[1]
    phi = (p[0] - 1) * (p[1] - 1)
    print("Please choose a power e bigger than 1 and smaller than", phi)
    e = get_integer() # Asking the user to pick a power e
    while not relatively_prime(phi, e): # This while loop runs until the user gives an e
                                    # that is relatively prime to phi(n)
        print("Could you please choose another e? ")
        e = get_integer()
    d = inverse(e, phi)
    return (n, e, d)

# 2.Encoding messages:

# Purpose: this function communicates with the user in order to get the message the user wants to send
# Contract:
    # Input: nothing
    # Output: a list of letters which contains the message
def get_message():
    message = []
    t = True
    while t: # This while loop repeatedly asks the user for the next letter and adds that letter to message
        print("What is the next letter you want to add to your message? Please enter 1 if your message has ended.")
        next_letter = get_letter()
        if next_letter == 1: # Condition for this while loop to stop: user enters 1, meaning end of message
            if not mod(len(message),2) == 0: # This if statement adds a blank space to message
                                        # if there is an odd number of letters in message
                message.append(" ")
                return message
            return message
        message.append(next_letter) # If we have not yet reached end of message, just keep on adding one letter at
                                # a time to the message

# Purpose: this function transforms a list of letters into a list of corresponding numbers according to the dictionary
# Contract:
    # Input: this function takes the message, which is a list of letters, as input
    # Output: this function returns a list of numbers
def letter_to_number(message):
    message_in_num = []
    for letter in message: # This for loop operates on every single letter in the list of letters
        message_in_num.append(Number[letter]) # This line uses the dictionary given in Help
    return message_in_num

# Purpose: this function encrypts a message into a list of numbers
# Contract:
    # Input: message, which is a list of letters, n and e, which are numbers respectively representing
    # the modulo and the power generated using set_up()
    # Output: this function returns the encrypted message as a list of numbers
def encode(message, n, e):
    in_number = letter_to_number(message) # This transforms the list of letters in numbers
    coded = []
    while not in_number == []: # This while loop keep on encrypting the numbers two by two until no more left
        x = in_number.pop(0)
        y = in_number.pop(0)
        number_to_encrypt = 100*x + y # This encrypts two letters at a time
        coded.append(pow(number_to_encrypt, e, n))
    return coded

# 3.Decoding messages:

# Purpose: this function communicates with the user in order to get the message the user wants to decrypt
# Contract:
    # Input: nothing
    # Output: this function returns a list of integers
def get_message_number():
    message = []
    t = True
    while t: # This while loop keeps on iterating until the user ends the message to decrypt
        print("What is the next number you want to add to the message you need to decrypt? \n"
              "Please enter -1 if your message has ended.")
        next_number = get_integer()
        if next_number == "end": # That means the user entered -1
            return message
        message.append(next_number)

# Purpose: this function transforms a list of numbers into a list of corresponding letters according to the dictionary
# Contract:
    # Input: this function takes in the message, which is a list of numbers between 0 and 26
    # Output: this function returns a list of letters
def number_to_letter(message):
    message_in_let = []
    for number in message: # This for loop operates on every single number in the list of numbers
        message_in_let.append(Letter[number]) # This line uses the dictionary given by Help
    return message_in_let

# Purpose: this function decrypts a message into a list of letters
# Contract:
    # Input: message, which is a list of numbers, n and d, which are numbers respectively representing
    # the modulo and the inverse of the power generated using set_up()
    # Output: this function returns the decrypted message as a list of letters
def decode(message, n, d):
    decoded = []
    while not message == []: # This while loop keeps on iterating until no more number to be decrypted
        x = message.pop(0)
        original_nb = pow(x,d,n)
        first_number = quot(original_nb, 100) # Since the original number is composed by 2 numbers, we need to separate them
        second_number = mod(original_nb, 100)
        if first_number > 26 or second_number > 26: # This makes sure that the decrypted message are indeed messages
                                                # in the alphabet
            return("The encoded number you entered doesn't make sense! Please try again.")
        decoded.append(first_number)
        decoded.append(second_number)
    return number_to_letter(decoded) # Finally, we transform the numbers to their corresponding letters
                                # using the previous function

# 4.Core:

# Purpose: menu is a function that first sets up the RSA and then asks the user what he wants and gives him the
# right answer, in this case, it offers the user 6 different choices:
# set up RSA again, encrypt, decrypt, print public key, print private key or leave
# Contract:
    # Input: nothing
    # Output: it prints out a bunch of strings, and sometimes lists for messages or tuples for keys
def menu():
    print("First, let's set up the RSA encryption! \n"
          "By using RSA, you will now be able to send messages without anyone \n"
          "knowing what you truly mean, unless they know your private key!")
    p = set_up()
    while True: # This while loop makes sure that the options keep on looping until user decides to leave
        print("Now, here are your options: \n"
            "-Press 1 if you want to set up the RSA again \n"
            "-Press 2 if you want to encrypt a message \n"
            "-Press 3 if you want to decrypt a message \n"
            "-Press 4 if you want to print the public key \n"
            "-Press 5 if you want to print the private key \n"
            "-Press 6 if you want to leave me alone :( \n")
        choice = get_integer()
        if choice == 1:
            return menu()
        elif choice == 2:
            print("So first, please enter letter by letter the message you want to encrypt. \n")
            message = get_message()
            n = p[0]
            e = p[1]
            print("So here is your message encrypted: \n")
            print(encode(message, n, e))
        elif choice == 3:
            print("So first, please enter number by number the message you want to encrypt. \n")
            message = get_message_number()
            n = p[0]
            d = p[2]
            print("So here is your message decrypted: \n")
            print(decode(message, n, d))
        elif choice == 4:
            pub_key = (p[0], p[1])
            print("Here is your public key (n, e)")
            print(pub_key)
        elif choice == 5:
            print("Here is your private key (d)")
            print(p[2])
            print("Don't share this key unless you want the other person to be able to understand your message!")
        else:
            print("Goodbye darkness my old friend, I'll come to talk to you again. \n"
                  "Thank you for this beautilful class!")
            return

menu()