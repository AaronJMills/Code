import matplotlib.pyplot as plt
import numpy as np
import sarracen

#File name prefix and directory
file_name_prefix = 'test10_00'
directory = 'Test10/test10/'

#Create a list of the file names
num_of_files = 300 #if 3 digits, change {i:02} to {i:03}, and file_name_prefix
file_name_list = [f"{file_name_prefix}{i:03}" for i in range(0, num_of_files)]

#Create list of snapshot times (units = years)
delta_t = 37.5 #time between snapshots
snap_time = [i * delta_t for i in range(num_of_files)]

#Creates lists of lists with the number of lists = final sink number
n_lists = 13
all_rad_lists = [[] for _ in range(n_lists)]
all_mass_lists = [[] for _ in range(n_lists)]

#Fills out lists with sink data
n = 0 #file number (will increment as the loop progresses)

for f in file_name_list:
    sdf, sdf_sinks = sarracen.read_phantom(directory + f)
        #applies phantom data to 2 arrays, particle data and sink data
    
    x_values = sdf_sinks.iloc[:, 0]
    y_values = sdf_sinks.iloc[:, 1]
    x_values_r = x_values - sdf_sinks.iloc[0, 0] #x values relative to the star
    y_values_r = y_values - sdf_sinks.iloc[0, 1] #y values relative to the star
    rads = np.sqrt(x_values_r**2 + y_values_r**2) #distance from the star
    masses = sdf_sinks.iloc[:, 3]
    
    #append the radius and mass values to the corresponding list for that sink    
    for sink_num in range(len(sdf_sinks)):
        all_rad_lists[sink_num].append(rads[sink_num])
        all_mass_lists[sink_num].append(masses[sink_num])
    
    n += 1

#Plots
#Plot resolution
plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500

#increases the number of different plot colours from 10 to 20
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab20.colors)

#%% Sink masses over time
fig, ax = plt.subplots()

#Fills the mass list with "none" values for times before sink formation
padded_lists = [[None] * (n - len(sublist)) + sublist for sublist in all_mass_lists[1:]]
    #star lists ([0:]) not included on plot

#Plots mass against time for each sink
skip = 0 #ignore the first skip number of snapshots
for i, sublist in enumerate(padded_lists):
    plt.plot(snap_time[skip:len(sublist)], sublist[skip:], label=f'Sink {i+1}')
        #sinks labeled as sink {i+1} as sink 0 excluded from padded_list

ax.set_title('Masses against time')
plt.xlabel('Time (Years)')
plt.ylabel('Mass (solar masses)')
plt.ylim(0, 0.05)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)
ax.set_axisbelow(True)


#%% Sink radii over time
fig, ax = plt.subplots()

#Fills the radius list with "none" values for times before sink formation
padded_lists = [[None] * (n - len(sublist)) + sublist for sublist in all_rad_lists[1:]]
    #star lists ([0:]) not included on plot

#Plots radius against time for each sink
skip = 160 #ignore the first skip number of snapshots
for i, sublist in enumerate(padded_lists):
    plt.plot(snap_time[skip:len(sublist)], sublist[skip:], alpha = 0.7, label=f'Sink {i+1}')
        #sinks labeled as sink {i+1} as sink 0 excluded from padded_list

ax.set_title('Radii against time')
plt.xlabel('Time (Years)')
plt.ylabel('Radii (AU)')
plt.ylim(0, 300)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)
ax.set_axisbelow(True)
