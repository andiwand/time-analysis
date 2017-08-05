import numpy as np
import pandas as pd

n = 100
a = np.column_stack([np.arange(n), np.random.rand(n)])

s = pd.Series(a[:,1])
df = pd.DataFrame(a)
rs = s.rolling(10)
rdf = df.rolling(10)
a = rdf.mean().values
b = rs.std().values
print(np.column_stack([a, b]))

