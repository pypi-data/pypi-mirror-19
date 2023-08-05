"""This module is Mike's rendition of the FizzBuzz screening question (program)"""

def fibonacci(seq_length):
    """Prints a fibonacci sequence of seq_length length """
    if seq_length < 2:
        print seq_length
        return
    else:
        fib_prev_2 = 1
        fib_prev_1 = 1
        print fib_prev_2
        print fib_prev_1

        for _number in xrange(2, seq_length):
            #Fibonacci algorithm
            fib_prev_2, fib_prev_1 = fib_prev_1, fib_prev_2 + fib_prev_1

            #set current fibonacci number for convenient use in conditional statements below
            fib_curr = fib_prev_1

            #Print "FizzBuzz" if divisible by 15
            if fib_curr % 15 == 0:
                print str(fib_curr) + " FizzBuzz"
                continue

            #Print "Buzz" if divisible by 3
            if fib_curr % 3 == 0:
                print str(fib_curr) + " Buzz"
                continue

            #Print "Fizz" if divisible by 5
            if fib_curr % 5 == 0:
                print str(fib_curr) + " Fizz"
                continue

            #Print "BuzzFizz" if a prime number
            if is_prime(fib_curr):
                print str(fib_curr) + " BuzzFizz"

            #Else, print the current number
            else:
                print fib_curr
        return

def is_prime(num):
    """Function to check if arg1 is a prime number"""
    if num >= 2:
        for divisor in xrange(2, num):
            if not num % divisor:
                return False
    else:
        return False
    return True

def main():
    '''main execution function'''
    str_seq_length = raw_input("Please input the fibonacci sequence length desired (0-10000): ")
    seq_length = 0
    try:
        seq_length = int(str_seq_length)
    except ValueError as ex:
        print "Details: Could not convert the input to a valid number: " + ex.message
    if seq_length < 1:
        print "Sequence length must greater than 0"
    elif seq_length > 10000:
        print "Sequence length must be smaller than 10000, this program is illustrative use only"
    else:
        fibonacci(seq_length)
