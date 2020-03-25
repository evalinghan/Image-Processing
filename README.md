# Image Processing

In this project, I was processing Mars HiRISE images (high-resolution sattelite images of Mars).
Each HiRISE image includes 3 bands: IR, RED, and BG. 
I had created regions of interest as ArcMap shapefiles through inspection of these images. 
I then produced scripts to extract the pixel data of these regions of interests. 
The extracted data were then processed in order to calculate spectral parameters that reflect changes to the IR, RED, and BG values within the 3-band Mars images. 
We were interested in understanding whether there were any clustersx within these calculated spectral parameters which was investigated using density plots. 

You'll find 4 scripts:

RDR_HiRISE_I-f.sh

shapefile_to_raster.py

extract_xyz.sh

ProcessBandParameters.py  

## RDR_HiRISE_I-f.sh

This script can download any HiRISE image ID and correct the digital values to I/F*cos(theta) - a common way of representing radiance values from sattelite imagery.  
GDAL is used for processing, so you'll need to have that installed.

An example HiRISE ID would be: ESP_016153_2005 but you could change this to your liking

Run the script through the following code: 

```bash
./RDR_HiRISE_I-f.sh ESP_016153_2005 
```
## shapefile_to_raster.py

This script converts shapefiles to raster files of the specific area designated by the shapefiles. 
This script utilizes acrpy, so you'll need to have a license to use arcpy and have this installed through ArcMap. 

## extract_xyz.sh

This script converts as many raster files as you want to a single xyz-file.
Here each column records the 3 band values (IR, RED, and BG in this case) of each pixel in the 3-band rasters.

## ProcessBandParameters

This script reads the xyz-file or any other 3-array data that includes the 3 band values of each pixel in a 3-band image.
It calculates band ratios and band profile angles. 
It then constructs 2D-histograms, density plots, and scatter plots of these data for visualization. 
You will need scipy to run density plots with this script. 


 
