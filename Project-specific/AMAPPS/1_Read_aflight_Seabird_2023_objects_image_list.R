
library (xml2)
library (XML)
library (tidyr)
library (dplyr)
library (filenamer)
library(stringr)
library(chron)
library(sf)
library(sfheaders)

# Enter your directory
setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'Seabird_workflow'))##

# Input: file name
input1 <- "20230910_115400.aflight"

path2 <- paste0(getwd(),"/",input1)
path3 <- substr(path2,1,nchar(path2)-8)
path <- paste0(path3,"_orig.aflight")


# copy aflight and rename one as xml
file.copy(input1, path)

new_path <- paste(path3,".xml")
new_path <- gsub(" ","",new_path)
file.rename(input1, new_path)

###########################################
xml_address <- new_path

xml_base = basename(xml_address)
xml_base = substr(xml_base,1,nchar(xml_base)-4)


output_file <- paste0("Metadata_",xml_base,".csv")

output_cam <- paste0("Metadata_", xml_base,"_cameras.csv")
output_detections <- paste0("Metadata_", xml_base,"_detections.csv")
unique_image_list <- paste0("Metadata_", xml_base, "_unique_images.csv")

xml_data <- read_xml(xml_address)
#str(xml_data)

# xml_structure(xml_data)
all_nodes <- xml_find_all(xml_data,"//FlightEntity//Cameras//CameraEntity//Captures//CaptureEntity")
#View(all_nodes)

a1 <- data.frame (
  filename = xml_find_first(all_nodes, ".//Filename") %>% xml_text(),
  computer_time = xml_find_first(all_nodes, ".//ComputerTime") %>% xml_text(),
  gps_time = xml_find_first(all_nodes, ".//Time") %>% xml_text(),
  BLLat = xml_find_first(all_nodes, ".//BLLat") %>% xml_text(),
  BLLong = xml_find_first(all_nodes, ".//BLLon") %>% xml_text(),
  BRLat = xml_find_first(all_nodes, ".//BRLat") %>% xml_text(),
  BRLong = xml_find_first(all_nodes, ".//BRLon") %>% xml_text(),
  TRLat = xml_find_first(all_nodes, ".//TRLat") %>% xml_text(),
  TRLong = xml_find_first(all_nodes, ".//TRLon") %>% xml_text(),
  TLLat = xml_find_first(all_nodes, ".//TLLat") %>% xml_text(),
  TLLong = xml_find_first(all_nodes, ".//TLLon") %>% xml_text(),
  camera_GUID = xml_find_first(all_nodes, ".//CameraGUID") %>%  xml_text(),
  gsd_cm = xml_find_first(all_nodes, ".//EstimatedGSD") %>% xml_text(),
  exposure_ms = xml_find_first(all_nodes, ".//ExposureDuration") %>% xml_text(),
  alt_m = xml_find_first(all_nodes, ".//Alt") %>% xml_text(),
  agl_m = xml_find_first(all_nodes, ".//EstimatedAGL") %>% xml_text(),
  motion_blur = xml_find_first(all_nodes, ".//MotionBlur") %>% xml_text(),
  roll = xml_find_first(all_nodes, ".//Roll") %>% xml_text(),
  pitch = xml_find_first(all_nodes, ".//Pitch") %>% xml_text(),
  yaw = xml_find_first(all_nodes, ".//Yaw") %>% xml_text(),
  rmse = xml_find_first(all_nodes, ".//RMSEstimate") %>% xml_text(),
  speed = xml_find_first(all_nodes, ".//Speed") %>% xml_text(),
  velocityD = xml_find_first(all_nodes, ".//VelocityD") %>% xml_text(),
  velocityE = xml_find_first(all_nodes, ".//VelocityE") %>% xml_text(),
  velocityN = xml_find_first(all_nodes, ".//VelocityN") %>% xml_text(),
  lat = xml_find_first(all_nodes, ".//Lat") %>% xml_text(),
  long = xml_find_first(all_nodes, ".//Lon") %>% xml_text(),
  flight_line = xml_find_first(all_nodes, ".//FlightLine") %>% xml_text(),
  frame_number = xml_find_first(all_nodes, ".//FrameNumber") %>% xml_text()
  )

