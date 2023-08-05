from .settings import *

def checkshift(i):

    left  = setup.table1[i][2]
    right = setup.table1[i][3]
    
    setup.shift,setup.cont,setup.slope,setup.z,setup.zero = 0,1,0,0,0

    for j in range(len(setup.table2)):

        val = setup.table2[j][0]
        N   = float(re.compile(r'[^\d.-]+').sub('',setup.table2[j][1]))
        z   = float(re.compile(r'[^\d.-]+').sub('',setup.table2[j][2]))
        b   = float(re.compile(r'[^\d.-]+').sub('',setup.table2[j][3]))
        reg = setup.table2[j][4]
        if val==">>" and (reg==i+1 or (reg==0 and left<1215.6701*(z+1)<right)):
            t = text(-.5*setup.dv,-.43,'>> %.5f km/s'%b,color='blue',fontsize=5)
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
            setup.shift = -b
        if val=="<>" and (reg==i+1 or (reg==0 and left<1215.6701*(z+1)<right)):
            t = text(-.5*setup.dv,-.28,'<> %.5f'%N,color='blue',fontsize=5)
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
            setup.cont  = N
            setup.slope = b
            setup.z     = z
        if val=="__" and (reg==i+1 or (reg==0 and left<1215.6701*(z+1)<right)):
            t = text(-.27*setup.dv,-.28,'__ %.5f'%N,color='blue',fontsize=5)
            t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
            setup.zero = -N

    ''' Insert comments in figure '''

    t1 = text(-.97*setup.dv,-.4,str(setup.header[i,0])+' '+str('%.2f'%float(setup.header[i,1])),color='blue',fontsize=10,ha='left')
    t2 = text(-.1*setup.dv,-.28,' f = %.4f'%float(setup.header[i,2]),color='blue',fontsize=5,ha='left')
    t3 = text(.1*setup.dv,-.28,' $\chi^2_{\mathrm{abs}}$ = '+setup.header[i,-4],color='blue',fontsize=5,ha='left')
    t5 = text(.1*setup.dv,-.43,'npix = '+setup.header[i,-2],color='blue',fontsize=5,ha='left')
    t4 = text(.35*setup.dv,-.28,' $\chi^2_{\mathrm{red}}$ = '+setup.header[i,-3],color='blue',fontsize=5,ha='left')
    t6 = text(.35*setup.dv,-.43,'ndf  = '+setup.header[i,-1],color='blue',fontsize=5,ha='left')
    t7 = text(.97*setup.dv,-.4,str(i+1)+' - '+str(setup.table1[i][0].split('/')[-1]),color='blue',fontsize=7,ha='right')
    for t in [t1,t2,t3,t4,t5,t6,t7]:
        t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))

    if setup.header[i,4]!='0':
        t = text(-.1*setup.dv,-.43,'q = %.0f'%float(setup.header[i,4]),color='blue',fontsize=5,ha='left')
        t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
    if 'overlap' in setup.comment[i,0]:
        t = text(.97*setup.dv,.3,'Overlapping system:\n'+setup.comment[i,1],color='darkorange',weight='bold',fontsize=6,horizontalalignment='right')
        t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
    if 'external' in setup.comment[i,0]:
        t = text(.97*setup.dv,.3,'External system:\n'+setup.comment[i,1],color='darkorange',weight='bold',fontsize=6,horizontalalignment='right')
        t.set_bbox(dict(color='white', alpha=0.5, edgecolor=None))        
        
