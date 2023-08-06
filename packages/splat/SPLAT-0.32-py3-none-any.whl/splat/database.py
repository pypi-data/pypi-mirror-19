# -*- coding: utf-8 -*-
from __future__ import print_function, division

"""
.. note::
         These are the database functions for SPLAT 
"""

# imports: internal
import base64
import copy
import csv
import glob
import os
import re
import requests
from shutil import copyfile

# imports: external
import astropy
import numpy
from astropy.io import ascii, fits            # for reading in spreadsheet
from astropy.table import Column, Table, join, vstack           # for reading in table files
from astropy.time import Time            # for reading in table files
from astropy.coordinates import SkyCoord
from astropy import units as u            # standard units
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier

# splat requirements
from .initialize import *
from .utilities import *
#from .splat import DB_SOURCES, DB_SPECTRA
#import splat as spl

# Python 2->3 fix for input
try: input=raw_input
except NameError: pass



#####################################################
###########   DATABASE QUERY AND ACCESS   ###########
#####################################################


def fetchDatabase(*args, **kwargs):
    '''
    :Purpose: Get the SpeX Database from either online repository or local drive
    '''
    filename = 'db_spexprism.txt'   # temporary original database file for backwards compatability
    if len(args) > 0:
        filename = args[0]
    kwargs['filename'] = kwargs.get('filename',filename)
    kwargs['filename'] = kwargs.get('file',kwargs['filename'])
    kwargs['folder'] = kwargs.get('folder',DB_FOLDER)
    url = kwargs.get('url',SPLAT_URL)+kwargs['folder']
    local = kwargs.get('local',True)
    online = kwargs.get('online',not local and checkOnline())
    local = not online
    kwargs['local'] = local
    kwargs['online'] = online
    kwargs['model'] = True

# determine format of file    
    delimiter = kwargs.get('delimiter','')
    fmt = kwargs.get('format','')
    fmt = kwargs.get('fmt',fmt)
    if delimiter == ',' or delimiter == 'comma' or delimiter == 'csv' or kwargs.get('comma',False) == True or ('.csv' in kwargs['filename']):
        delimiter = ','
        fmt = 'csv'
    if delimiter == '\t' or delimiter == 'tab' or kwargs.get('tab',False) == True or ('.txt' in kwargs['filename']):
        delimiter = '\t'
        fmt = 'tab'
    if fmt == '':
        raise NameError('\nCould not determine the file format of '+kwargs['filename']+'; please specify using format or delimiter keywords\n\n')


# check that folder/set is present either locally or online
# if not present locally but present online, switch to this mode
# if not present at either raise error
    folder = checkLocal(kwargs['folder'])
    if folder=='':
        folder = checkOnlineFile(kwargs['folder'])
        if folder=='':
            raise NameError('\nCould not find '+kwargs['folder']+' locally or on SPLAT website\n\n')
        else:
            kwargs['folder'] = folder
            kwargs['local'] = False
            kwargs['online'] = True
    else:
        kwargs['folder'] = folder

# locally:
    if kwargs['local']:
#        print('Reading local')
        infile = checkLocal(kwargs['filename'])
        if infile=='':
            infile = checkLocal(kwargs['folder']+'/'+kwargs['filename'])
        if infile=='':
            raise NameError('\nCould not find '+kwargs['filename']+' locally\n\n')
        else:
            try:
                data = ascii.read(infile, delimiter=delimiter,fill_values='-99.',format=fmt)
#                data = ascii.read(infile, delimiter='\t',fill_values='-99.',format='tab')
            except:
                raise NameError('\nCould not load {}: this may be a decoding error\n'.format(infile))


# check if file is present; if so, read it in, otherwise go to interpolated
# online:
    if kwargs['online']:
#        print('Reading online')
        infile = checkOnlineFile(kwargs['filename'])
        if infile=='':
            infile = checkOnlineFile(kwargs['folder']+'/'+kwargs['filename'])
        if infile=='':
            raise NameError('\nCould not find '+kwargs['filename']+' on the SPLAT website\n\n')
        try:
#            open(os.path.basename(TMPFILENAME), 'wb').write(urllib2.urlopen(url+infile).read())
            open(os.path.basename(TMPFILENAME), 'wb').write(requests.get(url+infile).content)
            kwargs['filename'] = os.path.basename(tmp)
            data = ascii.read(os.path.basename(TMPFILENAME), delimiter=delimiter,fill_values='-99.',format=fmt)
            os.remove(os.path.basename(TMPFILENAME))
        except:
            raise NameError('\nHaving a problem reading in '+kwargs['filename']+' on the SPLAT website\n\n')

    return data





#####################################################
###########   ACCESSING ONLINE CATALOGS   ###########
#####################################################


def queryVizier(coordinate,**kwargs):
    return getPhotometry(coordinate,**kwargs)

def getPhotometry(coordinate,**kwargs):
    '''
    Purpose
        Downloads photometry for a source by coordinate using astroquery

    Required Inputs:
        :param: coordinate: Either an astropy SkyCoord or a variable that can be converted into a SkyCoord using `spl.properCoordinates()`_

    .. _`spl.properCoordinates()` : api.html#spl.properCoordinates
        
    Optional Inputs:
        :param radius: Search radius, nominally in arcseconds although this can be changed by passing an astropy.unit quantity (default = 30 arcseconds)
        :param catalog: Catalog to query, which can be set to the Vizier catalog identifier code or to one of the following preset catalogs:
            * '2MASS' (or set ``2MASS``=True): the 2MASS All-Sky Catalog of Point Sources (`Cutri et al. 2003 <http://adsabs.harvard.edu/abs/2003yCat.2246....0C>`_), Vizier id II/246
            * 'SDSS' (or set ``SDSS``=True): the The SDSS Photometric Catalog, Release 9 (`Adelman-McCarthy et al. 2012 <http://adsabs.harvard.edu/abs/2012ApJS..203...21A>`_), Vizier id V/139
            * 'WISE' (or set ``WISE``=True): the WISE All-Sky Data Release (`Cutri et al. 2012 <http://adsabs.harvard.edu/abs/2012yCat.2311....0C>`_), Vizier id II/311
            * 'ALLWISE' (or set ``ALLWISE``=True): the AllWISE Data Release (`Cutri et al. 2014 <http://adsabs.harvard.edu/abs/2014yCat.2328....0C>`_), Vizier id II/328
            * 'VISTA' (or set ``VISTA``=True): the VIKING catalogue data release 1 (`Edge et al. 2013 <http://adsabs.harvard.edu/abs/2013Msngr.154...32E>`_), Vizier id II/329
            * 'CFHTLAS' (or set ``CFHTLAS``=True): the CFHTLS Survey (T0007 release) by (`Hudelot et al. 2012 <http://adsabs.harvard.edu/abs/2012yCat.2317....0H>`_), Vizier id II/317
            * 'DENIS' (or set ``DENIS``=True): the DENIS DR3 (DENIS Consortium 2005), Vizier id B/denis/denis
            * 'UKIDSS' (or set ``UKIDSS``=True): the UKIDSS-DR8 LAS, GCS and DXS Surveys (`Lawrence et al. 2012 <http://adsabs.harvard.edu/abs/2007MNRAS.379.1599L>`_), Vizier id II/314
            * 'LEHPM' (or set ``LEHPM``=True): the Liverpool-Edinburgh High Proper Motion Catalogue (`Pokorny et al. 2004 <http://adsabs.harvard.edu/abs/2004A&A...421..763P>`_), Vizier id J/A+A/421/763
            * 'SIPS' (or set ``SIPS``=True): the Southern Infrared Proper Motion Survey (`Deacon et al 2005 <http://adsabs.harvard.edu/abs/2005A&A...435..363D>`_), Vizier id J/A+A/435/363
            * 'UCAC4' (or set ``UCAC4``=True): the UCAC4 Catalogue (`Zacharias et al. 2012 <http://adsabs.harvard.edu/abs/2012yCat.1322....0Z>`_), Vizier id I/322A
            * 'USNOB' (or set ``USNO``=True): the USNO-B1.0 Catalog (`Monet et al. 2003 <http://adsabs.harvard.edu/abs/2003AJ....125..984M>`_), Vizier id I/284
            * 'LSPM' (or set ``LSPM``=True): the LSPM-North Catalog (`Lepine et al. 2005 <http://adsabs.harvard.edu/abs/2005AJ....129.1483L>`_), Vizier id I/298
            * 'GAIA' (or set ``GAIA``=True): the GAIA DR1 Catalog (`Gaia Collaboration et al. 2016 <http://adsabs.harvard.edu/abs/2016yCat.1337....0G>`_), Vizier id I/337
        :param: sort: String specifying the parameter to sort the returned SIMBAD table by; by default this is the offset from the input coordinate (default = 'sep')
        :param: nearest: Set to True to return on the single nearest source to coordinate (default = False)
        :param: verbose: Give feedback (default = False)

    Output:
        An astropy Table instance that contains data from the Vizier query, or a blank Table if no sources are found

    Example:

    >>> import splat
    >>> from astropy import units as u
    >>> c = spl.properCoordinates('J053625-064302')
    >>> v = spl.querySimbad(c,catalog='SDSS',radius=15.*u.arcsec)
    >>> print(v)
      _r    _RAJ2000   _DEJ2000  mode q_mode  cl ... r_E_ g_J_ r_F_ i_N_  sep  
     arcs     deg        deg                     ... mag  mag  mag  mag   arcs 
    ------ ---------- ---------- ---- ------ --- ... ---- ---- ---- ---- ------
     7.860  84.105967  -6.715966    1          3 ...   --   --   --   --  7.860
    14.088  84.108113  -6.717206    1          6 ...   --   --   --   -- 14.088
    14.283  84.102528  -6.720843    1      +   6 ...   --   --   --   -- 14.283
    16.784  84.099524  -6.717878    1          3 ...   --   --   --   -- 16.784
    22.309  84.097988  -6.718049    1      +   6 ...   --   --   --   -- 22.309
    23.843  84.100079  -6.711999    1      +   6 ...   --   --   --   -- 23.843
    27.022  84.107504  -6.723965    1      +   3 ...   --   --   --   -- 27.022

    '''

