from __future__ import print_function, division

"""
.. note::
         These are the plotting functions for the SPLAT code 
"""


# imports: internal
import copy
import glob
import os

# imports: external
import matplotlib.cm as cm
import matplotlib.colors as colmap
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy
from scipy.interpolate import interp1d 
from scipy import ndimage

# imports: splat
from .initialize import *
from .utilities import *
from .core import Spectrum, classifyByStandard



def plotSpectrum(*args, **kwargs):
    '''
    :Purpose: ``Primary plotting program for Spectrum objects.``

    :Input
    Spectrum objects, either sequentially, in list, or in list of lists
            - Spec1, Spec2, ...: plot multiple spectra together, or separately if multiplot = True
            - [Spec1, Spec2, ...]: plot multiple spectra together, or separately if multiplot = True
            - [[Spec1, Spec2], [Spec3, Spec4], ..]: plot multiple sets of spectra (multiplot forced to be True)

    :Parameters:
    title = ''
        string giving plot title  - NOTE: THIS IS NOT WORKING
    xrange = [0.85,2.42]:
        plot range for wavelength axis
    yrange = [-0.02,1.2]*fluxMax:
        plot range for wavelength axis
    xlabel:
        wavelength axis label; by default set by wlabel and wunit keywords in first spectrum object
    ylabel:
        flux axis label; by default set by fscale, flabel and funit keywords in first spectrum object


    features:
        a list of strings indicating chemical features to label on the spectra
        options include H2O, CH4, CO, TiO, VO, FeH, H2, HI, KI, NaI, SB (for spectral binary)
    mdwarf, ldwarf, tdwarf, young, binary = False:
        add in features characteristic of these classes
    telluric = False:
        mark telluric absorption features
    legend, legends, label or labels:
        list of strings providing legend-style labels for each spectrum plotted
    legendLocation or labelLocation = 'upper right':
        place of legend; options are 'upper left', 'center middle', 'lower right' (variations thereof) and 'outside'
    legendfontscale = 1:
        sets the scale factor for the legend fontsize (defaults to fontscale)
    grid = False:
        add a grid

    stack = 0:
        set to a numerical offset to stack spectra on top of each other
    zeropoint = [0,...]:
        list of offsets for each spectrum, giving finer control than stack
    showZero = True:
        plot the zeropoint(s) of the spectra

    comparison:
        a comparison Spectrum to compare in each plot, useful for common reference standard
    noise, showNoise or uncertainty = False:
        plot the uncertainty for each spectrum
    residual = False:
        plots the residual between two spectra

    color or colors:
        color of plot lines; by default all black
    colorUnc or colorsUnc:
        color of uncertainty lines; by default same as line color but reduced opacity
    colorScheme or colorMap:
        color map to apply based on matplotlib colormaps; 
        see http://matplotlib.org/api/pyplot_summary.html?highlight=colormaps#matplotlib.pyplot.colormaps
    linestyle:
        line style of plot lines; by default all solid
    fontscale = 1:
        sets a scale factor for the fontsize

    inset = False:
        place an inset panel showing a close up region of the spectral data
    inset_xrange = False:
        wavelength range for inset panel
    inset_position = [0.65,0.60,0.20,0.20]
        position of inset planet in normalized units, in order left, bottom, width, height
    inset_features = False
        list of features to label in inset plot

    file or filename or output:
        filename or filename base for output
    filetype = 'pdf':
        output filetype, generally determined from filename
    multiplot = False: 
        creates multiple plots, depending on format of input (optional)
    multipage = False: 
        spreads plots across multiple pages; output file format must be PDF
        if not set and plots span multiple pages, these pages are output sequentially as separate files
    layout or multilayout = [1,1]:
        defines how multiple plots are laid out on a page
    figsize:
        set the figure size; set to default size if not indicated
    interactive = False:
        if plotting to window, set this to make window interactive
        
        
    :Example 1: A simple view of a random spectrum
       >>> import splat
       >>> spc = splat.getSpectrum(spt = 'T5', lucky=True)[0]
       >>> spc.plot()                       # this automatically generates a "quicklook" plot
       >>> splat.plotSpectrum(spc)          # does the same thing
       >>> splat.plotSpectrum(spc,uncertainty=True,tdwarf=True)     # show the spectrum uncertainty and T dwarf absorption features

    :Example 2: Viewing a set of spectra for a given object
        In this case we'll look at all of the spectra of TWA 30B in the library, sorted by year and compared to the first epoch data
        This is an example of using multiplot and multipage

       >>> splist = splat.getSpectrum(name = 'TWA 30B')         # get all spectra of TWA 30B
       >>> junk = [sp.normalize() for sp in splist]             # normalize the spectra
       >>> dates = [sp.date for sp in splist]                   # observation dates
       >>> spsort = [s for (s,d) in sorted(zip(dates,splis))]   # sort spectra by dates
       >>> dates.sort()                                         # don't forget to sort dates!
       >>> splat.plotSpectrum(spsort,multiplot=True,layout=[2,2],multipage=True,\   # here's our plot statement
           comparison=spsort[0],uncertainty=True,mdwarf=True,telluric=True,legends=dates,\
           legendLocation='lower left',output='TWA30B.pdf')
       
    :Example 3: Display the spectra sequence of L dwarfs
        This example uses the list of standard files contained in SPLAT, and illustrates the stack feature

       >>> spt = [splat.typeToNum(i+20) for i in range(10)] # generate list of L spectral types
       >>> splat.initiateStandards()                        # initiate standards
       >>> splist = [splat.SPEX_STDS[s] for s in spt]       # extact just L dwarfs
       >>> junk = [sp.normalize() for sp in splist]         # normalize the spectra
       >>> labels = [sp.shortname for sp in splist]         # set labels to be names
       >>> splat.plotSpectrum(splist,figsize=[10,20],labels=labels,stack=0.5,\  # here's our plot statement
           colorScheme='copper',legendLocation='outside',telluric=True,output='lstandards.pdf')
       
    '''

