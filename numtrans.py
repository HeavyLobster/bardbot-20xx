_SUFFIXES = ["K", "M", "B", "T"]

# Discard every number after the first two digits of the number
# then clamp the second digit to 5 or less
def round_weirdly(number):
    zeros = 0

    # Find the number of zeros in the number
    while 10**zeros < number:
        zeros = zeros + 1
    zeros = zeros - 1

    # Discard everything after the second digit
    number = number - number % 10**(zeros - 1)

    # If the second digit is greater than five, set it to five
    if number % 10**zeros > 5 * 10**(zeros - 1):
        number = number - number % 10**zeros + 5 * 10**(zeros - 1)

    return int(number)

def to_shorthand(number):
    prefix = 0
    suffix = ""

    for x in range(12, 0, -3):
        if number > 10**x - 1 and number / 10**x < 1000:
            prefix = number / 10**x
            suffix = _SUFFIXES[int(x / 3) - 1]

    if prefix < 10 and prefix % 1 >= 0.5:
        prefix = int(prefix) + 0.5
    elif prefix > 100:
        prefix = int(prefix / 10) * 10
    else:
        prefix = int(prefix)

    return f"{prefix}{suffix}"

def mastery_range(mastery):
    num = round_weirdly(mastery)
    zeros = 0

    yield num

    while num > 0:
        if num <= 10**3:
            num = 0
        elif num <= 10**4:
            num = num - 10**3
        else:
            for x in range(10, 0, -1):
                if num <= 10**x:
                    zeros = x
            num = num - 5 * 10**(zeros - 2)

        yield num

def from_shorthand(shorthand):
    numerals = "1234567890."
    numString = ""
    realNumber = 1.0
    suffix = ""

    for c in shorthand:
        c = c.upper()

        if c in numerals:
            numString += c

        if c in _SUFFIXES and suffix == "":
            suffix = c

    realNumber = float(numString)

    if suffix in _SUFFIXES:
        realNumber = realNumber * 10**((_SUFFIXES.index(suffix) + 1) * 3)

    return int(realNumber)

if __name__ == "__main__":
    mastery = input("Generate mastery prefixes until this mastery "
                    "score: ")

    for x in mastery_range(int(mastery)):
        print(to_shorthand(x))