# check if online
    if not checkOnline():
        print('\nYou are currently not online; cannot do a Vizier query')
        return Table()

# parameters
    radius = kwargs.get('radius',30.*u.arcsec)
    if not isinstance(radius,u.quantity.Quantity):
        radius*=u.arcsec
    verbose = kwargs.get('verbose',False)

# sort out what catalog to query
    catalog = kwargs.get('catalog','2MASS')
    if kwargs.get('2MASS',False) or kwargs.get('2mass',False) or catalog == '2MASS' or catalog == '2mass':
        catalog = u'II/246'
    if kwargs.get('SDSS',False) or kwargs.get('sdss',False) or catalog == 'SDSS' or catalog == 'sdss':
        catalog = u'V/139'
    if kwargs.get('WISE',False) or kwargs.get('wise',False) or catalog == 'WISE' or catalog == 'wise':
        catalog = u'II/311'
    if kwargs.get('ALLWISE',False) or kwargs.get('allwise',False) or catalog == 'ALLWISE' or catalog == 'allwise':
        catalog = u'II/328'
    if kwargs.get('VISTA',False) or kwargs.get('vista',False) or catalog == 'VISTA' or catalog == 'vista':
        catalog = u'II/329'
    if kwargs.get('CFHT',False) or kwargs.get('cfht',False) or kwargs.get('CFHTLAS',False) or kwargs.get('cfhtlas',False) or catalog == 'CFHT' or catalog == 'cfht':
        catalog = u'II/317'
    if kwargs.get('DENIS',False) or kwargs.get('denis',False) or catalog == 'DENIS' or catalog == 'denis':
        catalog = u'B/denis'
    if kwargs.get('UKIDSS',False) or kwargs.get('ukidss',False) or catalog == 'UKIDSS' or catalog == 'ukidss':
        catalog = u'II/314'
    if kwargs.get('LEHPM',False) or kwargs.get('lehpm',False) or catalog == 'LEHPM' or catalog == 'lehpm':
        catalog = u'J/A+A/421/763'
    if kwargs.get('SIPS',False) or kwargs.get('sips',False) or catalog == 'SIPS' or catalog == 'sips':
        catalog = u'J/A+A/435/363'
    if kwargs.get('UCAC',False) or kwargs.get('ucac',False) or kwargs.get('UCAC4',False) or kwargs.get('ucac4',False) or catalog == 'UCAC' or catalog == 'ucac':
        catalog = u'I/322A'
    if kwargs.get('USNO',False) or kwargs.get('usno',False) or kwargs.get('USNOB',False) or kwargs.get('usnob',False) or kwargs.get('USNOB1.0',False) or kwargs.get('usnob1.0',False) or catalog == 'USNO' or catalog == 'usno':
        catalog = u'I/284'
    if kwargs.get('LSPM',False) or kwargs.get('lspm',False) or kwargs.get('LSPM-NORTH',False) or kwargs.get('lspm-north',False) or kwargs.get('LSPM-N',False) or kwargs.get('lspm-n',False) or catalog == 'LSPM' or catalog == 'lspm':
        catalog = u'I/298'
    if kwargs.get('GAIA',False) or kwargs.get('gaia',False) or kwargs.get('GAIA-DR1',False):
        catalog = u'I/337'

# convert coordinate if necessary
    if not isinstance(coordinate,SkyCoord):
        try:
            c = spl.properCoordinates(coordinate)
        except:
            print('\n{} is not a proper coordinate'.format(coordinate))
            return numpy.nan
    else:
        c = copy.deepcopy(coordinate)

# search Vizier, sort by separation        
    v = Vizier(columns=["*", "+_r"], catalog=catalog)
    t_vizier = v.query_region(c,radius=radius)
    if len(t_vizier) > 0:
        tv=t_vizier[0]
    else:
        tv = t_vizier

# sorting
    if len(tv) > 1:
        tv['sep'] = tv['_r']
        sortparam = kwargs.get('sort','sep')
        if sortparam in list(tv.keys()):
            tv.sort(sortparam)
        else:
            if verbose:
                print('\nCannot find sorting keyword {}; try using {}\n'.format(sort,list(tv.keys())))

# return only nearest
    if kwargs.get('nearest',False) == True:
        while len(tv) > 1:
            tv.remove_row(1)

    return tv



def querySimbad(variable,**kwargs):
    '''
    Purpose
        Queries Simbad using astroquery to grab information about a source

    Required Inputs:
        :param: variable: Either an astropy SkyCoord object containing position of a source, a variable that can be converted into a SkyCoord using `spl.properCoordinates()`_, or a string name for a source.

    .. _`spl.properCoordinates()` : api.html#spl.properCoordinates
        
    Optional Inputs:
        :param: radius: Search radius, nominally in arcseconds although can be set by assigning and astropy.unit value (default = 30 arcseconds)
        :param: sort: String specifying the parameter to sort the returned SIMBAD table by; by default this is the offset from the input coordinate (default = 'sep')
        :param: reject_type: Set to string or list of strings to filter out object types not desired. Useful for crowded fields (default = None)
        :param: nearest: Set to True to return on the single nearest source to coordinate (default = False)
        :param: iscoordinate: Specifies that input is a coordinate of some kind (default = False)
        :param: isname: Specifies that input is a name of some kind (default = False)
        :param: clean: Set to True to clean the SIMBAD output and reassign to a predefined set of parameters (default = True)
        :param: verbose: Give lots of feedback (default = False)

    Output:
        An astropy Table instance that contains data from the SIMBAD search, or a blank Table if no sources found

    Example:

    >>> import splat
    >>> from astropy import units as u
    >>> c = spl.properCoordinates('J053625-064302')
    >>> q = spl.querySimbad(c,radius=15.*u.arcsec,reject_type='**')
    >>> print(q)
              NAME          OBJECT_TYPE     OFFSET    ... K_2MASS K_2MASS_E
    ----------------------- ----------- ------------- ... ------- ---------
               BD-06  1253B        Star  4.8443894429 ...                  
                [SST2010] 3        Star 5.74624887682 ...   18.36       0.1
                BD-06  1253         Ae* 7.74205447776 ...   5.947     0.024
               BD-06  1253A          ** 7.75783861347 ...                  
    2MASS J05362590-0643020     brownD* 13.4818185612 ...  12.772     0.026
    2MASS J05362577-0642541        Star  13.983717577 ...                  

    '''

