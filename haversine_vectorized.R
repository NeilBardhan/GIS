library(tidyverse)
library(lubridate)
library(data.table)
library(foreach)
library(doParallel)

setwd("C:\\Users\\Neil Bardhan\\Desktop\\Learn Python\\GIS")
lat1 <- runif(1000000, min = -90, max = 90)
long1 <- runif(1000000, min = -180, max = 180)
lat2 <- runif(1000000, min = -90, max = 90)
long2 <- runif(1000000, min = -180, max = 180)

points <- data.frame(cbind(lat1, long1, lat2, long2))
write.csv(x = points, file = "points1M.csv", row.names = F)
#### Haversine Regular ####
R <- 6373000 # earth radius in meters
system.time({
  lat1_r <- points$lat1 * (pi / 180)
  lat2_r <- points$lat2 * (pi / 180)
  long1_r <- points$long1 * (pi / 180)
  long2_r <- points$long2 * (pi / 180)
  
  dlon = long2_r - long1_r
  dlat = lat2_r - lat1_r
  
  a <- sin(dlat / 2)^2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2)^2
  c <- 2 * atan2(sqrt(a), sqrt(1 - a))
  d <- R * c
  points["distance"] <- d
})
rm(list = ls())
