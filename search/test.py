from itertools import permutations
from collections import deque

order_list = permutations(range(0, 3) , 3)
d = {1:4,2:1}
return(sorted(d.items(), key=lambda d:d[1], reverse=True))

print(deque(order_list))