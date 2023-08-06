from __future__ import print_function, division

"""
.. note::
         These are the spectral modeling functions for SPLAT 
"""
# imports: internal
import copy
import glob
import os
import requests
import sys
import time

# imports: external
import numpy
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy import stats
from scipy.integrate import trapz        # for numerical integration
from scipy.interpolate import griddata, interp1d
import scipy.optimize as op
from astropy.io import ascii            # for reading in spreadsheet
from astropy.table import Table
from astropy.table import unique as tunique
import astropy.units as u

#from splat._initialize import *
from . import triangle             # will want to move this to corner
from .initialize import *
from .utilities import *
from . import plot as splot
from . import photometry as spphot
from . import empirical as spemp
from .core import Spectrum, classifyByIndex, compareSpectra, _generateMask

# some constants
MODELS_READIN = {}


#######################################################
#######################################################
##################   MODEL LOADING  ###################
#######################################################
#######################################################



def processModels(**kwargs):
    '''
    :Purpose: Generates a set of smoothed models and SEDs for an input model set; this is a function that requires 'superuser' access
    '''

    if checkAccess() is not True:
        print('\nThis routine may only be run by SPLAT administrators\n')
        return

# ALLARD files
    if kwargs.get('model',' ').lower() == 'btsettl2015':
        basefolder = os.path.expanduser("~")+'/models/allard/cifist2015/BT-Settl_M-0.0a+0.0/'
        files = glob.glob(basefolder+'lte*.7')
        teff = [100.*float(f[len(basefolder)+3:len(basefolder)+8]) for f in files]
        logg = [float(f[len(basefolder)+9:len(basefolder)+12]) for f in files]
        z = [float(f[len(basefolder)+12:len(basefolder)+16]) for f in files]

# baseline spectrum for wavelength solution        
        ospex = Spectrum(10001) 
#        uspex = Spectrum(12160)      - need to make this file available before using

        for f in files:
# read in file
            print('\nReading in file {}'.format(f))
            data = ascii.read(f,format='tab')
            wave  = numpy.array([float(x[0][0:13])/1.e4 for x in data])
            flux = numpy.array([10.**(float(x[0][13:25].replace('D','e'))-8.) for x in data])

# generate SpeX formats using a baseline spectrum
# THIS IS A TEMPORARY SET UP  
            w = numpy.where(numpy.logical_and(wave >= 0.6,wave <= 2.5))
            sp = Spectrum(wave=wave[w],flux=flux[w])
            wn = wave[numpy.where(numpy.logical_and(wave >= 1.6,wave <= 1.7))]
            sp.resolution = wn[1]/(wn[1]-wn[0])
            sp.smooth(resolution=200)
            s03 = sp.copy()




def _checkModelName(model):
    '''

    Purpose: 
        Checks that an input model name is one of the available spectral models, including a check of alternate names

    Required Inputs:
        :param: model: A string containing the spectral model to be checked. This should be one of the models listed in `loadModel()`_

    .. _`loadModel()` : api.html#splat_model.loadModel
        
    Optional Inputs:
        None

    Output:
        A string containing SPLAT's default name for a given model set, or False if that model set is not present

    Example:

    >>> import splat
    >>> print(splat._checkModelName('burrows'))
        burrows06
    >>> print(splat._checkModelName('allard'))
        BTSettl2008
    >>> print(splat._checkModelName('somethingelse'))
        False
    '''
    output = False
    if not isinstance(model,str):
        return output
    for k in list(DEFINED_MODEL_SETS.keys()):
        if model.lower()==k.lower() or model.lower() in DEFINED_MODEL_SETS[k]:
            output = k
    return output



def loadModel(*args, **kwargs):
    '''
    .. Note: this needs some clean up    

    Purpose: 
        Loads up a model spectrum based on a set of input parameters. The models may be any one of the following listed below. For parameters between the model grid points, loadModel calls the function `loadInterpolatedModel()`_.

    .. _`loadInterpolatedModel()` : api.html#splat_model.loadInterpolatedModel

    Required Inputs:
        :param: **model**: The model set to use; may be one of the following:

            - *BTSettl2008*: (default) model set from `Allard et al. (2012) <http://adsabs.harvard.edu/abs/2012RSPTA.370.2765A>`_  with effective temperatures of 400 to 2900 K (steps of 100 K); surface gravities of 3.5 to 5.5 in units of cm/s^2 (steps of 0.5 dex); and metallicity of -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.3, and 0.5 for temperatures greater than 2000 K only; cloud opacity is fixed in this model, and equilibrium chemistry is assumed. Note that this grid is not completely filled and some gaps have been interpolated (alternate designations: `btsettled`, `btsettl`, `allard`, `allard12`)
            - *burrows06*: model set from `Burrows et al. (2006) <http://adsabs.harvard.edu/abs/2006ApJ...640.1063B>`_ with effective temperatures of 700 to 2000 K (steps of 50 K); surface gravities of 4.5 to 5.5 in units of cm/s^2 (steps of 0.1 dex); metallicity of -0.5, 0.0 and 0.5; and either no clouds or grain size 100 microns (fsed = 'nc' or 'f100'). equilibrium chemistry is assumed. Note that this grid is not completely filled and some gaps have been interpolated (alternate designations: `burrows`, `burrows2006`)
            - *morley12*: model set from `Morley et al. (2012) <http://adsabs.harvard.edu/abs/2012ApJ...756..172M>`_ with effective temperatures of 400 to 1300 K (steps of 50 K); surface gravities of 4.0 to 5.5 in units of cm/s^2 (steps of 0.5 dex); and sedimentation efficiency (fsed) of 2, 3, 4 or 5; metallicity is fixed to solar, equilibrium chemistry is assumed, and there are no clouds associated with this model (alternate designations: `morley2012`)
            - *morley14*: model set from `Morley et al. (2014) <http://adsabs.harvard.edu/abs/2014ApJ...787...78M>`_ with effective temperatures of 200 to 450 K (steps of 25 K) and surface gravities of 3.0 to 5.0 in units of cm/s^2 (steps of 0.5 dex); metallicity is fixed to solar, equilibrium chemistry is assumed, sedimentation efficiency is fixed at fsed = 5, and cloud coverage fixed at 50% (alternate designations: `morley2014`)
            - *saumon12*: model set from `Saumon et al. (2012) <http://adsabs.harvard.edu/abs/2012ApJ...750...74S>`_ with effective temperatures of 400 to 1500 K (steps of 50 K); and surface gravities of 3.0 to 5.5 in units of cm/s^2 (steps of 0.5 dex); metallicity is fixed to solar, equilibrium chemistry is assumed, and no clouds are associated with these models (alternate designations: `saumon`, `saumon2012`)
            - *drift*: model set from `Witte et al. (2011) <http://adsabs.harvard.edu/abs/2011A%26A...529A..44W>`_ with effective temperatures of 1700 to 3000 K (steps of 50 K); surface gravities of 5.0 and 5.5 in units of cm/s^2; and metallicities of -3.0 to 0.0 (in steps of 0.5 dex); cloud opacity is fixed in this model, equilibrium chemistry is assumed (alternate designations: `witte`, `witte2011`, `helling`)
        
    Optional Inputs:
        :param: **teff**: effective temperature of the model in K (e.g. `teff` = 1000)
        :param: **logg**: log10 of the surface gravity of the model in cm/s^2 units (e.g. `logg` = 5.0)
        :param: **z**: log10 of metallicity of the model relative to solar metallicity (e.g. `z` = -0.5)
        :param: **fsed**: sedimentation efficiency of the model (e.g. `fsed` = 'f2')
        :param: **cld**: cloud shape function of the model (e.g. `cld` = 'f50')
        :param: **kzz**: vertical eddy diffusion coefficient of the model (e.g. `kzz` = 2)
        :param: **slit**: slit weight of the model in arcseconds (e.g. `slit` = 0.3)
        :param: **sed**: if set to True, returns a broad-band spectrum spanning 0.3-30 micron (applies only for BTSettl2008 models with Teff < 2000 K)

        :param: **local**: set to True to force program to read in local models (default = True)
        :param: **online**: set to True to force program to read in models from SPLAT webpage (default = False)
        :param: **folder**: string of the folder name containing the model set (default = '')
        :param: **filename**: string of the filename of the desired model; should be a space-delimited file containing columns for wavelength (units of microns) and surface flux (F_lambda units of erg/cm^2/s/micron) (default = '')
        :param: **force**: force the filename to be exactly as specified
        :param: **url**: string of the url to the SPLAT website (default = 'http://www.browndwarfs.org/splat/')

    Output:
        A SPLAT Spectrum object of the interpolated model with wavelength in microns and surface fluxes in F_lambda units of erg/cm^2/s/micron.

    Example:

    >>> import splat
    >>> mdl = splat.loadModel(teff=1000,logg=5.0)
    >>> mdl.info()
        BTSettl2008 model with the following parmeters:
        Teff = 1000 K
        logg = 5.0 cm/s2
        z = 0.0
        fsed = nc
        cld = nc
        kzz = eq
        Smoothed to slit width 0.5 arcseconds
    >>> mdl = splat.loadModel(teff=2500,logg=5.0,model='burrows')
        Input value for teff = 2500 out of range for model set burrows06
        Warning: Creating an empty Spectrum object
    '''


# path to model and set local/online
# by default assume models come from local SPLAT directory
    local = kwargs.get('local',True)
    online = kwargs.get('online',not local and not checkOnline())
    local = not online
    kwargs['local'] = local
    kwargs['online'] = online
    kwargs['folder'] = kwargs.get('folder','')
    kwargs['ismodel'] = True
    kwargs['force'] = kwargs.get('force',False)
    url = kwargs.get('url',SPLAT_URL)


# a filename has been passed - assume this file is a local file
# and check that the path is correct if its fully provided
# otherwise assume path is inside model set folder
    if (len(args) > 0):
        kwargs['filename'] = args[0]
        if not os.path.exists(kwargs['filename']):
            kwargs['filename'] = kwargs['folder']+os.path.basename(kwargs['filename'])
            if not os.path.exists(kwargs['filename']):
                raise NameError('\nCould not find model file {} or {}'.format(kwargs['filename'],kwargs['folder']+os.path.basename(kwargs['filename'])))
            else:
                return Spectrum(**kwargs)
        else:
            return Spectrum(**kwargs)


#    elif:
#        loadInterpolatedModel(**kwargs)


# set up the model set
    kwargs['model'] = kwargs.get('model','BTSettl2008')
    kwargs['model'] = kwargs.get('set',kwargs['model'])
    if kwargs.get('sed',False):
        kwargs['model'] = 'BTSettl2008'


# set replacements
    kwargs['model'] = _checkModelName(kwargs['model'])

#    if kwargs['model'].lower() == 'btsettl2008' or kwargs['model'].lower() == 'btsettl' or kwargs['model'].lower() == 'btsettled' or kwargs['model'].lower() == 'allard' or kwargs['model'].lower() == 'allard12' or kwargs['model'].lower() == 'allard2012':
#        kwargs['model'] = 'BTSettl2008'
#    if kwargs['model'].lower() == 'burrows06' or kwargs['model'].lower() == 'burrows' or kwargs['model'].lower() == 'burrows2006':
#        kwargs['model'] = 'burrows06'
#    if kwargs['model'].lower() == 'morley12' or kwargs['model'].lower() == 'morley2012':
#        kwargs['model'] = 'morley12'
#    if kwargs['model'].lower() == 'morley14' or kwargs['model'].lower() == 'morley2014':
#        kwargs['model'] = 'morley14'
#    if kwargs['model'].lower() == 'saumon12' or kwargs['model'].lower() == 'saumon' or kwargs['model'].lower() == 'saumon2012':
#        kwargs['model'] = 'saumon12'
#    if kwargs['model'].lower() == 'drift' or kwargs['model'].lower() == 'witte' or kwargs['model'].lower() == 'witte2011' or kwargs['model'].lower() == 'witte11' or kwargs['model'].lower() == 'helling':
#        kwargs['model'] = 'drift'
    kwargs['folder'] = SPLAT_PATH+SPECTRAL_MODEL_FOLDER+kwargs['model']+'/'

# preset defaults
    for ms in MODEL_PARAMETER_NAMES:
        kwargs[ms] = kwargs.get(ms,MODEL_PARAMETERS[ms])

# some special defaults
    if kwargs['model'] == 'morley12':
        if kwargs['fsed'] == 'nc':
            kwargs['fsed'] = 'f3'
    if kwargs['model'] == 'morley14':
        if kwargs['fsed'] == 'nc':
            kwargs['fsed'] = 'f5'
        if kwargs['cld'] == 'nc':
            kwargs['cld'] = 'f50'


# check that folder/set is present either locally or online
# if not present locally but present online, switch to this mode
# if not present at either raise error
    folder = checkLocal(kwargs['folder'])
    if folder=='':
        folder = checkOnline(kwargs['folder'])
        if folder=='':
            print('\nCould not find '+kwargs['folder']+' locally or on SPLAT website')
            print('\nAvailable model set options are:')
            for s in DEFINED_MODEL_SET:
                print('\t{}'.format(s))
            raise NameError()
        else:
            kwargs['folder'] = folder
            kwargs['local'] = False
            kwargs['online'] = True
    else:
        kwargs['folder'] = folder

# convert model parameters to unitless numbers
    for ms in MODEL_PARAMETER_NAMES:
        if isinstance(kwargs[ms],u.quantity.Quantity):
            kwargs[ms] = kwargs[ms].value

