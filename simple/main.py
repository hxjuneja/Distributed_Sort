
op1 = open("data1.txt", "r+")
op2 = open("dataA.txt", "w+")
op3 = open("dataB.txt", "w+")

data = op1.read().split("\n")

for i in data:
    field = i.split(" ")
    if len(field) > 1:
        if str(field[1]) == 'A':
             wf = " ".join(field)
             wf = wf + "\n" 
             op2.write(wf)
        else:
             wf = " ".join(field)
             wf = wf + "\n"
             op3.write(wf)


