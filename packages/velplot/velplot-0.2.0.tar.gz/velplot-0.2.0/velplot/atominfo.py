""" Prepare atomic data list and look for specific transition """

from .settings import *

def atominfo(atomID):     # Get atomic data from selected atomID
    target = [0,0,0,0,0]
    atomID = atomID.split('_')
    imet   = np.where(setup.atom[:,0]==atomID[0])[0]
    wmet   = [abs(float(setup.atom[i,1])-float(atomID[1])) for i in imet]
    iref   = imet[wmet.index(min(wmet))]
    wref   = float(setup.atom[iref,1])
    for i in imet:
        element    = setup.atom[i,0]
        wavelength = setup.atom[i,1]
        oscillator = setup.atom[i,2]
        gammavalue = setup.atom[i,3]
        qcoeff     = setup.atom[i,5]
        cond1      = abs( float(wavelength) - wref ) < 0.1
        cond2      = float(oscillator) > float(target[2])
        if cond1 and cond2:
            target = [element,wavelength,oscillator,gammavalue,qcoeff]
    if target==[0,0,0,0,0]:
        print 'Element ID not identifiable...'
        quit()
    return target

def atommass(species):     # Store data from atom.dat
    
    mass = None
    for i in range(len(setup.masslist)):
        for j in setup.ionlevel:
            if species==setup.masslist[i,0]+j:
                mass = setup.masslist[i,1]
    if mass==None:
        print 'Atomic mass not found for',species
        quit()
    return mass