# generate model filename
    kwargs['filename'] = kwargs['folder']+kwargs['model']+'_{:.0f}_{:.1f}_{:.1f}_{}_{}_{}_{:.1f}.txt'.\
        format(float(kwargs['teff']),float(kwargs['logg']),float(kwargs['z'])-0.001,kwargs['fsed'],kwargs['cld'],kwargs['kzz'],float(kwargs['slit']))
    kwargs['name'] = kwargs['model']
    if kwargs.get('sed',False):
        kwargs['filename'] = kwargs['folder']+kwargs['model']+'_{:.0f}_{:.1f}_{:.1f}_nc_nc_eq_sed.txt'.\
            format(float(kwargs['teff']),float(kwargs['logg']),float(kwargs['z'])-0.001)
        kwargs['name'] = kwargs['model']+' SED'

# get model parameters
#        parameters = loadModelParameters(**kwargs)
#        kwargs['path'] = kwargs.get('path',parameters['path'])
# check that given parameters are in range
#        for ms in MODEL_PARAMETER_NAMES[0:3]:
#            if (float(kwargs[ms]) < parameters[ms][0] or float(kwargs[ms]) > parameters[ms][1]):
#                raise NameError('\n\nInput value for {} = {} out of range for model set {}\n'.format(ms,kwargs[ms],kwargs['set']))
#        for ms in MODEL_PARAMETER_NAMES[3:6]:
#            if (kwargs[ms] not in parameters[ms]):
#                raise NameError('\n\nInput value for {} = {} not one of the options for model set {}\n'.format(ms,kwargs[ms],kwargs['set']))



# check if file is present; if so, read it in, otherwise go to interpolated
# locally:
    if kwargs.get('local',True) == True:
        file = checkLocal(kwargs['filename'])
        if file=='':
            if kwargs['force']:
                raise NameError('\nCould not find '+kwargs['filename']+' locally\n\n')
            else:
                return loadInterpolatedModel(**kwargs)
#                kwargs['local']=False
#                kwargs['online']=True
        else:
            try:
                return Spectrum(**kwargs)
            except:
                raise NameError('\nProblem reading in '+kwargs['filename']+' locally\n\n')

# online:
    if kwargs['online']:
        file = checkOnline(kwargs['filename'])
        if file=='':
            if kwargs['force']:
                raise NameError('\nCould not find '+kwargs['filename']+' online\n\n')
            else:
                return loadInterpolatedModel(**kwargs)
        else:
            try:
                ftype = kwargs['filename'].split('.')[-1]
                tmp = TMPFILENAME+'.'+ftype
                open(os.path.basename(tmp), 'wb').write(requests.get(url+kwargs['filename']).content) 
                kwargs['filename'] = os.path.basename(tmp)
                sp = Spectrum(**kwargs)
                os.remove(os.path.basename(tmp))
                return sp
            except:
                raise NameError('\nProblem reading in '+kwargs['filename']+' from SPLAT website\n\n')


def getModel(*args, **kwargs):
    '''
    Purpose: 
        Redundant routine with `loadModel()`_ to match syntax of `getSpectrum()`_

    .. _`loadModel()` : api.html#splat_model.loadModel
    .. _`getSpectrum()` : api.html#splat.getSpectrum

    '''
    return loadModel(*args, **kwargs)


def _checkModelParametersInRange(mparam):
# list of model parameters provided
    mp = list(mparam.keys())
    if 'model' not in mp:
        mparam['model'] = 'BTSettl2008'
    parameters = _loadModelParameters(**mparam)
    flag = True

# check that given parameters are in model ranges
    for ms in MODEL_PARAMETER_NAMES[0:3]:
        if ms in mp:
            if (float(mparam[ms]) < numpy.min(parameters[ms]) or float(mparam[ms]) > numpy.max(parameters[ms])):
                print('\n\nInput value for {} = {} out of range for model set {}\n'.format(ms,mparam[ms],mparam['model']))
                flag = False
    for ms in MODEL_PARAMETER_NAMES[3:6]:
        if ms in mp:
            if (mparam[ms] not in parameters[ms]):
                print('\n\nInput value for {} = {} not one of the options for model set {}\n'.format(ms,mparam[ms],mparam['model']))
                flag = False
    return flag


def loadInterpolatedModel(*args,**kwargs):
    '''
    Purpose: 
        Generates as spectral model with is interpolated between model parameter grid points. This routine is called by `loadModel()`_, or it can be called on its own.

    .. _`loadModel()` : api.html#splat_model.loadModel

    Required Inputs:
        :param model: set of models to use; see options in `loadModel()`_

    Optional Inputs:
        :param: The parameters for `loadModel()`_ can also be used here.

    Output:
        A SPLAT Spectrum object of the interpolated model with wavelength in microns and surfae fluxes in F_lambda units of erg/cm^2/s/micron.

    Example:

    >>> import splat
    >>> mdl = splat.loadModel(teff=1000,logg=5.0)
    >>> mdl.info()
        morley12 model with the following parmeters:
        Teff = 540 K
        logg = 4.7 cm/s2
        z = 0.0
        fsed = f3
        cld = nc
        kzz = eq
        Smoothed to slit width 0.5 arcseconds
    '''
# attempt to generalize models to extra dimensions
    mkwargs = kwargs.copy()
    mkwargs['force'] = True
    mkwargs['ismodel'] = True
    mkwargs['url'] = kwargs.get('url',SPLAT_URL+'/Models/')
    mkwargs['model'] = kwargs.get('model','BTSettl2008')
    mkwargs['model'] = kwargs.get('set',mkwargs['model'])
    mkwargs['local'] = kwargs.get('local',False)
    for ms in MODEL_PARAMETER_NAMES:
        mkwargs[ms] = kwargs.get(ms,MODEL_PARAMETERS[ms])

    if mkwargs.get('sed',False):
        mkwargs['model'] = 'BTSettl2008'

# set replacements
    if mkwargs['model'].lower() == 'btsettl2008' or mkwargs['model'].lower() == 'btsettl' or mkwargs['model'].lower() == 'btsettled' or mkwargs['model'].lower() == 'allard' or mkwargs['model'].lower() == 'allard12' or mkwargs['model'].lower() == 'allard2012':
        mkwargs['model'] = 'BTSettl2008'
    if mkwargs['model'].lower() == 'burrows06' or mkwargs['model'].lower() == 'burrows' or mkwargs['model'].lower() == 'burrows2006':
        mkwargs['model'] = 'burrows06'
    if mkwargs['model'].lower() == 'morley12' or mkwargs['model'].lower() == 'morley2012':
        mkwargs['model'] = 'morley12'
    if mkwargs['model'].lower() == 'morley14' or mkwargs['model'].lower() == 'morley2014':
        mkwargs['model'] = 'morley14'
    if mkwargs['model'].lower() == 'saumon12' or mkwargs['model'].lower() == 'saumon' or mkwargs['model'].lower() == 'saumon2012':
        mkwargs['model'] = 'saumon12'
    if mkwargs['model'].lower() == 'drift' or mkwargs['model'].lower() == 'witte' or mkwargs['model'].lower() == 'witte2011' or mkwargs['model'].lower() == 'witte11' or mkwargs['model'].lower() == 'helling':
        mkwargs['model'] = 'drift'
    mkwargs['folder'] = SPLAT_PATH+SPECTRAL_MODEL_FOLDER+kwargs['model']+'/'

# some special defaults
    if mkwargs['model'] == 'morley12':
        if mkwargs['fsed'] == 'nc':
            mkwargs['fsed'] = 'f2'
    if mkwargs['model'] == 'morley14':
        if mkwargs['fsed'] == 'nc':
            mkwargs['fsed'] = 'f5'
        if mkwargs['cld'] == 'nc':
            mkwargs['cld'] = 'f50'

# first get model parameters
    parameters = _loadModelParameters(**mkwargs)
    if _checkModelParametersInRange(mkwargs) == False:
        raise ValueError('\n\nModel parameter values out of range for model set {}\n'.format(mkwargs['model']))
    
# check that given parameters are in range
    for ms in MODEL_PARAMETER_NAMES[0:3]:
        if (float(mkwargs[ms]) < numpy.min(parameters[ms]) or float(mkwargs[ms]) > numpy.max(parameters[ms])):
            raise ValueError('\n\nInput value for {} = {} out of range for model set {}\n'.format(ms,mkwargs[ms],mkwargs['model']))
#            return Spectrum()
    for ms in MODEL_PARAMETER_NAMES[3:6]:
        if (mkwargs[ms] not in parameters[ms]):
            raise ValueError('\n\nInput value for {} = {} not one of the options for model set {}\n'.format(ms,mkwargs[ms],mkwargs['model']))
#            return Spectrum()

# identify grid points around input parameters
# 3x3 grid for teff, logg, z

    tvals = numpy.array([float(p['teff']) for p in parameters['parameter_sets']])
    tdiff = numpy.array([numpy.log10(float(mkwargs['teff']))-numpy.log10(v) for v in tvals])
    gvals = numpy.array([float(p['logg']) for p in parameters['parameter_sets']])
    gdiff = numpy.array([float(mkwargs['logg'])-v for v in gvals])
    zvals = numpy.array([float(p['z']) for p in parameters['parameter_sets']])
    zdiff = numpy.array([float(mkwargs['z'])-v for v in zvals])
    dist = tdiff**2+gdiff**2+zdiff**2

# get closest models in 8 quadrant points
    mparams = []
    mparam_names = []
    psets = numpy.array(parameters['parameter_sets'])
    for i in numpy.arange(0,2):
        dt = dist[numpy.where(tdiff*((-1)**i)>=0)]
        pt = psets[numpy.where(tdiff*((-1)**i)>=0)]
        gt = gdiff[numpy.where(tdiff*((-1)**i)>=0)]
        zt = zdiff[numpy.where(tdiff*((-1)**i)>=0)]
        for j in numpy.arange(0,2):
            dg = dt[numpy.where(gt*((-1)**j)>=0)]
            pg = pt[numpy.where(gt*((-1)**j)>=0)]
            zg = zt[numpy.where(gt*((-1)**j)>=0)]
            for k in numpy.arange(0,2):
                dz = dg[numpy.where(zg*((-1)**k)>=0)]
                pz = pg[numpy.where(zg*((-1)**k)>=0)]

# if we can't get a quadrant point, quit out
                if len(pz) == 0: raise ValueError('\n\nModel parameter values out of range for model set {}\n'.format(mkwargs['model']))

                pcorner = pz[numpy.argmin(dz)]
                mparams.append(pz[numpy.argmin(dz)])
                mstr = ''
                for ms in MODEL_PARAMETER_NAMES: mstr+=str(mparams[-1][ms])
                mparam_names.append(mstr)

# generate meshgrid with slight offset and temperature on log scale
    rng = []
    for ms in MODEL_PARAMETER_NAMES[0:3]:
        vals = [float(m[ms]) for m in mparams]
        r = [numpy.min(vals),numpy.max(vals)]
        if numpy.absolute(r[0]-r[1]) < 1.e-3*numpy.absolute(parameters[ms][1]-parameters[ms][0]):
            r[1] = r[0]+1.e-3*numpy.absolute(parameters[ms][1]-parameters[ms][0])
        if ms == 'teff':
            r = numpy.log10(r)
        rng.append(r)
    mx,my,mz = numpy.meshgrid(rng[0],rng[1],rng[2])

# read in only unique models
    mpsmall = [dict(y) for y in set(tuple(x.items()) for x in mparams)]
#    mpsmall = numpy.unique(numpy.array(mparams))
    bmodels = []
    bmodel_names = []
    for m in mpsmall:
        bmodels.append(loadModel(**m))
        mstr = ''
        for ms in MODEL_PARAMETER_NAMES: mstr+=str(m[ms])
        bmodel_names.append(mstr)

# then back fill all models
    bmodels = numpy.array(bmodels)
    bmodel_names = numpy.array(bmodel_names)
    models = []
    for i,m in enumerate(mparam_names):
        models.append(bmodels[numpy.where(bmodel_names==m)][0])


# final interpolation
    mflx = []
    for i,w in enumerate(models[0].wave):
        val = numpy.array([numpy.log10(m.flux.value[i]) for m in models])
        mflx.append(10.**(griddata((mx.flatten(),my.flatten(),mz.flatten()),\
            val,(numpy.log10(float(mkwargs['teff'])),float(mkwargs['logg']),float(mkwargs['z'])),'linear')))

    return Spectrum(wave=models[0].wave,flux=mflx*models[0].funit,**mkwargs)




def _loadModelParameters(*args,**kwargs):
    '''
    Purpose: 
        Assistant routine for `loadModel()`_ that loads in the spectral model grid points.

    .. _`loadModel()` : api.html#splat_model.loadModel

    Required Inputs:
        :param: model: set of models to use; see options in `loadModel()`_ (default = 'BTSettl2008')

    Optional Inputs:
        :param old: Old format for returning model parameters based parameter.txt file; now obsolete (default = False)
    
    The parameters for `loadModel()`_ can also be used here.

    Output:
        A dictionary containing the individual parameter values for the grid points in the given model set (not all of these grid points will be filled); this dictionary includs a list of dictionaries containing the individual parameter sets.
    '''

# model set
    if len(args) == 0:
        if kwargs.get('model',False) == False:
            raise ValueError('\n\nYou must give a model name as either a variable or as keyword `model`')
        mset = kwargs['model']
    else: mset = args[0]

    if _checkModelName(mset) == False:
        raise NameError('\n\nInput model set {} not in defined set of models:\n{}\n'.format(mset,DEFINED_MODEL_SET))

    parameters = {'model': mset, 'parameter_sets': []}
    for ms in MODEL_PARAMETER_NAMES:
        parameters[ms] = []

