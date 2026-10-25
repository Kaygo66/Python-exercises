fhand = open("mbox-short copy.txt")
count = 0
for line in fhand:
    if line.startswith("From "):
        line_list = line.split()
        print(line_list[1])
        count += 1
print(f"there were a total of  {count} emails")



