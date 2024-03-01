import matplotlib.pyplot as plt
import numpy as np
import sarracen

#File name prefix and directory
file_name_prefix = 'test_planet_000'
directory = 'test/'

#Create a list of the file names
num_of_files = 97 #if 3 digits, change {i:02} to {i:03}, and file_name_prefix
file_name_list = [f"{file_name_prefix}{i:02}" for i in range(0, num_of_files)]

#Create list of snapshot times (units = years)
delta_t = 20 #time between snapshots
snap_time = [i * delta_t for i in range(num_of_files)]

rad_list = []
mass_list = []

#Fills out lists with sink data
n = 0 #file number (will increment as the loop progresses)

for f in file_name_list:
    sdf, sdf_sinks = sarracen.read_phantom(directory + f)
        #applies phantom data to 2 arrays, particle data and sink data
    
    x_values = sdf_sinks.iloc[1, 0] #x value of star (relative to planet)
    y_values = sdf_sinks.iloc[1, 1] #y value of star (relative to planet)
    rads = np.sqrt(x_values**2 + y_values**2) #distance from the planet
    mass = sdf_sinks.iloc[1, 3]*1000 #convert to Jupiter masses
    
    #append planet values to lists
    rad_list.append(rads)
    mass_list.append(mass)
    
    n += 1

#Save data to file
array_snap_time = np.array(snap_time)
array_rad = np.array(rad_list)
array_mass = np.array(mass_list)

output_name = f"{file_name_prefix}_sinkdata.npz"
np.savez(output_name, array1=array_snap_time, array2=array_rad, array3=array_mass)
