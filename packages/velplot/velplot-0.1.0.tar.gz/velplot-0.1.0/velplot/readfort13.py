from .settings import *
from .atominfo import *

def do13():
    
    """
    Read fort.13
    """
    
    fort = open(setup.fortfile,'r')
    line13 = []
    for line in fort:
        if len(line.split())==0: break
        elif line[0]!='!': line13.append(line.replace('\n',''))

    # Prepare table1, initialise atomic header array, and get mid redshift of the system
    # Info sorted as followed: filename - position - lambinit - lambfina - sigvalue

    setup.header  = np.empty((0,9))                # [element,wavelength,oscillator,gammavalue,qcoeff,chisq,chisqnu,npix,ndf]
    setup.comment = np.empty((0,3))                # [headerline,comment,wamid]
    setup.table1  = []
    i = 1
    while line13[i].split()[0]!='*':
        l = line13[i].split()
        headline = line13[i].split('!')[-1] if type(setup.headlist)==str else setup.headlist[i-1]
        setup.header  = np.vstack([setup.header,atominfo(headline.split()[0])+[0,0,0,0]])
        setup.comment = np.vstack([setup.comment,[headline,'-',0]])
        dv  = l[4].split('=')[1].split('!')[0]
        dv  = dv if isfloat(dv)==False else float(dv) if 'vsig' in l[4] else float(dv)/(2*np.sqrt(2*np.log(2)))
        setup.table1.append([l[0],float(l[1]),float(l[2]),float(l[3]),dv])
        i=i+1

    ''' Prepare table2 listing all the components '''

    setup.table2 = []
    idx = 1
    for i in range(i+1,len(line13)):
        
        l = line13[i].split('!')[0].split()

        species  = l[0] if len(l[0])>1 else l[0]+l[1]
        coldens  = l[1] if len(l[0])>1 else l[2]
        redshift = l[2] if len(l[0])>1 else l[3]
        doppler  = l[3] if len(l[0])>1 else l[4]
        alpha    = l[4] if len(l)==8 else l[5] if len(l)==9 else 0
        region   = int(l[-1])
        
        if type(alpha)==str:
            if 'E-' in alpha:
                expon = re.compile(r'[^\d.-]+').sub('',alpha.split('E-')[-1])
                alpha = float(alpha.split('E-')[0])*10**-float(expon)
            elif 'E+' in alpha:
                expon = re.compile(r'[^\d.-]+').sub('',alpha.split('E+')[-1])
                alpha = float(alpha.split('E+')[0])*10**float(expon)
            else:
                alpha = float(re.compile(r'[^\d.-]+').sub('',alpha))
                
        mode = 'thermal' if float(l[-3])==float(l[-2])==0 else 'turbulent'
            
        setup.table2.append([species,coldens,redshift,doppler,region,idx,alpha,mode])

        idx=idx+1

    ''' Modify column density to summed column densities if necessary '''
    
    for k in range(len(setup.table2)):
        N   = re.compile(r'[^\d.-]+').sub('',setup.table2[k][1])
        tie = ''.join(re.findall('[a-zA-Z%]+',setup.table2[k][1][-2:]))
        if setup.table2[k][0] not in ['<>','>>','__','<<'] and setup.table2[k][1][-1].isdigit()==False:
            N    = 10**float(N)
            tie0 = ''.join(re.findall('[a-zA-Z%]+',setup.table2[k-1][1][-2:]))
            tie1 = ''.join(re.findall('[a-zA-Z%]+',setup.table2[k][1][-2:]))
            if '%' in tie1:
                for l in range(k+1,len(setup.table2)):
                    tie2 = ''.join(re.findall('[a-zA-Z%]+',setup.table2[l][1][-2:]))
                    if tie2==tie0.upper() and ord(tie2[0].lower())>=ord(setup.lastchtied):
                        N = N - 10**float(re.compile(r'[^\d.-]+').sub('',setup.table2[l][1]))
                    else:
                        break
            elif '%' not in tie0 and tie1!=tie0 and ord(tie1[0].lower())>=ord(setup.lastchtied):
                for l in range(k+1,len(setup.table2)):
                    tie2 = ''.join(re.findall('[a-zA-Z%]+',setup.table2[l][1][-2:]))
                    if tie2==tie1:
                        N = N - 10**float(re.compile(r'[^\d.-]+').sub('',setup.table2[l][1]))
                    else:
                        break
            N = '%.6f'%np.log10(N)
        setup.table2[k][1] = N+tie

    ''' Modify Doppler selfeter if thermally tied '''
    
    for k in range(len(setup.table2)):
        id0   = setup.table2[k][0]
        b0    = setup.table2[k][3]
        mode  = setup.table2[k][-1]
        val0  = re.compile(r'[^\d.-]+').sub('',b0)
        tie0  = ''.join(re.findall('[a-zA-Z%]+',b0[-2:]))
        if tie0.islower()==True and id0 not in ['<>','>>','__','<<']:
            mass0 = atommass(id0)
            for l in range(len(setup.table2)):
                id1   = setup.table2[l][0]
                b1    = setup.table2[l][3]
                val1  = re.compile(r'[^\d.-]+').sub('',b1)
                tie1  = ''.join(re.findall('[a-zA-Z%]+',b1[-2:]))
                if tie1==tie0.upper() and mode=='thermal':
                    mass1 = atommass(id1)
                    val1  = '%.6f'%(np.sqrt(mass0/mass1)*float(val0))
                    setup.table2[l][3] = val1+tie1
                if tie1==tie0.upper() and mode=='turbulent':
                    setup.table2[l][3] = val0+tie1
                    
    ''' Modify Redshift selfeter if tied '''
    
    for k in range(len(setup.table2)):
        id0   = setup.table2[k][0]
        z0    = setup.table2[k][2]
        val0  = re.compile(r'[^\d.-]+').sub('',z0)
        tie0  = ''.join(re.findall('[a-zA-Z%]+',z0[-2:]))
        if tie0.islower()==True and id0 not in ['<>','>>','__','<<']:
            for l in range(len(setup.table2)):
                id1   = setup.table2[l][0]
                z1    = setup.table2[l][2]
                val1  = re.compile(r'[^\d.-]+').sub('',z1)
                tie1  = ''.join(re.findall('[a-zA-Z%]+',z1[-2:]))
                if tie1==tie0.upper():
                    setup.table2[l][2] = val0+tie1
                    
