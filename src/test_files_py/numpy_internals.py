import numpy as np
from time import perf_counter

# When transposed, the memory allocated for the array is no longer Fortran_Contiguous and becomes C_Contiguous

# print(lst.strides)
# print(lst.itemsize)
# print(lst.flags)

# a = np.array([3, 5, 3, 5, 77, 34, 67, 23, 12, 42])

# b = a[2:5]

# b[0] = 95


# print(b)
# print(a)

# b = a[::2].copy()

# print(b.base is a)


n = 1000
a = np.random.rand(n)
b = np.random.rand(n, n)

k = perf_counter()
#print(np.dot(b, a))
p = perf_counter()
print("Np .dot method: " , p - k)



k = perf_counter()
total = []

for r_idx in range(len(b)): 
    row_total = 0
    for idx in range(len(a)): 
        row_total += a[idx]*b[r_idx][idx]
    total.append(row_total)

#print(total)
p = perf_counter()
print("Loop method time: " , p - k)

# By vectorizing the steps instead of looping, we gain speed by a factor of 500x
k = perf_counter()
def random_walk_fastest(n=1000):
    # No 's' in numpy choice (Python offers choice & choices)
    steps = np.random.choice([-1,+1], n)
    return np.cumsum(steps)

walk = random_walk_fastest(1000000)
print(walk)
p = perf_counter()
print("Loop method time: " , p - k)