import random

array = []
for i in range(6):
    array.append([random.randint(0, 54), random.randint(0, 6), random.randint(0, 5)])

array.sort()
print(array)

