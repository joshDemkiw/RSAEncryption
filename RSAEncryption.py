from random import randint

def eratosthenes(n):
    multiples = []  # array of non-primes Notice: implement this using set
    primes = []
    for i in range(2, n + 1):
        if i not in multiples:  # found prime
            primes.append(i)
            for j in range(i * i, n + 1, i):  # remove all multiples of found prime from search. start at i*i because lower multiples were previously removed by lower prime
                multiples.append(j)
    return primes

#faster algorithm for computing large squares
def exp_by_squaring(x,n):
    if n < 0:
        return exp_by_squaring((1/x),-n)
    elif n == 0:
        return 1
    elif n == 1:
        return x
    elif n % 2 == 0:
        return exp_by_squaring(x*x, n/2)
    elif n % 2 == 1:
        return x * exp_by_squaring(x*x, (n-1) / 2)
#print("x: {} x^2: {}".format(4, exp_by_squaring(1401,10000)))

def gcd(a, b):
    if (a < b):  # have x be the larger of the two numbers
        a = a + b
        b = a - b
        a = a - b
    if (a % b != 0):  # euclidean gcd algorithm
        a, b = b, a % b
        return gcd(a, b)
    else:
        return b


def xgcd(a, b, prevx, x, prevy, y):

    if (a < b):  # have x be the larger of the two numbers
        a = a + b
        b = a - b
        a = a - b
    if (a % b != 0):  # extended euclidean gcd algorithm
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b
        return xgcd(a, b, prevx, x, prevy, y)
    else:
        return [b, x, y] #x = number of times to multiply a to get gcd ----- guaranteed to exist g = ax + by
                         #y = number of times to multiply b to get gcd

#always call with 1,0,0,1 for iniatial recursive case
#exgcd = xgcd(780,17,1,0,0,1)


def lcm(x, y):
    lcm = (y * x) / gcd(x, y)
    return lcm


def randomPrimeNumber(start,stop):
    try:
        x = primes[randint(start, stop)]
        return x
    except:
        print("out of range of primes")


class encryptionKey: #note: use 'self' variables for instance classes
    def __init__(self):
        self.p = randomPrimeNumber(int((len(primes) - 1)/2), len(primes) - 1)  # select a prime from larger half of
        self.q = randomPrimeNumber(int((len(primes) - 1)/2), len(primes) - 1)  # the array of prime numbers
        self.n = self.p * self.q
        self.totient = int(lcm(self.p-1, self.q-1))
        self.e = self.createE()
        self.d = self.createD(self.e, self.totient)

        self.publicKey = [self.n, self.e]
        self.privateKey = [self.n, self.d]

    def createE(self):  # return a coprime to totient by selecting prime and ensuring totient is not divisible by the prime
        tmp = randomPrimeNumber(0,int((len(primes) - 1)/2))
        if(self.totient % tmp ==0):
            return self.getE()
        else:
            return tmp

    def createD(self, e, totient):
        tmp = xgcd(self.totient, e, 1, 0, 0, 1)
        mod_inverse = tmp[2]
        while mod_inverse < 0:
            mod_inverse += totient
        return tmp[2]

def encrypt_message(msg, public_key):
    encrypted = [ord(c) for c in msg]
    encrypted = [(exp_by_squaring(i,public_key[1]) % public_key[0]) for i in encrypted]
    return encrypted

def decrypt_message(encrypted, private_key):
    msg = [(exp_by_squaring(i,private_key[1]) % private_key[0]) for i in encrypted]
    msg = [chr(c) for c in msg]
    decrypted = "".join(msg)
    return decrypted


primes = eratosthenes(1000)

joshKey = encryptionKey()

message = "Hello, World!"
encrypted = encrypt_message(message,joshKey.publicKey)
decrypted = decrypt_message(encrypted, joshKey.privateKey)

print(encrypted)

print(decrypted)
