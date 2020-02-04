# multilambda_catalogs

`multilambda_catalogs.py` script takes R.A., Dec coordinates to download images for several predefined surveys (can be selected manually) using the python module `SkyView` from `astroquery`. It will produce images for a given FoV, by default 35 arcmin, as the FoV of e-MERLIN L-band data.

Normal example:
```python
python multilambda_catalogs.py -n my_source -ra 10:00:00 -de 40:00:00
```
- By default will use a radius of 35 arcmin and will try to download the following catalogs:  
["NVSS","VLA FIRST (1.4 GHz)", "WENSS", "TGSS ADR1", "VLSSr", "SDSSr", "DSS", "2MASS-H"]

- Source name can specify a directory location, for example:

```python
python multilambda_catalogs.py -n ./images/my_source -ra 10:00:00 -de 40:00:00
```
- The output is a set of fits file with the images from the available catalogs

### Requirements


### Usage

```
usage: multilambda_catalogs.py [-h] [-n NAME] [-ra RA] [-de DE] [-r RADIUS]
                 [-s SURVEYS [SURVEYS ...]]

Select dataset

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name prefix for output images
  -ra RA                R.A. coordinates in format 00:00:00.0
  -de DE                Dec. coordinates in format +00:00:00.0
  -r RADIUS, --radius RADIUS
                        Search radius in armin
  -s SURVEYS [SURVEYS ...], --surveys SURVEYS [SURVEYS ...]
                        Whispace separated list of surveys

```