# keyword parameters
#    from .splat import Spectrum
    nsamples = kwargs.get('nsamples',1000)
    multiplot = kwargs.get('multiplot',False)           # create multiple plots
    multipage = kwargs.get('multipage',False)           # create a multiple page sequence of plots
    multilayout = kwargs.get('multilayout',[1,1])       # layout of multiple plots, [# horizontal, # vertical]
    multilayout = kwargs.get('layout',multilayout)      
    stack = kwargs.get('stack',0)                   # stack spectra on top of each other
    grid = kwargs.get('grid',False)                 # plot internal grid lines
    filename = kwargs.get('filename','')            # output filename
    filename = kwargs.get('file',filename)
    filename = kwargs.get('output',filename)
    if filename == False:
        filename = ''
    title = kwargs.get('title','')
    fontscale = kwargs.get('fontscale',1)
    legendfontscale = kwargs.get('legendfontscale',0.8*fontscale)
    fb = filename.split('.')[:-1]               # filebase for multiple files
    if filename != '' and len(fb) > 1:
        filebase = fb[0]
        for x in fb[1:]:
            filebase+='.'+x
    elif filename != '' and len(fb) == 1:
        filebase = fb[0]
    else:
        filebase = filename
    filetype = kwargs.get('format',filename.split('.')[-1])
    filetype.lower()
    if filetype == '':
        filetype = 'pdf'
    comparison = kwargs.get('comparison',False)
    if not isinstance(comparison,Spectrum):
        comparison = False
    residual = kwargs.get('residual',False)
    inset = kwargs.get('inset',False)
    inset_xrange = kwargs.get('inset_xrange',False)
    inset_position = kwargs.get('inset_position',[.65, .6, .2, .2])
#    inset_color = kwargs.get('inset_color','k')
    inset_features = kwargs.get('inset_features',False)
    

#    mask = kwargs.get('mask',False)                # not yet implemented

