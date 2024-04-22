# Binary polynomials are represented as integers, with the least significant bit being the coefficient of x^0

# Binary polynomial division 
def binPolyDiv(dividend, divisor):
    power = 0
    while dividend >= divisor:
        dividend ^= divisor << power
        while (dividend >> (power + 1)) < divisor:
            power -= 1
    return dividend

# Function to calculate and correct syndromes
def syndrome(r_x, degree, g_x):
    syndromes = []
    for i in range(degree):
        # Calculating x^i*r(x)
        x_r = r_x << i 
        # Calculating syndrome as x^i*r(x) mod g(x)
        syndrome = binPolyDiv(x_r, g_x)
        syndromes.append(syndrome)

    return syndromes    

# Function to find burst length
def findBurstLength(s):
    first_one = s.index(1)
    last_one = len(s) - 1 - s[::-1].index(1)
    burst_length = last_one - first_one + 1
    return burst_length

# Set our generator and received message
g_x, r_x = 0b1111001, 0b111011101100000
# Calculating degree
degree = len(bin(g_x)) - 2
# Calculate all the syndromes
syndromes = syndrome(r_x, degree, g_x)
# Check that syndromes' burst length is at most 3
for s in syndromes:
    s = list(map(int, "{0:b}".format(s)))
    if findBurstLength(s) > 3:
        print ("Burst error cannot be corrected.")
        exit()

print("Burst error can be corrected.")
