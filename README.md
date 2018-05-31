# FoFCatalogMatching
Using friends-of-friends method to iteratively match multiple sky catalogs
without the need of specifying the main catalog.

## Installation

```sh
pip install https://github.com/yymao/FoFCatalogMatching/archive/master.zip
```

## Example

```python
import numpy as np
from astropy.table import Table
import FoFCatalogMatching

n = 100
ra = np.random.uniform(0, 360, n)
dec = np.random.uniform(-90, 90, n)

cat_a = Table({'ra': ra, 'dec': dec})
cat_b = Table({'ra': ra+np.random.normal(0, 0.0002, n), 'dec': dec+np.random.normal(0, 0.0002, n)})
cat_c = Table({'ra': ra+np.random.normal(0, 0.0002, n), 'dec': dec+np.random.normal(0, 0.0002, n)})

results = FoFCatalogMatching.match({'a': cat_a, 'b':cat_b, 'c':cat_c},
                                   {3.0: 3, 2.0: 3, 1: None})
```
