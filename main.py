from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=3)
scene.set_floor(-0.1, (0.8, 0.8, 0.8))
scene.set_directional_light((0, 0.8, 1), 0.2, (0.6, 0.6, 0.7))

@ti.func
def create_ball(pos,n,color,mix_color):
    for i, j, k in ti.ndrange((-n, n), (-n, n), (-n, n)):
        v_color = color*(1- j/n*0.5) + mix_color * j/n*0.5
        x = ivec3(i,j,k)
        if x.dot(x) < n*n*0.5:
            scene.set_voxel(vec3(i,j,k)+pos,1,v_color)
            p_wall = vec3(i+pos[0],-6,(j+pos[1]))
            scene.set_voxel(p_wall,1,vec3(0.2,0.2,0.2))

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    color =  vec3(0.6,0.0,0.1)
    noise = vec3(-0.1,0.01,0.05)
    mix_color = vec3(0.0,0.1,0.3)
    for i in range(0,4):
        create_ball(vec3(9-i*2, 22-i*6,0), 16-i*4, color - noise*i, mix_color - noise*i)
        create_ball(vec3(-(9-i*2), 22-i*6,0), 16-i*4, color-noise*i, mix_color - noise*i)
    create_ball(vec3(0,16,0),12,color-noise*1, mix_color - noise*1)
    create_ball(vec3(0,10,0),8,color-noise*2, mix_color - noise*2)
    create_ball(vec3(0,2,0),4,color-noise*3, mix_color - noise*3)

    for i, j in ti.ndrange((-30, 30), (-2, 40)):
        id = vec3(i,-6,j)
        material,_ = scene.get_voxel(id)
        if material!=1:
            scene.set_voxel(id,1,color*(1-j/80)+mix_color*(j/80))
        else:
            scene.set_voxel(id,0,vec3(0.0,0.0,0.0))


initialize_voxels()

scene.finish()
