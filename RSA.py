import math
import sys
import subprocess
from sympy import nextprime

# clear terminal

subprocess.run('clear', shell=True)

# for clearing input lines

def flush_input():
    sys.stdout.write("\033[F")      # Move cursor up one line
    sys.stdout.write("\033[K")      # Clear line
    sys.stdout.flush()

# encrypt a message 

def encrypt():

    e = 65537 # exponent

    message = str(input("Enter a message to encrypt: "))        # a message to encrypt
    message_byte = message.encode()                             # encode the message
    m = int.from_bytes(message_byte, byteorder="big")           # convert it to bytes

    bit_size = m.bit_length() + 16      # take the length in bits and add 16 for saftey
    byteLength = bit_size / 8           # convert it to bytes

    rounded = round(byteLength)         # round the result
    rounded = rounded * rounded         # multiply

    bits = pow(2, rounded)              # 2 to the power of the rounded bytes to get the bits for p and q

    p = nextprime(bits)
    q = nextprime(bits + 100)           # add 100 to prevent p == q

    n = p * q
    phi = (p - 1) * (q - 1)

    # m should be smaller than n to avoid errors

    if(m >= n):
        raise ValueError("Message too long for this key size!")
    
    c = pow(m, e, n)    # formula for c

    d = pow(e, -1, phi) # formula for d

    print(f"\nMessage: {message}")
    print(f"Value of N: {n}")
    print(f"Value of E: {e}")
    print(f"Value of PHI: {phi}")
    print(f"Value of D: {d}")
    print(f"Value of C: {c}")

def decrypt(n):
    
    e = 65537       # exponentd
    
    a = math.isqrt(n)       # a = square root of n

    if a * a == n:          # check if n is a perfect square
        return a, a
    
    while True:
        a = a + 1
        bsq = a * a - n
        b = math.isqrt(bsq)

        if b * b == bsq:
            break
    
    p = a + b
    q = a - b
    phi = (p - 1) * (q -1)
    d = pow(e, -1, phi)

    return d, p, q

def options():

    print("\n[====== O P T I O N S ======]")
    option = int(input("\n1. Encrypt\n2. Decrypt\n\nSelect one of the options: "))
    flush_input()

    if option == 1:
        encrypt()

    elif option == 2:
        n = int(input("Enter value of N: "))
        c = int(input("Enter value of C: "))
        d, p, q = decrypt(n)
        print(f"d: {d}\np: {p}\nq: {q}")

        # Decrypt the ciphertext
        m = pow(c, d, n)

        # Turn it back to a string
        message_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")
        message = message_bytes.decode()
        print(message)

options()