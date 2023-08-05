from .settings import *

def createchunks():

    opfile = open('fitcommands','w')
    opfile.write('d\n')                 # Run display command + enter
    if setup.pcvals=='yes':              # If development tools called...
        opfile.write('\n')              # ...used default setup -> enter only
    opfile.write('\n')                  # Used default selfeter (logN) -> enter only
    opfile.write(setup.fortfile+'\n')    # Insert fort file name + enter
    opfile.write('\n')                  # Plot the fitting region (default is yes) -> enter only
    opfile.write('\nas')
    for line in setup.table1:
        opfile.write('\n\n\n\n')
    opfile.write('\n\n\nn\n\n')
    opfile.close()

    os.system(setup.vpversion+' < fitcommands > termout')
    output = np.loadtxt('termout',dtype='str',delimiter='\n')
    for i in range(len(output)):
        if 'Statistics for each region :' in output[i]:
            i,k = i+2,0
            while 'Plot?' not in output[i]:
                setup.header[k,-4] = 'n/a' if '*' in output[i].split()[2] else '%.4f'%(float(output[i].split()[2]))
                setup.header[k,-3] = 'n/a' if '*' in output[i].split()[2] else '%.4f'%(float(output[i].split()[2])/float(output[i].split()[4]))
                setup.header[k,-2] = output[i].split()[3]
                setup.header[k,-1] = output[i].split()[4]
                k = k + 1
                i = i + 2
    
    if os.path.exists('chunks')==False:
        os.system('mkdir chunks')
    os.system('mv vpfit_chunk* chunks/')
    os.system('rm fitcommands termout')
    
