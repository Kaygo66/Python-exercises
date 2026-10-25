num_list =[]

while True:
    uinp = input("Enter a number:")
    if uinp == "done":
        break
    uinp = float(uinp)
    num_list.append(uinp)
    
print(max(num_list))
print(min(num_list))
