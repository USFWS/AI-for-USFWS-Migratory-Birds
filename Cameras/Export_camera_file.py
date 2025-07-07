import math
import os

sensor = 'FLIR2_2025'
fl = 98.9752
ppx = 1.8160 # principal point x
ppy = -0.2876 # principal point y
xdim = 1280 # CCD pixels in X
ydim = 720 # CCD pixels in Y
pixel_size = 0.014 # mm
k1 = 0.0
k2 = 0.0
k3 = 0.0

def gen_header(sensor, fl, ppx, ppy, xdim, ydim, pixel_size):
    h = '''sensor: %s
focal_length: %s
principal_point: %s %s
image_size: %s.0 %s.0
pixel_size: %s\n''' % (sensor, fl, ppx, ppy, xdim, ydim, pixel_size)
    return h

def gen_distortion_table(k1, k2, k3, xdim, ydim, pixel_size):
    '''Returns a distortion table for the cam file. Does not use k0.'''
    k1 = float(k1)
    k2 = float(k2)
    k3 = float(k3)

    a = (int(xdim)*float(pixel_size))/2.0
    b = (int(ydim)*float(pixel_size))/2.0
    c = int(math.ceil(math.sqrt(a**2+b**2)))
    dist_txt = ''
    for dp in range(0,c):
        # Convert k val to radial distortion and format to float with 3 decimals
        this_distortion = '%.3f'%((k1*(dp+1)**3+k2*(dp+1)**5+k3*(dp+1)**7)*1000)
        this_pair = 'd%s: %s %s\n' %(dp,dp+1,this_distortion)
        dist_txt += this_pair
    return dist_txt

def gen_footer():
    f = '''distortion_units: microns'''
    return f

head = gen_header(sensor, fl, ppx, ppy, xdim, ydim, pixel_size)
dt = gen_distortion_table(k1, k2, k3, xdim, ydim, pixel_size)
foot = gen_footer()

with open(sensor +'.cam', 'w') as cam:
    cam.write((head+dt+foot))
