import numpy as np
def MEF_from_Mach(M):
    Mach_numbers = np.array([0.25, 0.5, 0.65, 0.7, 0.8, 0.9, 0.95,
                          1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6,
                          1.8, 1.9, 2.0, 2.2, 2.5, 2.6])
    MEF_data = np.array([1.0, 1.0, 1.0, 0.97, 0.91, 0.72, 0.66,
                          0.75, 0.90, 0.96, 0.99, 0.999, 0.992,
                          0.98,  0.91, 0.85, 0.82, 0.75, 0.64, 0.62])
    MEF = np.interp(M, Mach_numbers, MEF_data)
    # print("MEF", MEF)
    return MEF