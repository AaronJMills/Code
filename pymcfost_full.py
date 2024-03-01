import subprocess
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pymcfost
import numpy as np

param = input('Enter mcfost parameter file name: ')
file = input('Enter phantom output file name: ')

response = input('Skip to plots (if data_th already created)? (y/n): ')

if response.lower() == 'n':
    #Run mcfost to create and fill data_th directory
    subprocess.Popen(['./mcfost', param, '-phantom', file]).wait()
    print('data_th directory created')
    print('----------------------------------')
    print(' ')

    #Creating image
    response1 = input('Create image? (y/n): ')

    if response1.lower() == 'y':
        wavelength = input('Enter desired wavelength for image creation (microns): ')
        #Run mcfost to create and fill selected wavelength data directory
        subprocess.Popen(['./mcfost', param, '-phantom', file, '-img', wavelength]).wait()
        print('data_' + wavelength + ' directory created')
        print('----------------------------------')
        print(' ')
    else:
        print('Skipping image creation')
else:
    print('Skipped to plots')


#Creating Plots
model = pymcfost.SED("./data_th/")

response2 = input('Create plot of SED at 0 inclination? (y/n): ')
response3 = input('Create plot of radial temperature profile? (y/n): ')
response4 = input('Create plot of 90 degree inclination (topdown) temperature profile? (y/n): ')

if response2.lower() == 'y':
    #SED at 0 inclination
    model.plot(0)

    plt.title(file + ' SED at 0 degree inclination')

    plt.rcParams['savefig.dpi'] = 500
    plt.savefig(file + '_SED_0_inc.png')

if response3.lower() == 'y':
    #Temperature profile
    plt.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    model.plot_T(log=True)

    plt.title(file + ' Temperature')

    plt.rcParams['savefig.dpi'] = 500
    plt.savefig(file + '_temp.png')

if response4.lower() == 'y':
    #pymcfost plot_T edited for 90 degree inclination

    grid = pymcfost.check_grid(model)
    plt.cla()

    T = model.T
    x = grid[0, :]
    y = grid[1, :]

    r = np.sqrt(x ** 2 + y ** 2)
    ou = r > 1e-6 # Removing star
    T = T[ou]
    x = x[ou]
    y = y[ou]

    Tmin = T.min()
    Tmax = T.max()

    plt.scatter(x, y, c=T, s=0.1, norm=mcolors.LogNorm(vmin=Tmin, vmax=Tmax))
    cb = plt.colorbar()
    cb.set_label('T [K]')
    plt.xlabel('x [au]')
    plt.ylabel('y [au]')
    plt.title(file + ' Temperature')

    plt.rcParams['savefig.dpi'] = 500
    plt.savefig(file + '_topdown_temp.png')

print('Done')