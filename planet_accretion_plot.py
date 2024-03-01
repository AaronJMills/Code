import matplotlib.pyplot as plt
import numpy as np

#Open numpy binary file
data = np.load('r_sim9_planet_00_data.npz')

#Redefine lists
snap_time = data['array1'].tolist()
#accretion_5AU_list = data['array2'].tolist()
accretion_3AU_list = data['array3'].tolist()
accretion_sink_list = data['array4'].tolist()

#Plot resolution
plt.rcParams['savefig.dpi'] = 500

#Plot
fig, ax = plt.subplots()

start = 0
stop = 8000
#plt.plot(snap_time[start+2:stop+1], accretion_5AU_list[start+1:stop], label='5AU', alpha=0.8)
plt.plot(snap_time[start+2:stop+1], accretion_3AU_list[start+1:stop], label='3AU', alpha=0.8)
plt.plot(snap_time[start+2:stop+1], accretion_sink_list[start+1:stop], label='planet', alpha=0.8)

ax.set_title('Accretion rate within set radius over time')
ax.set_yscale('log')
plt.xlabel('Time (Years)')
plt.ylabel('Accretion rate (Jupiter masses per year)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)
ax.set_axisbelow(True)
plt.show()