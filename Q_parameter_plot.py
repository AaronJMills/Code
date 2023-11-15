import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sarracen

#File name and directory
file_name = 'test10_00040'
directory = 'Test10/test10/'

#Converting ASCII file to csv and reading in csv file for particle data
df = pd.read_csv(directory + file_name + '.ascii', sep='\s+', comment='#')
df.to_csv(directory + file_name + '.csv', index=None)
df = pd.read_csv(directory + file_name + '.csv')

#Reading in sink data from output file
sdf, sdf_sinks = sarracen.read_phantom(directory + file_name)
#defining mass and radii of sinks
masses = sdf_sinks.iloc[:, 3] * 1.988E30 #kg
x_values = sdf_sinks.iloc[:, 0]
y_values = sdf_sinks.iloc[:, 1]
rads_AU = np.sqrt(x_values**2 + y_values**2)
rads = np.sqrt(x_values**2 + y_values**2) * 1.495978707E11 #m

#Limiting the dataframe to only rows corresponding to gas particles
df = df[df.iloc[:, 13] == 1] #itype = 1

#Defining particles columns
x = df.iloc[:, 0] #AU
y = df.iloc[:, 1] #AU
r = np.sqrt(x**2 + y**2)
r_m = r * 1.495978707E11 #m
Temp = df.iloc[:, 6] #K
mass = df.iloc[:, 3] #m_sol
mass_kg = mass * 1.988E30 #kg

#Defining constants
k = 1.3806E-23 #J/K
mu = 2.381 #mean molecular weight
h_mass = 1.67E-27 #(hydrogen mass) kg
G = 6.6743E-11 #N*m^2*kg^-2

#Create a new dataframe of relevant particle values, and sort them by radius
df2 = pd.DataFrame({'r_m': r_m, 'mass_kg': mass_kg, 'Temp': Temp})
df2 = df2.sort_values(by='r_m')

#add a cumulative particle mass column to the dataframe
df2['cu_pmass'] = df2['mass_kg'].cumsum()

#add a cumulative sink mass column to the dataframe
df2['cu_smass'] = 0.0 #adds column with 0 values

for index, row in df2.iterrows():
    smaller_rad = rads[rads < row['r_m']]
    cu_smass = masses[rads < row['r_m']].sum()
    df2.at[index, 'cu_smass'] = cu_smass
   
#Parameter calculations
n = 4 #intervals per 1 AU
r_interval = (1.495978707E11)/n #m
Q_list = []
r_list = []
sigma_list = []
temp_list = []

#Sound speed calculation (add to dataframe)
df2['cs'] = np.sqrt((k * Temp)/(mu * h_mass))
    #this line a causes warning due to a small amount of temp values being negative
    #as its an insignificant amount, the warning can be ignored for now
    #the cs column will have nan for rows with -temp

#Omega calculation (add to dataframe)
df2['omega'] = np.sqrt((G*(df2['cu_pmass'] + df2['cu_smass']))/r_m**3)

for i in range(n*100): #calculates up to 100 * r_interval
    r1 = i*r_interval
    r2 = (i+1)*r_interval
    r_average = ((r1+r2)/(2*1.495978707E11))
    r_list.append(r_average) #r_average in AU (for plot)

    #Limit the dataframe for the radius interval
    limited_df = df2.loc[(df2['r_m'] >= r1) & (df2['r_m'] < r2)]
    
    #calculate the average values of cs and omega for the interval
    cs_average = limited_df['cs'].mean()
    omega_average = limited_df['omega'].mean()
    
    #calculate the interval mass, not including the mass of sinks within the interval
    interval_mass = limited_df['mass_kg'].sum()

    #calculate surface density for the interval
    sigma = interval_mass/(np.pi*((r2**2)-(r1**2)))
    sigma_list.append(sigma)
    
    #calculate the average temperature of each interval for plots
    Temp_average = limited_df['Temp'].mean()
    temp_list.append(Temp_average)

    #calculate the toomre parameter for each interval
    Q = (cs_average*omega_average)/(np.pi*G*sigma)
    Q_list.append(Q)

#Smoothing the Q plot and sigma plot values to 1 AU intervals
smoothed_Q_list = []
smoothed_r_list = []
smoothed_sigma_list = []
for i in range(0, len(Q_list), n):
    Qgroup = Q_list[i:i+n]
    averageQ = sum(Qgroup)/len(Qgroup)
    smoothed_Q_list.append(averageQ)
    
    Rgroup = r_list[i:i+n]
    averageR = sum(Rgroup)/len(Rgroup)
    smoothed_r_list.append(averageR)

    sigmagroup = sigma_list[i:i+n]
    averagesigma = sum(sigmagroup)/len(sigmagroup)
    smoothed_sigma_list.append(averagesigma)

#Plots
#Plot resolution
plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500

#%% Toomre parameter against radius
fig, ax = plt.subplots()

skip = 10 #to ignore the first few outlying data points
plt.plot(smoothed_r_list[skip:], smoothed_Q_list[skip:])
rads_AU_to100 = rads_AU[rads_AU <= 100] #only plots sinks within 100AU
plt.scatter(rads_AU_to100[1:], [3.5]*len(rads_AU_to100[1:]), c='red', edgecolor='black')
    #plots dots with black outline on sink location

ax.set_title('Toomre parameter against radius: ' + file_name)
plt.ylabel('Toomre parameter Q')
plt.xlabel('Radius (AU)')
plt.grid(True)
ax.set_axisbelow(True)

#%% Surface density against radius
fig, ax = plt.subplots()

skip = 2 #to ignore the first few outlying data points
plt.plot(smoothed_r_list[skip:], smoothed_sigma_list[skip:])

ax.set_title('Surface density against radius: ' + file_name)
plt.ylabel('Surface density (g/cm^2)')
plt.xlabel('Radius (AU)')
plt.grid(True)
ax.set_axisbelow(True)

#%% Average temperature against radius
fig, ax = plt.subplots()

skip = 5 #to ignore the first few outlying data points
plt.scatter(r_list[skip:], np.log10(temp_list[skip:]), s=1)

ax.set_title('Average temperature against radius: ' + file_name)
plt.ylabel('log Temperature (K)')
plt.xlabel('Radius (AU)')
plt.grid(True)
ax.set_axisbelow(True)