# establish parameters from list of filenames
    if kwargs.get('old',False) == False:
        mfiles = glob.glob(SPLAT_PATH+SPECTRAL_MODEL_FOLDER+mset+'/'+mset+'*.txt')
        if len(mfiles) == 0:
            raise ValueError('\nCould not find any model files locally; try running without the "new" keyword')
        for mf in mfiles:
            sp = mf.replace('.txt','').split('_')[1:]
            p = {'model': mset}
            for i,ms in enumerate(MODEL_PARAMETER_NAMES):   # teff, logg, z
                if sp[i] not in parameters[ms]:
                    parameters[ms].append(sp[i])
                p[ms] = sp[i]                
            parameters['parameter_sets'].append(p)
        for ms in MODEL_PARAMETER_NAMES[0:3]:
            parameters[ms] = [float(x) for x in parameters[ms]]
        for ms in MODEL_PARAMETER_NAMES:
            parameters[ms].sort()
            parameters[ms] = numpy.array(parameters[ms])
        return parameters

#
#
# THE REST OF THIS ROUTINE IS NOW OBSOLETE AND IS IN PLACE ONLY FOR BACKWARDS COMPATABILITY
#
#

# read in parameter file - local and not local
    else:
        pfile = 'parameters.txt'
        try:
            open(os.path.basename(TMPFILENAME), 'wb').write(requests.get(SPLAT_URL+SPECTRAL_MODEL_FOLDER+mset+'/'+pfile).content)
            p = ascii.read(os.path.basename(TMPFILENAME))
            os.remove(os.path.basename(TMPFILENAME))
        except:
            print('\n\nCannot access online models for model set {}\n'.format(mset))
#            local = True
        if (os.path.exists(pfile) == False):
            pfile = SPLAT_PATH+SPECTRAL_MODEL_FOLDER+mset+'/'+os.path.basename(pfile)
            if (os.path.exists(pfile) == False):
                raise NameError('\nCould not find parameter file {}'.format(pfile))
        p = ascii.read(pfile)

# populate output parameter structure
        for ms in MODEL_PARAMETER_NAMES[0:3]:
            if ms in p.colnames:
                parameters[ms] = [float(x) for x in p[ms]]
            else:
                raise ValueError('\n\nModel set {} does not have defined parameter range for {}'.format(mset,ms))
        for ms in MODEL_PARAMETER_NAMES[3:6]:
            if ms in p.colnames:
                parameters[ms] = str(p[ms][0]).split(",")
            else:
                raise ValueError('\n\nModel set {} does not have defined parameter list for {}'.format(mset,ms))
        return parameters



#######################################################
#######################################################
##################   MODEL FITTING  ###################
#######################################################
#######################################################



def _modelFitPlotComparison(spec,model,**kwargs):
    '''
    Routine to compare spectrum to a model or models
    '''

# set up model spectrum or spectra
    if isinstance(model,list) == False:
        model = [model]
    scale = kwargs.get('scale',[1.0]*len(model))
    if isinstance(scale,list) == False:
        scale = [scale]
    stat = kwargs.get('stat',[False]*len(model))
    if isinstance(stat,list) == False:
        stat = [stat]
    if kwargs.get('compare',False) == True:
        scale = []
        stat = []
        for i,m in enumerate(model):
            st,sc = compareSpectra(spec,m,stat='chisqr',**kwargs)      # note: assumed to be chi-square
            scale.append(sc)
            stat.append(st)
    for i,m in enumerate(model):
        m.scale(scale[i])

# plotting
    olegend = kwargs.get('name',spec.name)

# plot one model on top of one spectrum in one plot
    if kwargs.get('overplot',True) == True and len(model) == 1:
        sps = [spec,model[0]]
#        model[0].info()
        colors = ['k','b']
        mlegend = r'{} '.format(DEFINED_MODEL_NAMES[getattr(model[0],'modelset')])
        mlegend+='{:s}={:.0f} '.format(MODEL_PARAMETER_TITLES['teff'],getattr(model[0],'teff'))
        mlegend+='{:s}={:.2f} '.format(MODEL_PARAMETER_TITLES['logg'],getattr(model[0],'logg'))
        mlegend+='{:s}={:.1f} '.format(MODEL_PARAMETER_TITLES['z'],getattr(model[0],'z'))
        legend = [olegend,mlegend]
        if kwargs.get('showdifference',True) == True: 
            sps.append(spec-model[0])
            colors.append('grey')
            legend.append(r'Difference ($\chi^2$ = {:.0f})'.format(stat[i]))
        sps = tuple(sps)
        return splot.plotSpectrum(*sps,colors=kwargs.get('colors',colors),file=kwargs.get('file',False),\
            uncertainty=kwargs.get('uncertainty',True),telluric=kwargs.get('telluric',True),legend=legend)

# plot several models on top of spectrum in one plot
    elif kwargs.get('overplot',True) == True and len(model) > 1:
        sps = [spec]
        colors = ['k']
        legend = [olegend]
        for i,m in enumerate(model):
            sps.append(m)
            colors.append('grey')
            mlegend = r'{:s}={:.0f} '.format(MODEL_PARAMETER_TITLES['teff'],getattr(m,'teff'))
            mlegend+='{:s}={:.2f} '.format(MODEL_PARAMETER_TITLES['logg'],getattr(m,'logg'))
            mlegend+='{:s}={:.1f} '.format(MODEL_PARAMETER_TITLES['z'],getattr(m,'z'))
            legend.append(mlegend)
        sps = tuple(sps)
        return splot.plotSpectrum(*sps,colors=kwargs.get('colors',colors),file=kwargs.get('file',False),\
            uncertainty=kwargs.get('uncertainty',True),telluric=kwargs.get('telluric',True),legend=legend)

# plot individual panels of spectra - there must be a filename given
    else: 
        if kwargs.get('file',False) == False:
            kwargs['file'] = 'modelFitComparison.pdf'
        plotlist = []
        legends = []
        colors = []
        for i,m in enumerate(model): 
            sps = [spec,m]
            c = ['k','b']
            mlegend = r'{}\n'.format(DEFINED_MODEL_NAMES[getattr(m,'modelset')])
            mlegend+='{:s}={:.0f} '.format(MODEL_PARAMETER_TITLES['teff'],getattr(m,'teff'))
            mlegend+='{:s}={:.2f} '.format(MODEL_PARAMETER_TITLES['logg'],getattr(m,'logg'))
            mlegend+='{:s}={:.1f} '.format(MODEL_PARAMETER_TITLES['z'],getattr(m,'z'))
            leg = [olegend,mlegend]
            if kwargs.get('showdifference',True): 
                plotlist.append(spec-m)
                c.append('grey')
                leg.append(r'Difference ($\chi^2$ = {:.0f})'.format(stat[i]))
            plotlist.append(sps)
            colors.append(kwargs.get('colors',c))
            legends.append(leg)

        return splot.plotSpectrum(plotlist,multiplot=True,multipage=True,legends=legends,colors=colors,\
            file=kwargs.get('file',False),uncertainty=kwargs.get('uncertainty',True),telluric=kwargs.get('telluric',True))




def modelFitGrid(spec, **kwargs):
    '''
    :Purpose: Fits a spectrum to a grid of atmosphere models, reports the best-fit and weighted average parameters, and returns either a dictionary with the best-fit model parameters or the model itself scaled to the optimal scaling factor.

    If spectrum is absolutely flux calibrated with the `fluxcalibrate()`_ method, the routine will also calculate the equivalent radii of the source.

    .. _`fluxcalibrate()` : api.html#splat.Spectrum.fluxCalibrate

    Required inputs:

    :param spec: a Spectrum class object, which should contain wave, flux and noise array elements.

    Optional inputs:

    :param model: set of models to use (``set`` and ``model_set`` may also be used), from the available models given by `loadModel()`_.

    .. _`loadModel()` : api.html#splat_model.loadModel

    :param stat: the statistic to use for comparing models to spectrum; can be any one of the statistics allowed in `compareSpectra()`_ routine (default = `chisqr`)

    .. _`compareSpectra()` : api.html#splat.compareSpectra

    :param weights: an array of the same length as the spectrum flux array, specifying the weight for each pixel (default: equal weighting)
    :param mask: an array of the same length as the spectrum flux array, specifying which data to include in comparison statistic as coded by 0 = good data, 1 = bad (masked). The routine `generateMask()`_ is called to create a mask, so parameters from that routine may be specified (default: no masking)

    .. _`generateMask()` : api.html#splat.generateMask

    :param compute\_radius: if set to True, force the computation of the radius based on the model scaling factor. This is automatically set to True if the input spectrum is absolutely flux calibrated (default = False)

    :param teff\_range: set to the range of temperatures over which model fitting will be done (``temperature_range`` and ``t_range`` may also be used; default = full range of model temperatures)
    :param logg\_range: set to the range of surface gravities over which model fitting will be done (``gravity_range`` and ``g_range`` may also be used; default = full range of model temperatures)
    :param z\_range: set to the range of metallicities over which model fitting will be done (``metallicity_range`` may also be used; default = full range of model temperatures)

    :param return\_model: set to True to return a Spectrum class of the best-fit model instead of a dictionary of parameters (default = False)
    :param return\_mean\_parameters: set to True a dictionary of mean parameters (default = False)
    :param return\_all\_parameters: set to True to return all of the parameter sets and fitting values (default = False)

    :param output: a string containing the base filename for outputs associated with this fitting routine (``file`` and ``filename`` may also be used; default = 'fit')
    :param noPlot: set to True to suppress plotting outputs (default = False)
    :param plot\_format: specifes the file format for output plots (default = `pdf`)
    :param file\_best\_comparison: filename to use for plotting spectrum vs. best-fit model (default = '``OUTPUT``\_best\_comparison.``PLOT_FORMAT``')
    :param file\_mean\_comparison: filename to use for plotting spectrum vs. mean parameter model (default = '``OUTPUT``\_mean\_comparison.``PLOT_FORMAT``')

    In addition, the parameters for `compareSpectra()`_ , `generateMask()`_ and `plotSpectrum()`_ may be used; see SPLAT API for details.

    .. _`plotSpectrum()`: api.html#splat_plot.plotSpectrum

    Output:
    
    Default output is a dictionary containing the best-fit model parameters: model name, teff, logg, z, fsed, kzz, cloud and slit, as well as the scaling factor for the model and comparison statistic.  
    If the input spectrum is absolutely flux calibrated, radius is also returned.  Alternate outputs include:

        *  a dictionary of the statistic-weighted mean parameters (``return_mean_parameters`` = True)
        *  a list of dictionaries containing all parameters and fit statistics (``return_all_parameters`` = True)
        *  a Spectrum class of the best-fit model scaled to the best-fit scaling (``return_model`` = True)

    :Example:
    >>> import splat
    >>> sp = splat.Spectrum(shortname='1507-1627')[0]
    >>> sp.fluxCalibrate('2MASS J',12.32,absolute=True)
    >>> p = splat.modelFitGrid(sp,teff_range=[1200,2500],model='Saumon',file='fit1507')
        Best Parameters to fit to BT-Settl (2008) models:
            $T_{eff}$=1800.0 K
            $log\ g$=5.0 dex(cm / s2)
            $[M/H]$=-0.0 dex
            $f_{sed}$=nc 
            $cld$=nc 
            $log\ \kappa_{zz}$=eq dex(cm2 / s)
            R=0.143324498969 solRad
            chi=4500.24997585
        Mean Parameters:
            $T_{eff}$: 1800.0+/-0.0 K
            $log\ g$: 5.0+/-0.0 dex(cm / s2)
            Radius: 0.143324498969+/-0.0 solRad
            $[M/H]$: 0.0+/-0.0 dex
    '''

# model parameters
    model_set = kwargs.get('model', 'BTSettl2008')
    model_set = kwargs.get('set', model_set)
    model_set = kwargs.get('model_set', model_set)
    model_set = _checkModelName(model_set)
    if model_set == False:
        raise ValueError('\n{} is not in the SPLAT model suite; try {}'.format(kwargs['set'],' '.join(list(DEFINED_MODEL_NAMES.keys()))))
    if kwargs.get('verbose',False) == True:
        print('\nmodelFitGrid is using {} model set'.format(model_set))

# fitting parameters
    stat = kwargs.get('stat','chisqr')
    mask = kwargs.get('mask',_generateMask(spec.wave,**kwargs))
    weights = kwargs.get('weights',numpy.ones(len(spec.wave)))

# plotting and reporting keywords
    compute_radius = kwargs.get('compute_radius', spec.fscale == 'Absolute')
    filebase = kwargs.get('output', 'fit')
    filebase = kwargs.get('filename',filebase)
    filebase = kwargs.get('file',filebase)
    plot_format = kwargs.get('plot_format','pdf')
    file_best_comparison = kwargs.get('file_best_comparison',os.path.splitext(filebase)[0]+'_best_comparison.'+plot_format)
    file_mean_comparison = kwargs.get('file_mean_comparison',os.path.splitext(filebase)[0]+'_mean_comparison.'+plot_format)

#    file_iterative = kwargs.get('file_iterative',os.path.splitext(filebase)[0]+'_iterative.dat')
#    file_chains = kwargs.get('file_chains',os.path.splitext(filebase)[0]+'_chains.'+plot_format)
#    file_corner = kwargs.get('file_corner',os.path.splitext(filebase)[0]+'_corner.'+plot_format)
#    file_summary = kwargs.get('file_summary',os.path.splitext(filebase)[0]+'_summary.txt')
#    if kwargs.get('save',True):
#        f = open(file_iterative,'w')
#        f.close()

# read in available model grid points
    gridparam = _loadModelParameters(model_set) # Range parameters can fall in
