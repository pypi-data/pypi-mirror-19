from .settings import *
from .readspec import *
from .voigt    import *

def plotfit(i,f):

    ''' Load data and model '''

    chunk = np.loadtxt('chunks/vpfit_chunk'+'%03d'%(i+1)+'.txt',comments='!')

    ibeg    = abs(chunk[:,0]-setup.table1[i][2]).argmin()+1 if setup.table1[i][2]!=setup.table1[i][3] else 0
    iend    = abs(chunk[:,0]-setup.table1[i][3]).argmin()-1 if setup.table1[i][2]!=setup.table1[i][3] else -1
    setup.wa = chunk[ibeg:iend,0]
    setup.fl = chunk[ibeg:iend,1]
    setup.er = chunk[ibeg:iend,2]
    setup.mo = chunk[ibeg:iend,3]
    wamid   = float(setup.comment[i,2])
    pos     = abs(setup.wa-wamid).argmin()
    vel     = 2*(setup.wa-wamid)/(setup.wa+wamid)*setup.c

    ''' Estimate the half-pixel size to shift the steps of the flux array when plotting '''
    
    pos    = abs(setup.wa-(setup.table1[i][2]+setup.table1[i][3])/2).argmin()
    pix1   = setup.wa[pos]
    pix2   = (setup.wa[pos]+setup.wa[pos-1])/2
    dempix = 2*(pix1-pix2)/(pix1+pix2)*setup.c
    
    ''' Plot residuals based on the flux, error, and model from the chunks '''

    axhline(y=1.6,color='magenta',zorder=2)
    axhline(y=1.7,color='magenta',ls='dotted',zorder=2)
    axhline(y=1.8,color='magenta',zorder=2)
    
    if '--nores' not in sys.argv and setup.table1[i][2]!=setup.table1[i][3]:
        velo = vel if '--unscale' in sys.argv else vel+setup.shift
        res  = (setup.fl-setup.mo)/setup.er/10+1.7
        plot(velo+dempix,res,lw=0.1,drawstyle='steps',color='magenta',zorder=3)

    ''' Plot model corrected for floating zero and continuum and velocity shift '''
    
    if setup.table1[i][2]!=setup.table1[i][3]:
        
        corr   = setup.cont+setup.slope*(setup.wa/((1+setup.z)*1215.6701)-1)
        model  = setup.mo/corr+setup.zero
        model  = model / (1+setup.zero)
        model  = setup.mo if '--unscale' in sys.argv else model
        velo   = vel if '--unscale' in sys.argv else vel+setup.shift
        plot(velo,model,lw=1.,color='lime',alpha=0.8,zorder=1)
        plot(velo+dempix,setup.er,lw=.1,drawstyle='steps',color='cyan')

    ''' Plot data '''

    if '--getwave' in sys.argv:
        readspec(i)
        wabeg   = wamid * (2*setup.c-setup.dv) / (2*setup.c+setup.dv)
        waend   = wamid * (2*setup.c+setup.dv) / (2*setup.c-setup.dv)
        ibeg    = abs(setup.specwa-wabeg).argmin()
        iend    = abs(setup.specwa-waend).argmin()
        ibeg    = ibeg-1 if ibeg>0 else ibeg
        iend    = iend+1 if iend<len(setup.specwa)-1 else iend
        setup.wa = setup.specwa[ibeg:iend]
        setup.fl = setup.specfl[ibeg:iend]
        pos     = abs(setup.wa-wamid).argmin()
        vel     = 2*(setup.wa-wamid)/(setup.wa+wamid)*setup.c

    corr   = setup.cont+setup.slope*(setup.wa/((1+setup.z)*1215.6701)-1)
    flux   = setup.fl/corr + setup.zero
    flux   = flux / (1+setup.zero)
    flux   = setup.fl if '--unscale' in sys.argv else flux
    velo   = vel if '--unscale' in sys.argv else vel+setup.shift
    plot(velo+dempix,flux,drawstyle='steps',lw=0.2,color='black',zorder=2)

    ''' Prepare high dispersion wavelength array '''

    start  = wamid * (2*setup.c-setup.dv) / (2*setup.c+setup.dv)
    end    = wamid * (2*setup.c+setup.dv) / (2*setup.c-setup.dv)
    val    = 1
    wave   = [start-2]
    dv     = setup.dispersion
    while wave[-1]<end+2:
        wave.append(wave[-1]*(2*setup.c+dv)/(2*setup.c-dv))
    wave   = np.array(wave)
    vel    = 2*(wave-wamid)/(wave+wamid)*setup.c
    vel    = vel-setup.shift if '--unscale' in sys.argv else vel
    model  = [1]*len(vel)
    show   = []
    
    for k in range(len(setup.table2)):

        complist = np.empty((0,2))
        
        z = float(re.compile(r'[^\d.-]+').sub('',setup.table2[k][2]))
        N = float(re.compile(r'[^\d.-]+').sub('',setup.table2[k][1]))
        b = float(re.compile(r'[^\d.-]+').sub('',setup.table2[k][3]))
        
        ''' Plot high dispersion Voigt profiles, lines, and labels for each component '''
                
        for p in range(len(setup.atom)):
            
            alpha = setup.table2[k][-2]*setup.daoaun
            cond1 = setup.table2[k][0]==setup.atom[p,0]
            cond2 = setup.table2[k][0] not in ['<>','>>','__','<<']
            cond3 = setup.wa[0] < (1+z)*float(setup.atom[p,1]) < setup.wa[-1]

            if cond1 and cond2 and cond3:

                lambda0 = float(setup.atom[p,1])

                if '--details' in sys.argv:

                    q       = float(setup.atom[p,5])
                    wavenum = 1./(lambda0*10**(-8))
                    wavenum = wavenum - q*(alpha**2-2*alpha)
                    lambda0 = 1/wavenum*10**(8)
                    f       = float(setup.atom[p,2])
                    gamma   = float(setup.atom[p,3])
                    profile = voigtmodel(N,b,wave/(z+1),lambda0,gamma,f)
                    model   = model*profile
                    vsig    = setup.table1[i][4]/dv
                    conv    = gaussian_filter1d(profile,vsig)
                    if '--unscale' in sys.argv:
                        corr = setup.cont+setup.slope*(wave/((1+setup.z)*1215.6701)-1)
                        conv = conv*corr-setup.zero
                        conv = conv/(1-setup.zero)
                    plot(vel,conv,lw=0.1,color='orange')

                if setup.atom[p,1]==setup.header[i][1] or abs(float(setup.atom[p,1])-float(setup.header[i][1])) > 0.1:
                    
                    lobs  = lambda0*(z+1)
                    vobs  = 2*(lobs-wamid)/(lobs+wamid)*setup.c
                    vobs  = vobs - setup.shift if '--unscale' in sys.argv else vobs
                    pos   = 1.08 if val%2==0 else 1.25
                    zdiff = abs(2*(z-setup.zmid)/(z+setup.zmid))
                    color = '#FF4D4D' if zdiff < 0.003 and setup.atom[p,0]==setup.header[i][0] and setup.atom[p,1]==setup.header[i][1] \
                            else '#9370db' if zdiff < 0.003\
                            else '#ba55d3' if zdiff > 0.003 and setup.atom[p,0] in ['HI','??'] \
                            else 'darkorange'
    
                    axvline(x=vobs,ls='dotted',color=color,lw=.2,zorder=1)
                    
                    lab1 = setup.table2[k][-3]
                    lab2 = ''.join(re.findall('[a-zA-Z]+',setup.table2[k][2][-2:]))
                    if setup.table2[k][2][-1].isdigit()==True and str(lab1)+color not in show:
                        t = text(vobs,pos,lab1,color=color,weight='bold',fontsize=7,horizontalalignment='center')
                        t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))
                        show.append(str(lab1)+color)
                        val = val + 1
                    elif setup.table2[k][2][-1].isdigit()==False and lab2+color not in show:
                        t = text(vobs,pos,lab2[-1],color=color,weight='bold',fontsize=7, horizontalalignment='center')
                        t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))
                        show.append(lab2+color)
                        val = val + 1                         
                    
    if '--details' in sys.argv:

        vsig  = setup.table1[i][4]/dv
        model = gaussian_filter1d(model,vsig)
        if '--unscale' in sys.argv:
            corr  = setup.cont+setup.slope*(wave/((1+setup.z)*1215.6701)-1)
            model = model*corr-setup.zero
            model = model/(1-setup.zero)
        plot(vel,model,lw=1.,color='orange',alpha=.5,zorder=1)

    axhline(y=1,color='black',ls='dotted')
    axhline(y=0,color='black',ls='dotted')
    