# check that online
    if not checkOnline():
        print('\nYou are currently not online; cannot do a SIMBAD query')
        return Table()

# parameters 
    radius = kwargs.get('radius',30.*u.arcsec)
    if not isinstance(radius,u.quantity.Quantity):
        radius*=u.arcsec
    verbose = kwargs.get('verbose',False)
    coordFlag = kwargs.get('iscoordinate',False)
    nameFlag = kwargs.get('isname',False)

# check if this is a coordinate query
    if isinstance(variable,SkyCoord):
        c = copy.deepcopy(variable)
        coordFlag = True
    elif not nameFlag:
        try:
            c = spl.properCoordinates(variable)
            coordFlag = True
# this is probably a name
        except:
            nameFlag = True
    else:
        if isinstance(variable,unicode):
            c = variable.decode()
        else:
            c = str(variable)

# prep Simbad search
    sb = Simbad()
    votfields = ['otype','parallax','sptype','propermotions','rot','rvz_radvel','rvz_error',\
    'rvz_bibcode','fluxdata(B)','fluxdata(V)','fluxdata(R)','fluxdata(I)','fluxdata(g)','fluxdata(r)',\
    'fluxdata(i)','fluxdata(z)','fluxdata(J)','fluxdata(H)','fluxdata(K)']
    for v in votfields:
        sb.add_votable_fields(v)

# search SIMBAD by coordinate
    if coordFlag:
        t_sim = sb.query_region(c,radius=radius)
        if not isinstance(t_sim,Table):
            if verbose:
                print('\nNo sources found; returning empty Table\n')
            return Table()

# if more than one source, sort the results by separation
        sep = [c.separation(SkyCoord(str(t_sim['RA'][lp]),str(t_sim['DEC'][lp]),unit=(u.hourangle,u.degree))).arcsecond for lp in numpy.arange(len(t_sim))]
        t_sim['sep'] = sep

# search SIMBAD by name
    elif nameFlag:
        t_sim = sb.query_object(c,radius=radius)
        t_sim['sep'] = numpy.zeros(len(t_sim['RA']))

    else:
        raise ValueError('problem!')

# sort results by separation by default
    if kwargs.get('sort','sep') in list(t_sim.keys()):
        t_sim.sort(kwargs.get('sort','sep'))
    else:
        if verbose:
            print('\nCannot sort by {}; try keywords {}\n'.format(kwargs.get('sort','sep'),list(t_sim.keys())))


# reject object types not wanted
    if kwargs.get('reject_type',False) != False:
        rej = kwargs['reject_type']
        if not isinstance(rej,list):
            rej = [rej]
        for r in rej:
            w = numpy.array([str(r) not in str(o) for o in t_sim['OTYPE']])
            if len(w) > 0:
                t_sim = t_sim[w]

# trim to single source if nearest flag is set
    if coordFlag and kwargs.get('nearest',False):
        while len(t_sim)>1:
            t_sim.remove_row(1) 

# clean up the columns    
    if kwargs.get('clean',True) == True and len(t_sim) > 0:
        t_src = Table()
        if not isinstance(t_sim['MAIN_ID'][0],str):
            t_src['NAME'] = [x.decode().replace('  ',' ') for x in t_sim['MAIN_ID']]
        else: 
            t_src['NAME'] = t_sim['MAIN_ID']
        if not isinstance(t_sim['OTYPE'][0],str):
            t_src['OBJECT_TYPE'] = [x.decode().replace('  ',' ') for x in t_sim['OTYPE']]
        else:
            t_src['OBJECT_TYPE'] = t_sim['OTYPE']
        t_src['OFFSET'] = t_sim['sep']
        if not isinstance(t_sim['SP_TYPE'][0],str):
            t_src['LIT_SPT'] = [x.decode().replace(' ','') for x in t_sim['SP_TYPE']]
        else:
            t_src['LIT_SPT'] = t_sim['SP_TYPE']
        if not isinstance(t_sim['SP_BIBCODE'][0],str):
            t_src['LIT_SPT_REF'] = [x.decode() for x in t_sim['SP_BIBCODE']]
        else: 
            t_src['LIT_SPT_REF'] = t_sim['SP_BIBCODE']
        t_src['DESIGNATION'] = ['J{}{}'.format(t_sim['RA'][i],t_sim['DEC'][i]).replace(' ','').replace('.','') for i in range(len(t_sim))] 
        t_src['RA'] = numpy.zeros(len(t_sim))
        t_src['DEC'] = numpy.zeros(len(t_sim))
        for i in range(len(t_sim)):
            c2 = spl.properCoordinates(t_src['DESIGNATION'][i])
            t_src['RA'][i] = c2.ra.value
            t_src['DEC'][i] = c2.dec.value
        t_src['PARALLAX'] = [str(p).replace('--','') for p in t_sim['PLX_VALUE']]
        t_src['PARALLAX_E'] = [str(p).replace('--','') for p in t_sim['PLX_ERROR']]
        if not isinstance(t_sim['PLX_BIBCODE'][0],str):
            t_src['PARALLEX_REF'] = [x.decode() for x in t_sim['PLX_BIBCODE']]
        else:
            t_src['PARALLEX_REF'] = t_sim['PLX_BIBCODE']
        t_src['MU_RA'] = [str(p).replace('--','') for p in t_sim['PMRA']]
        t_src['MU_DEC'] = [str(p).replace('--','') for p in t_sim['PMDEC']]
        t_src['MU'] = numpy.zeros(len(t_sim))
        for i in range(len(t_sim)):
            if t_src['MU_RA'][i] != '':
                t_src['MU'][i] = (float(t_src['MU_RA'][i])**2+float(t_src['MU_DEC'][i])**2)**0.5
        t_src['MU_E'] = [str(p).replace('--','') for p in t_sim['PM_ERR_MAJA']]
        if not isinstance(t_sim['PM_BIBCODE'][0],str):
            t_src['MU_REF'] = [x.decode() for x in t_sim['PM_BIBCODE']]
        else:
            t_src['MU_REF'] = t_sim['PM_BIBCODE']
        t_src['RV'] = [str(p).replace('--','') for p in t_sim['RVZ_RADVEL']]
        t_src['RV_E'] = [str(p).replace('--','') for p in t_sim['RVZ_ERROR']]
        if not isinstance(t_sim['RVZ_BIBCODE'][0],str):
            t_src['RV_REF'] = [x.decode() for x in t_sim['RVZ_BIBCODE']]
        else:
            t_src['RV_REF'] = t_sim['RVZ_BIBCODE']
        t_src['VSINI'] = [str(p).replace('--','') for p in t_sim['ROT_Vsini']]
        t_src['VSINI_E'] = [str(p).replace('--','') for p in t_sim['ROT_err']]
        if not isinstance(t_sim['ROT_bibcode'][0],str):
            t_src['VSINI_REF'] = [x.decode() for x in t_sim['ROT_bibcode']]
        else:
            t_src['VSINI_REF'] = t_sim['ROT_bibcode']
        t_src['J_2MASS'] = [str(p).replace('--','') for p in t_sim['FLUX_J']]
        t_src['J_2MASS_E'] = [str(p).replace('--','') for p in t_sim['FLUX_ERROR_J']]
        t_src['H_2MASS'] = [str(p).replace('--','') for p in t_sim['FLUX_H']]
        t_src['H_2MASS_E'] = [str(p).replace('--','') for p in t_sim['FLUX_ERROR_H']]
        t_src['K_2MASS'] = [str(p).replace('--','') for p in t_sim['FLUX_K']]
        t_src['K_2MASS_E'] = [str(p).replace('--','') for p in t_sim['FLUX_ERROR_K']]
    else:
        t_src = t_sim.copy()

    return t_src



