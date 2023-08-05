""" Loading module and variables """

import sys,os

def showhelp():

    print ""
    print "-------------------------------------------------------------------"
    print "  Velocity plot software"
    print "-------------------------------------------------------------------"
    print ""
    print "usage: velplot <fortfile> [--args]" 
    print ""
    print "optional arguments: "
    print "   --atomdir       Path to a custom atom.dat"
    print "                     (default: in current repository)"
    print "   --details       Plot individual Voigt profiles"
    print "   --dispersion    Spectral velocity dispersion for high-resolution"
    print "                   individual Voigt profiles"
    print "                     (default: 0.01 km/s)"
    print "   --dv            Custom velocity range for plotting"
    print "   --extra         Add vertical line to identify specific region."
    print "                     Multiple velocities can be specified by using"
    print "                     the colon symbol (:) to separate the values"
    print "   --fit           Run VPFIT and embed final results in fort.13"
    print "   --getwave       Get wavelength array from the spectrum"
    print "   --header        List of transition IDs of each fitting region"
    print "                     (default: embedded in the fort file)"
    print "   --nores         Do not plot the residuals"
    print "   --output        Give custom output filename"
    print "                     (default: date-time in yyyymmdd-HHMMSS format)"
    print "   --unscale       Don't correct the data and distort the models"
    print "   --version       Path to a custom vpfit executable"
    print "                     (default: vpfit)"
    print "   --vpfsetup      Path to a custom vp_setup.dat"
    print "                     9default: in current repository)"
    print "   --zmid          Central redshift to plot transitions"
    print ""
    print "-------------------------------------------------------------------"
    print ""
    quit()

def isfloat(value):
    """
    Check if given value is of float type or not

    Parameters
    ----------
    value : str
      Value to be checked.
    """
    try:
      float(value)
      return True
    except ValueError:
      return False

def atomlist(atompath):     # Store data from atom.dat
    """
    Create list of atomic data based on input atom.dat

    Parameters
    ----------
    atompath : str
      Full path to the atom.dat
    """
    import numpy as np
    atom        = np.empty((0,6))
    atomdat     = np.loadtxt(atompath,dtype='str',delimiter='\n')
    for element in atomdat:
        l       = element.split()
        i       = 0      if len(l[0])>1 else 1
        species = l[0]   if len(l[0])>1 else l[0]+l[1]
        wave    = 0 if len(l)<i+2 else 0 if isfloat(l[i+1])==False else l[i+1]
        f       = 0 if len(l)<i+3 else 0 if isfloat(l[i+2])==False else l[i+2]
        gamma   = 0 if len(l)<i+4 else 0 if isfloat(l[i+3])==False else l[i+3]
        mass    = 0 if len(l)<i+5 else 0 if isfloat(l[i+4])==False else l[i+4]
        alpha   = 0 if len(l)<i+6 else 0 if isfloat(l[i+5])==False else l[i+5]
        if species not in ['>>','<<','<>','__']:
            atom = np.vstack((atom,[species,wave,f,gamma,mass,alpha]))
    return atom