# features to label on spectra
    feature_labels = { \
        'h2o': {'label': r'H$_2$O', 'type': 'band', 'wavelengths': [[0.92,0.95],[1.08,1.20],[1.325,1.550],[1.72,2.14]]}, \
        'ch4': {'label': r'CH$_4$', 'type': 'band', 'wavelengths': [[1.1,1.24],[1.28,1.44],[1.6,1.76],[2.2,2.35]]}, \
        'co': {'label': r'CO', 'type': 'band', 'wavelengths': [[2.29,2.39]]}, \
        'tio': {'label': r'TiO', 'type': 'band', 'wavelengths': [[0.76,0.80],[0.825,0.831]]}, \
        'vo': {'label': r'VO', 'type': 'band', 'wavelengths': [[1.04,1.08]]}, \
#        'feh': {'label': r'FeH', 'type': 'band', 'wavelengths': [[0.86,0.90],[0.98,1.03],[1.19,1.25],[1.57,1.64]]}, \
        'feh': {'label': r'FeH', 'type': 'band', 'wavelengths': [[0.98,1.03],[1.19,1.25],[1.57,1.64]]}, \
        'h2': {'label': r'H$_2$', 'type': 'band', 'wavelengths': [[1.5,2.4]]}, \
        'sb': {'label': r'*', 'type': 'band', 'wavelengths': [[1.6,1.64]]}, \
        'h': {'label': r'H I', 'type': 'line', 'wavelengths': [[1.004,1.005],[1.093,1.094],[1.281,1.282],[1.944,1.945],[2.166,2.166]]},\
        'hi': {'label': r'H I', 'type': 'line', 'wavelengths': [[1.004,1.005],[1.093,1.094],[1.281,1.282],[1.944,1.945],[2.166,2.166]]},\
        'h1': {'label': r'H I', 'type': 'line', 'wavelengths': [[1.004,1.005],[1.093,1.094],[1.281,1.282],[1.944,1.945],[2.166,2.166]]},\
        'na': {'label': r'Na I', 'type': 'line', 'wavelengths': [[0.8186,0.8195],[1.136,1.137],[2.206,2.209]]}, \
        'nai': {'label': r'Na I', 'type': 'line', 'wavelengths': [[0.8186,0.8195],[1.136,1.137],[2.206,2.209]]}, \
        'na1': {'label': r'Na I', 'type': 'line', 'wavelengths': [[0.8186,0.8195],[1.136,1.137],[2.206,2.209]]}, \
        'mg': {'label': r'Mg I', 'type': 'line', 'wavelengths': [[1.7113336,1.7113336],[1.5745017,1.5770150],[1.4881595,1.4881847,1.5029098,1.5044356],[1.1831422,1.2086969],]}, \
        'mgi': {'label': r'Mg I', 'type': 'line', 'wavelengths': [[1.7113336,1.7113336],[1.5745017,1.5770150],[1.4881595,1.4881847,1.5029098,1.5044356],[1.1831422,1.2086969],]}, \
        'mg1': {'label': r'Mg I', 'type': 'line', 'wavelengths': [[1.7113336,1.7113336],[1.5745017,1.5770150],[1.4881595,1.4881847,1.5029098,1.5044356],[1.1831422,1.2086969],]}, \
        'ca': {'label': r'Ca I', 'type': 'line', 'wavelengths': [[2.263110,2.265741],[1.978219,1.985852,1.986764],[1.931447,1.945830,1.951105]]}, \
        'cai': {'label': r'Ca I', 'type': 'line', 'wavelengths': [[2.263110,2.265741],[1.978219,1.985852,1.986764],[1.931447,1.945830,1.951105]]}, \
        'ca1': {'label': r'Ca I', 'type': 'line', 'wavelengths': [[2.263110,2.265741],[1.978219,1.985852,1.986764],[1.931447,1.945830,1.951105]]}, \
        'caii': {'label': r'Ca II', 'type': 'line', 'wavelengths': [[1.184224,1.195301],[0.985746,0.993409]]}, \
        'ca2': {'label': r'Ca II', 'type': 'line', 'wavelengths': [[1.184224,1.195301],[0.985746,0.993409]]}, \
        'al': {'label': r'Al I', 'type': 'line', 'wavelengths': [[1.672351,1.675511],[1.3127006,1.3154345]]}, \
        'ali': {'label': r'Al I', 'type': 'line', 'wavelengths': [[1.672351,1.675511],[1.3127006,1.3154345]]}, \
        'al1': {'label': r'Al I', 'type': 'line', 'wavelengths': [[1.672351,1.675511],[1.3127006,1.3154345]]}, \
        'fe': {'label': r'Fe I', 'type': 'line', 'wavelengths': [[1.5081407,1.5494570],[1.25604314,1.28832892],[1.14254467,1.15967616,1.16107501,1.16414462,1.16931726,1.18860965,1.18873357,1.19763233]]}, \
        'fei': {'label': r'Fe I', 'type': 'line', 'wavelengths': [[1.5081407,1.5494570],[1.25604314,1.28832892],[1.14254467,1.15967616,1.16107501,1.16414462,1.16931726,1.18860965,1.18873357,1.19763233]]}, \
        'fe1': {'label': r'Fe I', 'type': 'line', 'wavelengths': [[1.5081407,1.5494570],[1.25604314,1.28832892],[1.14254467,1.15967616,1.16107501,1.16414462,1.16931726,1.18860965,1.18873357,1.19763233]]}, \
        'k': {'label': r'K I', 'type': 'line', 'wavelengths': [[0.7699,0.7665],[1.169,1.177],[1.244,1.252]]}, \
        'ki': {'label': r'K I', 'type': 'line', 'wavelengths': [[0.7699,0.7665],[1.169,1.177],[1.244,1.252]]}, \
        'k1': {'label': r'K I', 'type': 'line', 'wavelengths': [[0.7699,0.7665],[1.169,1.177],[1.244,1.252]]}}

    features = kwargs.get('features',[])
    if not isinstance(features,list):
        features = [features]
    if (kwargs.get('ldwarf',False) or kwargs.get('mdwarf',False)):
        features.extend(['k','na','feh','tio','co','h2o','h2'])
    if (kwargs.get('tdwarf',False)):
        features.extend(['k','ch4','h2o','h2'])
    if (kwargs.get('young',False)):
        features.extend(['vo'])
    if (kwargs.get('binary',False)):
        features.extend(['sb'])
# clean repeats while maintaining order - set does not do this
    fea = []
    for i in features:
        if i not in fea:
            fea.append(i)
    features = fea

# error check - make sure you're plotting something
    if (len(args) < 1):
        print('plotSpectrum needs at least one Spectrum object to plot')
        return

# if a list is passed, use this list
    elif (len(args) == 1 and isinstance(args[0],list)):
        splist = args[0]
    
# if a set of objects is passed, turn into a list
    else:
        splist = []
        for a in args:
            if isinstance(a,Spectrum):      # a spectrum object
                splist.append(a)
            elif isinstance(a,list):
                splist.append(a)
            else:
                print('\nplotSpectrum: Ignoring input object {} as it is neither a Spectrum object nor a list\n\n'.format(a))

# set up for multiplot
    if (len(splist) == 1):
        multiplot = False
    
# array of lists => force multiplot
    elif (len(splist) > 1 and isinstance(splist[0],list)):
        multiplot = True

# reformat array of spectra of multiplot is used (i.e., user forgot to set)
    if multiplot == True and isinstance(splist[0],Spectrum):
        splist = [[s] for s in splist]

    elif multiplot == False and isinstance(splist[0],Spectrum):
        splist = [splist]
        
# flatten array if multiplot is not set
    elif multiplot == False and isinstance(splist[0],list) and len(splist) > 1:
        splist = [[item for sublist in splist for item in sublist]]       # flatten

    tot_sp = len([item for sublist in splist for item in sublist])    # Total number of spectra
    
# prep legend
    legend = kwargs.get('legend',[str() for x in numpy.arange(tot_sp)])
    legend = kwargs.get('legends',legend)
    legend = kwargs.get('label',legend)
    legend = kwargs.get('labels',legend)
    if not isinstance(legend,list):
        legend = [legend]
    if(len(legend) < tot_sp):
        legend.extend([str() for x in numpy.arange(tot_sp-len(legend))])
    legendLocation = kwargs.get('legendLocation','upper right')       # sets legend location
    legendLocation = kwargs.get('labelLocation',legendLocation)       # sets legend location

