def rev(str):
    return rev(str[::-1])

def is_palindrome(str):
    rev= rev(str)
    if(str == rev):
        print("Palindrome")
    else:
        print("Not palindrome")

is_palindrome("madam")