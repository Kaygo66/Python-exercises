uniquie = ["yonder", "envious","sick","pale"]

words = open("romeo.txt")
for word in words:
    word = word.strip()
    if word not in uniquie:
        uniquie.append(word)

print(uniquie)