#    tvals = numpy.arange(mlimits['teff'][0],mlimits['teff'][1]+mlimits['teff'][-1],mlimits['teff'][-1])
#    gvals = numpy.arange(mlimits['logg'][0],mlimits['logg'][1]+mlimits['logg'][-1],mlimits['logg'][-1])
#    zvals = numpy.arange(mlimits['z'][0],mlimits['z'][1]+mlimits['z'][-1],mlimits['z'][-1])

# set points based on input ranges
    rng = kwargs.get('teff_range',[numpy.min(gridparam['teff']),numpy.max(gridparam['teff'])])
    rng = kwargs.get('temperature_range',rng)
    rng = kwargs.get('t_range',rng)
    if numpy.max(rng) < numpy.min(gridparam['teff']) or numpy.min(rng) > numpy.max(gridparam['teff']):
        print('\nWarning: input temperature range {}-{} is outside limits of models {}-{}; defaulting to model range'.format(numpy.min(rng),numpy.max(rng),numpy.min(gridparam['teff']),numpy.max(gridparam['teff'])))
    if numpy.max(rng) < numpy.max(gridparam['teff']) or numpy.min(rng) > numpy.min(gridparam['teff']):
        gridparam['teff'] = gridparam['teff'][numpy.where(numpy.logical_and(gridparam['teff'] >= numpy.min(rng),gridparam['teff'] <= numpy.max(rng)))]

    rng = kwargs.get('logg_range',[numpy.min(gridparam['logg']),numpy.max(gridparam['logg'])])
    rng = kwargs.get('gravity_range',rng)
    rng = kwargs.get('g_range',rng)
    if numpy.max(rng) < numpy.min(gridparam['logg']) or numpy.min(rng) > numpy.max(gridparam['logg']):
        print('\nWarning: input gravity range {}-{} is outside limits of models {}-{}; defaulting to model range'.format(numpy.min(rng),numpy.max(rng),numpy.min(gridparam['logg']),numpy.max(gridparam['logg'])))
    if numpy.max(rng) < numpy.max(gridparam['logg']) or numpy.min(rng) > numpy.min(gridparam['logg']):
        gridparam['logg'] = gridparam['logg'][numpy.where(numpy.logical_and(gridparam['logg'] >= numpy.min(rng),gridparam['logg'] <= numpy.max(rng)))]

    rng = kwargs.get('z_range',[numpy.min(gridparam['z']),numpy.max(gridparam['z'])])
    rng = kwargs.get('metallicity_range',rng)
    if kwargs.get('nometallicity',False) == True: rng = [0,0]
    if numpy.max(rng) < numpy.min(gridparam['z']) or numpy.min(rng) > numpy.max(gridparam['z']):
        print('\nWarning: input metallicity range {}-{} is outside limits of models {}-{}; defaulting to model range'.format(numpy.min(rng),numpy.max(rng),numpy.min(gridparam['z']),numpy.max(gridparam['z'])))
    if numpy.max(rng) < numpy.max(gridparam['z']) or numpy.min(rng) > numpy.min(gridparam['z']):
        gridparam['z'] = gridparam['z'][numpy.where(numpy.logical_and(gridparam['z'] >= numpy.min(rng),gridparam['z'] <= numpy.max(rng)))]


#    fit_parameters = {\
#        'teff': tvals,'logg': gvals, 'z': zvals}
#    for i,m in enumerate(MODEL_PARAMETER_NAMES[3:-1]):
#        fit_parameters[m] = kwargs.get(m,mlimits[m])
#        if isinstance(fit_parameters[m],list) == False:
#            fit_parameters[m] = [fit_parameters[m]]


# start a fitting loop
    parameters = []
    stats = []
    mparam = {'set': model_set,'force': True}
    for t in gridparam['teff']:
        mparam['teff'] = t
        for g in gridparam['logg']:
            mparam['logg'] = g
            for z in gridparam['z']:
                mparam['z'] = z
                for f in gridparam['fsed']:
                    mparam['fsed'] = f
                    for k in gridparam['kzz']:
                        mparam['kzz'] = k
                        for c in gridparam['cld']:
                            mparam['cld'] = c
                            try:
                                model = loadModel(**mparam)
                                chi,scl = compareSpectra(spec, model, mask=mask, weights=weights, stat=stat)
                                mparam['stat'] = chi
                                mparam['scale'] = scl
                                mparam['radius'] = ((scl*(10.*u.pc)**2)**0.5).to(u.Rsun).value
                                parameters.append(copy.deepcopy(mparam))
                                stats.append(chi)
                                if kwargs.get('verbose',False): print('{}: T={},g={},z={},stat={},scale={},radius={}'.format(len(stats)-1,mparam['teff'],mparam['logg'],mparam['z'],numpy.round(mparam['stat']),mparam['scale'],mparam['radius']))
                            except:
                                if kwargs.get('verbose',False): print('\nNo model for {}'.format(mparam))

# report best parameters
    parameters = [p for (c,p) in sorted(zip(stats,parameters))]
    stats.sort()
#    print('\n\n')
#    for i,s in enumerate(stats):
#        line = '{}: chi={}'.format(i,s)
#        for ms in MODEL_PARAMETER_NAMES[:-1]:
#            line+='{} = {} {}'.format(MODEL_PARAMETER_TITLES[ms],parameters[i][ms],MODEL_PARAMETER_UNITS[ms])
#        if compute_radius == True:
#            line+='Radius = {} {}'.format(parameters[i]['radius'].value,parameters[i]['radius'].unit)
#        print(line)
    bparam = copy.deepcopy(parameters[0])
    bmodel = loadModel(**bparam)
    bmodel.scale(parameters[0]['scale'])

    if kwargs.get('verbose',False): 
        print('\nBest Parameters to fit to {} models:'.format(DEFINED_MODEL_NAMES[model_set]))
        for ms in MODEL_PARAMETER_NAMES[:-1]:
            print('\t{} = {} {}'.format(MODEL_PARAMETER_TITLES[ms],parameters[0][ms],MODEL_PARAMETER_UNITS[ms]))
        if compute_radius == True:
            print('\tRadius = {} {}'.format(parameters[0]['radius'].value,parameters[0]['radius'].unit))
        print('\tchi={}'.format(stats[0]))

    if kwargs.get('noPlot',False) != True:
        _modelFitPlotComparison(spec,bmodel,stat=stats[0],file=file_best_comparison)

# weighted means/uncertainties
    fitweights = numpy.exp(-0.5*(numpy.array(stats)-numpy.min(stats)))
    fparam = copy.deepcopy(parameters[0])
    for ms in MODEL_PARAMETER_NAMES[0:3]:
        vals = [(p[ms]*(u.m/u.m)).value for p in parameters]
        fparam[ms],fparam[ms+'_unc'] = weightedMeanVar(vals,fitweights)
        fparam[ms]*=MODEL_PARAMETER_UNITS[ms]
        fparam[ms+'_unc']*=MODEL_PARAMETER_UNITS[ms]
    if compute_radius == True:
        vals = [(p['radius']*(u.m/u.m)).value for p in parameters]
        fparam['radius'],fparam['radius_unc'] = weightedMeanVar(vals,fitweights)
        fparam['radius']*=u.Rsun
        fparam['radius_unc']*=u.Rsun

    if kwargs.get('verbose',False): 
        print('\nStatistic-weighted Mean Parameters:')
        for k in list(fparam.keys()):
            if k in MODEL_PARAMETER_NAMES[0:3]:
                print('\t{}: {}+/-{} {}'.format(MODEL_PARAMETER_TITLES[k],fparam[k].value,fparam[k+'_unc'].value,fparam[k].unit))
#        if k == 'radius':
#            print('\tRadius: {}+/-{} {}'.format(fparam[k].value,fparam[k+'_unc'].value,fparam[k].unit))

    if kwargs.get('noPlot',False) != True:
        mmodel = loadModel(**fparam)
        chi,scl = compareSpectra(spec, mmodel, mask=mask, weights=weights, stat=stat)
        mmodel.scale(scl)
        _modelFitPlotComparison(spec,mmodel,stat=stats[0],file=file_mean_comparison)

# return parameters; otherwise return 
    if kwargs.get('return_model',False) == True:
        return bmodel
    elif kwargs.get('return_mean_parameters',False) == True:
        return fparam
    elif kwargs.get('return_all_parameters',False) == True:
        return parameters
    else:
        return bparam



def modelFitMCMC(spec, **kwargs):
    '''
    :Purpose: Uses Markov chain Monte Carlo method to compare an object with models from a 
                given set. Returns the best estimate of the effective temperature, surface 
                gravity, and metallicity. Can also determine the radius of the object by 
                using these estimates. 
    :param spec: Spectrum class object, which should contain wave, flux and 
                  noise array elements.
    :param nsamples: number of Monte Carlo samples
    :type nsamples: optional, default = 1000
    :param initial_cut: the fraction of the initial steps to be discarded. (e.g., if 
                ``initial_cut = 0.2``, the first 20% of the samples are discarded.)
    :type initial_cut: optional, default = 0.1
    :param burn: the same as ``initial_cut``
    :type burn: optional, default = 0.1
    :param set: set of models to use; options include:

        - *'BTSettl2008'*: model set with effective temperature of 400 to 2900 K, surface gravity of 3.5 to 5.5 and metallicity of -3.0 to 0.5 
          from `Allard et al. (2012) <http://adsabs.harvard.edu/abs/2012RSPTA.370.2765A>`_
        - *'burrows06'*: model set with effective temperature of 700 to 2000 K, surface gravity of 4.5 to 5.5, metallicity of -0.5 to 0.5, 
          and sedimentation efficiency of either 0 or 100 from `Burrows et al. (2006) <http://adsabs.harvard.edu/abs/2006ApJ...640.1063B>`_
        - *'morley12'*: model set with effective temperature of 400 to 1300 K, surface gravity of 4.0 to 5.5, metallicity of 0.0 
          and sedimentation efficiency of 2 to 5 from `Morley et al. (2012) <http://adsabs.harvard.edu/abs/2012ApJ...756..172M>`_
        - *'morley14'*: model set with effective temperature of 200 to 450 K, surface gravity of 3.0 to 5.0, metallicity of 0.0 
          and sedimentation efficiency of 5 from `Morley et al. (2014) <http://adsabs.harvard.edu/abs/2014ApJ...787...78M>`_
        - *'saumon12'*: model set with effective temperature of 400 to 1500 K, surface gravity of 3.0 to 5.5 and metallicity of 0.0 
          from `Saumon et al. (2012) <http://adsabs.harvard.edu/abs/2012ApJ...750...74S>`_
        - *'drift'*: model set with effective temperature of 1700 to 3000 K, surface gravity of 5.0 to 5.5 and metallicity of -3.0 to 0.0 
          from `Witte et al. (2011) <http://adsabs.harvard.edu/abs/2011A%26A...529A..44W>`_
    
    :type set: optional, default = 'BTSettl2008'
    :param model: the same as ``set``
    :type model: optional, default = 'BTSettl2008'
    :param models: the same as ``set``
    :type models: optional, default = 'BTSettl2008'
    :param verbose: give lots of feedback
    :type verbose: optional, default = False
    :param mask_ranges: mask any flux value of ``spec`` by specifying the wavelength range.
                        Must be in microns.
    :type mask_ranges: optional, default = []
    :param mask_telluric: masks certain wavelengths to avoid effects from telluric absorption
    :type mask_telluric: optional, default = False
    :param mask_standard: masks wavelengths below 0.8 and above 2.35 microns
    :type mask_standard: optional, default = True
    :param mask: mask any flux value of ``spec``; has to be an array with length equal as ``spec`` with only 0 (unmask) or 1 (mask).
    :type mask: optional, default = [0, ..., 0] for len(sp1.wave)
    :param radius: calculates and returns radius of object if True
    :type radius: optional
    
    :param filename: filename or filename base for output
    :type filename: optional
    :param filebase: the same as ``filename``
    :type filebase: optional
    :param savestep: indicate when to save data output (e.g. ``savestep = 10`` will save the output every 10 samples)
    :type savestep: optional, default = ``nsamples/10``
    :param dataformat: output data format type
    :type dataformat: optional, default = 'ascii.csv'
    :param initial_guess: array including initial guess of the effective temperature, surface gravity and metallicity of ``spec``.
                            Can also set individual guesses of spectral parameters by using **initial_temperature** or **initial_teff**,
                            **initial_gravity** or **initial_logg**, and **initial_metallicity** or **initial_z**.
    :type initial_guess: optional, default = array of random numbers within allowed ranges
    :param ranges: array of arrays indicating ranges of the effective temperature, surface gravity and metallicity of the model set.
                    Can also set individual ranges of spectral parameters by using **temperature_range** or **teff_range**,
                    **gravity_range** or **logg_range**, and **metallicity_range** or **z_range**.
    :type ranges: optional, default = depends on model set
    :param step_sizes: an array specifying step sizes of spectral parameters. Can also set individual step sizes by using
                        **temperature_step** or **teff_step**, **gravity_step** or **logg_step**, and **metallicity_step** or **z_step**.
    :type step_sizes: optional, default = [50, 0.25, 0.1]
    :param nonmetallicity: if True, sets metallicity = 0
    :type nonmetallicity: optional, default = False
    :param addon: reads in prior calculation and starts from there. Allowed object types are tables, dictionaries and strings.
    :type addon: optional, default = False
    :param evolutionary_model: set of evolutionary models to use. See Brown Dwarf Evolutionary Models page for
        more details. Options include:
    
        - *'baraffe'*: Evolutionary models from `Baraffe et al. (2003) <http://arxiv.org/abs/astro-ph/0302293>`_.
        - *'burrows'*: Evolutionary models from `Burrows et al. (1997) <http://adsabs.harvard.edu/abs/1997ApJ...491..856B>`_.
        - *'saumon'*: Evolutionary models from `Saumon & Marley (2008) <http://adsabs.harvard.edu/abs/2008ApJ...689.1327S>`_.
        
    :type evolutionary_model: optional, default = 'Baraffe'
    :param emodel: the same as ``evolutionary_model``
    :type emodel: optional, default = 'Baraffe'
    
    :Example:
    >>> import splat
    >>> sp = splat.getSpectrum(shortname='1047+2124')[0]        # T6.5 radio emitter
    >>> spt, spt_e = splat.classifyByStandard(sp,spt=['T2','T8'])
    >>> teff,teff_e = splat.typeToTeff(spt)
    >>> sp.fluxCalibrate('MKO J',splat.typeToMag(spt,'MKO J')[0],absolute=True)
    >>> table = splat.modelFitMCMC(sp, mask_standard=True, initial_guess=[teff, 5.3, 0.], zstep=0.1, nsamples=100, savestep=0, verbose=True)
        Trouble with model BTSettl2008 T=1031.61, logg=5.27, z=-0.02
        At cycle 0: fit = T=1031.61, logg=5.27, z=0.00 with chi2 = 35948.5
        Trouble with model BTSettl2008 T=1031.61, logg=5.27, z=-0.13
        At cycle 1: fit = T=1031.61, logg=5.27, z=0.00 with chi2 = 35948.5 
                                        .
                                        .
                                        .
                            # Skipped a few lines
                                        .
                                        .
                                        .
        Trouble with model BTSettl2008 T=973.89, logg=4.95, z=-0.17
        At cycle 99: fit = T=973.89, logg=4.95, z=0.00 with chi2 = 30569.6 
        <BLANKLINE>
        Number of steps = 170
        <BLANKLINE>
        Best Fit parameters:
        Lowest chi2 value = 29402.3750247 for 169.0 degrees of freedom
        Effective Temperature = 1031.608 (K)
        log Surface Gravity = 5.267 
        Metallicity = 0.000 
        Radius (relative to Sun) from surface fluxes = 0.103 
        <BLANKLINE>
        Median parameters:
        Effective Temperature = 1029.322 + 66.535 - 90.360 (K)
        log Surface Gravity = 5.108 + 0.338 - 0.473 
        Metallicity = 0.000 + 0.000 - 0.000 
        Radius (relative to Sun) from surface fluxes = 0.094 + 0.012 - 0.007 
        <BLANKLINE>
        <BLANKLINE>
        fit_J1047+2124_BTSettl2008
        Quantiles:
        [(0.16, 0.087231370556002871), (0.5, 0.09414839610875167), (0.84, 0.10562967101117798)]
        Quantiles:
        [(0.16, 4.6366512070621884), (0.5, 5.1077094570511488), (0.84, 5.4459108887603094)]
        Quantiles:
        [(0.16, 938.96254520460286), (0.5, 1029.3222563137401), (0.84, 1095.8574021575118)]
        <BLANKLINE>
        Total time elapsed = 0:01:46.340169
    >>> print table
             teff          logg      z       radius         chisqr   
        ------------- ------------- --- --------------- -------------
        1031.60790828 5.26704520744 0.0  0.103152256465 29402.3750247
        1031.60790828 5.26704520744 0.0  0.103152256465 29402.3750247
                  ...           ... ...             ...           ...   # Skipped a few lines
        938.962545205 5.43505121711 0.0  0.125429265207 43836.3720496
        938.962545205 5.43505121711 0.0  0.129294090544 47650.4267022
    '''

