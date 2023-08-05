from .settings import *
from .atominfo import *
    
def getdv():

    ''' Calculate mid-redshift among all fitting regions '''
    
    zreg = np.empty((0,2))
    for j in range (len(setup.table1)):
        comment = setup.comment[j,0].split()
        if 'external' not in comment:
            zmin = float(setup.table1[j][2])/float(setup.header[j,1])-1
            zmax = float(setup.table1[j][3])/float(setup.header[j,1])-1
        else:
            # Get redshit edges of the external fitting region
            wref = float(atominfo(comment[0])[1])
            wmin = setup.table1[j][2]
            wmax = setup.table1[j][3]
            zmin = float(wmin)/wref-1
            zmax = float(wmax)/wref-1
            # Get wavelength edges of the associated tied region
            wref = float(atominfo(comment[2])[1])
            wmin = wref*(zmin+1)
            wmax = wref*(zmax+1)
            # Get redshift edges of the corresponding overlapping region
            wref = float(atominfo(gettrans(comment[2]))[1])
            zmin = float(wmin)/wref-1
            zmax = float(wmax)/wref-1
        zreg = np.vstack([zreg,[zmin,zmax]])
    setup.zmid = (min(zreg[:,0])+max(zreg[:,1]))/2.

    ''' Calculate maximum velocity dispersions '''
    
    setup.dv = 0
    for j in range (len(setup.header)):
        comment = setup.comment[j,0].split()
        if 'external' in comment:
            wref    = float(setup.header[j,1])
            # Wavelength at setup.zmid in the overlapping region
            reg     = float(atominfo(gettrans(comment[2]))[1])*(setup.zmid+1)
            # Transition wavelength of the overlapping element
            atom    = float(atominfo(comment[2])[1])
            # Central wavelength of external tied transition for the overlapped system
            wamid   = wref*(reg/atom)
            text    = comment[0]+' at z='+str(round(wamid/float(setup.header[j,1])-1,6))
            dvmin   = abs(2*(setup.table1[j][2]-wamid)/(setup.table1[j][2]+wamid))*setup.c
            dvmax   = abs(2*(setup.table1[j][3]-wamid)/(setup.table1[j][3]+wamid))*setup.c
            setup.dv = max(setup.dv,dvmin,dvmax)
        elif 'overlap' in comment:
            wamid   = float(setup.header[j,1])*(setup.zmid+1)
            text    = comment[2]+' at z='+str(round(wamid/float(atominfo(comment[2])[1])-1,6))
            dvmin   = abs(2*(setup.table1[j][2]-wamid)/(setup.table1[j][2]+wamid))*setup.c
            dvmax   = abs(2*(setup.table1[j][3]-wamid)/(setup.table1[j][3]+wamid))*setup.c
            setup.dv = max(setup.dv,dvmin,dvmax)
        else:
            wamid   = float(setup.header[j,1])*(setup.zmid+1)
            text    = '-'
            dvmin   = abs(2*(setup.table1[j][2]-wamid)/(setup.table1[j][2]+wamid))*setup.c
            dvmax   = abs(2*(setup.table1[j][3]-wamid)/(setup.table1[j][3]+wamid))*setup.c
            setup.dv = max(setup.dv,dvmin,dvmax)
        setup.comment[j,1:] = [text,wamid]
    setup.dv = setup.plotdv if setup.plotdv!=None else 150 if setup.dv<150 else setup.dv

def gettrans(overlaptrans):

    ''' Get which of the system's transition overlaps with the external system '''

    for k in range (len(setup.comment)):
        headline = setup.comment[k,0].split()
        if 'overlap' in headline and headline[2]==overlaptrans:
            break
        
    return headline[0]
