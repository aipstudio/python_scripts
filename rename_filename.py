import os
i=0
d="c:/tmp"
for file in os.listdir(d):
    i=i+1
    old_file = os.path.join(d, file)
    new_file = os.path.join(d, str(i))
    os.rename (old_file, new_file)
    print(i,old_file,new_file)
