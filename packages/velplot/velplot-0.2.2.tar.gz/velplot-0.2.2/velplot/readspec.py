from .settings import *

def readspec(i):

    specfile = setup.table1[i][0]
    datatype = specfile.split('.')[-1]
    wavefile = specfile.replace('.fits','.wav.fits')
    if datatype=='fits' and os.path.exists(wavefile)==True:
        fh = fits.open(wavefile)
        hd = fh[0].header
        setup.specwa = fh[0].data
        fh = fits.open(specfile)
        hd = fh[0].header
        setup.specfl = fh[0].data        
    elif datatype=='fits':
        fh = fits.open(specfile)
        hd = fh[0].header
        d  = fh[0].data
        if ('CTYPE1' in hd and hd['CTYPE1'] in ['LAMBDA','LINEAR']) or ('DC-FLAG' in hd and hd['DC-FLAG']=='0'):
            setup.specwa = hd['CRVAL1'] + (hd['CRPIX1'] - 1 + np.arange(hd['NAXIS1']))*hd['CDELT1']
        else:
            setup.specwa = 10**(hd['CRVAL1'] + (hd['CRPIX1'] - 1 + np.arange(hd['NAXIS1']))*hd['CDELT1'])
        if len(d.shape)==1:
            setup.specfl = d[:]
        else:
            setup.specfl = d[0,:]
    else:
        d = np.loadtxt(specfile,comments='!')
        setup.specwa = d[:,0]
        setup.specfl = d[:,1]
