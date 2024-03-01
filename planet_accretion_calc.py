import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sarracen

#File name prefix and directory
file_name_prefix = 'r_sim10_planet_00'
directory = './sim10/'

#Create a list of the file names
num_of_files = 401 #if 3 digits, change {i:02} to {i:03}, and file_name_prefix
file_name_list = [f"{file_name_prefix}{i:03}" for i in range(0, num_of_files)]

#Create list of snapshot times (units = years)
delta_t = 20 #time between snapshots
snap_time = [i * delta_t for i in range(num_of_files)]

#read particle mass from first dump (same for all gas particles in all dumps)
sdf, sdf_sinks = sarracen.read_phantom(directory + file_name_prefix + '000')
gas_mass = sdf.params['mass'] * 1000 #m_jup

#Create accretion rate lists
r_list = []
accretion_5AU_list = []
accretion_3AU_list = []
accretion_sink_list = []

#Fills out lists with sink data
n = 0 #file number (will increment as the loop progresses)

for f in file_name_list:
	#Read in data using sarracen
	sdf, sdf_sinks = sarracen.read_phantom(directory + f)

	#Defining particles columns
	x = sdf['x'] #AU
	y = sdf['y'] #AU
	r = np.sqrt(x**2 + y**2)

	#Create a new dataframe of relevant particle values, and sort them by radius
	df2 = pd.DataFrame({'r': r, 'mass': gas_mass})
	df2 = df2.sort_values(by='r')

	#Calculate mass within set radii
	planet_mass = sdf_sinks.iloc[1, 3] * 1000 #m_jup
	mass_in_5AU = df2[df2['r'] <= 5]['mass'].sum() + planet_mass
	mass_in_3AU = df2[df2['r'] <= 3]['mass'].sum() + planet_mass

	#Calculate mass change and accretion rate
	if n != 0:
		#for 5AU radius
		mass_change_5AU = mass_in_5AU - last_mass_5AU
		accretion_5AU = mass_change_5AU/delta_t
		accretion_5AU_list.append(accretion_5AU)

		#for 3AU radius
		mass_change_3AU = mass_in_3AU - last_mass_3AU
		accretion_3AU = mass_change_3AU/delta_t
		accretion_3AU_list.append(accretion_3AU)

		#for planet
		mass_change_sink = planet_mass - last_sink_mass
		accretion_sink = mass_change_sink/delta_t
		accretion_sink_list.append(accretion_sink)

		#define last mass
		last_mass_5AU = mass_in_5AU
		last_mass_3AU = mass_in_3AU
		last_sink_mass = planet_mass
	else:
		last_mass_5AU = 0
		last_mass_3AU = 0
		last_sink_mass = 0

	n += 1

#Save data to file
array_snap_time = np.array(snap_time)
array_accretion_5 = np.array(accretion_5AU_list)
array_accretion_3 = np.array(accretion_3AU_list)
array_accretion_sink = np.array(accretion_sink_list)

output_name = f"{file_name_prefix}_data.npz"
np.savez(output_name, array1=array_snap_time, array2=array_accretion_5, array3=array_accretion_3, array4=array_accretion_sink)





