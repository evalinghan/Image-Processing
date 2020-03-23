
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.stats import kde
from scipy.stats import linregress
import csv
print('Running functions')

def calculate_all_params(lst_IR,lst_RED,lst_BG):
    '''
    This fundtion reads all the IR, RED, and BG band values for each pixel of a 3-band image.
    It then calcualates band ratios and the band profile angle. 
    
    Input:
        Lists of IR, RED, and BG bands of each pixel from 3-band image
    Output:
        angles: list of all calculated angles of band profile within each pixel of image
        IR_BG: list of all calculated IR/BG ratios within each pixel of image
    '''
    angles = []
    x1 = 0.01 #arbitrary selection of position of band
    x2 = 0.02 #arbitrary selection of position of band
    x3 = 0.03 #arbitrary selection of position of band

    #First calculating the distance between IR and BG bands through trig formulas
    distance_1 = []
    for i in range(len(lst_IR)):
        y1 = lst_BG[i]
        y3 = lst_IR[i]    
        distance = math.sqrt(((x3 - x1) ** 2) + ((y3 - y1) ** 2))
        distance_1.append(distance)
    #First calculating the distance between BG and RED bands through trig formulas
    distance_2 = []
    for i in range(len(lst_IR)):
        y1 = lst_BG[i]
        y2 = lst_RED[i]    
        distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
        distance_2.append(distance)
    #First calculating the distance between IR and RED bands through trig formulas
    distance_3 = []
    for i in range(len(lst_IR)):
        y3 = lst_IR[i]
        y2 = lst_RED[i]    
        distance = math.sqrt(((x3 - x2) ** 2) + ((y3 - y2) ** 2))
        distance_3.append(distance)
    #By approximating the bands as a triangle, we can now calculate the spectal angle of this triangle by trig formulas
    #If needed you can easily calculate the area of this triangle using this angle and trig formulas
    slopes_remove = []
    for i in range(len(distance_1)):
        c = distance_1[i]
        a = distance_2[i]
        b = distance_3[i]
        inside = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        if inside > 1 or inside < -1: #Some of the pixels have anomalous values - so I'm storing these to eventually remove from data
            slopes_remove.append(i)
        else:
            angle = math.acos(inside)
            angles.append(angle)
    #Removing anomalous pixels from data    
    for i in slopes_remove:
        distance_1.remove(distance_1[i])
        distance_2.remove(distance_2[i])
        distance_3.remove(distance_3[i])
    #Next I'm calculating the ratios if IR and BG bands.
    #Here you could easily calculate any other band ratios, ie. BG/RED, IR/RED, etc. 
    IR_BG = []
    for i in range(len(lst_IR)):
        IR_BG.append(lst_IR[i]/lst_BG[i])
    
    return (angles,IR_BG)

def filter_for_nan(angles,IRdivBG):
    '''
    This function filters the data and removes any NaN and inf values resulting from calculations.
    In most cases, this is not needed but somtimes NaN values appear
    Input:
        lists of calculated angels and IR/BG
    Output:
        lists of calcualted angles and IR/BG that have been filered for NaN and inf values
    '''
    all_angles = np.array(angles)
    all_IRdivBG = np.array(IRdivBG)

    indices_1 = np.logical_not(np.logical_or(np.isnan(all_angles),np.isnan(IRdivBG))) #check for nan 
    all_angles = all_angles[indices_1] #remove any nan data
    all_IRdivBG = all_IRdivBG[indices_1] #remove any nan data
    
    indices_2 = []
    for i in range(all_angles.__len__()): #check for inf
        if np.isinf(all_angles[i]):
            indices_2.append(i)
    all_angles_filtered = np.delete(all_angles,indices_2) #remove any inf
    all_IRdivBG_filtered = np.delete(all_IRdivBG, indices_2) #remove any inf
    
    return (all_angles_filtered, all_IRdivBG_filtered)
#_______________________________________________________________________________

print('Loading textfile...')
Data = np.loadtxt('Data/Extract_mb_79/all-rasters.xyz',delimiter=",")
IR = list(Data[:,3])
RED = list(Data[:,4])
BG = list(Data[:,5])
print('Calculating params...')
angles,IR_BG = calculate_all_params(IR,RED,BG)
print('Filtering data....')
(all_angles_filtered,all_IRdivBG_filtered) = filter_for_nan(angles,IR_BG)

#Write out calculated parameters to a file for future analysis
with open('Processed_angles_IRdivBG.csv','w') as f:
    writer = csv.writer(f,delimiter='\t')
    writer.writerows(zip(all_angles_filtered,all_IRdivBG_filtered))
f.close()

#Now let's plot a few useful things
print('Making plots')

#First let's create a 2D histogram
bin_number = 400 #Adjust number of bins as wanted
plt.figure(1)
h=plt.hist2d(all_IRdivBG_filtered, all_angles_filtered, bins=(bin_number,bin_number), cmap=plt.cm.jet, norm=colors.LogNorm()) #adjust color scheme as wanted
plt.colorbar(h[3])
plt.xlabel('IR/BG')
plt.ylabel('Angle')
plt.title('2D Histogram')
plt.savefig('2D_histogram')

#Let's create a scatter plot
plt.figure(2)
plt.plot(all_IRdivBG_filtered, all_angles_filtered,'ro')
plt.xlabel('IR/BG')
plt.ylabel('Angle')
plt.title('Scatter plot')
plt.savefig('Scatter_plot')

#If you want to create a density plot instead of a 2D histogram, play with the code below
#print('creating probability distribution...')
#IR_BG_min = min(all_IRdivBG_filtered)
#IR_BG_max = max(all_IRdivBG_filtered)
#angles_min = min(all_angles_filtered)
#angles_max = max(all_angles_filtered)
#nbins=400 #Ajust number of bins as wanted
#k=kde.gaussian_kde([np.array(all_IRdivBG_filtered),np.array(all_angles_filtered)])
#xi,yi=np.mgrid[IR_BG_min:IR_BG_max:nbins*1j,angles_min:angles_max:nbins*1j]
#zi=k(np.vstack([xi.flatten(),yi.flatten()]))

#print('plotting probability distribution')
#plt.figure(3)
#plt.pcolormesh(xi,yi,zi.reshape(xi.shape),cmap=plt.cm.jet,norm=colors.LogNorm())
#plt.colorbar()
#plt.xlabel('IR/BG')
#plt.ylabel('Angle')
#plt.title('Density plot')
#plt.savefig('Density_plot')

plt.close()
