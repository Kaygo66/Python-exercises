fh = open("mbox-short.txt")
for line in fh:
    line = line.upper().rstrip()
    print(line)