# MCMC keywords
    timestart = time.time()
    nsample = kwargs.get('nsamples', 1000)
    burn = kwargs.get('initial_cut', 0.1)  # what fraction of the initial steps are to be discarded
    burn = kwargs.get('burn', burn)  # what fraction of the initial steps are to be discarded
    m_set = kwargs.get('set', 'BTSettl2008')
    m_set = kwargs.get('model', m_set)
    m_set = kwargs.get('models', m_set)
    verbose = kwargs.get('verbose', False)

# plotting and reporting keywords
    showRadius = kwargs.get('radius', spec.fscale == 'Absolute')
    try:
        filebase = kwargs.get('filebase', 'fit_'+spec.name+'_'+m_set)
    except:
        filebase = kwargs.get('filebase', 'fit_'+m_set)
    filebase = kwargs.get('filename',filebase)
    kwargs['filebase'] = filebase
    savestep = kwargs.get('savestep', nsample/10)
    dataformat = kwargs.get('dataformat','ascii.csv')
# evolutionary models    
    emodel = kwargs.get('evolutionary_model', 'baraffe')
    emodel = kwargs.get('emodel', emodel)

# set mask   
    mask = kwargs.get('mask',_generateMask(spec.wave,**kwargs))
    
# set the degrees of freedom    
    try:
        slitwidth = spec.slitpixelwidth
    except:
        slitwidth = 3.
    eff_dof = numpy.round((numpy.nansum(mask) / slitwidth) - 1.)

# TBD - LOAD IN ENTIRE MODEL SET

# set ranges for models - input or set by model itself
    modelgrid = _loadModelParameters(m_set) # Range parameters can fall in
    ranges = kwargs.get('ranges', \
        [[numpy.min(modelgrid['teff']),numpy.max(modelgrid['teff'])],\
        [numpy.min(modelgrid['logg']),numpy.max(modelgrid['logg'])],\
        [numpy.min(modelgrid['z']),numpy.max(modelgrid['z'])]])
    teff_range = kwargs.get('teff_range',ranges[0])
    teff_range = kwargs.get('temperature_range',teff_range)
    logg_range = kwargs.get('logg_range',ranges[1])
    logg_range = kwargs.get('gravity_range',logg_range)
    z_range = kwargs.get('z_range',ranges[2])
    z_range = kwargs.get('metallicity_range',z_range)

# set initial parameters

    param0_init = kwargs.get('initial_guess',[\
        numpy.random.uniform(teff_range[0],teff_range[1]),\
        numpy.random.uniform(logg_range[0],logg_range[1]),\
#        numpy.random.uniform(z_range[0],z_range[1])])
        numpy.random.uniform(0.,0.)])
    if len(param0_init) < 3:
        param0_init.append(0.0)
        
    t0 = kwargs.get('initial_temperature',param0_init[0])
    t0 = kwargs.get('initial_teff',t0)
    g0 = kwargs.get('initial_gravity',param0_init[1])
    g0 = kwargs.get('initial_logg',g0)
    z0 = kwargs.get('initial_metallicity',param0_init[2])
    z0 = kwargs.get('initial_z',z0)
    param0 = [t0,g0,z0]

    tstep = kwargs.get('teff_step',50)
    tstep = kwargs.get('temperature_step',tstep)
    gstep = kwargs.get('logg_step',0.25)
    gstep = kwargs.get('gravity_step',gstep)
    zstep = kwargs.get('z_step',0.1)
    zstep = kwargs.get('metallicity_step',zstep)

# catch for no metallicity input - assume not fitting this parameter
    param_step = kwargs.get('step_sizes',[tstep,gstep,zstep])
    if len(param_step) < 3:
        param_step.append[0.0]
        kwargs['nometallicity'] = True

    if kwargs.get('nometallicity',False):
        param_step[2] = 0.
        param0[2] = 0.0

    
# Check that initial guess is within range of models
    if not (teff_range[0] <= param0[0] <= teff_range[1] and \
        logg_range[0] <= param0[1] <= logg_range[1] and \
        z_range[0] <= param0[2] <= z_range[1]):
        sys.stderr.write("\nInitial guess T={}, logg = {} and [M/H] = {} is out of model range;" + \
            "defaulting to a random initial guess in range.".format(param0[0],param0[1],param0[2]))
        param0 = param0_init
        if param0[2] == 0.:
            param_step[2] = 0.


# read in prior calculation and start from there
    if kwargs.get('addon',False) != False:
        addflg = False
# a table is passed
        if isinstance(kwargs.get('addon'),Table):
            t = kwargs.get('addon')
            addflg = True
# a dictionary is passed
        elif isinstance(kwargs.get('addon'),dict):
            t = Table(kwargs.get('addon'))
            addflg = True
# a filename is passed
        elif isinstance(kwargs.get('addon'),str):
            try:
                p = ascii.read(kwargs.get('addon'))
            except:
                print('\nCould not read in parameter file {}'.format(kwargs.get('addon')))


# initial fit cycle
    try:
        model = loadModel(teff = param0[0], logg = param0[1], z = param0[2], set = m_set)
    except:
        raise ValueError('\nInitial {} model with T = {}, logg = {} and [M/H] = {} did not work; aborting.'.format(m_set,param0[0],param0[1],param0[2]))

    chisqr0,alpha0 = compareSpectra(spec, model, mask_ranges=mask_ranges)
    chisqrs = [chisqr0]    
    params = [param0]
    radii = [(10.*u.pc*numpy.sqrt(alpha0)).to(u.Rsun)]
    for i in numpy.arange(nsample):
        for j in numpy.arange(len(param0)):
            if param_step[j] > 0.:          # efficient consideration - if statement or just run a model?
                param1 = copy.deepcopy(param0)
                param1[j] = numpy.random.normal(param1[j],param_step[j])
                try:            
                    model = loadModel(teff = param1[0], logg = param1[1],z = param1[2], set = m_set)
                    chisqr1,alpha1 = compareSpectra(spec, model ,mask_ranges=mask_ranges)  

# Probability that it will jump to this new point; determines if step will be taken
                    h = 1. - stats.f.cdf(chisqr1/chisqr0, eff_dof, eff_dof)
#                    print(chisqr1, chisqr0, eff_dof, h)
                    if numpy.random.uniform(0,1) < h:
                        param0 = copy.deepcopy(param1)
                        chisqr0 = copy.deepcopy(chisqr1)
                        alpha0 = copy.deepcopy(alpha1)
                
# update list of parameters, chi^2 and radii
                    params.append(param0)
                    chisqrs.append(chisqr0)
                    radii.append((10.*u.pc*numpy.sqrt(alpha0)).to(u.Rsun))
                    
                except:
                    if verbose:
                        print('Trouble with model {} T={:.2f}, logg={:.2f}, z={:.2f}'.format(m_set,param1[0],param1[1],param1[2]))
                    continue

        if verbose:
            print('At cycle {}: fit = T={:.2f}, logg={:.2f}, z={:.2f} with chi2 = {:.1f}'.format(i,param0[0],param0[1],param0[2],chisqr0))

# save results iteratively
        if i*savestep != 0:
            if i%savestep == 0:
                t = Table(zip(*params[::-1]),names=['teff','logg','z'])
                if param_step[2] == 0.:
                    del t['z']
                if showRadius:
                    t['radius'] = radii
                t['chisqr'] = chisqrs
                t.write(filebase+'rawdata.dat',format=dataformat)
                reportModelFitResults(spec,t,iterative=True,model_set=m_set,**kwargs)

# Final results
    t = Table(zip(*params[::-1]),names=['teff','logg','z'])
    if param_step[2] == 0. or kwargs.get('nometallicity',False):
        del t['z']
    if showRadius:
        t['radius'] = radii
    t['chisqr'] = chisqrs
# cut first x% of parameters
    s = Table(t[burn*len(t):])

# save data
    s.write(filebase+'rawdata.dat',format=dataformat)
    
    reportModelFitResults(spec,s,iterative=False,model_set=m_set,**kwargs)
    if verbose:
        print('\nTotal time elapsed = {}'.format(time.time()-timestart))
    return s



def reportModelFitResults(spec,t,*arg,**kwargs):
    '''
    :Purpose: 
        Reports the result of model fitting parameters. Produces triangle plot, best fit model, statistics of parameters and saves raw data if ``iterative = True``.

    Required Inputs:

        :param spec: Spectrum class object, which should contain wave, flux and noise array elements.
        :param t: Must be an astropy Table with columns containing parameters fit, and one column for chi-square values ('chisqr').
    
    Optional Inputs:
        :param evol: computes the mass, age, temperature, radius, surface gravity, and luminosity by using various evolutionary model sets. See below for the possible set options and the Brown Dwarf Evolutionary Models page for more details (default = True)
        :param emodel: set of evolutionary models to use; see `loadEvolModelParameters()`_ (default = 'Baraffe')

    .. _`loadEvolModelParameters()` : api.html#splat_evolve.loadEvolModel

        :param weight: set to True to use fitting statistic as a weighting to compute best fit statistics (default = True)
        :param stat: name of the statistics column in input table ``t`` (default = 'chisqr')
        :param stats: if True, prints several statistical values, including number of steps, best fit parameters, lowest chi2 value, median parameters and key values along the distribution (default = True)
        :param triangle: creates a triangle plot, plotting the parameters against each other, demonstrating areas of high and low chi squared values. Useful for demonstrating correlations between parameters (default = True)
        :param bestfit: set to True to plot best-fit model compared to spectrum (default=True)
        :param model_set: desired model set of ``bestfit``; see `loadModel()`_ for allowed options (can also use 'mset'; default = blank)

    .. _`loadModel()` : api.html#splat_model.loadModel

        :param filebase: a string that is the base filename for output (default = 'modelfit_results')
    
        :param sigma: when printing statistical results (``stats`` = True), print the value at ``sigma`` standard deviations away from the mean (default = 1)
        :param iterative: if True, prints quantitative results but does not plot anything (default = False)

    Output:
        No formal output, but results are plotted to various files

    :Example:
    >>> import splat
    >>> sp = splat.getSpectrum(shortname='1047+2124')[0]        # T6.5 radio emitter
    >>> spt, spt_e = splat.classifyByStandard(sp,spt=['T2','T8'])
    >>> teff,teff_e = splat.typeToTeff(spt)
    >>> sp.fluxCalibrate('MKO J',splat.typeToMag(spt,'MKO J')[0],absolute=True)
    >>> table = splat.modelFitMCMC(sp, mask_standard=True, initial_guess=[teff, 5.3, 0.], zstep=0.1, nsamples=100, savestep=0, verbose=False)
    >>> splat.reportModelFitResults(sp, table, evol = True, stats = True, sigma = 2, triangle = False)
        Number of steps = 169
        Best Fit parameters:
        Lowest chi2 value = 29567.2136599 for 169.0 degrees of freedom
        Effective Temperature = 918.641 (K)
        log Surface Gravity = 5.211 
        Metallicity = 0.000 
        Radius (relative to Sun) from surface fluxes = 0.096 
        <BLANKLINE>
        Median parameters:
        Effective Temperature = 927.875 + 71.635 - 73.237 (K)
        log Surface Gravity = 5.210 + 0.283 - 0.927 
        Metallicity = 0.000 + 0.000 - 0.000 
        Radius (relative to Sun) from surface fluxes = 0.108 + 0.015 - 0.013 
    '''

    evolFlag = kwargs.get('evol',True)
    emodel = kwargs.get('emodel','Baraffe')
    statsFlag = kwargs.get('stats',True)
    triangleFlag = kwargs.get('triangle',True)
    bestfitFlag = kwargs.get('bestfit',True)
    summaryFlag = kwargs.get('summary',True)
    weights = kwargs.get('weight',None)
    filebase = kwargs.get('filebase','modelfit_results')
    statcolumn = kwargs.get('stat','chisqr')
    mset = kwargs.get('model_set','')
    mset = kwargs.get('mset',mset)
    mask_ranges = kwargs.get('mask_ranges',[])
    sigma = kwargs.get('sigma',1.)

