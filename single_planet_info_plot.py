import matplotlib.pyplot as plt
import numpy as np

#Open numpy binary file
data = np.load('r_sim10_planet_00_sinkdata.npz')

#Redefine lists
snap_time = data['array1'].tolist()
rad_list = data['array2'].tolist()
mass_list = data['array3'].tolist()

#Plot resolution
plt.rcParams['savefig.dpi'] = 500

#Plots
fig, ax = plt.subplots(2, 1, sharex=True)

#skip = 0 #ignore the first skip number of snapshots

#Plot of mass against time
ax[0].plot(snap_time, mass_list)
ax[0].set_title('Mass against time')
ax[0].set_ylabel('Mass (Jupiter masses)')
ax[0].grid(True)

#Plot of radius against time
ax[1].plot(snap_time, rad_list)
ax[1].set_title('Radius against time')
ax[1].set_ylabel('Radius (AU)')
ax[1].grid(True)

plt.xlabel('Time (Years)')
plt.show()