# now run a loop through the input subarrays
    plt.close('all')

# set up here for multiple file output
    nplot = 1
    if multipage == True or multiplot == True:
        nplot = multilayout[0]*multilayout[1]
        numpages = int(len(splist) / nplot) + 1
        if (len(splist) % nplot == 0):
               numpages -= 1
        fig = []
        
    if multipage == True and filetype == 'pdf':
        pdf_pages = PdfPages(filename)
        
    if multipage == False:
        if len(splist) > 1:
            files = [filebase+'{}.'.format(i+1)+filetype for i in numpy.arange(len(splist))]
        else:
            files = [filebase+'.'+filetype]

    pg_n = 0        # page counter
    plt_n = 0       # plot per page counter
    lg_n = 0        # legend per plot counter
    for plts,sp in enumerate(splist):
# set specific plot parameters
#        print(sp[0],Spectrum,isinstance(sp[0],Spectrum))
        if not isinstance(sp[0],Spectrum):
            raise ValueError('\nInput to plotSpectrum has wrong format:\n\n{}\n\n'.format(sp[0]))
        zeropoint = kwargs.get('zeropoint',[0. for x in numpy.arange(len(sp))])

# settings that work if the spectrum was read in as legitmate Spectrum object
        try:
            xlabel = kwargs.get('xlabel','{} ({})'.format(sp[0].wlabel,sp[0].wunit))
            ylabel = kwargs.get('ylabel','{} {} ({})'.format(sp[0].fscale,sp[0].flabel,sp[0].funit))
        except:
            xlabel = kwargs.get('xlabel','Wavelength (unknown units)')
            ylabel = kwargs.get('ylabel','Flux (unknown units)')
        xrange = kwargs.get('xrange',[0.85,2.42])
        bound = xrange
        ymax = [s.fluxMax().value for s in sp]
        yrng = kwargs.get('yrange',map(lambda x: x*numpy.nanmax(ymax)+numpy.nanmax(zeropoint),[-0.02,1.2]))
        bound.extend(yrng)
        linestyle = kwargs.get('linestyle',['steps' for x in numpy.arange(len(sp))])
        linestyle = kwargs.get('linestyles',linestyle)
        if (len(linestyle) < len(sp)):
            linestyle.extend(['steps' for x in numpy.arange(len(sp)-len(linestyle))])

# colors
# by default all black lines
        colors = kwargs.get('colors',['k' for x in numpy.arange(len(sp))])
        colors = kwargs.get('color',colors)
        if not isinstance(colors,list):
            colors = [colors]
        if (len(colors) < len(sp)):
            while len(colors) < len(sp):
                colors.extend(colors[-1])
        colorScheme = kwargs.get('colorScheme',None)
        colorScheme = kwargs.get('colorMap',colorScheme)
        if (colorScheme != None):
            values = numpy.arange(len(sp))
            color_map = plt.get_cmap(colorScheme)
            norm  = colmap.Normalize(vmin=0, vmax=1.0*values[-1])
            scalarMap = cm.ScalarMappable(norm=norm, cmap=color_map)
            for i in numpy.arange(len(sp)):
                colors[i] = scalarMap.to_rgba(values[i])
        colorsUnc = kwargs.get('colorsUnc',colors)
        colorsUnc = kwargs.get('colorUnc',colorsUnc)
        if (len(colorsUnc) < len(sp)):
            while len(colorsUnc) < len(sp):
                colorsUnc.extend(colors[-1])


# show uncertainties
        showNoise = kwargs.get('showNoise',[False for x in numpy.arange(len(sp))])
        showNoise = kwargs.get('noise',showNoise)
        showNoise = kwargs.get('uncertainty',showNoise)
        if not isinstance(showNoise, list):
            showNoise = [showNoise]
        if (len(showNoise) < len(sp)):
            showNoise.extend([True for x in numpy.arange(len(sp)-len(showNoise))])

# zero points - by default true
        showZero = kwargs.get('showZero',[True for x in numpy.arange(len(sp))])
        if not isinstance(showZero, list):
            showZero = [showZero]
        if (len(showZero) < len(sp)):
            while len(showZero) < len(sp):
                showZero.extend(showZero[-1])

# GENERATE PLOTS
        if (multiplot == True or multipage == True):
            plt_n = plts % nplot
            if (plt_n == 0):# and plts != len(splist)):
#                ax = range(nplot)
#                t = tuple([tuple([i+b*multilayout[1] for i in range(multilayout[1])]) for b in range(multilayout[0])])
#                fig[pg_n], ax = plt.subplots(multilayout[0], multilayout[1], sharex = True, sharey = True)
#
# NOTE THE FOLLOWING LINE IS HAVING PROBLEMS IN PYTHON3
#
#
                fig.append(plt.figure())
                pg_n += 1
            ax = fig[pg_n-1].add_subplot(multilayout[0], multilayout[1], plt_n+1)
            
# plotting a single plot with all spectra
        else:
            plt.close('all')
#            ax = range(1)
            plt_n = 0
            fig = []
            if (kwargs.get('figsize') != None):
                fig.append(plt.figure(figsize = kwargs.get('figsize')))
            else:
                fig.append(plt.figure())
            ax = fig[0].add_subplot(111)
        
        for ii, a in enumerate(sp):
            flx = [i+zeropoint[ii] for i in a.flux.value]
#stack
            if stack > 0:
                flx = [f + (len(sp)-ii-1)*stack for f in flx]