# map some common column names to full descriptive texts
    plotname_assoc = {\
        'teff': r'T$_{eff}$',\
        'logg': r'log g',\
        'z': r'[M/H]',\
        'mass': r'M/M$_{\odot}$',\
        'age': r'$\tau$',\
        'lbol': r'log L$_{bol}$/L$_{\odot}$',\
        'radius': r'R/R$_{\odot}$',\
        'radius_evol': r'R/R$_{\odot}$'}

    format_assoc = {\
        'teff': '.0f',\
        'logg': '.2f',\
        'z': '.2f',\
        'mass': '.3f',\
        'age': '.1f',\
        'lbol': '.2f',\
        'radius': '.3f',\
        'radius_evol': '.3f'}

    descrip_assoc = {\
        'teff': 'Effective Temperature',\
        'logg': 'log Surface Gravity',\
        'z': 'Metallicity',\
        'mass': 'Mass',\
        'age': 'Age',\
        'lbol': 'log Luminosity (relative to Sun)',\
        'radius': 'Radius (relative to Sun) from surface fluxes',\
        'radius_evol': 'Radius (relative to Sun) from evolutionary models'}

    unit_assoc = {\
        'teff': 'K',\
#        'logg': r'cm/s$^2$',\
        'age': 'Gyr'}

    if kwargs.get('iterative',False):
        statsFlag = True
        evolFlag = True
        triangleFlag = False
        bestfitFlag = False
        summaryFlag = False

# check that table has the correct properties
    if isinstance(t,Table) == False:
        raise ValueError('\nInput is not an astropy table')
    if len(t.columns) < 2:
        raise ValueError('\nNeed at least two columns in input table')
    if statcolumn not in t.colnames:
        raise ValueError('\n{} column must be present in input table'.format(statcolumn))

    parameters = t.colnames
    parameters.remove(statcolumn)
 
# get the evolutionary model parameters
# turned off for now
#    evolFlag = False
#    if evolFlag:
#        if 'teff' not in t.colnames or 'logg' not in t.colnames:
#            print('\nCannot compare to best fit without teff and logg parameters')
#
#        else:
#            values=bdevopar.Parameters(emodel, teff=t['teff'], grav=t['logg'])
#            t['age'] = values['age']
#            t['lbol'] = values['luminosity']
#            t['mass'] = values['mass']
#            t['radius_evol'] = values['radius']
#            parameters = t.colnames
#            parameters.remove(statcolumn)
    
   
# calculate statistics
    if statsFlag:
        if weights == True:
            weights = numpy.exp(0.5*(numpy.nanmin(t[statcolumn])-t[statcolumn]))

        print('\nNumber of steps = {}'.format(len(t)))
        
        print('\nBest Fit parameters:')
        print('Lowest chi2 value = {} for {} degrees of freedom'.format(numpy.nanmin(t[statcolumn]),spec.dof))
        for p in parameters:
            sort = [x for (y,x) in sorted(zip(t[statcolumn],t[p]))]
            name = p
            if p in descrip_assoc.keys():
                name = descrip_assoc[p]
            unit = ''
            if p in unit_assoc.keys():
                unit = '('+unit_assoc[p]+')'
            print('{} = {:.3f} {}'.format(name,sort[0],unit))

        print('\nMedian parameters:')
        for p in parameters:
            sm, mn, sp = distributionStats(t[p],sigma=sigma,weights=weights)      # +/- 1 sigma
            name = p
            if p in descrip_assoc.keys():
                name = descrip_assoc[p]
            unit = ''
            if p in unit_assoc.keys():
                unit = '('+unit_assoc[p]+')'
            print('{} = {:.3f} + {:.3f} - {:.3f} {}'.format(name,mn,sp-mn,mn-sm,unit))
        print('\n')

        
# best fit model
    if bestfitFlag and mset in DEFINED_MODEL_SET:
# check to make sure at least teff & logg are present
        if 'teff' not in t.colnames or 'logg' not in t.colnames:
            print('\nCannot compare to best fit without teff and logg parameters')

        else:
            t.sort(statcolumn)
            margs = {'set': mset, 'teff': t['teff'][0], 'logg': t['logg'][0]}
            legend = [spec.name,'{} T = {:.0f}, logg =  {:.2f}'.format(mset,margs['teff'],margs['logg']),r'$\chi^2$ = {:.0f}, DOF = {:.0f}'.format(t[statcolumn][0],spec.dof)]
            if 'z' in t.colnames:
                margs['z'] = t['z'][0]
                legend[1]+=', z = {:.2f}'.format(margs['z'])
            model = loadModel(**margs)
            chisqr,alpha = compareSpectra(spec, model ,mask_ranges=mask_ranges)
            model.scale(alpha)

            w = numpy.where(numpy.logical_and(spec.wave.value > 0.9,spec.wave.value < 2.35))
            diff = spec-model
            print(filebase)
            splot.plotSpectrum(spec,model,diff,uncertainty=True,telluric=True,colors=['k','r','b'], \
                legend=legend,filename=filebase+'bestfit.eps',\
                yrange=[1.1*numpy.nanmin(diff.flux.value[w]),1.25*numpy.nanmax([spec.flux.value[w],model.flux.value[w]])])  
 
# triangle plot of parameters
    if triangleFlag:
        y=[]
        labels = []
        fmt = []
        for p in parameters:
            if min(numpy.isfinite(t[p])) == True and numpy.nanstd(t[p]) != 0.:       # patch to address arrays with NaNs in them
                y.append(t[p])
                if p in plotname_assoc.keys():
                    labels.append(plotname_assoc[p])
                else:
                    labels.append(p)
                if p in unit_assoc.keys():
                    labels[-1] = labels[-1]+' ('+unit_assoc[p]+')'
                if p in format_assoc.keys():
                    fmt.append(format_assoc[p])
                else:
                    fmt.append('.2f')
#        print(labels)
        print(labels, fmt)
        fig = triangle.corner(zip(*y[::-1]), labels=list(reversed(labels)), show_titles=True, quantiles=[0.16,0.5,0.84],cmap=cm.Oranges,title_fmt=list(reversed(fmt)),plot_contours=True)
        fig.savefig(filebase+'parameters.eps')
        fig.clf()
           
# plain language summary
    if summaryFlag:
        pass

    return
            


#######################################################
#######################################################
###############   EMCEE MODEL FITTING  ################
#######################################################
#######################################################



def modelFitEMCEE(spec, **kwargs):
    '''
    :Purpose: Uses the ``emcee`` package by Dan Foreman-Mackey et al. to perform 
        Goodman & Weare's Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler
        to fit a spectrum to a set of atmosphere models. 
        Returns the best estimate of the effective temperature, surface 
        gravity, and (if selected) metallicity.  Includes an estimate of the time required to run, prompts
        user if they want to proceed, and shows progress with iterative saving of outcomes
    :param spec: Spectrum class object, which should contain wave, flux and noise array elements.
    :param nwalkers: number of MCMC walkers, should have at least 20
    :type nwalkers: optional, default = 20
    :param nsamples: number of MCMC samples, for model fitting about 500 seems OK
    :type nsamples: optional, default = 500
    :param burn_fraction: the fraction of the initial steps to be discarded. (e.g., if 
                ``burn_fraction = 0.2``, the first 20% of the samples are discarded.)
    :type burn_fraction: optional, default = 0.5
    :param initial_guess: array including initial guess of the model parameters.
            Can also set individual guesses of spectral parameters by using 
            **initial_temperature**, **initial_teff**, or **t0**;
            **initial_gravity**, **initial_logg** or **g0**; 
            and **initial_metallicity**, **initial_z** or **z0**.
    :type initial_guess: optional, default = array of random numbers within allowed ranges
    :param limits: list of 2-element arrays indicating ranges of the model parameters to limit the parameter space.
            Can also set individual ranges of spectral parameters by using 
            **temperature_range**, **teff_range** or **t_range**;
            **gravity_range**, **logg_range** or **g_range**;
            and **metallicity_range** or **z_range**.
    :type limits: optional, default = depends on model set
    :param prior_scatter: array giving the widths of the normal distributions from which to draw prior parameter values
    :type prior_scatter: optional, default = [25,0.1,0.1]
    :param model: set of models to use (``set`` and ``model_set`` do the same); options include:

        - *'BTSettl2008'*: model set with effective temperature of 400 to 2900 K, surface gravity of 3.5 to 5.5 and metallicity of -3.0 to 0.5 
          from `Allard et al. (2012) <http://adsabs.harvard.edu/abs/2012RSPTA.370.2765A>`_
        - *'burrows06'*: model set with effective temperature of 700 to 2000 K, surface gravity of 4.5 to 5.5, metallicity of -0.5 to 0.5, 
          and sedimentation efficiency of either 0 or 100 from `Burrows et al. (2006) <http://adsabs.harvard.edu/abs/2006ApJ...640.1063B>`_
        - *'morley12'*: model set with effective temperature of 400 to 1300 K, surface gravity of 4.0 to 5.5, metallicity of 0.0 
          and sedimentation efficiency of 2 to 5 from `Morley et al. (2012) <http://adsabs.harvard.edu/abs/2012ApJ...756..172M>`_
        - *'morley14'*: model set with effective temperature of 200 to 450 K, surface gravity of 3.0 to 5.0, metallicity of 0.0 
          and sedimentation efficiency of 5 from `Morley et al. (2014) <http://adsabs.harvard.edu/abs/2014ApJ...787...78M>`_
        - *'saumon12'*: model set with effective temperature of 400 to 1500 K, surface gravity of 3.0 to 5.5 and metallicity of 0.0 
          from `Saumon et al. (2012) <http://adsabs.harvard.edu/abs/2012ApJ...750...74S>`_
        - *'drift'*: model set with effective temperature of 1700 to 3000 K, surface gravity of 5.0 to 5.5 and metallicity of -3.0 to 0.0 
          from `Witte et al. (2011) <http://adsabs.harvard.edu/abs/2011A%26A...529A..44W>`_
    
    :type model: optional, default = 'BTSettl2008'
    :param radius: set to True to calculate and returns radius of object [NOT CURRENT IMPLEMENTED]
    :type radius: optional, default = False
    :param save: save interim results to a .dat file based on output filename
    :type save: optional, default = True
    :param output: base filename for output (``filename`` and ``outfile`` do the same); 
        outputs will include (each can be set individually with associated keywords):
        - ``filename_iterative.dat``: interative saved data
        - ``filename_summary.txt``: summary of results
        - ``filename_corner.eps``: corner plot of parameters
        - ``filename_comparison.eps``: plot spectrum compared to best fit model
    :type output: optional, default = None
    :param plot_format: file type for diagnostic plots
    :type plot: optional, default = 'pdf'
    :param noprompt: don't prompt user to continue of emcee run will be > 10 minutes
    :type noprompt: optional, default = False
    :param verbose: give lots of feedback
    :type verbose: optional, default = False

    In addition, the parameters for compareSpectra_, generateMask_, plotSpectrum_; see SPLAT API for details.

    .. _plotSpectrum: api.html#splat_plot.plotSpectrum
    .. _plotSpectrum: api.html#splat.compareSpectra
    .. _generateMask api.html#splat.generateMask
    
    Note: modelfitEMCEE requires external packages: 
        - ``emcee``: http://dan.iel.fm/emcee/current
        -``corner``: http://corner.readthedocs.io/en/latest

    :Example:
    >>> import splat
    >>> sp = splat.Spectrum(shortname='1507-1627')[0]
    >>> spt,spt_e = splat.classifyByStandard(sp)
    >>> teff,teff_e = splat.typeToTeff(spt)
    >>> result = modelFitEMCEE(sp,t0=teff,g0=5.0,fit_metallicity=False,\
    >>>    nwalkers=50,nsamples=500,output='/Users/adam/test_modelfitEMCEE')
        Estimated time to compute = 9228 seconds = 153.8 minutes = 2.56 hours = 0.11 days
        Do you want to continue? [Y/n]: 
        Progress: [**************************************************]
    
    Results are saved in test_modelfitEMCEE_interative.dat, *_chains.pdf, *_comparison.pdf, *_corner.pdf, and *_summary.txt
    '''

