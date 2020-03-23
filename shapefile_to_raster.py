import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

ID = "ESP_016153_2005"
shape = "mb_79.shp"
shape_name = "mb_79"
dir="Data/"
fc=dir + shape
cursor = arcpy.SearchCursor(fc)
field = "OBJECTID"
row = cursor.next()
n=0
while n <= 1000:
    expression = '"FID" = ' + str(n)
    print expression
    arcpy.management.MakeFeatureLayer(fc, "new_layer", expression)
    arcpy.management.CopyFeatures("new_layer", dir + "Features_{}/".format(shape_name) + str(n) + ".shp")
    arcpy.management.Delete("new_layer")
    out=arcpy.sa.ExtractByMask(dir + "{}_COLOR_IF.tif".format(ID), dir + "Features_{}/".format(shape_name) + str(n) + ".shp")
    out.save(dir + "Extract_{}/{}_COLOR_IF_extracted_".format(shape_name,ID) + str(n) + ".tif")
    n=n+1