def _querySimbad2(t_src,**kwargs):
    '''
    Purpose
        Internal function that queries Simbad and populates data for source table.

    :Note:
        **this program is in beta testing; bugs/errors are likely**

    :Required parameters:
        :param table: an astropy Table object, requires the presence of DESIGNATION column

    :Optional parameters:
        :param simbad_radius = 30 arcseconds: circular radius to search for sources (note: must be an angular quantity)
        :param export = '': filename to which to export resulting table to; if equal to a null string then no expoer is made. Note that a populated table is returned in either case
        :param closest = False: return only the closest source to given coordinate
    '''    
# parameters 
    simbad_radius = kwargs.get('simbad_radius',30.*u.arcsec)
    verbose = kwargs.get('verbose',True)
# checks
    if 'DESIGNATION' not in t_src.keys():
        raise NameError('\nDESIGNATION column is required for input table to querySimbad\n')
    if 'SIMBAD_SEP' not in t_src.keys():
        t_src['SIMBAD_SEP'] = Column(numpy.zeros(len(t_src)),dtype='float')
# must be online
    if not checkOnline():
        print('\nYou are currently not online so cannot query Simbad\n')
        return t_src

# if necessary, populate columns that are expected for source database
    for c in DB_SOURCES.keys():
        if c not in t_src.keys():
            t_src[c] = Column([' '*50 for des in t_src['DESIGNATION']],dtype='str')

# prep Simbad search
    sb = Simbad()
    votfields = ['otype','parallax','sptype','propermotions','rot','rvz_radvel','rvz_error',\
    'rvz_bibcode','fluxdata(B)','fluxdata(V)','fluxdata(R)','fluxdata(I)','fluxdata(g)','fluxdata(r)',\
    'fluxdata(i)','fluxdata(z)','fluxdata(J)','fluxdata(H)','fluxdata(K)']
    for v in votfields:
        sb.add_votable_fields(v)

# search by source
    for i,des in enumerate(t_src['DESIGNATION']):
        print(i,des)
        c = spl.designationToCoordinate(des)
        try:
            t_sim = sb.query_region(c,radius=simbad_radius)
        except:
            t_sim = None
# source found in query
        if isinstance(t_sim,Table):
# many sources found
#            if len(t_sim) >= 1:      # take the closest position
            if verbose:
                print('\nSource {} Designation = {} {} match(es)'.format(i+1,des,len(t_sim)))
                print(t_sim)

            sep = [c.separation(SkyCoord(str(t_sim['RA'][lp]),str(t_sim['DEC'][lp]),unit=(u.hourangle,u.degree))).arcsecond for lp in numpy.arange(len(t_sim))]
            t_sim['sep'] = sep
            t_sim.sort('sep')
            if len(t_sim) > 1:
                while len(t_sim)>1:
                    t_sim.remove_row(1) 
# one source found
#            else:
#                t_sim['sep'] = [c.separation(SkyCoord(str(t_sim['RA'][0]),str(t_sim['DEC'][0]),unit=(u.hourangle,u.degree))).arcsecond]

# fill in information
            t_src['SIMBAD_NAME'][i] = t_sim['MAIN_ID'][0]
            t_src['NAME'][i] = t_src['SIMBAD_NAME'][i]
            t_src['SIMBAD_OTYPE'][i] = t_sim['OTYPE'][0]
            if not isinstance(t_sim['SP_TYPE'][0],str):
                t_sim['SP_TYPE'][0] = t_sim['SP_TYPE'][0].decode()
            spt = t_sim['SP_TYPE'][0]
            spt.replace(' ','').replace('--','')
            t_src['SIMBAD_SPT'][i] = spt
            t_src['SIMBAD_SPT_REF'][i] = t_sim['SP_BIBCODE'][0]
            t_src['SIMBAD_SEP'][i] = t_sim['sep'][0]
            if spt != '':
                t_src['LIT_TYPE'][i] = t_src['SIMBAD_SPT'][i]
                t_src['LIT_TYPE_REF'][i] = t_src['SIMBAD_SPT_REF'][i]
            t_src['DESIGNATION'][i] = 'J{}{}'.format(t_sim['RA'][0],t_sim['DEC'][0]).replace(' ','').replace('.','')
            coord = spl.properCoordinates(t_src['DESIGNATION'][i])
            t_src['RA'][i] = coord.ra.value
            t_src['DEC'][i] = coord.dec.value
            t_src['OBJECT_TYPE'][i] = 'VLM'
            if 'I' in t_sim['SP_TYPE'][0] and 'V' not in t_sim['SP_TYPE'][0]:
                t_src['LUMINOSITY_CLASS'][i] = 'I{}'.format(t_sim['SP_TYPE'][0].split('I',1)[1])
                t_src['OBJECT_TYPE'][i] = 'GIANT'
            if 'VI' in t_sim['SP_TYPE'][0] or 'sd' in t_sim['SP_TYPE'][0]:
                t_src['METALLICITY_CLASS'][i] = '{}sd'.format(t_sim['SP_TYPE'][0].split('sd',1)[0])
            t_src['PARALLAX'][i] = str(t_sim['PLX_VALUE'][0]).replace('--','')
            t_src['PARALLAX_E'][i] = str(t_sim['PLX_ERROR'][0]).replace('--','')
            if isinstance(t_sim['PLX_BIBCODE'][0],str):
                t_src['PARALLEX_REF'][i] = str(t_sim['PLX_BIBCODE'][0]).replace('--','')
            else:
                t_src['PARALLEX_REF'][i] = t_sim['PLX_BIBCODE'][0].decode()
            t_src['MU_RA'][i] = str(t_sim['PMRA'][0]).replace('--','')
            t_src['MU_DEC'][i] = str(t_sim['PMDEC'][0]).replace('--','')
#                try:            # this is in case MU is not present
            t_src['MU'][i] = (float('{}0'.format(t_src['MU_RA'][i]))**2+float('{}0'.format(t_src['MU_DEC'][i]))**2)**0.5
            t_src['MU_E'][i] = str(t_sim['PM_ERR_MAJA'][0]).replace('--','')
#                except:
#                    pass
            t_src['MU_REF'][i] = t_sim['PM_BIBCODE'][0]
            t_src['RV'][i] = str(t_sim['RVZ_RADVEL'][0]).replace('--','')
            t_src['RV_E'][i] = str(t_sim['RVZ_ERROR'][0]).replace('--','')
            t_src['RV_REF'][i] = t_sim['RVZ_BIBCODE'][0]
            t_src['VSINI'][i] = str(t_sim['ROT_Vsini'][0]).replace('--','')
            t_src['VSINI_E'][i] = str(t_sim['ROT_err'][0]).replace('--','')
            t_src['VSINI_REF'][i] = t_sim['ROT_bibcode'][0]
            if isinstance(t_sim['FLUX_J'][0],str):
                t_src['J_2MASS'][i] = t_sim['FLUX_J'][0].replace('--','')
            else:
                t_src['J_2MASS'][i] = t_sim['FLUX_J'][0]
            if isinstance(t_sim['FLUX_ERROR_J'][0],str):
                t_src['J_2MASS_E'][i] = t_sim['FLUX_ERROR_J'][0].replace('--','')
            else:
                t_src['J_2MASS_E'][i] = t_sim['FLUX_ERROR_J'][0]
            if isinstance(t_sim['FLUX_H'][0],str):
                t_src['H_2MASS'][i] = t_sim['FLUX_H'][0].replace('--','')
            else:
                t_src['H_2MASS'][i] = t_sim['FLUX_H'][0]
            if isinstance(t_sim['FLUX_ERROR_H'][0],str):
                t_src['H_2MASS_E'][i] = t_sim['FLUX_ERROR_H'][0].replace('--','')
            else:
                t_src['H_2MASS_E'][i] = t_sim['FLUX_ERROR_H'][0]
            if isinstance(t_sim['FLUX_K'][0],str):
                t_src['KS_2MASS'][i] = t_sim['FLUX_K'][0].replace('--','')
            else:
                t_src['KS_2MASS'][i] = t_sim['FLUX_K'][0]
            if isinstance(t_sim['FLUX_ERROR_K'][0],str):
                t_src['KS_2MASS_E'][i] = t_sim['FLUX_ERROR_K'][0].replace('--','')
            else:
                t_src['KS_2MASS_E'][i] = t_sim['FLUX_ERROR_K'][0]

    return



#####################################################
###########   ADDING SPECTRA TO LIBRARY   ###########
#####################################################



