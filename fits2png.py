import glob
import sys

def fits2png(fitsfile):
    imstat_image = imstat(fitsfile)
    noise = imstat_image['medabsdevmed'][0]
    peak = imstat_image['max'][0]
    scaling =  np.min([0, -np.log(1.0*peak/noise)+4])
    level0 = 3.0
    levels = level0*np.sqrt(8**np.arange(20))
    imview(raster={'file':fitsfile,
                   'colormap':'Greyscale 1',
                   'scaling': float(scaling),
                   'colorwedge':True},
           contour = {'file':fitsfile,
                      'levels':list(levels),
                      'color':'green',
                      'base':0,
                      'unit':float(noise)*2.},
           out = fitsfile+'.png')

name = sys.argv[-1]
print(name)
print('Searching files matching: {0}*fits'.format(name))
filenames = glob.glob('{0}*.fits'.format(name))
print('Converting files: {0}'.format(filenames))
for filename in filenames:
    fits2png(filename)


