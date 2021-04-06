library('data.table')
library('ggplot2')
library('rstudioapi')
library('forecast')
library('zoo')
library('dplyr')
library('xts')
setwd(dirname(rstudioapi::getSourceEditorContext()$path))

# get the directory of current script
root <- dirname(rstudioapi::getSourceEditorContext()$path)
csv_name <- 'weatherAUS.csv'

# read in dataset
weather_aus <- fread(paste0(root, '/', csv_name))

# take the rows with NA's out of dataframe
weather_aus <- na.exclude(weather_aus)
locs <- unique(weather_aus$Location)

plot_vars <- function(loc){
  temp <- weather_aus[Location == loc]
  temp$rain_status <- ifelse(temp$RainToday == 'Yes', 'Rain today', 'No Rain today')
  temp$rain_forecast <- ifelse(temp$RainToday == 'Yes', 'Rain tomorrow', 'No Rain tomorrow')
  temp$MeanTemp <- as.numeric((temp$MinTemp + temp$MaxTemp) / 2)
  temp$MeanHumidity <- as.numeric((temp$Humidity9am + temp$Humidity3pm) / 2)
  ts <- xts(temp[,-1:-2], order.by=as.Date(temp$Date))
  pdf(file = paste0(root, '/plots/', loc, '.pdf'), width = 15, height = 10)
  plot1 <- ggplot(data = temp, aes(Date)) + 
    geom_line(aes(y = MeanHumidity, colour = 'MeanTemp')) + 
    labs(title = paste0('Location: ', loc),
         subtitle = ' Mean Humidity of the day vs. Date', 
         y = 'Humidity (Unit = Percent)', x = 'Date') +
    facet_wrap(~ rain_status)
  plot2 <- ggplot(data = temp, aes(Date)) + 
    geom_line(aes(y = MeanTemp, colour = 'MeanTemp')) + 
    geom_line(aes(y = Temp9am, colour = 'Temp9am')) +
    geom_line(aes(y = Temp3pm, colour = 'Temp3pm')) +
    labs(title = paste0('Location: ', loc),
         subtitle = 'Mean Temperature of the day vs. year', 
         y = 'Temperature (Unit = Celsius)', x = 'Date') +
    facet_wrap(~ rain_status)
  plot3 <- ggplot(data = temp, aes(Date)) + 
    geom_line(aes(y = MeanHumidity, colour = 'MeanTemp')) + 
    labs(title = paste0('Location: ', loc),
         subtitle = 'Mean Temperature of the day vs. year', 
         y = 'Humidity (Unit = Percent)', x = 'Date') +
    facet_wrap(~ rain_forecast)
  plot4 <- ggplot(data = temp, aes(Date)) + 
    geom_line(aes(y = MeanTemp, colour = 'MeanTemp')) + 
    geom_line(aes(y = Temp9am, colour = 'Temp9am')) +
    geom_line(aes(y = Temp3pm, colour = 'Temp3pm')) +
    labs(title = paste0('Location: ', loc),
         subtitle = 'Mean Temperature of the day vs. year', 
         y = 'Temperature (Unit = Celsius)', x = 'Date') +
    facet_wrap(~ rain_forecast)
  print(plot1)
  print(plot2)
  print(plot3)
  print(plot4)
}

for (loc in locs) {
  print(loc)
  pdf(file = paste0(root, '/plots/', loc, '.pdf'), width = 15, height = 10)
  plot_vars(loc)
  dev.off()
}

