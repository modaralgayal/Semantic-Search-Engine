import cos_sim
import numpy as np
import torch


def run ():
    matrix = torch.tensor(np.array([[1.0,0.0,5.0],
                       [-1.0,0.0,0.0],
                       [0.0,0.0,5.0],
                       [1.0,2.0,5.0]])).cpu().numpy()
    
    query = torch.tensor(np.array([1.0, 0.0, 0.0])).cpu().numpy()

    results = cos_sim.cos_sim(matrix, query)

    print(results)
    return results

if __name__=="__main__":
    run()