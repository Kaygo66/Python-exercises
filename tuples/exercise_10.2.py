from pathlib import Path

DATA = Path(__file__).parent.parent/"data"

fname = input("enter a file name:")

fhand = open(DATA/fname)

count = dict()

for line in fhand:
    if line.startswith("From "):

        words = line.split()
        time = words[5].split(":")[0]
    #   print(time)
        for n in time:
            count[time] = count.get(time,0) + 1

newlist = sorted(count.items())
print(newlist)

for v,k in newlist:
    print(v, k)

#list_of_hour = print(sorted(count.items()))






