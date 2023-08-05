""" Note that the calibration starts from the LBL files, not the IMG !!! """
from __future__ import division, print_function

import logging
import os
from os.path import join as pjoin
from pathlib import Path

import numpy as np

try:
    from pysis import IsisPool
    from pysis.exceptions import ProcessError
    from pysis.isis import (ciss2isis, cisscal, dstripe, editlab, getkey, isis2std,
                            ringscam2map, spiceinit)
    from pysis.util import file_variations
except ImportError:
    print("Cannot load the ISIS system. pipeline module not functional.")
else:
    ISISDATA = Path(os.environ['ISIS3DATA'])

from . import io


def calib_to_isis(pm_or_path):
    try:
        img_name = str(pm_or_path.calib_label)
    except AttributeError:
        img_name = str(pm_or_path)
    (cub_name,) = file_variations(img_name, ['.cub'])
    try:
        ciss2isis(from_=img_name, to=cub_name)
    except ProcessError as e:
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return
    return cub_name


def calibrate_ciss(img_name, ringdata=True, map_project=False):
    """
    Calibrate raw Cassini ISS images using ISIS.

    ISIS is using an official released version the calibration routine `cisscal`
    that is being developed under IDL, but has been converted to C++ for ISIS.
    I am using the pipeline as described here:
    https://isis.astrogeology.usgs.gov/IsisWorkshop/index.php/Working_with_Cassini_ISS_Data
    It is customary to indicate the pipeline of ISIS apps that a file went through
    with a chain of extensions, e.g. '.cal.dst.map.cub', indicating calibration, destriping,
    and map projection.

    Parameters
    ----------
    img_name : pathlib.Path, str
        Absolute path to image

    Returns
    -------
    str : absolute path to map-projected ISIS cube.
    """
    # Check if img_name is maybe a PathManager object with a `raw_label` attribute:
    try:
        img_name = str(img_name.raw_label)
    except AttributeError:
        # doesn't seem to be the case, so I assume it's just a path
        img_name = str(img_name)
    (cub_name,
     cal_name,
     dst_name,
     map_name) = file_variations(img_name,
                                 ['.cub',
                                  '.cal.cub',
                                  '.cal.dst.cub',
                                  '.cal.dst.map.cub'])
    ciss2isis(from_=img_name, to=cub_name)
    logging.info("Import to ISIS done.")
    targetname = getkey(from_=cub_name,
                        grp='instrument',
                        keyword='targetname')
    # forcing the target name to Saturn here, because some observations of
    # the rings have moons as a target, but then the standard map projection
    # onto the Saturn ring plane fails.
    # see also
    # https://isis.astrogeology.usgs.gov/IsisSupport/index.php/topic,3922.0.html
    if targetname.lower() != 'saturn':
        editlab(from_=cub_name, options='modkey',
                keyword='TargetName', value='Saturn',
                grpname='Instrument')

    # perform either normal spiceinit or one for ringdata
    if ringdata is True:
        spiceinit(from_=cub_name, cksmithed='yes', spksmithed='yes',
                  shape='ringplane')
    else:
        spiceinit(from_=cub_name, cksmithed='yes', spksmithed='yes')
    logging.info("spiceinit done.")
    cisscal(from_=cub_name, to=cal_name, units='I/F')
    logging.info('cisscal done.')
    dstripe(from_=cal_name, to=dst_name, mode='horizontal')
    logging.info('Destriping done.')
    if map_project:
        ringscam2map(from_=dst_name, to=map_name, defaultrange='Camera',
                     map=ISISDATA / 'base/templates/maps/ringcylindrical.map')
        isis2std(from_=map_name, to=map_name[:-3] + 'tif', format='tiff')
        logging.info('Map projecting done. Function finished.')
    else:
        isis2std(from_=dst_name, to=dst_name[:-3] + 'tif', format='tiff',
                 minpercent=0, maxpercent=100)
        logging.warning('Map projection was skipped, set map_project to True if wanted.')
    return map_name


def remapping(img_name):
    (cal_name, map_name) = file_variations(img_name,
                                           ['.cal.cub', '.map.cal.cub'])
    print("Mapping", cal_name, "to", map_name)
    mapfname = pjoin(io.HOME, 'data', 'ciss', 'opus', 'ringcylindrical.map')
    ringscam2map(from_=cal_name, to=map_name, map=mapfname, pixres='map')


def calibrate_many(images):
    images = [[img_name, ] + file_variations(img_name, ['.cub', '.cal.cub',
                                                        '.map.cal.cub'])
              for img_name in images]

    with IsisPool() as isis_pool:
        for img_name, cub_name, cal_name, map_name in images:
            isis_pool.ciss2isis(from_=img_name, to=cub_name)

    return images


def remove_mean_value(data, axis=1):
    mean_value = np.nanmean(data, axis=axis)
    subtracted = data - mean_value[:, np.newaxis]
    return subtracted
