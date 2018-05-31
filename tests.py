import numpy as np
from astropy.table import Table
import FoFCatalogMatching

def test_basic():
    n = 100
    ra = np.random.RandomState(123).uniform(0, 360, n)
    dec = np.random.RandomState(456).uniform(-90, 90, n)

    cat_a = Table({'ra': ra, 'dec': dec})
    cat_b = Table({'ra': ra+np.random.RandomState(789).normal(0, 0.0002, n), 'dec': dec+np.random.RandomState(987).normal(0, 0.0002, n)})
    cat_c = Table({'ra': ra+np.random.RandomState(432).normal(0, 0.0002, n), 'dec': dec+np.random.RandomState(654).normal(0, 0.0002, n)})

    results = FoFCatalogMatching.match({'a': cat_a, 'b':cat_b, 'c':cat_c}, {3: 3, 2: 3, 1: None})

    assert len(results) == n*3
    for group in results.groups:
        assert len(group) == 3
        assert (group['row_index'] == group['row_index'][0]).all()
        assert all(c in group['catalog_key'] for c in 'abc')
