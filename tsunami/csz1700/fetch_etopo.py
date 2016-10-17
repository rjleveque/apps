"""
Simple script to download etopo1 topography/bathymetry data from
    http://www.ngdc.noaa.gov/mgg/global/global.html

The etopo1 data has 1-arcminute resolution, but you can request coarsening.
E.g. set resolution = 4./60. for 4-arcminute resolution.

"""

import os
from clawpack.geoclaw import etopotools


plot_topo = False

# Set the limits of the domain and resolution:

xlimits = (-150, -121)
ylimits = (37,52)
resolution = 1./60.   # degrees

# If user environment variable ETOPO is set to a valid path to a directory, 
# downloaded data will be stored there.  Allows sharing same data among
# various projects.

try:
    etopo_dir = os.environ['ETOPO']
    # make sure it's a valid directory
    assert os.path.isdir(etopo_dir), ''
except:
    print "ETOPO not set or invalid directory, setting etopo_dir='.'"
    etopo_dir = '.'

topo = etopotools.etopo1_download(xlimits,ylimits, dx=resolution, \
        output_dir=etopo_dir, return_topo=True)


if plot_topo:
    # plot the topo and save as a png file...
    import matplotlib.pyplot as plt
    topo.plot()
    topo_file_name = os.path.split(topo.path)[-1]
    plt.title('Topo file %s' % topo_file_name)
    fname = os.path.splitext(topo_file_name)[0] + '.png'
    fname = os.path.join(etopo_dir, fname)
    plt.savefig(fname)
    print 'Created %s' % fname