# View(a1)
####### Look at data types ###########
print(sapply(a1, class)) 

a1$exposure_ms = as.numeric(a1$exposure_ms)
a1$alt_m = as.numeric(a1$alt_m)
a1$agl_m = as.numeric(a1$agl_m)
a1$gsd_cm = as.numeric(a1$gsd_cm)
a1$gsd_cm = a1$gsd_cm*100
a1$motion_blur = as.numeric(a1$motion_blur)
a1$yaw = as.numeric(a1$yaw)
a1$pitch = as.numeric(a1$pitch)
a1$velocityN = as.numeric(a1$velocityN)
a1$speed = as.numeric(a1$speed)
a1$velocityD = as.numeric(a1$velocityD)
a1$velocityE = as.numeric(a1$velocityE)
a1$rmse = as.numeric(a1$rmse)
a1$roll = as.numeric(a1$roll)
a1$BRLat = as.numeric(a1$BRLat)
a1$BRLong = as.numeric(a1$BRLong)
a1$BLLong = as.numeric(a1$BLLong)
a1$BLLat = as.numeric(a1$BLLat)
a1$TLLat = as.numeric(a1$TLLat)
a1$TLLong = as.numeric(a1$TLLong) 
a1$TRLat = as.numeric(a1$TRLat)
a1$TRLong = as.numeric(a1$TRLong)
a1$lat = as.numeric(a1$lat)
a1$long = as.numeric(a1$long)

a1$filename
#a1$computer_time = as.character(a1$computer_time)

print(sapply(a1, class))
#######################################
## Split date, time
library (tidyr)
library (dplyr)
library (filenamer)
library (lubridate)

# For Computer time replace 'T' with '_'
a1$computer_time <- gsub('T',',', a1$computer_time) 

### Separate date and time
a1$time <- str_sub(a1$computer_time, 12, 25)
a1$time <- chron (times=a1$time)
a1$date <- str_sub(a1$computer_time, 1, 10)
a1$year <- year (a1$date)
a1$doy <- yday (a1$date)
a1$computer_time <- NULL

#### Correct filename to be "unique_image"
a1$filename 
a1$unique_image <- basename(a1$filename)
a1$unique_image = substr(a1$unique_image,1,nchar(a1$unique_image)-4)
a1$unique_image 

## Flight folder
a1$filename
a1$flight_name <- gsub('\\',',', a1$filename, fixed=TRUE) 
a1$flight_name

a1 <- separate(a1, col = "flight_name", into = c(NA, NA, "flight_name", NA, NA), sep = ",")
a1$flight_name 

a1$filename <- NULL

# remove duplicates, as needed
a1[!duplicated(a1),]

# removes overview files
a1 <- subset(a1,unique_image !="Over",)

# write column of image lat, long
a1$image_long <- (a1$BLLong + a1$TRLong) / 2
a1$image_lat <- (a1$BLLat + a1$TRLat) / 2

#####
### Write table
write.table(a1, output_file, sep =",", row.names=FALSE)


# write shapefile
#image_list$unique_image <- paste0(image_list$unique_image,".jpg")


# write shapefile
#shapefile <- a1[which(!is.na(a1$image_lat) & !is.na(a1$image_long)),]
#names(shapefile)

#shapefile$image_lat <- as.numeric(shapefile$image_lat)
#shapefile$image_long <- as.numeric(shapefile$image_lat)


#data_sf <- st_as_sf(shapefile, coords = c("image_long", "image_lat"), id="unique_image",crs = 4326)
#st_write(data_sf, paste0(path3,".shp"))

