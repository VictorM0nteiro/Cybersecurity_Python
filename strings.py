# Basic string creation
text = "Hello, Python!"
text2 = 'Using single quotes'

# String concatenation
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print("Concatenation:", full_name)

# String methods
text = "   Python Programming   "
print("Upper:", text.upper())
print("Lower:", text.lower())
print("Strip:", text.strip())  # Removes whitespace
print("Replace:", text.replace("Python", "Java"))

# String slicing
message = "Hello World"
print("First 5 characters:", message[0:5])
print("Last 5 characters:", message[-5:])
print("Every second character:", message[::2])

# String formatting
name = "Alice"
age = 25
# Using .format()
print("Name: {}, Age: {}".format(name, age))
# Using f-strings (modern way)
print(f"Name: {name}, Age: {age}")

# String methods for searching
text = "Python is amazing and Python is fun"
print("Count 'Python':", text.count("Python"))
print("Find 'is':", text.find("is"))
print("StartsWith 'Python':", text.startswith("Python"))
print("EndsWith 'fun':", text.endswith("fun"))

# Split and Join
sentence = "This is a sample sentence"
words = sentence.split()  # Split into list
print("Split:", words)
print("Join:", "-".join(words))

# Check string properties
text = "Python3.9"
print("Is alphanumeric?", text.isalnum())
print("Is alphabetic?", text.isalpha())
print("Is numeric?", "123".isnumeric())

# Length of string
text = "Hello World"
print("Length:", len(text))

# String multiplication
print("Ha " * 3)  # Repeats string

# Character escaping
print("Line 1\nLine 2")  # New line
print("Tab\tspace")      # Tab
print("Quote: \"Hello\"") # Quotes