# check that emcee package is installed
    try:
        import emcee
    except:
        raise NameError('\nYou must install emcee to run this program; see http://dan.iel.fm/emcee/current/')

    start_time = time.time()

# keywords
    nwalkers = kwargs.get('nwalkers', 10)
    nsamples = kwargs.get('nsamples', 1000)
    burn_fraction = kwargs.get('burn_fraction', 0.5)  # what fraction of the initial steps are to be discarded
    prior_scale = {'teff': 25, 'logg': 0.1, 'z': 0.1, 'radius': 0.001*RADIUS_SUN.value}
    prior_scale['teff'] = kwargs.get('t_scale',prior_scale['teff'])
    prior_scale['logg'] = kwargs.get('g_scale',prior_scale['logg'])
    prior_scale['z'] = kwargs.get('z_scale',prior_scale['z'])
    verbose = kwargs.get('verbose', False)
    feedback_width = 50

# plotting and reporting keywords
    showRadius = kwargs.get('radius', spec.fscale == 'Absolute')
    filebase = kwargs.get('output', 'fit_')
    filebase = kwargs.get('filename',filebase)
    filebase = kwargs.get('outfile',filebase)
    plot_format = kwargs.get('plot_format','pdf')

# model parameters
    model_set = kwargs.get('set', 'BTSettl2008')
    model_set = kwargs.get('model', model_set)
    model_set = kwargs.get('model_set', model_set)

# prep outputs
    file_iterative = kwargs.get('file_iterative',os.path.splitext(filebase)[0]+'_iterative.dat')
    file_chains = kwargs.get('file_chains',os.path.splitext(filebase)[0]+'_chains.'+plot_format)
    file_corner = kwargs.get('file_corner',os.path.splitext(filebase)[0]+'_corner.'+plot_format)
    file_comparison = kwargs.get('file_comparison',os.path.splitext(filebase)[0]+'_comparison.'+plot_format)
    file_bestcomparison = kwargs.get('file_bestcomparison',os.path.splitext(filebase)[0]+'_bestcomparison.'+plot_format)
    file_summary = kwargs.get('file_summary',os.path.splitext(filebase)[0]+'_summary.txt')
    if kwargs.get('save',True):
        f = open(file_iterative,'w')
        f.close()

# set limits for models - input or set by model itself
    modelgrid = _loadModelParameters(model_set) # Range parameters can fall in
    ranges = kwargs.get('ranges', \
        [[numpy.min(modelgrid['teff']),numpy.max(modelgrid['teff'])],\
        [numpy.min(modelgrid['logg']),numpy.max(modelgrid['logg'])],\
        [numpy.min(modelgrid['z']),numpy.max(modelgrid['z'])]])
    teff_range = kwargs.get('teff_range',ranges[0])
    teff_range = kwargs.get('temperature_range',teff_range)
    logg_range = kwargs.get('logg_range',ranges[1])
    logg_range = kwargs.get('gravity_range',logg_range)
    z_range = kwargs.get('z_range',ranges[2])
    z_range = kwargs.get('metallicity_range',z_range)
    limits = kwargs.get('limits', [teff_range,logg_range,z_range])

# create a mask
    mask = kwargs.get('mask',_generateMask(spec.wave,**kwargs))

# set initial parameters
    parameters0 = kwargs.get('initial_guess',[\
        numpy.random.uniform(teff_range[0],teff_range[1]),\
        numpy.random.uniform(logg_range[0],logg_range[1]),\
        0.0])
    if len(parameters0) < 3:
        parameters0.append(0.0)
        
    parameters0[0] = kwargs.get('initial_temperature',parameters0[0])
    parameters0[0] = kwargs.get('initial_teff',parameters0[0])
    parameters0[0] = kwargs.get('t0',parameters0[0])
    parameters0[1] = kwargs.get('initial_gravity',parameters0[1])
    parameters0[1] = kwargs.get('initial_logg',parameters0[1])
    parameters0[1] = kwargs.get('g0',parameters0[1])
    parameters0[2] = kwargs.get('initial_metallicity',parameters0[2])
    parameters0[2] = kwargs.get('initial_z',parameters0[2])
    parameters0[2] = kwargs.get('z0',parameters0[2])

    if not kwargs.get('fit_metallicity',False):
        parameters0 = parameters0[0:2]

    parameter_names = MODEL_PARAMETER_NAMES[:len(parameters0)]
    parameter_titles = [MODEL_PARAMETER_TITLES[p] for p in parameter_names]
    parameter_units = [MODEL_PARAMETER_UNITS[p] for p in parameter_names]
    nparameters = len(parameters0)
    pscale = [prior_scale[p] for p in parameter_names]
    initial_parameters = [parameters0+pscale*numpy.random.randn(len(parameters0)) for i in range(nwalkers)]

# check the time it should take to run model, and that user has models
    testtimestart = time.time()
    try:
        mdl = loadModel(teff=2125,logg=5.1,z=-0.2,set='BTSettl2008')
    except:
        raise ValueError('\nProblem reading in a test model; make sure you have the full SPLAT model set installed')
    testtimeend = time.time()
    time_estimate = (testtimeend-testtimestart)*nwalkers*nsamples*1.2
    print('Estimated time to compute = {:.0f} seconds = {:.1f} minutes = {:.2f} hours'.\
        format(time_estimate,time_estimate/60.,time_estimate/3600.))
    if time_estimate > 1200. and not kwargs.get('noprompt',False):
        resp = input('Do you want to continue? [Y/n]: ')
        if resp.lower()[0] == 'n':
            print('\nAborting')
            return

# run EMCEE with iterative saving and updates
    model_params = {'model': model_set, 'limits': limits, 'mask': mask}
    sampler = emcee.EnsembleSampler(nwalkers, nparameters, _modelFitEMCEE_lnprob, args=(spec.wave.value,spec.flux.value,spec.noise.value,model_params))
    sys.stdout.write("\n")
    for i, result in enumerate(sampler.sample(initial_parameters, iterations=nsamples)):
        if i > 0:
            ch = sampler.chain[:,:i,:]
            radii = ((sampler.blobs[:i]*(kwargs.get('distance',10.)*u.pc.to(u.cm)/RADIUS_SUN)**2)**0.5).value.reshape(-1)
            cr = ch.reshape((-1, nparameters))
            mcr = numpy.append(cr.transpose(),[radii],axis=0).transpose()
            lnp = sampler.lnprobability[:,:i].reshape(-1)
            if verbose: print(lnp)
            if kwargs.get('use_weights',False) != False:
                parameter_weights = numpy.exp(lnp-numpy.max(lnp))
            else:
                parameter_weights = numpy.ones(len(lnp))
            bparam,mparam,qparam = _modelFitEMCEE_bestparameters(mcr,lnp,parameter_weights=parameter_weights)
            if verbose: print(bparam)
    #        lnp = result[1]
    #        scales = result[-1]
    #        radii = ((scales*(kwargs.get('distance',10.)*u.pc.to(u.cm)/RADIUS_SUN)**2)**0.5).value.reshape(-1)
            n = int((feedback_width+1) * float(i) / nsamples)
            resp = '\rProgress: [{0}{1}] '.format('*' * n, ' ' * (feedback_width - n))
            for kkk in range(nparameters):
                resp+=' {:s}={:.2f}'.format(MODEL_PARAMETER_NAMES[kkk],bparam[kkk])
            resp+=' R={:.2f} lnP={:e}'.format(bparam[-1],lnp[-1])
            print(resp)
    # save iteratively
            position = result[0]
            if verbose: print(position)
            if kwargs.get('save',True) and i > 5:
                _modelFitEMCEE_plotchains(ch,file_chains)
                _modelFitEMCEE_plotcomparison(cr,spec,file_comparison,model=model_set,draws=5,parameter_weights=parameter_weights)
                _modelFitEMCEE_plotbestcomparison(spec,bparam[:-1],file_bestcomparison,model=model_set)
#                _modelFitEMCEE_plotcorner(mcr,file_corner,parameter_weights=parameter_weights,**kwargs)
                f = open(file_iterative, 'a')
                for k in range(position.shape[0]):
                    f.write('{0:4d} {1:s} {2:e}\n'.format(k, ' '.join([str(mmm) for mmm in position[k]]),lnp[k]))
                f.close()
    sys.stdout.write("\n")

# burn out the initial section
    orig_samples = sampler.chain.reshape((-1, nparameters))
    orig_lnp = sampler.lnprobability.reshape(-1)
    orig_radii = ((numpy.array(sampler.blobs).reshape(-1)*(kwargs.get('distance',10.)*u.pc.to(u.cm)/RADIUS_SUN)**2)**0.5).value.reshape(-1)
    samples = sampler.chain[:, (burn_fraction*nsamples):, :].reshape((-1, nparameters))
    lnp = orig_lnp[(burn_fraction*nsamples*nwalkers):]
    radii = orig_radii[(burn_fraction*nsamples*nwalkers):]
    merged_samples = numpy.append(samples.transpose(),[radii],axis=0).transpose()

    if verbose: print(orig_radii.shape,orig_samples.shape,orig_lnp.shape)
    if verbose: print(radii.shape,samples.shape,lnp.shape,sampler.chain.shape)

# determine parameters
    if kwargs.get('use_weights',False) != False:
        parameter_weights = numpy.exp(lnp-numpy.max(lnp))
    else:
        parameter_weights = numpy.ones(len(lnp))

    bparam,mparam,qparam = _modelFitEMCEE_bestparameters(merged_samples,lnp,parameter_weights=parameter_weights)
    if verbose: print(bparam)


# reporting
    _modelFitEMCEE_plotchains(sampler.chain,file_chains)
    _modelFitEMCEE_plotcomparison(samples,spec,file_comparison,model=model_set,draws=20,parameter_weights=parameter_weights,**kwargs)
    _modelFitEMCEE_plotbestcomparison(spec,bparam[:-1],file_bestcomparison,model=model_set,**kwargs)
    _modelFitEMCEE_plotcorner(merged_samples,file_corner,parameter_weights=parameter_weights,**kwargs)

    end_time = time.time()
    total_time = (end_time-start_time)
    if verbose: print('Total run time = {:.0f} seconds or {:.2f} hours'.format(total_time,total_time/3600.))

    skwargs = {'burn_fraction': burn_fraction, 'filebase': filebase, 'total_time': total_time, 'mask': mask, 'model': model_set}
    _modelFitEMCEE_summary(sampler,spec,file_summary,**skwargs)
    return sampler



def _modelFitEMCEE_bestparameters(values,lnp,**kwargs):
    '''
    Return three sets of parameters: by quantiles, the weighted mean, and the best values
    '''
    parameter_weights = kwargs.get('parameter_weights',numpy.ones(values.shape[-1]))
    quantiles = kwargs.get('quantiles',[16,50,84])

    quant_parameters = []
    best_parameters = []
    mean_parameters = []
    for i in range(values.shape[-1]):
        q = numpy.percentile(values[:,i],quantiles)
        quant_parameters.append([q[1],q[2]-q[1],q[1]-q[0]])
        mean_parameters.append(numpy.sum(parameter_weights*values[:,i])/numpy.sum(parameter_weights))
        best_parameters.append(values[numpy.where(lnp == numpy.max(lnp)),i].reshape(-1)[0])
    return best_parameters,mean_parameters,quant_parameters


def _modelFitEMCEE_lnlikelihood(theta,x,y,yerr,model_params):
    mparam = copy.deepcopy(model_params)
    for i in range(len(theta)):
        mparam[MODEL_PARAMETER_NAMES[i]] = theta[i]
    try:
        mdl = loadModel(**mparam)
    except:
        resp = '\nProblem reading in model '
        for k,v in enumerate(theta):
            resp+='{} = {}, '.format(MODEL_PARAMETER_NAMES[k],v)
        print(resp)
        return -1.e30,0.
#    chi,scl = splat.compareSpectra(sp,mdl,**model_params)
    chi,scl = compareSpectra(Spectrum(wave=x,flux=y,noise=yerr),mdl,**model_params)
    lnp = -0.5*chi
    if model_params.get('noise_scaling',False):
        f = interp1d(mdl.wave.value,mdl.flux.value*scl,bounds_error=False,fill_value=0.)
        inv_sigma2 = 1./(yerr**2+f(x)**2*numpy.exp(theta[-1]))
        lnp = -0.5*numpy.nansum((1.-mparam['mask'])*((y-f(x))**2*inv_sigma2-numpy.log(inv_sigma2)))
#            inv_sigma2 = 1./yerr**2
#            lnp = -0.5*numpy.nansum((y-f(x))**2*inv_sigma2)
    return lnp,scl
#    except:
#        resp = '\nProblem comparing model '
#        for k,v in enumerate(theta):
#            resp+='{} = {}, '.format(MODEL_PARAMETER_NAMES[k],v)
#        print(resp+' to data')
#    return -numpy.inf


def _modelFitEMCEE_lnprior_limits(theta,limits):
    '''
    compute the log of the probability assuming a uniform distribution
    with hard limits; if outside limits, probability returns -infinity
    '''
    for i,t in enumerate(theta):
        try:
            if t < numpy.min(limits[i]) or t > numpy.max(limits[i]):
                return -1.e30
        except:
            pass
    return 0.0