##############################
#####cameras
########################
all_nodes2 <- xml_find_all(xml_data,"//FlightEntity//Cameras//CameraEntity")
#View(all_nodes2)
a2 <- data.frame (
  CameraGUID = xml_find_first(all_nodes2, ".//CameraGUID") %>% xml_text(),
  camera_name = xml_find_first(all_nodes2, ".//Name") %>% xml_text(),
  CCDHeight = xml_find_first(all_nodes2, ".//CCDHeight") %>% xml_text(),
  CCDWidth = xml_find_first(all_nodes2, ".//CCDWidth") %>%  xml_text(),
  focal_length = xml_find_first(all_nodes2, ".//FocalLength") %>% xml_text(),
  height = xml_find_first(all_nodes2, ".//Height") %>% xml_text(),
  width = xml_find_first(all_nodes2, ".//Width") %>% xml_text(),
  AngleX = xml_find_first(all_nodes2, ".//AngleX") %>% xml_text(),
  AngleY = xml_find_first(all_nodes2, ".//AngleY") %>% xml_text(),
  AngleZ = xml_find_first(all_nodes2, ".//AngleZ") %>% xml_text(),
  INS = xml_find_first(all_nodes2, ".//INS") %>% xml_text(),
  PrincipalPointX = xml_find_first(all_nodes2, ".//PrincipalPointX") %>% xml_text(),
  PrincipalPointY = xml_find_first(all_nodes2, ".//PrincipalPointY") %>% xml_text(),
  SigmaAngleX = xml_find_first(all_nodes2, ".//SigmaAngleX") %>% xml_text(),
  SigmaAngleY = xml_find_first(all_nodes2, ".//SigmaAngleY") %>% xml_text(),
  SigmaAngleZ = xml_find_first(all_nodes2, ".//SigmaAngleZ") %>% xml_text(),
  SigmaOffsetX = xml_find_first(all_nodes2, ".//SigmaOffsetX") %>% xml_text(),
  SigmaOffsetY = xml_find_first(all_nodes2, ".//SigmaOffsetY") %>% xml_text(),
SigmaOffsetZ = xml_find_first(all_nodes2, ".//SigmaOffsetZ") %>% xml_text(),
  BiasAngleX = xml_find_first(all_nodes2, ".//BiasAngleX") %>% xml_text(),
  BiasAngleY = xml_find_first(all_nodes2, ".//BiasAngleY") %>% xml_text(),
  BiasAngleZ = xml_find_first(all_nodes2, ".//BiasAngleZ") %>% xml_text(),
  BiasOffsetX = xml_find_first(all_nodes2, ".//BiasOffsetX") %>% xml_text(),
  BiasOffsetY = xml_find_first(all_nodes2, ".//BiasOffsetY") %>% xml_text(),
  BiasOffsetZ = xml_find_first(all_nodes2, ".//BiasOffsetZ") %>% xml_text(),
  k0 = xml_find_first(all_nodes2, ".//K0") %>% xml_text(),
  k1 = xml_find_first(all_nodes2, ".//K1") %>% xml_text(),
  k2 = xml_find_first(all_nodes2, ".//K2") %>% xml_text(),
  k3 = xml_find_first(all_nodes2, ".//K3") %>% xml_text(),
  k4 = xml_find_first(all_nodes2, ".//K4") %>% xml_text(),
  offsetX = xml_find_first(all_nodes2, ".//OffsetX") %>% xml_text(),
  offsetY = xml_find_first(all_nodes2, ".//OffsetY") %>% xml_text(),
  offsetZ = xml_find_first(all_nodes2, ".//OffsetZ") %>% xml_text(),
  P1 = xml_find_first(all_nodes2, ".//P1") %>% xml_text(),
  P2 = xml_find_first(all_nodes2, ".//P2") %>% xml_text(),
  P3 = xml_find_first(all_nodes2, ".//P3") %>% xml_text()
)
#View(a2)
####### Look at data types ###########
#################################
print(sapply(a2, class)) 

