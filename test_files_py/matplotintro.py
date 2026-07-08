import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

data = torch.tensor([[ 0.1142,  0.1242,  0.1761,  0.0931,  0.1134,  0.0423,  0.2145,  0.0881,
          0.1075,  0.0935,  0.2339,  0.1626,  0.0853,  0.0733,  0.1899,  0.0635,
          0.3895,  0.2143,  0.3747,  0.2373,  0.1307,  0.2758,  0.1942,  0.3643,
          0.2136,  0.7092,  0.1554,  0.2778,  0.3220,  0.3298,  0.0884,  0.1160,
          0.1640,  0.0592,  0.2064,  0.0512,  0.1577,  0.1937,  0.1339,  0.1005,
         -0.0069,  0.2078,  0.0756,  0.1006,  0.1292,  0.1387,  0.0749, -0.0162,
          0.2538,  0.0446,  0.1632,  0.1818,  0.1139,  0.1174,  0.2275,  0.0688,
         -0.0140,  0.1087,  0.0161,  0.0271, -0.0757]])

values = data.tolist()[0]
max_idx = values.index(max(values))  # finds index 25
max_val = max(values)   

fig, ax = plt.subplots(figsize=(5, 2.7))
ax.set_xlabel("Queries")
ax.set_ylabel("Cosine similarity")

ax.scatter(range(len(values)), values)


ax.annotate(
    'CopperSeam Jeans',
    xy=(max_idx, max_val),
    xycoords="data",
    xytext=(max_idx + 5, max_val - 0.15),
    textcoords="data",
    va="top",
    ha="left",
    arrowprops=dict(facecolor="black", shrink=0.05),
)

plt.show()