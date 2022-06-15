# This code was made for CanSat Greece 2022 competition
# for the 3rd High School of Rhodes by the team of students
# of Aerospace Science and Technology Department of the
# National and Kapodestrian University of Athens

# Aggelos Motsios           aggelosmots@gmail.com
# Niki Papavasileiou        nickypap01@gmail.com 
# Mariana Mandilara         marianamandilara@gmail.com
# Stella - Rafaela Maladaki maladakistella2001@gmail.com
# Angela Mema               memaangela96@gmail.com

# Python - 3.9.7

import folium
import csv
import file_formating

# Converting Degrees, minutes and seconds to demical value
def deg2dem(coord_deg):

    coord = coord_deg.split(" ")

    degrees = float(coord[0])
    minutes = float(coord[1])
    seconds = float(coord[2])
    coord_dem = (degrees + (minutes / 60.) + (seconds/3600.))

    return coord_dem


# Coordinates in degrees, minutes and seconds
# Format of coordinates -> DD MM SS.SS
# D = Degrees
# M = Minutes
# S = Seconds

info = {}
Rodos_coordinates_demx = deg2dem("36 24 59.16")
Rodos_coordinates_demy = deg2dem("28 12 63.48")
Rodos_coordinates_dem = [Rodos_coordinates_demx, Rodos_coordinates_demy]
map = folium.Map(location= Rodos_coordinates_dem, zoom_start= 17) # zoom_start = 18 is max zoom

# Info dictionary format
# info (x, y, ip, temp, pressure, pressure_alt,
#       co2, co, humidity, formald, PM, gps_ground_speed,
#       gps_altitude, time, date)

with open('final.txt', mode='r') as infile:
    data = csv.reader(infile)
    for row in data:
        info.update({int(row[1]): [row[10], row[11], row[1], row[2], 
                                   row[3], row[4], row[5], row[6], 
                                   row[7], row[8], row[9], row[12], 
                                   row[13], row[14], row[15] ]})

# Create map with coordinates
for i in info:

    # IP
    Location = info[i][2]
  
    # Putting x and y to a list
    dem_coord_x = deg2dem(info[i][0])
    dem_coord_y = deg2dem(info[i][1])

    # Collecting coordinates in list
    coordinates_demical = [dem_coord_x, dem_coord_y]

    # Editing html file
    html = f"""
        <h1>Location {Location}</h1>
        <p><b>Info for x = {round(dem_coord_x, 2)}, y = {round(dem_coord_y, 2)}: </b></p>
        <ul>
            <li>Temperature = {info[i][3]}</>
            <li>Pressure = {info[i][4]}</>
            <li>Pressure altitude = {info[i][5]}</>
            <li>CO2 = {info[i][6]}</>
            <li>CO = {info[i][7]}</>
            <li>Humidity = {info[i][8]}</>
            <li>Formald = {info[i][9]}</>
            <li>PM = {info[i][10]}</>
            <li>GPS ground speed = {info[i][11]}</>
            <li>GPS altitude = {info[i][12]}</>
            <li>Time: {info[i][13]}</>
            <li>Date: {info[i][14]}</>
        </ul>
    """

    iframe = folium.IFrame(html=html, width=400, height=400)
    popup = folium.Popup(iframe, max_width=2650)
    tooltip = "Click for more info"

    folium.Marker(coordinates_demical, popup=popup, tootltip=tooltip).add_to(map)


# Generate map in html file 
map.save("map.html")