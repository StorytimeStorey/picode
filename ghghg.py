import math
import random

def trim_data_list(data):
    '''takes the length of a list and divides it by 1950 (if its bigger than that). It then trims
        data until 1950 remain.'''
    if len(data) > 49:
        step = len(data) // 49
        trimmed_data = data[::step]
        return trimmed_data
    else:
        return data
    
l = []
n = random.randint(2000,140000)
for i in range(n):
    l.append(i)

new_l = trim_data_list(l)

print(new_l)
print(len(new_l))