def importSpectra(*args,**kwargs):
    '''
    Purpose
        imports a set of spectra into the SPLAT library; requires manager access.

    :Note:
        **this program is in beta testing; bugs/errors are likely**

    :Optional parameters:
        :param data_folder = "./": Full path to folder containing data; by default this is the current directory
        :param review_folder = "./review/": Full path to folder in which review materials will be kept; by default a new folder ``review`` will be created inside the data_folder
        :param spreadsheet = "": Filename for a spreadsheet (ascii, tab- or comma-delimited) listing the input spectra, one per row. At least one column must be named ``filename`` or ``file`` that contains the name of the data file; the following columns are also recommended:

            * ``designation``: source desigation; e.g., ``J15420830-2621138`` (strongly recommended)
            * ``ra`` and ``dec``: Right Ascension and declination in decimal format (only needed if no designation column provided)
            * ``name``: source name, designation will be used if not provided
            * ``type``, ``opt_type``, ``nir_type``: spectral type of source (string); ``type`` will default to ``lit_type``
            * ``date`` or ``observation_date``: date of observation in format YYYYMMDD
            * ``slit``: slit width used (for computing resolution)
            * ``airmass``: airmass of observation
            * ``observer``: last name of primary observer
            * ``data_reference``: bibcode of data reference

    :Output:
        - Source DB update file: spreadsheet containing update to source_data.txt, saved in review folder as source_data.txt
        - Spectral DB update file: spreadsheet containing update to spectral_data.txt, saved locally as UPDATE_spectral_data.txt
        - Photometry DB update file: spreadsheet containing update to photometry_data.txt, saved locally as UPDATE_photometry_data.txt

    '''
# check user access
    if checkAccess() == False:
        print('\nSpectra may only be imported into library by designated manager or while online; please email {}'.format(SPLAT_EMAIL))
        return

# check online
#    if spl.checkOnline() == False:
#        print('\nWarning! You are not currently online so you will not be able to retrieve SIMBAD and Vizier data\n')

# set up optional inputs
    simbad_radius = kwargs.get('simbad_radius',60.*u.arcsec)
    if isinstance(simbad_radius,u.quantity.Quantity) == False:
        simbad_radius*=u.arcsec

    vizier_radius = kwargs.get('vizier_radius',30.*u.arcsec)
    if isinstance(vizier_radius,u.quantity.Quantity) == False:
        vizier_radius*=u.arcsec

    data_folder = kwargs.get('data_folder','./')
    data_folder = kwargs.get('dfolder',data_folder)
    data_folder = kwargs.get('folder',data_folder)
    if data_folder[-1] != '/':
        data_folder+='/'
    review_folder = kwargs.get('review_folder','{}/review/'.format(data_folder))
    review_folder = kwargs.get('rfolder',review_folder)
    if review_folder[-1] != '/':
        review_folder+='/'
    spreadsheet = kwargs.get('spreadsheet','')
    spreadsheet = kwargs.get('sheet',spreadsheet)
    spreadsheet = kwargs.get('entry',spreadsheet)
    instrument = kwargs.get('instrument','uSpeX prism')
    verbose = kwargs.get('verbose',True)