def _modelFitEMCEE_lnprior_normal(theta,meansds):
    '''
    compute the log of the probability assuming a normal distribution
    there probably needs to be better error checking here
    '''
    lnp = 0.0
    for i,t in enumerate(theta):
        try:
            lnp-=0.5*(((t-meansds[i][0])/meansds[i][1])**2-numpy.log(meansds[i][1]))
        except:
            pass
    return lnp

def _modelFitEMCEE_lnprob(theta,x,y,yerr,model_params):
#    lnp = 0.
#    if kwargs.get('normal_priors',None) != None and kwargs.get('priors_meansds',None) != None:
#        lnp+=modelFitEMCEE_lnprior_normal(theta,kwargs.get('priors_meansds'),**kwargs)
#    if kwargs.get('limits',None) != None:
    lnp0 = _modelFitEMCEE_lnprior_limits(theta,model_params['limits'])
    if not numpy.isfinite(lnp0):
        return -1.e30
    lnp,scale = _modelFitEMCEE_lnlikelihood(theta,x,y,yerr,model_params)
    return lnp0+lnp, scale


def _modelFitEMCEE_plotchains(chains,file,**kwargs):
    plt.figure(1,figsize=kwargs.get('figsize',[8,4*chains.shape[-1]]))
    for i in range(chains.shape[-1]):
        plt.subplot(int('{}1{}'.format(chains.shape[-1],i+1)))
        xr = [0,chains.shape[1]-1]
        yr = [numpy.min(chains[:,:,i]),numpy.max(chains[:,:,i])]
        yr[0] -= 0.05*(numpy.max(chains[:,:,i])-numpy.min(chains[:,:,i]))
        yr[1] += 0.05*(numpy.max(chains[:,:,i])-numpy.min(chains[:,:,i]))
#        print(yr)
        for j in range(chains.shape[0]):
            plt.plot(numpy.arange(chains.shape[1]),chains[j,:,i],'k-',alpha=0.4)
        if kwargs.get('burn_fraction',0) > 0:
            plt.plot([chains.shape[1]*kwargs.get('burn_fraction')]*2,yr,'k:')
            mn = numpy.mean(chains[:,chains.shape[1]*kwargs.get('burn_fraction'):,i])
        else:
            mn = numpy.mean(chains[:,:,i])
        plt.axis(xr+yr)
        plt.plot(xr,[mn]*2,'r-')
        plt.xlabel('Steps')
        plt.ylabel(r''+MODEL_PARAMETER_TITLES[MODEL_PARAMETER_NAMES[i]]+' ('+MODEL_PARAMETER_UNITS[MODEL_PARAMETER_NAMES[i]].to_string()+')')
    try:
        plt.savefig(file)
        plt.clf()
    except:
        print('\nProblem saving chains plot to {}'.format(file))
    return plt


def _modelFitEMCEE_plotcomparison(samples,spec,file,**kwargs):
    '''
    for now just plotting best model
    would like to do draws from posterior instead
    '''
# extract best fit values
    draws = kwargs.get('draws',1)
    pargs = (spec,)
    legend = [spec.name]
    colors = ['k']
    alpha = [0]
    tbl = Table()
    tbl['parameter_weights'] = kwargs.get('parameter_weights',numpy.ones(samples.shape[0]))
    tbl['parameter_weights'] = numpy.max(tbl['parameter_weights'])-tbl['parameter_weights']
    for i in range(samples.shape[-1]):
        tbl[MODEL_PARAMETER_NAMES[i]] = samples[:,i]
    tbl.sort('parameter_weights')
    tblu = tunique(tbl,keys=MODEL_PARAMETER_NAMES[:samples.shape[-1]])
    draws = numpy.min([draws,len(tblu)])
    for k in range(draws):
        mkwargs = copy.deepcopy(kwargs)
        mlegend = r''
        for i in range(samples.shape[-1]):
            mkwargs[MODEL_PARAMETER_NAMES[i]] = tblu[MODEL_PARAMETER_NAMES[i]][k]
            mlegend+='{:s}={:.2f} '.format(MODEL_PARAMETER_TITLES[MODEL_PARAMETER_NAMES[i]],mkwargs[MODEL_PARAMETER_NAMES[i]])
        mdl = loadModel(**mkwargs)
#    print(mdl.teff,mdl.logg)
        stat,scl = compareSpectra(spec,mdl,**kwargs)
        mdl.scale(scl)
        pargs = pargs + (mdl,)
        legend.append(mlegend)
        colors.append('grey')
        alpha.append(tblu['parameter_weights'][k])
#    print(*pargs)
    return splot.plotSpectrum(*pargs,colors=colors,alpha=alpha,\
        uncertainty=True,telluric=True,file=file,legend=legend)


def _modelFitEMCEE_plotbestcomparison(spec,mparam,file,**kwargs):
    '''
    for now just plotting best model
    would like to do draws from posterior instead
    '''

# extract best fit values
    mkwargs = copy.deepcopy(kwargs)
    mlegend = r''
#    print(mparam)
    for i,m in enumerate(mparam):
        mkwargs[MODEL_PARAMETER_NAMES[i]] = m
        mlegend+='{:s}={:.2f} '.format(MODEL_PARAMETER_TITLES[MODEL_PARAMETER_NAMES[i]],float(m))
#    print(mkwargs)
    mdl = loadModel(**mkwargs)
#    print(mdl.teff,mdl.logg)
    stat,scl = compareSpectra(spec,mdl,**kwargs)
    mdl.scale(scl)
    return splot.plotSpectrum(spec,mdl,spec-mdl,colors=['k','b','grey'],uncertainty=True,telluric=True,file=file,\
        legend=[spec.name,mlegend,r'difference ($\chi^2$ = {:.0f})'.format(stat)])



def _modelFitEMCEE_plotcorner(samples,file,**kwargs):
    '''
    corner plot for modelFitEMCEE
    '''
    try:
        import corner
    except:
        print('\nYou must install corner to display corner plot; see http://corner.readthedocs.io/en/latest/')
        return None

    if len(kwargs.get('truths',[])) == 0:
        truths = [numpy.inf for i in range(samples.shape[-1])]

    labels = [r''+MODEL_PARAMETER_TITLES[MODEL_PARAMETER_NAMES[i]]+' ('+MODEL_PARAMETER_UNITS[MODEL_PARAMETER_NAMES[i]].to_string()+')' for i in range(samples.shape[-1]-1)]
    labels.append(r'Radius (R$_{\odot}$)')
    weights = kwargs.get('parameter_weights',numpy.ones(samples.shape[0]))

    fig = corner.corner(samples, quantiles=[0.16, 0.5, 0.84], truths=truths, \
            labels=labels, show_titles=True, weights=weights,\
            title_kwargs={"fontsize": kwargs.get('fontsize',12)})

    try:
        fig.savefig(file)
        fig.clf()
    except:
        print('\nProblem saving corner plot to {}'.format(file))
    return fig


def _modelFitEMCEE_summary(sampler,spec,file,**kwargs):
    '''
    for now just plotting best model
    would like to do draws from posterior instead
    '''

# extract best fit values
    base_samples = sampler.chain
    nwalkers = base_samples.shape[0]
    nsamples = base_samples.shape[1]
    nparameters = base_samples.shape[2]
    samples = base_samples[:, (kwargs['burn_fraction']*nsamples):, :].reshape((-1, nparameters))

    f = open(file,'w')
    f.write('EMCEE fitting analysis of spectrum of {} using the models of {}'.format(spec.name,kwargs['model']))
    f.write('\nFitting performed on {}'.format(time.strftime("%Y %h %d %I:%M:%S")))
    f.write('\n\nMCMC paramaters:')
    f.write('\n\tNumber of walkers = {}'.format(nwalkers))
    f.write('\n\tNumber of samples = {}'.format(nsamples))
    f.write('\n\tNumber of fit parameters = {}'.format(nparameters))
    f.write('\n\tBurn-in fraction = {}'.format(kwargs['burn_fraction']))

    f.write('\n\nBest fit parameters')
    for i in range(nparameters):
        fit = numpy.percentile(samples[:,i], [16, 50, 84])
        f.write('\n\t{} = {}+{}-{} {}'.format(MODEL_PARAMETER_TITLES[MODEL_PARAMETER_NAMES[i]],fit[1],fit[2]-fit[1],fit[1]-fit[0],MODEL_PARAMETER_UNITS[MODEL_PARAMETER_NAMES[i]].to_string()))

    mkwargs = copy.deepcopy(kwargs)
    for i in range(samples.shape[-1]):
        mkwargs[MODEL_PARAMETER_NAMES[i]] = numpy.median(samples[:,i])
    mdl = loadModel(**mkwargs)
    stat,scl = compareSpectra(spec,mdl,**kwargs)

# copmute DOF
    try:
        dof = spec.dof
    except:
        dof = len(spec.wave)
    if len(kwargs.get('mask',[])) > 0:
        dof = dof*(numpy.sum(1.-kwargs['mask']))/len(kwargs['mask'])
    dof = dof-nparameters-1

    f.write('\n\nResidual chi^2 = {:.0f} for {:.0f} degrees of freedom'.format(stat,dof))
    f.write('\nProbability that model matches data = {:.4f}'.format(stats.chi2.sf(stat,dof)))
    f.write('\nSource/model scale factor = {:.2f} implying a radius of {:.3f} solar radii at 10 pc\n'.format(scl,(scl**0.5*10.*u.pc).to(u.Rsun).value))

    f.write('\n\nFitting completed in {:.1f} seconds = {:.2f} hours'.format(kwargs['total_time'],kwargs['total_time']/3600.))
    f.write('\nResults may be found in the files {}*'.format(kwargs['filebase']))
    f.close()
    return 




#######################################################
#######################################################
#############   ROUNTINES IN DEVELOPMENT  #############  
#######################################################
#######################################################



def calcLuminosity(sp, mdl=False, absmags=False, **kwargs):
    '''
    :Purpose: Calculate luminosity from photometry and stitching models.

    THIS IS CURRENTLY BEING WRITTEN - DO NOT USE!

    :param sp: Spectrum class object, which should contain wave, flux and 
               noise array elements.
    :param mdl: model spectrum loaded using ``loadModel``
    :type mdl: default = False
    :param absmags: a dictionary whose keys are one of the following filters: 'SDSS Z', 
                    '2MASS J', '2MASS H', '2MASS KS', 'MKO J', 'MKO H', 'MKO K', 'SDSS R', 
                    'SDSS I', 'WISE W1', 'WISE W2', 'WISE W3', 'WISE W4', 'IRAC CH1', 
                    'IRAC CH2', 'IRAC CH3', 'IRAC CH4'
    :type absmags: default = False
    
    '''

    spec_filters = ['SDSS Z','2MASS J','2MASS H','2MASS KS','MKO J','MKO H','MKO K']
    sed_filters = ['SDSS R','SDSS I','WISE W1','WISE W2','WISE W3','WISE W4','IRAC CH1','IRAC CH2','IRAC CH3','IRAC CH4']
    
    if ~isinstance(absmags,dict):
        raise ValueError('\nAbsolute magnitudes should be a dictionary whose keys are one of the following filters:\n{}'.format(spec_filters+sed_filters))

# read in a model if one is not provided based on classification and temperature
    if mdl == False or 'SED' not in mdl.name:
        spt,spt_unc = classifyByIndex(sp)
        teff,unc = spemp.typeToTeff(spt)
        mdl = loadModel(teff=teff,logg=5.0,sed=True)

# prep arrays
    flux = []
    flux_unc = []
    flux_wave = []
    
# steps:
# scale spectrum to absolute magnitude if necessary and integrate flux, varying noise and including variance in abs mag factor
    spcopy = sp
    if spcopy.fscale != 'Absolute':
        scale = []
        scale_unc = []
        for k in absmags.keys():
            if k.upper() in spec_filters:
                m = spphot.filterMag(spcopy,k)
                scale.extend(10.**(0.4*(m-absmags[k][0])))
# note: need to add in spectral flux uncertainty as well
                scale_unc.extend(numpy.log(10.)*0.4*absmags[k][1]*scale[-1])
        if len(scale) == 0:
            raise ValueError('\nNo absolute magnitudes provided to scale spectrum; you specified:\n{}'.format(absmags.keys()))
        scl,scl_e = weightedMeanVar(scale,scale_unc,uncertainty=True)
        spcopy.scale(numpy.mean(scl))
        spcopy.fscale = 'Absolute'

# integrate data
# NEED TO INSERT UNCERTAINTY HERE
    flux.extend(trapz(spcopy.flux,spcopy.wave))
    flux_unc.extend(0.)
    flux_wave.extend([numpy.nanmin(spcopy.wave),numpy.nanmax(spcopy.wave)])

# scale segments of models scaled to WISE or IRAC bands if available, include variance in abs mag factor
# PROBLEM: WHAT IF SPECTRAL PIECES OVERLAP?
    for k in absmags.keys():
        if k.upper() in sed_filters:
            filterdat = spphot.filterProperties(k.upper())
            mdl.fluxCalibrate(k,absmags[k][0])
            w = numpy.where(mdl.wave.value >= filterdat['lambda_min'] and mdl.wave.value <= filterdat['lambda_max'])
            flux.extend(trapz(mdl.flux[w],mdl.wave[w]))
            flux_unc.extend(2.5*numpy.log(10.)*absmags[k][1]*flux[-1])
            flux_wave.extend([filterdat['lambda_min'],filterdat['lambda_max']])

# match model between these scaled pieces and out to ends and integrate, include variance in abs mag factor(s)
# report log luminosity in solar units and uncertainty
# optional report the various pieces and percentages of whole ()
#
# absmags is a dictionary whose keys are filter names and whose elements are 2-element lists of value and uncertainty        

    
