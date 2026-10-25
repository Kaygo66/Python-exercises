from pathlib import Path

DATA = Path(__file__).parent.parent/"data"

fname = input("enter a file name:")

try:
    fhand = open(DATA/fname)
except:
    print("File cannot be found:", fname)
    exit()

count = dict()

for line in fhand:
    if line.startswith("From "):
        line = line.split()
        print(line) # to see which line created the error if the program crashes
        key = line[2] 
        count[key] = count.get(key,0) + 1 # read the current value for "key" (or 0 if it doesn’t exist yet), add 1.


print(count)



    
