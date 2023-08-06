# -*- coding: utf-8 -*-

from __future__ import print_function

"""
Calculate effective infrared pumping rates by solar radiation as
a black body radiation field
"""

import numpy as np
from astroquery.lamda import Lamda
from astroquery.hitran import read_hitran_file, download_hitran, cache_location
from scipy import constants
import argparse
import itertools
import os

def omega(theta):
    """Solid angle subtended by the Sun

    Parameters
    ----------
    theta : float
        Angular diameter of the Sun

    Returns
    -------
    omega : float
        The resulting solid angle for the Sun
        https://en.wikipedia.org/wiki/Solid_angle"""
    omega = 2*np.pi*(1-np.cos(theta/2))
    return omega


def glu(sigma, gu, gl):
    """Pumping rate from lower to upper level glu
    divided by the Einstein coefficient Aul
    (equation A7 from Crovisier & Encrenaz 1983)

    Parameters
    ----------
    sigma : float
        wavenumber in units of cm-1
    gu : float
        upper level degeneracy
    gl : float
        lower level degeneracy

    Returns
    -------
    glu : float
        This is glu/Aul
    """
    # solid angle subtended by the Sun at 1 AU
    om = omega(9.35e-3)
    # black-body Sun temperature in K
    Tbb = 5778
    glu = om/4./np.pi*gu/gl/\
        (np.exp(constants.h*constants.c*sigma*1e2/constants.k/Tbb)-1)
    return glu


def hitran_bands(df):
    """Print all bands in HITRAN transitions

    Parameters
    ----------
    df : pandas DataFrame

    """
    bands = df.global_upper_quanta.unique()
    for b in bands:
        nu = df[(df.global_upper_quanta.str.contains(b))
                & (df.global_lower_quanta.str.contains(b'GROUND'))
                ].nu.mean()
        print(b, nu)


def lamda_to_hitran(level, mol):
    """Convert methanol levels from Lamda to HITRAN notation
    """
    import re
    if mol == "aCH3OH":
        m = re.match('(\d+)_(-?)(\d+)', level)
        if m.group(2) == '-':
            quanta = m.group(1).rjust(3)+m.group(3).rjust(3)+'  A-     '
        else:
            quanta = m.group(1).rjust(3)+m.group(3).rjust(3)+'  A+     '
    elif mol == "eCH3OH":
        m = re.match('(\d+)_(-?)(\d+)', level)
        if m.group(2) == '-':
            quanta = m.group(1).rjust(3)+m.group(3).rjust(3)+'  E2     '
        else:
            quanta = m.group(1).rjust(3)+m.group(3).rjust(3)+'  E1     '
    elif mol == "H2O":
        m = re.match('(\d+)_(\d+)_(\d+)', level)
        quanta = m.group(1).rjust(3)+m.group(2).rjust(3)+m.group(3).rjust(3)+'      '
    return quanta.encode('utf-8')


# Read path to HITRAN data from environment variable
HITRAN_DATA = os.environ.get(
    "HITRAN_DATA",
    cache_location
)

# names in LAMDA database
lamda = {'H2O': 'oh2o@daniel',
        'HDO': 'hdo',
        'aCH3OH': 'a-ch3oh',
        'eCH3OH': 'e-ch3oh'}
ground_band = {'H2O': b'0 0 0',
               'HDO': b'0 0 0',
               'aCH3OH': b'GROUND',
               'eCH3OH': b'GROUND'}
excitation_band = {'H2O': ['0 0 1', '0 1 0', '1 0 0', '1 0 1', '0 1 1'],
                   # b' *[01] [01] [01] *',
                   'HDO': b'.*',
                   # bands with transitions to ground state
                   'aCH3OH': ['4V12', 'V12', 'V7', 'V8'],
                   'eCH3OH': ['3V12', 'V12', 'V7', 'V8']}
