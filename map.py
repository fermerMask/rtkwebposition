from flask import Flask, render_template, jsonify
import random
import time
from collections import deque
import threading
import pyproj
import sys,os,json

def mile_to_meter(mile):
  v = float(mile) * 1.852 * 1000 / 3600
  return v

def dm_to_sd(dm):
    x = float(dm)
    d = x // 100
    m = (x - d * 100) / 60
    return d + m

def reader(fn):
  print(f'reading {fn}')
  with open(fn, 'r+') as f:
    while True:
      line = f.readline()
      ds = line.strip().split(',')
      if ds[0] == '$GNGGA' and len(ds) == 15 and ds[2] != '' and ds[4] != '':
        GGA.append(ds)
        #print(f'GGA:{ds}')
      if ds[0] == "$GNRMC" and len(ds) == 14 and ds[3] != '' and ds[5] != '' and ds[7] != '':
        RMC.append(ds)

app = Flask(__name__)

GGA = deque([],5)
RMC = deque([],5)
EPSG4612 = pyproj.Proj("+init=EPSG:4612")
EPSG2451 = pyproj.Proj("+init=EPSG:2451")

@app.route("/")
def app_route():
    return render_template('test.html')

@app.route("/api/data")
def get_data():
    while len(GGA) == 0:
        time.sleep(0.01)

    ds = GGA.popleft()
    dg = RMC.popleft()

    t = float(ds[1])
    ts = float(dg[1])
    lat = dm_to_sd(ds[2])
    lon = dm_to_sd(ds[4])
    qual = int(ds[6])
    y, x = pyproj.transform(EPSG4612, EPSG2451, lon, lat)
    alt = float(ds[9])
    vel = mile_to_meter(dg[7])

    jd = json.dumps({"lat": lat, "lon" : lon})
    print(f'send:{jd}\n')
    return jd

if __name__ == '__main__':

    fn_log = 'nmea-toda.txt'

    thred = threading.Thread(target=reader, args=[fn_log])
    thred.start()
    time.sleep(3)

    app.run(debug=True)
