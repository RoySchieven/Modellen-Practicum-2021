import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os
import zlib
import sys

import mayavi
from mayavi import mlab
from tvtk.util.ctf import PiecewiseFunction

input_file = "C:\\users\\roysc\\outputpiff"


###### OPTIONS ######

lattice_dim = [200,200,200] # [x,y,z]. If you're visualising a 2D field, set z=1.
lowest_coord = [0,0,0] # [x,y,z]. If x runs from 40 to 110, then change x in lattice_dim to 70 and in
                       # lowest_coord to 40
fields = ["CTP"]
contour_toggle_3d = True # Set True if you want a contour map.

animate_toggle = False

output_frequency = 10
compression_save_frequency = 100

#####################
#Lets load my settings
frame_file = open(input_file,"rb").read()

numof_frames = np.frombuffer(frame_file[:4],dtype='int32')[0]
lattice_dim = np.frombuffer(frame_file[4:16],dtype='int32')
lattice_size = np.prod(lattice_dim)

print(numof_frames)

frames_type = []
frames_id =[]

for i in range(numof_frames)[:70]:
    frames_type.append(np.frombuffer(frame_file[16 + 2*i*lattice_size: 16 + (2*i+1)*lattice_size],dtype='int8').reshape(lattice_dim).astype("float32")/2)
#    frames_id.append(np.frombuffer(frame_file[16 + (2*i+1)*lattice_size: 16 + (2*i+2)*lattice_size],dtype='int8').reshape(lattice_dim))

frame_file = None

frames_type

print(len(frames_type))
#Frames are now loaded in

####################
fig = mlab.figure(size=(600,600),bgcolor=(0,0,0))
fig.scene.magnification = 2
fig.scene.off_screen_rendering = True
fig.scene.movie_maker.record = True


@mlab.animate(delay=1000)
def anim_3d(frames,ms):
    for i in range(len(frames)):
        ms.scalars = frames[i]
        mlab.view(45,distance=600,elevation=45)
        yield

def plot_3d(index,data):
    if not contour_toggle_3d:
        grid = mlab.pipeline.scalar_field(data)
        vol = mlab.pipeline.volume(grid,vmin=1e-06)

        # Change the opacity to something more reasonable
        otf = PiecewiseFunction()
        otf.add_point(0.0, 0.0)
        otf.add_point(0.315,0.3)
        vol._otf = otf
        vol._volume_property.set_scalar_opacity(otf)
        
    else:
        mlab.contour3d(data,transparent=False)

    mlab.axes()
    #mlab.title(" ".join(["","mcs = %d" % (index*output_frequency)]),size=1,opacity=0.8)
    mlab.colorbar(orientation="vertical")
    #mlab.show()
    return

def animate_3d(frames):

    cont = mlab.contour3d(frames[0],transparent=True, vmin=0.2, vmax=0.8)
    #mlab.pipeline.volume(mlab.pipeline.scalar_field(frames[0]), vmin=0.1, vmax=0.9)
    #mlab.pipeline.iso_surface(cont, contours=[0, ], opacity=0.1)
    
    ms = cont.mlab_source
    #ms.trait_set(transparent=True)

    #ms = mlab.pipeline.scalar_field(frames[0])
    #vol = mlab.pipeline.volume(ms,vmin=1e-06)
    #vol._mapper_types = ['FixedPointVolumeRayCastMapper']
    #otf = PiecewiseFunction()
    #otf.add_point(0.0, 0.0)
    #otf.add_point(0.315,0.3)
    #vol._otf = otf
    #vol._volume_property.set_scalar_opacity(otf)
    global gcf
    #gcf=mlab.gcf()
    #mlab.axes()
    
    #mlab.title(" ".join([field,"mcs = 0"]),size=0.5,opacity=0.8)
    #mlab.colorbar(orientation="vertical")
    anim_3d(frames,ms)
    mlab.show()
    return

animate_3d(frames_type)
