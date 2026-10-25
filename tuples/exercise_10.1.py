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


print(sorted(count.items()))

tmp = dict()
newlist = list()

for k,v in count.items():
    tup = (v,k)
    newlist.append(tup)


first = sorted(newlist, reverse = True)

for v,k in first[:5]:
    print(k, v)