#                if kwargs.get('yrange') == None:
#                    bound[3] = bound[3] + stack

            ax.plot(a.wave.value,flx,color=colors[ii],linestyle=linestyle[ii], zorder = 10, label = legend[lg_n])  

# add comparison
            if comparison != False:
                colorComparison = kwargs.get('colorComparison',colors[0])
                linestyleComparison = kwargs.get('linestyleComparison',linestyle[0])
                cflx = [i+zeropoint[ii] for i in comparison.flux.value]

                if stack > 0:
                    cflx = [f + (len(sp)-ii-1)*stack for f in cflx]

                ax.plot(comparison.wave.value,cflx,color=colorComparison,linestyle=linestyleComparison,alpha=0.5, zorder = 10)
    
# add residual
            if residual == True and len(sp) == 2:
                # Save flux values from first spectrum
                if ii == 0:
                    flx0 = [f - (len(sp)-ii-1)*stack for f in flx]
                    
                # Subtract fluxes and plot
                elif ii == 1:
                    res = [flx0[f_n] - f for f_n, f in enumerate(flx)]
                    ax.plot(a.wave.value, res, alpha = 0.3, color = 'g')
                    
                    # Fix bound[2] if res goes below 0
                    if min(res) < 0:
                        b0 = numpy.argmax(a.wave.value > bound[0])
                        b1 = numpy.argmin(a.wave.value < bound[1])
                        bound[2] = bound[2] + min(res[b0:b1])

# noise
            if (showNoise[ii]):
                ns = [i+zeropoint[ii] for i in a.noise.value]
                ax.plot(a.wave.value,ns,color=colorsUnc[ii],linestyle=linestyle[ii],alpha=0.3, zorder = 10)


# zeropoint
            if (showZero[ii]):
                ze = numpy.ones(len(a.flux))*zeropoint[ii]
                ax.plot(a.wave.value,ze,color=colors[ii],linestyle=':',alpha=0.3, zorder = 10)

# determine maximum flux for all spectra
            f = interp1d(a.wave,flx,bounds_error=False,fill_value=0.)
            if (ii == 0):
                wvmax = numpy.arange(bound[0],bound[1],0.001)
                flxmax = f(wvmax)
            else:
                flxmax = numpy.maximum(flxmax,f(wvmax))

# legend counter
            lg_n = lg_n + 1 # Increment lg_n



# label features
# THIS NEEDS TO BE FIXED WITH GRETEL'S STUFF
        yoff = 0.02*(bound[3]-bound[2])
        fontsize = 10-numpy.min([(multilayout[0]*multilayout[1]-1),6])
        for ftr in features:
            ftr = ftr.lower()
            if ftr in feature_labels:
                for ii,waveRng in enumerate(feature_labels[ftr]['wavelengths']):
                    if (numpy.min(waveRng) > bound[0] and numpy.max(waveRng) < bound[1]):
                        x = (numpy.arange(0,nsamples+1.0)/nsamples)* \
                            (numpy.nanmax(waveRng)-numpy.nanmin(waveRng)+0.04)+numpy.nanmin(waveRng)-0.02
                        f = interp1d(wvmax,flxmax,bounds_error=False,fill_value=0.)
                        y = numpy.nanmax(f(x))+0.5*yoff

                        if feature_labels[ftr]['type'] == 'band':
                            ax.plot(waveRng,[y+yoff]*2,color='k',linestyle='-')
                            ax.plot([waveRng[0]]*2,[y,y+yoff],color='k',linestyle='-')
                            ax.text(numpy.mean(waveRng),y+1.5*yoff,feature_labels[ftr]['label'],horizontalalignment='center',fontsize=fontsize)
                        else:
                            for w in waveRng:
                                ax.plot([w]*2,[y,y+yoff],color='k',linestyle='-')
                            ax.text(numpy.mean(waveRng),y+1.5*yoff,feature_labels[ftr]['label'],horizontalalignment='center',fontsize=fontsize)
                            waveRng = [waveRng[0]-0.02,waveRng[1]+0.02]   # for overlap

# update offset
                        foff = [y+3*yoff if (w >= waveRng[0] and w <= waveRng[1]) else 0 for w in wvmax]
                        flxmax = [numpy.max([xx,yy]) for xx, yy in zip(flxmax, foff)]
        bound[3] = numpy.max([numpy.max(flxmax)+1.*yoff,bound[3]])
        ax.axis(bound)


# grid
        if (grid):
            ax.grid()            

# axis labels 
        fontsize = (13-numpy.min([(multilayout[0]*multilayout[1]-1),8])) * fontscale        # Added in fontscale
        legendfontsize = (13-numpy.min([(multilayout[0]*multilayout[1]-1),8])) * legendfontscale        # Added in fontscale
        ax.set_xlabel(xlabel, fontsize = fontsize)
        ax.set_ylabel(ylabel, fontsize = fontsize)
        ax.tick_params(axis='x', labelsize=fontsize)
        ax.tick_params(axis='y', labelsize=fontsize)

# place legend
        if len(legend) > 0:
            if legendLocation == 'outside':
                box = ax.get_position()
                ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width * 0.7, box.height * 0.7])
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':legendfontsize})
            else:
                ax.legend(loc=legendLocation, prop={'size':legendfontsize})
                bound[3] = bound[3]+0.1*(bound[3]-bound[2])     # extend axis for in-plot legends
            ax.axis(bound)

