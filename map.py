from flask import Flask, render_template, jsonify
import random
import time
from collections import deque
import threading
import pyproj
import sys,os,json

def dm_to_sd(dm):
    x = float(dm)
    d = x // 100
    m = (x - d * 100) / 60
    return d + m

def reader(q, fn):
    with open(fn) as file:
        for line in file:
            ds = line.strip().strip(',')
            if ds[0] == '$GNGGA' and len(ds) == 15 and ds[2] != '' and ds[4] != '':
                q.append()
                print(f'GGA:{ds}\n')

EPSG4612 = pyproj.Proj("+init=EPSG:4612")
EPSG2451 = pyproj.Proj("+init=EPSG:2451")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/api/get_location')
def get_location():
   while len(GGA) == 0:
       time.sleep(0.01)
   ds = GGA.popleft()
   lat = dm_to_sd(ds[2])
   lon = dm_to_sd(ds[4])
   y,x = pyproj.transform(EPSG4612,EPSG2451,lon,lat)

   return jsonify(lat,lon)

if __name__ == '__main__':
    fn_log = 'nmea-toda.txt'
    GGA = deque([],5)

    thred = threading.Thread(target=reader, args=(GGA, fn_log))
    thred.start()

    app.run(debug=True)
