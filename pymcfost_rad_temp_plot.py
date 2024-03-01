import numpy as np
import pymcfost
from scipy import stats
import matplotlib.pyplot as plt

#Read data using pymcfost
model = pymcfost.SED("./data_th/")

grid = pymcfost.check_grid(model)

T = model.T #K
x = grid[0, :]
y = grid[1, :]
r = np.sqrt(x ** 2 + y ** 2) #au

def calculate_mean(binned_quantity, mean_quantity, bins):
    #Radially binned mean
    bins = np.logspace(np.log10(1), np.log10(5), bins)
    return stats.binned_statistic(binned_quantity, mean_quantity, 'mean', bins=bins)

bin_number = 11
rad_temp = calculate_mean(r, T, bin_number)

plt.figure()

x_values = rad_temp[1][:bin_number-1]
y_values = rad_temp[0]

#Filter out the nan values from y_values
valid = ~np.isnan(y_values)
x_values = x_values[valid]
y_values = y_values[valid]

#print(x_values)
#print(y_values)

plt.scatter(x_values, y_values, s=3, c='black')

#Best-fit line
coefficients = np.polyfit(np.log10(x_values), y_values, 1)

poly_x = np.linspace(min(x_values), max(x_values), 100)
poly_y = coefficients[0] * np.log10(poly_x) + coefficients[1]

#print(poly_x)
#print(poly_y)

plt.plot(poly_x, poly_y, color='lightblue')

plt.xscale('log')
plt.xlabel('Radius (au)')
plt.ylabel('Temperature (K)')
plt.title('Radially Binned Temperature')

plt.rcParams['savefig.dpi'] = 500
plt.savefig('radial_temp.png')