# make sure relevant files and folders are in place
    if not os.path.exists(review_folder):
        try:
            os.makedirs(review_folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
#        raise NameError('\nCannot find review folder {}'.format(review_folder))
    if not os.path.exists(data_folder):
        raise NameError('\nCannot find data folder {}'.format(data_folder))
    if not os.path.exists('{}/published'.format(review_folder)):
        try:
            os.makedirs('{}/published'.format(review_folder))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    if not os.path.exists('{}/unpublished'.format(review_folder)):
        try:
            os.makedirs('{}/unpublished'.format(review_folder))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

# if spreadsheet is given, use this to generate list of files
    if spreadsheet != '':
        try:
            t_input = fetchDatabase(spreadsheet)        
        except:
            try:
                t_input = fetchDatabase(data_folder+spreadsheet)        
            except:
                raise NameError('\nCould not find spreadsheet {} in local or data directories\n'.format(spreadsheet))
        tkeys = list(t_input.keys())
        if 'FILENAME' in tkeys:
            files = t_input['FILENAME']
        elif 'FILE' in tkeys:
            files = t_input['FILE']
        elif 'FILES' in tkeys:
            files = t_input['FILES']
        else:
            raise NameError('\nSpreadsheet {} does not have a column named filename; aborting\n'.format(spreadsheet))
        if data_folder not in files[0]:
            files = [data_folder+f for f in files]

# otherwise search for *.fits and *.txt files in data folder
    else:
        files = glob.glob(data_folder+'*.fits')+glob.glob(data_folder+'*.txt')
        if len(files) == 0:
            raise NameError('\nNo spectral files in {}\n'.format(data_folder))

# prep tables containing information
    t_spec = Table()
    for c in DB_SPECTRA.keys():
        t_spec[c] = Column([' '*200 for f in files],dtype='str')
    t_src = Table()
    for c in DB_SOURCES.keys():
        t_src[c] = Column([' '*200 for f in files],dtype='str')
    source_id0 = numpy.max(DB_SOURCES['SOURCE_KEY'])
    spectrum_id0 = numpy.max(DB_SPECTRA['DATA_KEY'])

# read in files into Spectrum objects
    if verbose:
        print('\nReading in {} files from {}'.format(len(files),data_folder))
#    splist = []
    t_spec['DATA_FILE'] = Column(files,dtype='str')
    t_spec['SPECTRUM'] = [spl.Spectrum(filename=f) for f in files]
    t_spec['INSTRUMENT'] = [instrument for f in files]
#    for f in files:
#        splist.append()

# populate spec array
    if verbose:
        print('\nGenerating initial input tables')
    t_spec['SOURCE_KEY'] = Column(numpy.arange(len(files))+source_id0+1,dtype='int')
    t_spec['DATA_KEY'] = Column(numpy.arange(len(files))+spectrum_id0+1,dtype='int')
#    t_spec['SPECTRUM'] = [sp for sp in splist]
    t_spec['QUALITY_FLAG'] = Column(['OK' for f in t_spec['DATA_FILE']],dtype='str')
    t_spec['PUBLISHED'] = Column(['N' for f in t_spec['DATA_FILE']],dtype='str')
#  measurements
    t_spec['MEDIAN_SNR'] = Column([sp.computeSN() for sp in t_spec['SPECTRUM']],dtype='float')
    t_spec['SPEX_TYPE'] = Column([spl.classifyByStandard(sp,string=True,method='kirkpatrick')[0] for sp in t_spec['SPECTRUM']],dtype='str')
    t_spec['SPEX_GRAVITY_CLASSIFICATION'] = Column([spl.classifyGravity(sp,string=True) for sp in t_spec['SPECTRUM']],dtype='str')
# populate spectral data table from fits file header
    for i,sp in enumerate(t_spec['SPECTRUM']):
        if 'DATE_OBS' in sp.header:
            t_spec['OBSERVATION_DATE'][i] = sp.header['DATE_OBS'].replace('-','')
            t_spec['JULIAN_DATE'][i] = Time(sp.header['DATE_OBS']).mjd
        if 'DATE' in sp.header:
            t_spec['OBSERVATION_DATE'][i] = sp.header['DATE'].replace('-','')
            t_spec['JULIAN_DATE'][i] = Time(sp.header['DATE']).mjd
        if 'TIME_OBS' in sp.header:
            t_spec['OBSERVATION_TIME'][i] = sp.header['TIME_OBS'].replace(':',' ')
        if 'MJD_OBS' in sp.header:
            t_spec['JULIAN_DATE'][i] = sp.header['MJD_OBS']
        if 'OBSERVER' in sp.header:
            t_spec['OBSERVER'][i] = sp.header['OBSERVER']
        if 'RESOLUTION' in sp.header:
            t_spec['RESOLUTION'][i] = sp.header['RESOLUTION']
        elif 'RES' in sp.header:
            t_spec['RESOLUTION'][i] = sp.header['RES']
        elif 'SLITW' in sp.header:
            t_spec['RESOLUTION'][i] = 200.*0.3/sp.header['SLITW']       # this is for new spex
        if 'AIRMASS' in sp.header:
            t_spec['AIRMASS'][i] = sp.header['AIRMASS']
        if 'VERSION' in sp.header:
            v = sp.header['VERSION']
            t_spec['REDUCTION_SPEXTOOL_VERSION'][i] = 'v{}'.format(v.split('v')[-1])
# populate spectral data table from spreadsheet 
    if spreadsheet != '':
#        if 'FILENAME' in tkeys:
#            t_spec['DATA_FILE'] = t_input['FILENAME']
        if 'DATE' in tkeys:
            t_spec['OBSERVATION_DATE'] = [spl.properDate(str(a),output='YYYYMMDD') for a in t_input['DATE']]
#            for a in t_input['DATE']:
#                print(a,spl.properDate(str(a)),Time(spl.properDate(str(a),output='YYYY-MM-DD')),Time(spl.properDate(str(a),output='YYYY-MM-DD')).mjd)
            t_spec['JULIAN_DATE'] = [Time(spl.properDate(str(a),output='YYYY-MM-DD')).mjd for a in t_input['DATE']]
        if 'RESOLUTION' in tkeys:
            t_spec['RESOLUTION'] = [r for r in t_input['RESOLUTION']]
        if 'SLIT' in tkeys:
            t_spec['RESOLUTION'] = [150.*0.5/float(s) for s in t_input['SLIT']]
        if 'AIRMASS' in tkeys:
            t_spec['AIRMASS'] = t_input['AIRMASS']
        if 'OBSERVER' in tkeys:
            t_spec['OBSERVER'] = t_input['OBSERVER']
        if 'DATA_REFERENCE' in tkeys:
            t_spec['DATA_REFERENCE'] = t_input['DATA_REFERENCE']
            for i,ref in enumerate(t_spec['DATA_REFERENCE']):
                if ref != '':
                    t_spec['PUBLISHED'][i] = 'Y'

#    for c in splist[0].header.keys():
#        if c != 'HISTORY':
#            print('{} {}'.format(c,splist[0].header[c]))

    t_src['SOURCE_KEY'] = t_spec['SOURCE_KEY']
    t_src['GRAVITY_CLASS_NIR'] = t_spec['SPEX_GRAVITY_CLASSIFICATION']
    t_src['GRAVITY_CLASS_NIR_REF'] = Column(['SPL' for sp in t_spec['SPECTRUM']],dtype='str')
    t_spec['COMPARISON_SPECTRUM'] = [SPEX_STDS[spt] for spt in t_spec['SPEX_TYPE']]
    t_spec['COMPARISON_TEXT'] = [' '*200 for spt in t_spec['SPEX_TYPE']]
    for i,spt in enumerate(t_spec['SPEX_TYPE']):
        t_spec['COMPARISON_TEXT'][i] = '{} standard'.format(spt)

# determine coordinates as best as possible
    for i,sp in enumerate(t_spec['SPECTRUM']):
#        if i == 0:
#            for k in list(sp.header.keys()):
#                print(k,sp.header[k])
        if 'TCS_RA' in sp.header.keys() and 'TCS_DEC' in sp.header.keys():
            sp.header['RA'] = sp.header['TCS_RA']
            sp.header['DEC'] = sp.header['TCS_DEC']
            sp.header['RA'] = sp.header['RA'].replace('+','')
        if t_src['DESIGNATION'][i].strip() == '' and sp.header['RA'] != '' and sp.header['DEC'] != '':
            t_src['DESIGNATION'][i] = 'J{}+{}'.format(sp.header['RA'].replace('+',''),sp.header['DEC']).replace(':','').replace('.','').replace('+-','-').replace('++','+').replace('J+','J').replace(' ','')
#            print('DETERMINED DESIGNATION {} FROM RA/DEC'.format(t_src['DESIGNATION'][i]))
        if t_src['RA'][i].strip() == '' and t_src['DESIGNATION'][i].strip() != '':
            coord = spl.properCoordinates(t_src['DESIGNATION'][i])
            t_src['RA'][i] = coord.ra.value
            t_src['DEC'][i] = coord.dec.value
#            print('DETERMINED RA/DEC FROM DESIGNATION {}'.format(t_src['DESIGNATION'][i]))
#    print(t_src['DESIGNATION'],t_src['RA'],t_src['DEC'])
# populate source data table from spreadsheet
    if spreadsheet != '':
        if 'DESIGNATION' in tkeys:
            t_src['DESIGNATION'] = t_input['DESIGNATION']
            t_src['NAME'] = t_src['DESIGNATION']
#            coord = [spl.properCoordinates(s) for s in t_src['DESIGNATION']]
#            t_src['RA'] = [c.ra.value for c in coord]
#            t_src['DEC'] = [c.dec.value for c in coord]
        if 'NAME' in tkeys:
            t_src['NAME'] = t_input['NAME']
        if 'RA' in tkeys and 'DEC' in tkeys:
            if spl.isNumber(t_input['RA'][0]):
                t_src['RA'] = t_input['RA']
                t_src['DEC'] = t_input['DEC']
        if 'TYPE' in tkeys:
            t_src['LIT_TYPE'] = t_input['TYPE']
        if 'OPT_TYPE' in tkeys:
            t_src['OPT_TYPE'] = t_input['OPT_TYPE']
        if 'NIR_TYPE' in tkeys:
            t_src['NIR_TYPE'] = t_input['NIR_TYPE']

#    for c in DB_SOURCES.keys():
#        if c not in t_src.keys():
#            t_src[c] = Column([' '*50 for sp in splist],dtype='str')        # force string

# transfer spectral types
    for i,t in enumerate(t_src['NIR_TYPE']):
        if t.replace(' ','') == '':
            t_src['NIR_TYPE'][i] = t_spec['SPEX_TYPE'][i]
            t_src['NIR_TYPE_REF'][i] = 'SPL'
        if t_src['LIT_TYPE'][i].replace(' ','') == '':
            t_src['LIT_TYPE'][i] = t_spec['SPEX_TYPE'][i]
            t_src['LIT_TYPE_REF'][i] = 'SPL'


# now do a SIMBAD search for sources based on coordinates
    if kwargs.get('nosimbad',False) == False:
        if verbose:
            print('\nSIMBAD search')
        _querySimbad2(t_src,simbad_radius=simbad_radius)


# fill in missing 2MASS photometry with Vizier query
    if kwargs.get('novizier',False) == False:
        if verbose:
            print('\n2MASS photometry from Vizier')

        if not checkOnline():
            if verbose:
                print('\nCould not perform Vizier search, you are not online')
        else:
            for i,jmag in enumerate(t_src['J_2MASS']):
                if float('{}0'.format(jmag.replace('--',''))) == 0.0:
                    t_vizier = spl.getPhotometry(spl.properCoordinates(t_src['DESIGNATION'][i]),radius=vizier_radius,catalog='2MASS')

        # multiple sources; choose the closest
                    if len(t_vizier) > 0:
                        t_vizier.sort('_r')
        #                print(len(t_vizier),t_vizier.keys())
        #                while len(t_vizier)>1:
        #                    t_vizier.remove_row(1) 
                        if verbose:
                            print('\n{}'.format(t_src['DESIGNATION'][i]))
                            print(t_vizier)
                        t_src['DESIGNATION'][i] = 'J{}'.format(t_vizier['_2MASS'][0])
                        t_src['J_2MASS'][i] = str(t_vizier['Jmag'][0]).replace('--','')
                        t_src['J_2MASS_E'][i] = str(t_vizier['e_Jmag'][0]).replace('--','')
                        t_src['H_2MASS'][i] = str(t_vizier['Hmag'][0]).replace('--','')
                        t_src['H_2MASS_E'][i] = str(t_vizier['e_Hmag'][0]).replace('--','')
                        t_src['KS_2MASS'][i] = str(t_vizier['Kmag'][0]).replace('--','')
                        t_src['KS_2MASS_E'][i] = str(t_vizier['e_Kmag'][0]).replace('--','')

    # add in distance if spectral type and magnitude are known
    for i,spt in enumerate(t_src['LIT_TYPE']):
        if spt.replace(' ','') != '' and float('{}0'.format(str(t_src['J_2MASS'][i]).replace('--',''))) != 0.0:
    #            print(spt,t_src['J_2MASS'][i],t_src['J_2MASS_E'][i])
            dist = spl.estimateDistance(spt=spt,filter='2MASS J',mag=float(t_src['J_2MASS'][i]))
            if not numpy.isnan(dist[0]):
                t_src['DISTANCE_PHOT'][i] = dist[0]
                t_src['DISTANCE_PHOT_E'][i] = dist[1]
                t_src['DISTANCE'][i] = dist[0]
                t_src['DISTANCE_E'][i] = dist[1]
        if float('{}0'.format(str(t_src['PARALLAX'][i]).replace('--',''))) != 0.0 and float('{}0'.format(str(t_src['PARALLAX_E'][i]).replace('--',''))) != 0.0 :
            t_src['DISTANCE'][i] = 1000./float(t_src['PARALLAX'][i])
            t_src['DISTANCE_E'][i] = float(t_src['DISTANCE'][i])*float(t_src['PARALLAX_E'][i])/float(t_src['PARALLAX'][i])
    # compute vtan
        if float('{}0'.format(str(t_src['MU'][i]).replace('--',''))) != 0.0 and float('{}0'.format(str(t_src['DISTANCE'][i]).replace('--',''))) != 0.0:
            t_src['VTAN'][i] = 4.74*float(t_src['DISTANCE'][i])*float(t_src['MU'][i])/1000.

    # clear up zeros
        if float('{}0'.format(str(t_src['J_2MASS'][i]).replace('--',''))) == 0.0:
            t_src['J_2MASS'][i] = ''
            t_src['J_2MASS_E'][i] = ''
        if float('{}0'.format(str(t_src['H_2MASS'][i]).replace('--',''))) == 0.0:
            t_src['H_2MASS'][i] = ''
            t_src['H_2MASS_E'][i] = ''
        if float('{}0'.format(str(t_src['KS_2MASS'][i]).replace('--',''))) == 0.0:
            t_src['KS_2MASS'][i] = ''
            t_src['KS_2MASS_E'][i] = ''
        if float('{}0'.format(str(t_src['PARALLAX'][i]).replace('--',''))) == 0.0:
            t_src['PARALLAX'][i] = ''
            t_src['PARALLAX_E'][i] = ''
        if float('{}0'.format(str(t_src['MU'][i]).replace('--',''))) == 0.0:
            t_src['MU'][i] = ''
            t_src['MU_E'][i] = ''
            t_src['MU_RA'][i] = ''
            t_src['MU_DEC'][i] = ''
        if float('{}0'.format(str(t_src['RV'][i]).replace('--',''))) == 0.0:
            t_src['RV'][i] = ''
            t_src['RV_E'][i] = ''
        if float('{}0'.format(str(t_src['VSINI'][i]).replace('--',''))) == 0.0:
            t_src['VSINI'][i] = ''
            t_src['VSINI_E'][i] = ''
        if float('{}0'.format(str(t_src['SIMBAD_SEP'][i]).replace('--',''))) == 0.0:
            t_src['SIMBAD_SEP'][i] = ''
        if t_src['GRAVITY_CLASS_NIR'][i] == '':
            t_src['GRAVITY_CLASS_NIR_REF'][i] = ''

    # compute J-K excess and color extremity
        if spt.replace(' ','') != '' and float('{}0'.format(str(t_src['J_2MASS'][i]).replace('--',''))) != 0.0 and float('{}0'.format(str(t_src['KS_2MASS'][i]).replace('--',''))) != 0.0:
            t_src['JK_EXCESS'][i] = float(t_src['J_2MASS'][i])-float(t_src['KS_2MASS'][i])-spl.typeToColor(spt,'J-K')[0]
            if t_src['JK_EXCESS'][i] == numpy.nan or t_src['JK_EXCESS'][i] == '' or t_src['JK_EXCESS'][i] == 'nan':
                t_src['JK_EXCESS'][i] = ''
            elif float(t_src['JK_EXCESS'][i]) > 0.3:
                t_src['COLOR_EXTREMITY'][i] == 'RED'
            elif float(t_src['JK_EXCESS'][i]) < -0.3:
                t_src['COLOR_EXTREMITY'][i] == 'BLUE'
            else:
                pass


# check for previous entries
    t_src['SHORTNAME'] = [spl.designationToShortName(d) for d in t_src['DESIGNATION']]
    DB_SOURCES['SHORTNAME'] = [spl.designationToShortName(d) for d in DB_SOURCES['DESIGNATION']]
    for i,des in enumerate(t_src['DESIGNATION']):

# check if shortnames line up
        if t_src['SHORTNAME'][i] in DB_SOURCES['SHORTNAME']:
            for c in list(t_src.keys()):
                t_src[c][i] = DB_SOURCES[c][numpy.where(DB_SOURCES['SHORTNAME'] == t_src['SHORTNAME'][i])][0]
            t_spec['SOURCE_KEY'][i] = t_src['SOURCE_KEY'][i]

# check if SIMBAD names line up
        elif t_src['SIMBAD_NAME'][i] != '' and t_src['SIMBAD_NAME'][i] in DB_SOURCES['SIMBAD_NAME']:
            for c in t_src.keys():
                if t_src[c][i] == '':
                    t_src[c][i] = DB_SOURCES[c][numpy.where(DB_SOURCES['SIMBAD_NAME'] == t_src['SIMBAD_NAME'][i])][0]
            t_spec['SOURCE_KEY'][i] = t_src['SOURCE_KEY'][i]

        else:
            pass

# check to see if prior spectrum was taken on the same date (possible redundancy)
        matchlib = searchLibrary(idkey=t_src['SOURCE_KEY'][i],date=t_spec['OBSERVATION_DATE'][i])
# previous observation on this date found - retain in case this is a better spectrum
        if len(matchlib) > 0.:
            mkey = matchlib['DATA_KEY'][0]
            if verbose:
                print('Previous spectrum found in library for data key {}'.format(mkey))
            t_spec['COMPARISON_SPECTRUM'][i] = spl.Spectrum(int(mkey))
            t_spec['COMPARISON_TEXT'][i] = 'repeat spectrum: {}'.format(mkey)
            print(t_spec['COMPARISON_TEXT'][i])
# no previous observation on this date - retain the spectrum with the highest S/N
        else:
            matchlib = spl.searchLibrary(idkey=t_src['SOURCE_KEY'][i])
            if len(matchlib) > 0:
                matchlib.sort('MEDIAN_SNR')
                matchlib.reverse()
                t_spec['COMPARISON_SPECTRUM'][i] = spl.Spectrum(int(matchlib['DATA_KEY'][0]))
                t_spec['COMPARISON_TEXT'][i] = 'alternate spectrum: {} taken on {}'.format(matchlib['DATA_KEY'][0],matchlib['OBSERVATION_DATE'][0])
                print(matchlib['DATA_KEY'][0])
                print(t_spec['COMPARISON_TEXT'][i])


# generate check plots
    legend = []
    for i,sp in enumerate(t_spec['SPECTRUM']):
        legend.extend(['Data Key: {} Source Key: {}\n{}'.format(t_spec['DATA_KEY'][i],t_spec['SOURCE_KEY'][i],t_spec['SPECTRUM'][i].name),'{} {}'.format(t_spec['COMPARISON_SPECTRUM'][i].name,t_spec['COMPARISON_TEXT'][i])])
    for s in t_spec['COMPARISON_SPECTRUM']: print(s)
    spl.plotBatch([s for s in t_spec['SPECTRUM']],comparisons=[s for s in t_spec['COMPARISON_SPECTRUM']],normalize=True,output=review_folder+'/review_plots.pdf',legend=legend,noise=True,telluric=True)


# output database updates
    if 'SHORTNAME' in t_src.keys():
        t_src.remove_column('SHORTNAME')
    if 'SELECT' in t_src.keys():
        t_src.remove_column('SELECT')
    if 'SELECT' in t_spec.keys():
        t_spec.remove_column('SELECT')   
    if 'SOURCE_SELECT' in t_spec.keys():
        t_spec.remove_column('SOURCE_SELECT')
    if 'SPECTRUM' in t_spec.keys():
        t_spec.remove_column('SPECTRUM')
    if 'COMPARISON_SPECTRUM' in t_spec.keys():
        t_spec.remove_column('COMPARISON_SPECTRUM')
    if 'COMPARISON_TEXT' in t_spec.keys():
        t_spec.remove_column('COMPARISON_TEXT')
#    for i in numpy.arange(len(t_spec['NOTE'])):
#        t_spec['NOTE'][i] = compdict[str(t_spec['DATA_KEY'][i])]['comparison_type']
    t_src.write(review_folder+'/source_update.csv',format='ascii.csv')
    t_spec.write(review_folder+'/spectrum_update.csv',format='ascii.csv')

# open up windows to review spreadsheets
# NOTE: WOULD LIKE TO MAKE THIS AUTOMATICALLY OPEN FILE
#    app = QtGui.QApplication(sys.argv)
#    window = Window(10, 5)
#    window.resize(640, 480)
#    window.show()
#    app.exec_()

    print('\nSpectral plots and update speadsheets now available in {}'.format(review_folder))
    response = input('Please review and edit, and press any key when you are finished...\n')


# NEXT STEP - MOVE FILES TO APPROPRIATE PLACES, UPDATE MAIN DATABASES
# source db
    t_src = fetchDatabase(review_folder+'/source_update.csv',csv=True)
#    if 'SIMBAD_SEP' in t_src.keys():
#        t_src.remove_column('SIMBAD_SEP')

    for col in t_src.colnames:
        tmp = t_src[col].astype(DB_SOURCES[col].dtype)
        t_src.replace_column(col,tmp)
    t_merge = vstack([DB_SOURCES,t_src])
    t_merge.sort('SOURCE_KEY')
    if 'SHORTNAME' in t_merge.keys():
        t_merge.remove_column('SHORTNAME')
    if 'SELECT' in t_merge.keys():
        t_merge.remove_column('SELECT')
    t_merge.write(review_folder+DB_SOURCES_FILE,format='ascii.tab')

# spectrum db
    t_spec = fetchDatabase(review_folder+'spectrum_update.csv',csv=True)

# move files
    for i,file in enumerate(t_spec['DATA_FILE']):
        t_spec['DATA_FILE'][i] = '{}_{}.fits'.format(t_spec['DATA_KEY'][i],t_spec['SOURCE_KEY'][i])
        print(file[-4:],t_spec['DATA_FILE'][i])
        if file[-4:] == 'fits':
            if t_spec['PUBLISHED'][i] == 'Y':
                copyfile(file,'{}/published/{}'.format(review_folder,t_spec['DATA_FILE'][i]))
#                if verbose:
#                    print('Moved {} to {}/published/'.format(t_spec['DATA_FILE'][i],review_folder))
            else:
                copyfile(file,'{}/unpublished/{}'.format(review_folder,t_spec['DATA_FILE'][i]))
#                if verbose:
#                    print('Moved {} to {}/unpublished/'.format(t_spec['DATA_FILE'][i],review_folder))
        else:
            print(data_folder+file)
            sp = spl.Spectrum(file=file)
            if t_spec['PUBLISHED'][i] == 'Y':
                sp.export('{}/published/{}'.format(review_folder,t_spec['DATA_FILE'][i]))
#                if verbose:
#                    print('Moved {} to {}/published/'.format(t_spec['DATA_FILE'][i],review_folder))
            else:
                sp.export('{}/unpublished/{}'.format(review_folder,t_spec['DATA_FILE'][i]))
#                if verbose:
#                    print('Moved {} to {}/unpublished/'.format(t_spec['DATA_FILE'][i],review_folder))

# merge and export
    for col in t_spec.colnames:
#        print(col,DB_SPECTRA[col].dtype)
        tmp = t_spec[col].astype(DB_SPECTRA[col].dtype)
        t_spec.replace_column(col,tmp)
    t_merge = vstack([DB_SPECTRA,t_spec])
    t_merge.sort('DATA_KEY')
    if 'SHORTNAME' in t_merge.keys():
        t_merge.remove_column('SHORTNAME')
    if 'SELECT' in t_merge.keys():
        t_merge.remove_column('SELECT')
    if 'SOURCE_SELECT' in t_merge.keys():
        t_merge.remove_column('SOURCE_SELECT')
    if 'DATEN' in t_merge.keys():
        t_merge.remove_column('DATEN')
    t_merge.write(review_folder+DB_SPECTRA_FILE,format='ascii.tab')

    if verbose:
        print('\nDatabases updated; be sure to move these from {} to {}{}'.format(review_folder,SPLAT_PATH,DB_FOLDER))
        print('and to move spectral files from {}/published and {}/unpublished/\n'.format(review_folder,review_folder))

    return




###############################################################################
###################### TESTING FUNCTIONS #####################################
###############################################################################

def test_baseline():
    basefolder = '/Users/adam/projects/splat/exercises/ex9/'
    sp = spl.getSpectrum(shortname='1047+2124')[0]        # T6.5 radio emitter
    spt,spt_e = spl.classifyByStandard(sp,spt=['T2','T8'])
    teff,teff_e = spl.typeToTeff(spt)
    sp.fluxCalibrate('MKO J',spl.typeToMag(spt,'MKO J')[0],absolute=True)
    table = spl.modelFitMCMC(sp, mask_standard=True, initial_guess=[teff, 5.3, 0.], zstep=0.1, nsamples=100,savestep=0,filebase=basefolder+'fit1047',verbose=True)


def test_ingest(folder='./',**kwargs):
    importSpectra(data_folder=folder,**kwargs)

def test_combine():
# source db
    data_folder = '/Users/adam/projects/splat/adddata/daniella/spex_prism_160218/'
    review_folder = '/Users/adam/projects/splat/adddata/review/'
    t_src = fetchDatabase(review_folder+'source_update.csv',csv=True)
# convert all t_src columns to the same format in DB_SOURCES
    for col in t_src.colnames:
        tmp = t_src[col].astype(DB_SOURCES[col].dtype)
        t_src.replace_column(col,tmp)
    t_merge = vstack([DB_SOURCES,t_src])
    t_merge.sort('SOURCE_KEY')
    t_merge.write(review_folder+DB_SOURCES_FILE,format='ascii.tab')

# spectrum db
    t_spec = fetchDatabase(review_folder+'spectrum_update.csv',csv=True)
# move files
# WARNING - ASSUMING THESE ARE FITS; NEED A FIX IF THEY ARE NOT
# COULD JUST READ IN TO SPECTRUM OBJECT AND OUTPUT AS FITS FILE
    for i,file in enumerate(t_spec['DATA_FILE']):
        t_spec['DATA_FILE'][i] = '{}_{}.fits'.format(t_spec['DATA_KEY'][i],t_spec['SOURCE_KEY'][i])
        if t_spec['PUBLISHED'][i] == 'Y':
            copyfile(data_folder+file,'{}/published/{}'.format(review_folder,t_spec['DATA_FILE'][i]))
            print('Moved {} to {}/published/'.format(t_spec['DATA_FILE'][i],review_folder))
        else:
            copyfile(data_folder+file,'{}/unpublished/{}'.format(review_folder,t_spec['DATA_FILE'][i]))
            print('Moved {} to {}/unpublished/'.format(t_spec['DATA_FILE'][i],review_folder))
# convert all t_src columns to the same format in DB_SOURCES
    for col in t_spec.colnames:
        tmp = t_spec[col].astype(DB_SPECTRA[col].dtype)
        t_spec.replace_column(col,tmp)
    t_merge = vstack([DB_SPECTRA,t_spec])
    t_merge.sort('DATA_KEY')
    t_merge.write(review_folder+DB_SPECTRA_FILE,format='ascii.tab')
    print('\nDatabases updated; be sure to move these from {} to {}{}'.format(review_folder,SPLAT_PATH,DB_FOLDER))
    print('and to move spectral files from {}/published and {}/unpublished/\n'.format(review_folder,review_folder))






# main testing of program
#if __name__ == '__main__':
#    dfolder = '/Users/adam/projects/splat/adddata/tobeadded/simp/prism/'
#    test_ingest(dfolder,spreadsheet=dfolder+'input.csv')
#    test_missingbibs()

