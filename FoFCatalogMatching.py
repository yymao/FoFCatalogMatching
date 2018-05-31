"""
FoFCatalogMatching
"""
import numpy as np
from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
from fast3tree import find_friends_of_friends

__version__ = '0.1.0'
__all__ = ['match']


def _check_max_count(count):
    if count is not None:
        count = int(count)
        if count < 1:
            raise ValueError('`count` must be None or a positive integer.')
        return count


def _arcsec2dist(sep, r=1.0):
    return np.sin(np.deg2rad(sep / 3600.0 / 2.0)) * 2.0 * r


def match(catalog_dict, linking_lengths,
          ra_label='ra', dec_label='dec',
          ra_unit='deg', dec_unit='deg', catalog_len_getter=len):

    """
    Match multiple catalogs.
    Ruturns an astropy Table that have group id and row id in each catalog.

    Parameters
    ----------
    catalog_dict : dict
        Catalogs to match.
        In the format of {'cat_a': catalog_table_a, 'cat_b': catalog_table_b, }

    linking_lengths : dict or float
        FoF linking length. Assuming the unit of arcsecond.
        Can specify multiple values with the maximal allowed numbers in each group.
        Use `None` to mean to constraint.
        Example: {5.0: 5, 4.0: 5, 3.0: 4, 2.0: 3, 1.0: None}

    ra_label : str, optional, default: 'ra'
    dec_label : str, optional, default: 'dec'
    ra_unit : str or astropy.units.Unit, optional, default: 'deg'
    dec_unit : str or astropy.units.Unit, optional, default: 'deg'
    catalog_len_getter : callable, optional, default: len

    Returns
    -------
    matched_catalog : astropy.table.Table
    """

    if isinstance(linking_lengths, dict):
        linking_lengths = [(float(k), _check_max_count(linking_lengths[k])) \
                for k in sorted(linking_lengths, key=float, reverse=True)]
    else:
        linking_lengths = [(float(linking_lengths), None)]

    stacked_catalog = []
    for catalog_key, catalog in catalog_dict.items():
        if catalog is None:
            continue

        n_rows = catalog_len_getter(catalog)
        stacked_catalog.append(Table({
            'ra': catalog[ra_label],
            'dec': catalog[dec_label],
            'row_index': np.arange(n_rows),
            'catalog_key': np.repeat(catalog_key, n_rows),
        }))

    if not stacked_catalog:
        raise ValueError('No catalogs to merge!!')

    stacked_catalog = vstack(stacked_catalog, 'exact', 'error')
    points = SkyCoord(stacked_catalog['ra'], stacked_catalog['dec'], unit=(ra_unit, dec_unit)).cartesian.xyz.value.T
    del stacked_catalog['ra'], stacked_catalog['dec']

    group_id = regroup_mask = group_id_shift = None

    for linking_length_arcsec, max_count in linking_lengths:
        d = _arcsec2dist(linking_length_arcsec)

        if group_id is None:
            group_id = find_friends_of_friends(points, d, reassign_group_indices=False)
        else:
            group_id[regroup_mask] = find_friends_of_friends(points[regroup_mask], d, reassign_group_indices=False)
            group_id[regroup_mask] += group_id_shift

        if max_count is None:
            _, group_id = np.unique(group_id, return_inverse=True)
            break

        _, group_id, counts = np.unique(group_id, return_inverse=True, return_counts=True)
        group_id_shift = group_id.max() + 1
        regroup_mask = (counts[group_id] > max_count)
        del counts

        if not regroup_mask.any():
            break

    stacked_catalog['group_id'] = group_id
    del points, group_id, regroup_mask

    return stacked_catalog.group_by('group_id')