# overplot telluric absorption
        if (kwargs.get('telluric',False) == True):
            twv = [[1.1,1.2],[1.3,1.5],[1.75,2.0]]
            for waveRng in twv:
                rect = patches.Rectangle((waveRng[0],bound[2]),waveRng[1]-waveRng[0],bound[3]-bound[2],facecolor='0.95',alpha=0.2,color='0.95')
                ax.add_patch(rect)
                ax.text(numpy.mean(waveRng),bound[2]+3*yoff,r'$\oplus$',horizontalalignment='center',fontsize=fontsize)

# place inset - RIGHT NOW ONLY SETTING LIMITS WITH FIRST SPECTRUM IN LIST
        if inset == True and inset_xrange != False:
            ax_inset = fig[pg_n-1].add_axes(inset_position) #, axisbg='white')
            bound2 = inset_xrange
            b0 = numpy.argmax(sp[0].wave.value > bound2[0])
            b1 = numpy.argmin(sp[0].wave.value < bound2[1])
            bound2.extend([min(sp[0].flux.value[b0:b1]),max(sp[0].flux.value[b0:b1])])
            db = (bound2[3]-bound2[2])
            bound2[2] = bound2[2]-0.05*db
            bound2[3] = bound2[3]+0.05*db
            ax_inset.axis(bound2)
            inset_fontsize = fontsize*0.7

            for ii,a in enumerate(sp):
                flx = [i+zeropoint[ii] for i in a.flux.value]
                ax_inset.plot(a.wave.value,flx,color=colors[ii],linestyle=linestyle[ii])            
                ax_inset.set_xlabel('')
                ax_inset.set_ylabel('')
                ax_inset.tick_params(axis='x', labelsize=inset_fontsize)
                ax_inset.tick_params(axis='y', labelsize=inset_fontsize)
#                ax_inset.legend()

# inset feature labels
            if inset_features != False:
                f = interp1d(sp[0].wave,flx,bounds_error=False,fill_value=0.)
                wvmax = numpy.arange(bound2[0],bound2[1],0.001)
                flxmax = f(wvmax)
                yoff = 0.05*(bound2[3]-bound2[2])
                for ftr in inset_features:
                    ftr = ftr.lower()
                    if ftr in feature_labels:
                        for ii,waveRng in enumerate(feature_labels[ftr]['wavelengths']):
                            if (numpy.min(waveRng) > bound2[0] and numpy.max(waveRng) < bound2[1]):
                                x = (numpy.arange(0,nsamples+1.0)/nsamples)* \
                                    (numpy.nanmax(waveRng)-numpy.nanmin(waveRng)+0.04)+numpy.nanmin(waveRng)-0.02
                                f = interp1d(wvmax,flxmax,bounds_error=False,fill_value=0.)
                                y = numpy.nanmax(f(x))+0.5*yoff
        
                                if feature_labels[ftr]['type'] == 'band':
                                    ax_inset.plot(waveRng,[y+yoff]*2,color='k',linestyle='-')
                                    ax_inset.plot([waveRng[0]]*2,[y,y+yoff],color='k',linestyle='-')
                                    ax_inset.text(numpy.mean(waveRng),y+2*yoff,feature_labels[ftr]['label'],horizontalalignment='center',fontsize=inset_fontsize)
                                else:
                                    for w in waveRng:
                                        ax_inset.plot([w]*2,[y,y+yoff],color='k',linestyle='-')
                                    ax_inset.text(numpy.mean(waveRng),y+2*yoff,feature_labels[ftr]['label'],horizontalalignment='center',fontsize=inset_fontsize)
                                    waveRng = [waveRng[0]-0.02,waveRng[1]+0.02]   # for overlap
        
# update offset
                                foff = [y+3*yoff if (w >= waveRng[0] and w <= waveRng[1]) else 0 for w in wvmax]
                                flxmax = [numpy.max([xx,yy]) for xx, yy in zip(flxmax, foff)]
                bound2[3] = numpy.max([bound2[3],numpy.max(flxmax)+5.*yoff])
                ax_inset.axis(bound2)

    
# save to file or display
        if multipage == False:
            if filebase != '' and (plts % nplot == 3 or plts == len(splist)-1):
                plt.savefig(files[plts], format=filetype)
    if filename == '' and not kwargs.get('web',False):
        plt.show()
        if (kwargs.get('interactive',False) != False):
            plt.ion()        # make window interactive 
        else:
            plt.ioff()


# save figures in multipage format and write off pdf file
    if (multipage == True):    
        for pg_n in numpy.arange(numpages):
#            fig[pg_n].text(0.5, 0.04, xlabel, ha = 'center', va = 'center')
#            fig[pg_n].text(0.06, 0.5, ylabel, ha = 'center', va = 'center', rotation = 'vertical')
            fig[pg_n].tight_layout
            fig[pg_n].suptitle(title, fontsize = 14, fontweight = 'bold')
            pdf_pages.savefig(fig[pg_n])
        if filetype == 'pdf':
            pdf_pages.close()

    return fig