a2$CCDHeight = as.numeric(a2$CCDHeight)
#a2$CCDWidth = as.numeric(a2$CCDwidth)
a2$height = as.numeric(a2$height)
a2$width = as.numeric(a2$width)
a2$AngleX = as.numeric(a2$AngleX)
a2$AngleY = as.numeric(a2$AngleY)
a2$AngleZ = as.numeric(a2$AngleZ)
a2$PrincipalPointX = as.numeric(a2$PrincipalPointX)
a2$PrincipalPointY = as.numeric(a2$PrincipalPointY)
a2$SigmaAngleX = as.numeric(a2$SigmaAngleX)
a2$SigmaAngleY = as.numeric(a2$SigmaAngleY)
a2$SigmaAngleZ = as.numeric(a2$SigmaAngleZ)
a2$focal_length = as.numeric(a2$focal_length)
a2$SigmaOffsetX = as.numeric(a2$SigmaOffsetX)
a2$SigmaOffsetY = as.numeric(a2$SigmaOffsetY)
a2$SigmaOffsetZ = as.numeric(a2$SigmaOffsetZ)
a2$k0 = as.numeric(a2$k0)
a2$k1 = as.numeric(a2$k1)
a2$k2= as.numeric(a2$k2)
a2$k3 = as.numeric(a2$k3)
a2$k4 = as.numeric(a2$k4)
a2$P1= as.numeric(a2$P1)
a2$P2 = as.numeric(a2$P2)
a2$P3 = as.numeric(a2$P3)

### write table
write.table(a2, output_cam, sep=",", row.names=FALSE)

#####################
##############
## Detector model-- for censoring?
################
all_nodes3 <- xml_find_all(xml_data,"//FlightEntity//Images//ImageEntity")

a3 <- data.frame (
  imageGUID = xml_find_first(all_nodes3, ".//ImageGUID") %>% xml_text(), filename = xml_find_first(all_nodes3, ".//Filename") %>% xml_text(),observations = xml_find_first(all_nodes3, ".//Observations") %>% xml_text())

a3$observations = as.integer(a3$observations)
a3$unique_image <- basename(a3$filename)
a3$unique_image <- substr(a3$unique_image,1,nchar(a3$unique_image)-4)
a3$unique_image_jpg <- paste0(a3$unique_image,".jpg")

a3$flight_name <- gsub('\\',',', a3$filename, fixed=TRUE) 

a3 <- separate(a3, col = "flight_name", into = c(NA, NA, "flight_name", NA, NA), sep = ",")

a3$filename <- NULL

#write.table(a3, output_total_detects, sep =",", row.names=FALSE)

#############
# Annotation data classes
all_nodes4 <- xml_find_all(xml_data,"//FlightEntity//Images//ImageEntity//Observations_//ObservationEntity")

a4 <- data.frame (
  class_ID = xml_find_all(all_nodes3, ".//ClassID") %>% xml_text(),
  score = xml_find_all(all_nodes3, ".//Score") %>% xml_text(),  
  x1 = xml_find_all(all_nodes3, ".//X1") %>% xml_text(),
  y1 = xml_find_all(all_nodes3, ".//Y1") %>% xml_text(),
  x2 = xml_find_all(all_nodes3, ".//X2") %>% xml_text(),
  y2 = xml_find_all(all_nodes3, ".//Y2") %>% xml_text(),
   imageGUID = xml_find_all(all_nodes3, ".//ObservationEntity//ImageGUID") %>% xml_text()
  )
## Modify coordinates to coco style
a4$x1 = as.integer(a4$x1)
a4$y1 = as.integer(a4$y1)
a4$x2 = as.integer(a4$x2)
a4$y2 = as.integer(a4$y2)

a4$x_min <- a4$x1
a4$y_min <- a4$y1
a4$h <- (a4$y2 - a4$y1)
a4$w <- (a4$x2 - a4$x1)

a4$score = as.numeric(a4$score)
a4$score <- round(a4$score, 2)
a3$observations <- NULL

a5 <- merge(a3,a4, by="imageGUID", x.all = TRUE, y.all= FALSE)

a5$unique_BB <- paste0(a5$unique_image,"_",a4$x_min,"_",a4$y_min,"_", a4$w, "_",a4$h)

write.table(a5, output_detections, sep =",", row.names=FALSE)

###### Create unique image csv list
image_list <- data.frame(
  a5$unique_image_jpg
)

# remove duplicates parent images
unique_image_jpg <- image_list[!duplicated(image_list),]
unique_image_jpg <- data.frame(unique_image_jpg)

write.table(unique_image_jpg, unique_image_list, sep =",", row.names=FALSE)
