

with open('dummy.txt' , 'r') as f : 
    data = f.readlines()


new_ = []

for i in range(len(data)) :
    new_.append(data[i].replace('\n' , ''))


print(new_)