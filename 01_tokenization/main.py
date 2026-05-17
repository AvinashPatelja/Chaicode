import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")

text = "Hey there, I am Avinash Patel"

print("Token", enc.encode(text))

print("Text", enc.decode([25216, 1354, 11, 357, 939, 7541, 258, 1229, 122760]))