species = {'H2O': b'',
           'HDO': b'',
           'aCH3OH': b'A',
           'eCH3OH': b'E'}

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mol", default="H2O", choices=lamda.keys(), help="molecule")
parser.add_argument("-n", "--nlevels", type=int, default=-1, help="number of levels")
parser.add_argument("-r", "--rh", type=float, default=1., help="heliocentric distance")
args = parser.parse_args()

tbl = read_hitran_file(os.path.join(HITRAN_DATA,
                                    '{0}.data'.format(''.join(x for x in args.mol if not x.islower()))),
                       # formatfile=os.path.join(HITRAN_DATA, 'readme.txt')
                       ).to_pandas()


collrates,radtransitions,enlevels = Lamda.query(mol=lamda[args.mol])

levels = enlevels.to_pandas()

levels.loc[:,'local_quanta'] = levels['J'].apply(lamda_to_hitran, args=(args.mol,))

lamda_levels = levels.Energy.values
if args.mol == 'aCH3OH':
    # Fix a bug in energy levels for aCH3OH in HITRAN 2012
    lamda_levels += 128.1069

# select species
tbl = tbl[tbl["local_lower_quanta"].str.contains(species[args.mol])]

# select bands with vibrational transitions to ground state
trans = tbl[
            # mol['global_lower_quanta'].str.contains(ground_band[args.mol]) &
            # ~mol['global_upper_quanta'].str.contains(ground_band[args.mol])
            tbl['global_upper_quanta'].isin([i.rjust(15).encode('utf-8') for i in excitation_band[args.mol]])
            # & mol['global_upper_quanta'].str.match(excitation_band[args.mol])
            # & mol['global_upper_quanta'].str.contains(b'1 0 0')
            # & np.isclose(mol["elower"].values[:, None], lamda_levels, atol=.01).any(axis=1)
            # & mol["local_lower_quanta"].isin(levels["local_quanta"])
            ]

# hitran_bands(trans, args.mol)

hitran_levels = tbl[tbl['global_lower_quanta'].str.contains(ground_band[args.mol])]["local_lower_quanta"].unique()

nlev = len(lamda_levels)
# nlev = len(hitran_levels)
gcube = np.zeros((nlev, nlev))

# group transitions by common upper level
grouped = trans.groupby(['global_upper_quanta', 'local_upper_quanta'])

# print(trans[~trans.global_lower_quanta.str.contains(b'0 0 0')])

# select upper level from any band different from ground
for _, group in grouped:
    if len(group) >= 2:
        # transitions that go to the lamda levels in the ground state
        ground = group[
            group['global_lower_quanta'].str.contains(ground_band[args.mol]) &
            group['local_lower_quanta'].isin(levels["local_quanta"]) ]
        if len(ground) >= 2:
            # transitions from k to ground level
            Asum = group['a'].sum()
            # add a new column with glu values
            ground.loc[:,'glu'] = glu(ground['nu'], ground['gp'], ground['gpp'])
            # combination of pairs of possible levels in ground vibrational state
            for lo, up in itertools.combinations(ground['local_lower_quanta'], 2):
                trans_lo = ground[ground['local_lower_quanta'] == lo]
                trans_up = ground[ground['local_lower_quanta'] == up]
                # multiply Aeins for the pair
                Aprod = ground[ground['local_lower_quanta'].isin([lo, up])]['a'].product()
                if lo != up:
                    i = levels[levels["local_quanta"] == lo]["Level"].values[0]
                    j = levels[levels["local_quanta"] == up]["Level"].values[0]
                    gcube[i-1, j-1] += trans_lo['glu'].values[0]*Aprod/Asum
                    gcube[j-1, i-1] += trans_up['glu'].values[0]*Aprod/Asum

gcube /= args.rh**2
# print(gcube[:7,:7])
ii,jj = np.nonzero(gcube[:args.nlevels,:args.nlevels])

for i,j in zip(ii, jj):
    print(i+1, j+1, gcube[j,i])

# np.savetxt('G_ch3oh.dat', gcube)
