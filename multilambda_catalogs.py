import os
import argparse
from astropy.coordinates import SkyCoord
from astroquery.skyview import SkyView
from astropy import units as u
import requests
import astropy


def get_url(coords, surveys, radius=None, width=None, height=None):
    print('Reading urls')
    urls = []
    valid_surveys = []
    missing_surveys = []
    for survey in surveys:
        url = SkyView.get_image_list(position=coords,
                                 survey=survey,
                                 radius=radius,
                                 width=width,
                                 height=height)
        if url != []:
            if requests.get(url[0]).status_code != 404:
                urls.append(url)
                valid_surveys.append(survey)
            print('OK:     ', survey)
        else:
            missing_surveys.append(survey)
            print('Failed: ', survey)
    for u,s in zip(urls, valid_surveys):
        print(u,s)
    return urls, valid_surveys, missing_surveys

def filter_available(urls):
    print('Checking file availability')
    status = [requests.get(url).status_code for url in urls]
    available = [s!=404 for s in status]
    return available

def download_image(coords, surveys, name='field', radius=None, width=None, height=None):
    print('Getting fitsfiles')
    fitsfiles = SkyView.get_images(position=coords,
                              survey=surveys,
                              radius=radius,
                              width=width,
                              height=height)
    os.system('mkdir catalogs')
    for fitsfile, survey in zip(fitsfiles, surveys):
        print('Writing to file: {0} ...'.format(survey), end='')
        filename = f'./catalogs/{name}_{survey}.fits'.replace(' ', '_')
        try:
            fitsfile[0].writeto(filename, overwrite=True)
            print('...Done')
        except astropy.io.fits.verify.VerifyError:
            print('...Failed')

def generate_png(name, casa):
    casa_command = f'{casa} --nologger --nologfile --nogui -c fits2png.py ./catalogs/{name}'
    print('Trying to execute casa command:')
    print(casa_command)
    try:
        os.system(casa_command)
    except:
        print('Could not execute CASA script. Try specifying casa executable with -casa /path/to/bin/casa')

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Select dataset'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n', '--name', dest='name', help='Name prefix for output images', default='field')
    parser.add_argument('-ra', dest='ra', help='R.A. coordinates in format  00:00:00.0')
    parser.add_argument('-de', dest='de', help='Dec. coordinates in format +00:00:00.0')
    parser.add_argument('-r', '--radius', dest='radius', help='Search radius in armin', default=35.)
    parser.add_argument('-c', '--casa', dest='casa', help='casa version to use', default='casa')
    default_surveys = ["NVSS","VLA FIRST (1.4 GHz)", "WENSS", "TGSS ADR1", "VLSSr", "SDSSr", "DSS", "2MASS-H"]
    parser.add_argument('-s', '--surveys', dest='surveys',
                        type=str, nargs='+',
                        help='Whispace separated list of surveys',
                        default=default_surveys)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    name = args.name
    coords = SkyCoord(args.ra, args.de, unit=(u.hourangle, u.deg), frame='icrs')
    radius = args.radius*u.arcmin
    surveys = args.surveys
    print(surveys)
    urls, valid_surveys, missing_surveys = get_url(coords=coords, surveys=surveys, radius=radius)
    download_image(coords=coords, surveys=valid_surveys, radius=radius, name=name)
    casa = args.casa
    generate_png(name, casa)




# https://astroquery.readthedocs.io/en/latest/skyview/skyview.html
# https://docs.astropy.org/en/stable/coordinates/
# https://astroquery.readthedocs.io/en/latest/skyview/skyview.html
# https://github.com/aframosp/Review-Photcode/blob/96f2ddcafa73ce9148b11d4cab8be22a7a47c4c7/SkyView_Galaxies.ipynb
# https://github.com/andreww5au/Prosp/blob/849cdbdf0cebfbd76c5b9484cdb76e12a0a7556d/skyviewint.py
