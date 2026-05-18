import matplotlib.pyplot as pt
import numpy as np

xpoints = np.array([1,3,5,7,9])
ypoints = np.array([2,4,6,8,10])

pt.plot(xpoints , ypoints)

pt.show()

xpoints = [1,2,3,4,5]

pt.plot(xpoints, marker = 'o')

pt.show()