def variables():
    """
    Initializing all variables to be read and updated during the process.
    """
    rc('font', size=2, family='serif')
    rc('axes', labelsize=2, linewidth=0.2)
    rc('legend', fontsize=2, handlelength=10)
    rc('xtick', labelsize=8)
    rc('ytick', labelsize=8)
    rc('lines', lw=0.2, mew=0.2)
    rc('grid', linewidth=0.2)
    v = type('v', (), {})()
    v.k = 1.3806488*10**-23    # m^2.kg.s^-2.K^-1
    v.c = 299792.458           # km/s
    v.ionlevel = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
    v.masslist = np.array([['Al',26.981539],
                              ['Ar',39.948000],
                              ['Be', 9.012182],
                              ['C' ,12.010700],
                              ['Ca',40.078000],
                              ['Cl',35.453000],
                              ['Cr',51.996100],
                              ['Cu',63.546000],
                              ['D' , 2.014102],
                              ['Fe',55.845000],
                              ['Ga',69.723000],
                              ['Ge',72.640000],
                              ['H' , 1.007940],
                              ['He', 4.002602],
                              ['O' ,15.999400],
                              ['Mg',24.305000],
                              ['Mn',54.938045],
                              ['N' ,14.006700],
                              ['Na',22.989769],
                              ['Ne',20.179700],
                              ['Ni',58.693400],
                              ['P' ,30.973762],
                              ['S' ,32.065000],
                              ['Si',28.085500],
                              ['Ti',47.867000],
                              ['Zn',65.380000]],dtype=object)
    argument  = np.array(sys.argv, dtype='str')
    v.dispersion = 0.01
    if '--dispersion' in sys.argv:
        k = np.where(argument=='--dispersion')[0][0]
        v.dispersion = float(argument[k+1])
    v.plotdv = None
    if '--dv' in sys.argv:
        k = np.where(argument=='--dv')[0][0]
        v.plotdv = float(argument[k+1])
    v.zmid = None
    if '--zmid' in sys.argv:
        k = np.where(argument=='--zmid')[0][0]
        v.zmid = float(argument[k+1])
    v.extra = None
    if '--extra' in sys.argv:
        k = np.where(argument=='--extra')[0][0]
        v.extra = argument[k+1]
    v.headlist  = 'infort'
    if '--header' in sys.argv:
        k = np.where(argument=='--header')[0][0]
        v.headlist = np.loadtxt(argument[k+1],dtype='str',comments='!',delimiter='\n',ndmin=1)
    v.filename  = (datetime.now()).strftime('%y%m%d-%H%M%S')
    if '--output' in sys.argv:
        k = np.where(argument=='--output')[0][0]
        v.filename = argument[k+1]
    v.vpversion = 'vpfit'
    if '--version' in sys.argv:
        k = np.where(argument=='--version')[0][0]
        v.vpversion = argument[k+1]
    v.vpfsetup = './vp_setup.dat'
    os.environ['VPFSETUP'] = v.vpfsetup
    if '--vpfsetup' in sys.argv:
        k = np.where(argument=='--vpfsetup')[0][0]
        v.vpfsetup = argument[k+1]
        os.environ['VPFSETUP'] = v.vpfsetup
    if os.path.exists(v.vpfsetup)==True:
        v.pcvals,v.lastchtied,v.daoaun = 'no','z',1
        for line in np.loadtxt(v.vpfsetup,dtype='str',delimiter='\n'):
            if 'pcvals' in line and line.split()[0][0]!='!':
                v.pcvals = 'yes'
            if 'lastchtied' in line and line.split()[0][0]!='!':
                v.lastchtied = line.split()[1].lower()
            if 'daoaun' in line and line.split()[0][0]!='!':
                v.daoaun = float(line.split()[1])
    else:
        print 'ERROR: vp_setup.dat not found...'
        quit()
    v.atomdat = './atom.dat'
    os.environ['ATOMDIR'] = v.atomdat
    if '--atomdir' in sys.argv:
        k = np.where(argument=='--atomdir')[0][0]
        v.atomdat = argument[k+1]
        os.environ['ATOMDIR'] = v.atomdat
    if os.path.exists(v.atomdat):
        v.atom = atomlist(v.atomdat)
    else:
        print 'ERROR: atom.dat not found...'
        quit()
    return v

if sys.argv[0].split('/')[-1]!='velplot':
    pass
elif len(sys.argv)==1 or '--help' in sys.argv or '-h' in sys.argv:
    showhelp()
elif os.path.exists(sys.argv[1])==False:
    print "ERROR: spectrum '"+sys.argv[1]+"' not found..."
    quit()
else:
    sys.stderr.write('Import all relevant packages...')
    import re
    import numpy                           as np
    import matplotlib.pyplot               as plt
    import astropy.io.fits                 as fits
    from math                              import sqrt, pi
    from datetime                          import datetime
    from scipy                             import stats
    from matplotlib                        import rc
    from matplotlib.backends.backend_pdf   import PdfPages
    from scipy.ndimage                     import gaussian_filter1d
    from matplotlib.pyplot                 import figure,axis,subplots_adjust,title,text,plot,axhline,axvline
    print >>sys.stderr,' done!'
    setup = variables()
