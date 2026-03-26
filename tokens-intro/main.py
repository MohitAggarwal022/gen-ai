import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I am Mohit Aggarwal"
tokens = enc.encode(text)

print("Tokens:", tokens)

tokens = [13225, 11, 357, 939, 31564, 278, 88220, 277, 22314]
decoded = enc.decode(tokens)

print("Decoded Text:", decoded)