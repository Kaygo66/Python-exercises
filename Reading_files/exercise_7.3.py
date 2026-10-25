fname = input("Enter file name: ")
try:
    fhand = open(fname)
except:
    print("File cannot be found:", fname)
    exit()

trail = 0
count = 0
for line in fhand:
    if line.startswith("X-DSPAM-Confidence:"):
        pos = line.find(":")
        line = line[pos +1::]
        value = float(line)
        trail += value
        count += 1
print("total is", trail)
print("average is", trail / count)