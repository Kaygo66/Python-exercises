from pathlib import Path

DATA = Path(__file__).parent.parent/"data"

fname = input("enter a file name:")

fhand = open(DATA/fname)

count = dict()

for line in fhand:
    if line.startswith("From"):
        line = line.split()
        key = line[1] 
        count[key]= count.get(key,0) + 1

print(count)

bigword = None
bigcount = None


for word, number in count.items():
    if bigcount == None or number > bigcount:
        bigcount = number
        bigword = word
print("most frequent email:", bigcount, "which is", bigword)