def plotBatch(*args, **kwargs):
    '''
    :Purpose: Plots a batch of spectra into a 2x2 set of PDF files, with options of overplotting comparison spectra, including best-match spectral standards. 

    :param input: A single or list of Spectrum objects or filenames, or the glob search string for a set of files (e.g., '/Data/myspectra/*.fits'). 
    :type input: required

    :param output: Filename for PDF file output; full path should be include if not saving to current directory
    :type output: optional, default = 'spectra_plot.pdf'
    :param comparisons: list of Spectrum objects or filenames for comparison spectra. If comparisons list is shorter than source list, then last comparison source will be repeated. If the comparisons list is longer, the list will be truncated. 
    :type comparisons: optional, default = None
    :param classify: Set to True to classify sources based on comparison to MLT spectral standards following the method of `Kirkpatrick et al. (2010) <http://adsabs.harvard.edu/abs/2010ApJS..190..100K>`_. This option normalizes the spectra by default
    :type classify: optional, default = False
    :param normalize: Set to True to normalize source and (if passed) comparison spectra.
    :type normalize: optional, default = False
    :param legend: Set to list of legends for plots. The number of legends should equal the number of sources and comparisons (if passed) in an alternating sequence. T
    :type legend: optional, default = displays file name for source and object name for comparison (if passed)

    Relevant parameters for plotSpectrum may also be passed

    :Example:
       >>> import glob, splat
       >>> files = glob.glob('/home/mydata/*.fits')
       >>> sp = splat.plotBatch(files,classify=True,output='comparison.pdf')
       >>> sp = splat.plotBatch('/home/mydata/*.fits',classify=True,output='comparison.pdf')
       >>> sp = splat.plotBatch([splat.Spectrum(file=f) for f in files],classify=True,output='comparison.pdf')
       All three of these commands produce the same result
    '''

# keyword check
    parameters = ['output','comparisons','classify','normalize','legend']
    checkKeys(kwargs,parameters,forcekey=False)
    kwargs['layout']=kwargs.get('layout',[2,2])
    kwargs['fontscale']=kwargs.get('fontscale',0.7)

# input check
    if len(args) == 0:
        print('\nNeed to provide a list of spectra or filenames, or a file search string, to use plotBatch')
        return
    kwargs['output'] = kwargs.get('output','spectra_plot.pdf')
#    from .splat import Spectrum
# break out a list
    if isinstance(args[0],list):
        inputlist = args[0]
    else:
        inputlist = args

# if filenames, read in each file to a spectrum object
    if isinstance(inputlist[0],str):
# try a glob search string  
        files = glob.glob(inputlist[0])
        if len(files) > 1 or (len(files) == 1 and inputlist[0].find('*') != -1):
            inputlist = files
# try reading in files into Spectrum object
        try:
            splist = [Spectrum(file = f) for f in inputlist]
        except:
            raise ValueError('\nCould not read in list of files - make sure the full path is specified and the files are correctly formatted')

# if filenames, read in each file to a spectrum object
    elif isinstance(inputlist[0],Spectrum):
        splist = copy.deepcopy(inputlist)
    else:
        print('\nInput should be list of Spectra objects or filenames')
        return

# comparison files are present
    compflag = False
    complist = []
    if kwargs.get('comparisons',False) != False:
        comp = kwargs.get('comparisons')
        if not isinstance(comp,list):
            comp = [comp]
        if len(comp) < len(splist):
            while len(comp) < len(splist):
                comp.append(comp[-1])
        if isinstance(comp[0],str):
            try:
                complist = [Spectrum(file = f) for f in comp]
                compflag = True
            except:
                print('\nCould not read in comparison files: ignoring comparisons')
        if isinstance(comp[0],Spectrum):
            complist = comp
            compflag = True

# set comparison files to be standards for spectral classification
    if kwargs.get('classify',False):
        complist = []
        for sp in splist:
#            from .splat import classifyByStandard
            spt = classifyByStandard(sp,method='kirkpatrick')
            complist.append(STDS_DWARF_SPEX[spt[0]])
        compflag = True
        kwargs['normalize'] = kwargs.get('normalize',True)

# normalize if desired
    if kwargs.get('normalize',False):
        tmp = [sp.normalize() for sp in splist]
        if compflag == True:
            tmp = [sp.normalize() for sp in complist]

# prep for plotting
    plotlist = []
    clist = []
    for i,sp in enumerate(splist):
        if compflag == True:
            plotlist.append([sp,complist[i]])
            clist.extend(['k','r'])
        else:
            plotlist.append([sp])
            clist.extend(['k'])

# manage legends
    if kwargs.get('legend',False) != False:
        legends = kwargs.get('legend')
        if not isinstance(legends,list):
            legends = [legends]
        if len(legends) < (len(splist)+len(complist)):
# guess: just left out the comparison legends            
            if len(complist) > 0 and len(legends) == len(splist):
                legtmp = []
                for i,l in enumerate(legends):
                    legtmp.extend([l,'{}'.format(complist[i].name)])
                legends = legtmp
            else:
# otherwise: pad the remaining legends with the last legend (pairs)           
                while len(legends) < (len(splist)+len(complist)):
                    if compflag:
                        legends.extend([legends[-2],legends[-1]])
                    else:
                        legends.extend([legends[-1]])
        if len(legends) > (len(splist)+len(complist)):
            legends = legends[0:(len(splist)+len(complist))]
    else:
        legends = []
        for i,sp in enumerate(splist):
            if compflag == True:
                legends.extend(['{}'.format(os.path.basename(sp.filename)),'{}'.format(complist[i].name)])
            else:
                legends.extend(['{}'.format(os.path.basename(sp.filename))])

# generate pdf
    plotSpectrum(plotlist,multiplot=True,multipage=True,legends=legends,colors=clist,**kwargs)

    return


def plotIndices(*args, **kwargs):
    '''
    :Purpose: ``Plot index-index plots.``

    Not currently implemented
    '''
    pass
    return

