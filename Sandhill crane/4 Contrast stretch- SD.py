# Must be implemented from desktop folder to use ArcPro, Arcpy license
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

arcpy.env.workspace = "C:/users/bpickens/Desktop/SACR_detection/images"
outFolder = "C:/users/bpickens/Desktop/SACR_detection/demo2/stretched/"

# Loop through rasters, append names and savefiles
rasters = arcpy.ListRasters()

# Loop through rasters, append names and save files
for inRaster in rasters:
    basename = os.path.splitext(inRaster)[0]
    outRaster = outFolder + "/" + basename + ".jpg"
    stretch1 = arcpy.ia.Stretch(inRaster, "StdDev", num_stddev = 2.0, min=0, max=255, gamma=0.5)
    arcpy.CopyRaster_management(stretch1, outRaster, pixel_type = "8_BIT_UNSIGNED", scale_pixel_value="ScalePixelValue")