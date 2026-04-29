# Adapted from: https://www.machinelearningplus.com/python/cprofile-how-to-profile-your-python-code/
# Install the snakeviz module:
# pip install snakeviz
# %load_ext snakeviz
#
# Then CLI-call snakeviz with the profiled script or function:
# %snakeviz bessel_kernel(4)

import cProfile, pstats
from bessel_kernel import *


if __name__ == '__main__':
    # call directly cProfile
    #cProfile.run('re.compile("bessel_kernel(4)")')
    #cProfile.run('bessel_kernel(4)')
    
    #...or use the Profile class, which introduces more benefits
    prof = cProfile.Profile()
    prof.enable()
    bessel_kernel(4)
    prof.disable()
    
    p = pstats.Stats(prof).sort_stats('tottime')
    #p.strip_dirs()
    p.print_stats()
    #p.dump_stats('./export-data')
    