def plotSED(*args, **kwargs):
    '''
    :Purpose: ``Plot SED photometry with SpeX spectrum.``

    Not currently implemented
    '''
    pass
    return



def plotSequence(*args, **kwargs):
    '''
    :Purpose: Compares a spectrum to a sequence of standards a batch of spectra into a 2x2 set of PDF files, with options of overplotting comparison spectra, including best-match spectral standards. 

    :param input: A single or list of Spectrum objects or filenames, or the glob search string for a set of files (e.g., '/Data/myspectra/*.fits'). 
    :type input: required

    :param type_range: Number of subtypes to consider above and below best-fit spectral type 
    :type type_range: optional, default = 2
    :param spt: Default spectral type for source; this input skips classifyByStandard
    :type spt: optional, default = None
    :param output: Filename for output; full path should be include if not saving to current directory. If blank, plot is shown on screen
    :type output: optional, default = None (screen display)

    Relevant parameters for plotSpectrum may also be passed

    :Example:
       >>> import glob, splat
       >>> files = glob.glob('/home/mydata/*.fits')
       >>> sp = splat.plotBatch(files,classify=True,output='comparison.pdf')
       >>> sp = splat.plotBatch('/home/mydata/*.fits',classify=True,output='comparison.pdf')
       >>> sp = splat.plotBatch([splat.Spectrum(file=f) for f in files],classify=True,output='comparison.pdf')
       All three of these commands produce the same result
    '''

# check inputs
    if len(args) == 0:
        raise ValueError('\nNeed to provide a spectrum object or filename for plotStandardSequence')

#    from .splat import classifyByStandard, Spectrum
    parameters = ['type_range']
    checkKeys(kwargs,parameters,forcekey=False)
    type_range =kwargs.get('type_range',2)
    kwargs['stack']=kwargs.get('stack',0.5)
#    kwargs['legendLocation']=kwargs.get('legendLocation','outside')
    kwargs['telluric']=kwargs.get('telluric',True)
    kwargs['method']=kwargs.get('method','kirkpatrick')
#    kwargs['color']=kwargs.get('color','r')
    kwargs['colorComparison']=kwargs.get('colorComparison','k')
    kwargs['colorScheme']=kwargs.get('colorScheme','winter')
    kwargs['figsize']=kwargs.get('figsize',[10,10*type_range*kwargs['stack']])
    kwargs['fontscale']=kwargs.get('fontscale',1.5)

# process input
    if isinstance(args[0],str):
        if len(glob.glob(args[0])) == 0:
            raise ValueError('\nCannot find input file {} - make sure full path is included'.format(args[0]))
        try:
            sp = Spectrum(file = args[0])
        except:
            raise ValueError('\nCould not read in file {} - make sure the file is correctly formatted'.format(args[0]))
    elif isinstance(args[0],Spectrum):
        sp = copy.deepcopy(args[0])
    else:
        raise ValueError('\nInput should be a Spectrum object or filename')
    sp.normalize()

# classify by comparison to standards
    spt = kwargs.get('spt',classifyByStandard(sp,**kwargs)[0])
    if not isinstance(spt,str):
        spt = typeToNum(spt)

# produce range of standards for plot
    stdnum = numpy.arange(numpy.floor(typeToNum(spt)-type_range),numpy.ceil(typeToNum(spt)+type_range)+1)
    if numpy.max(stdnum) > 39:
        stdnum-=(numpy.max(stdnum)-39)
    if numpy.min(stdnum) < 10:
        stdnum+=(10-numpy.min(stdnum))
    stdspt = [typeToNum(i) for i in stdnum]
    stds = [STDS_DWARF_SPEX[s] for s in stdspt]
    stdlabels = ['{} Standard'.format(s) for s in stdspt]
    plotlist = []
    labels = []
    colors = []
    for i,stdsp in enumerate(stds):
        plotlist.append([stdsp,sp])
        labels.extend([])
    fig = plotSpectrum(stds,comparison=sp,labels=stdlabels,**kwargs)

    return fig

# main testing of program
if __name__ == '__main__':
    out_folder = '/Users/adam/projects/splat/code/testing/'
    def test_plotBatch():
        data_folder = '/Users/adam/projects/splat/adddata/done/daniella/'
        files = glob.glob(data_folder+'*.fits')
        plotBatch(files,classify=True,output=out_folder+'plotBatch_test1.pdf',telluric=True)
        plotBatch(data_folder+'*.fits',classify=True,output=out_folder+'plotBatch_test2.pdf',noise=True)
        splist = [Spectrum(file=f) for f in files]
        plotBatch(splist,classify=True,output=out_folder+'plotBatch_test3.pdf',features=['h2o','feh','co'],legend=[s.name for s in splist])
        return

    def test_plotSequence():
        sp = Spectrum(10001)
        plotSequence(sp,output=out_folder+'plotSequence_test1.pdf')
        plotSequence(sp,type_range=3,output=out_folder+'plotSequence_test2.png')
        data_folder = '/Users/adam/projects/splat/adddata/done/daniella/'
        files = glob.glob(data_folder+'*.fits')
        plotSequence(files[0],telluric=True,stack=0.7,spt='M0',output=out_folder+'plotSequence_test3.eps')
        sp = getSpectrum(shortname='0415-0935')[0]
        plotSequence(sp,telluric=True,stack=0.3,output=out_folder+'plotSequence_test4.eps')
        plotSequence(sp,telluric=True,stack=0.3)
        return

    test_plotBatch()
#    test_plotSequence()


    
