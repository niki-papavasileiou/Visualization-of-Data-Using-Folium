# Formatting the given data to be used in map.py

import pandas as pd
import csv
import os

# DDMM.SSSS -> DD MM SS.SS
def encrypt(string, length):
    s = ' '.join(string[i:i+length] for i in range(0,len(string),length))
    format= s[0:3] + s[3:6] + s[7]+ s[9]  + '.' + s[10] + s[12]
    return format

# Filling missing zeros to coordinates
def zerofilling(number):
    number = float(number)
    number = "{:.4f}".format(number)
    return number.zfill(9)


file = "CANSAT.TXT"
replaced_file = "nospace.txt"
zeros = "zeros.txt"
final_file = "final.txt"

# Removing spaces between comma and next data of every row
with open(file,'r') as f:
    output = open(replaced_file,'w')

    for line in f:
        output.write(line.replace(", ", ","))
    output.close()
      
# Header list for csv
headerList = ["FIRPACK#", "ip", "temp", "pressure", "pressure_alt", "co2", "co", 
              "humidity", "formald", "PM", "GPS_lat", "GPS_long", "gps_ground_speed",
              "gps_altitude", "time", "date"]

with_headers = pd.read_csv(replaced_file)
with_headers.columns = headerList
with_headers.to_csv(replaced_file, header=headerList, index=False)
df = pd.DataFrame(with_headers)

# Convert to string for the formating in DD MM SS.SS
df = df.astype({'GPS_lat':'string','GPS_long':'string'})

# Deleting lines with altitude value equal to 0
df.drop(df.index[df['gps_altitude'] == 0], inplace=True)
df.to_csv(zeros, index=None, mode='w+')

# Creating file with nice format of all values in order to be used in map.py
with open(zeros, 'r') as rp_f, open(final_file, 'w') as ff:
    data = csv.reader(rp_f)
    next(rp_f)
    for row in data:
        for i in range(len(headerList)):
            if i == 10 or i == 11:
                val = zerofilling(row[i])
                val = encrypt(val, 2)
                ff.write("{},".format(val))
            elif i == 15:
                ff.write("{}\n".format(row[i]))
            else:
                ff.write("{},".format(row[i]))

# Deleting unneeded files
os.remove(zeros)
os.remove(replaced_file)