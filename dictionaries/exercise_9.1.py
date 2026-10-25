handle = open("words.txt")
counts =dict()

for line in handle:
    words = line.split()
    for word in words:
        counts[word]= counts.get(word,0) + 1

print(counts)

print ("fun" in counts)