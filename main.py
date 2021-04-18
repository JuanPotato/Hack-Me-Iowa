from vpython import *

# GlowScript 3.1 VPython


# !/usr/bin/python
import sys
import socket

thruster_T = [50.0, -50.0, 0, 0.0]  # T1_X+, T2_Y+, T3_X-, T4_Y-
thruster_R = [0.0, 0.0, 0.0, 0.0]  # R1_X+, R2_Z-, R3_X-, R4_Z+
thruster_B = [0.0, 0.0, 0.0, 0.0]  # B1_X+, B2_Y+, B3_X-, B4_Y-
thruster_L = [0.0, 0.0, 0.0, 0.0]  # L1_X+, L2_Z+, L3_X-, L4_Z-
main_thrust = 100

# Process the command line arguments.
if (len(sys.argv) == 2):
    trick_varserver_port = int(sys.argv[1])
else:
    print("Usage: vsclient <port_number>")
    sys.exit()

# constatns and item creation
teal_color = vector(0.0, 0.7, 0.69)
blue_color = vector(0.0, 0.0, 1.0)
red_color = vector(1.0, 0.0, 0.0)
lavender = vector(0.76, 0.49, 1.0)

flame_color = vector(1.0, 0.35, 0.0)

sat_body = box(size=vector(4, 4, 4), pos=vector(0.0, 0.0, 0.0), color=color.gray(0.6))
solar_panel = box(size=vector(0.2, 16, 2.5), pos=vector(0.0, 0.0, 0.0), color=color.blue)

t_thruster = box(size=vector(0.5, 0.5, 0.5), pos=vector(-2.0, 0.0, 2.0), color=teal_color)
r_thruster = box(size=vector(0.5, 0.5, 0.5), pos=vector(-2.0, 2.0, 0.0), color=red_color)
b_thruster = box(size=vector(0.5, 0.5, 0.5), pos=vector(-2.0, 0.0, -2.0), color=blue_color)
l_thruster = box(size=vector(0.5, 0.5, 0.5), pos=vector(-2.0, -2.0, 0.0), color=lavender)

thrusters = {
    'T': t_thruster.pos,
    'R': r_thruster.pos,
    'B': b_thruster.pos,
    'L': l_thruster.pos,
}

main_thruster = cylinder(pos=vector(-2.0, 0.0, 0.0), axis=vector(-0.2, 0, 0), radius=1)
sat = compound([sat_body, solar_panel, main_thruster, t_thruster, b_thruster, r_thruster, l_thruster],
               pos=vector(0, 0, 0), make_trail=True)

tarr = [
    arrow(pos=t_thruster.pos, axis=1.0 * vector(1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=t_thruster.pos, axis=1.0 * vector(0.0, 1.0, 0.0), color=flame_color, visible=False),
    arrow(pos=t_thruster.pos, axis=1.0 * vector(-1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=t_thruster.pos, axis=1.0 * vector(0.0, -1.0, 0.0), color=flame_color, visible=False),
]

rarr = [
    arrow(pos=r_thruster.pos, axis=1.0 * vector(1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=r_thruster.pos, axis=1.0 * vector(0.0, 0.0, -1.0), color=flame_color, visible=False),
    arrow(pos=r_thruster.pos, axis=1.0 * vector(-1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=r_thruster.pos, axis=1.0 * vector(0.0, 0.0, 1.0), color=flame_color, visible=False),
]

barr = [
    arrow(pos=b_thruster.pos, axis=1.0 * vector(1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=b_thruster.pos, axis=1.0 * vector(0.0, 1.0, 0.0), color=flame_color, visible=False),
    arrow(pos=b_thruster.pos, axis=1.0 * vector(-1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=b_thruster.pos, axis=1.0 * vector(0.0, -1.0, 0.0), color=flame_color, visible=False),
]

larr = [
    arrow(pos=l_thruster.pos, axis=1.0 * vector(1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=l_thruster.pos, axis=1.0 * vector(0.0, 0.0, 1.0), color=flame_color, visible=False),
    arrow(pos=l_thruster.pos, axis=1.0 * vector(-1.0, 0.0, 0.0), color=flame_color, visible=False),
    arrow(pos=l_thruster.pos, axis=1.0 * vector(0.0, 0.0, -1.0), color=flame_color, visible=False)
]

arrs = {
    'T': tarr,
    'B': barr,
    'R': rarr,
    'L': larr,
}

world_scale = 0.0005
vector_scale = 0.002

earth = sphere(pos=vector(0, 0, 0), radius=6367500 * world_scale, texture=textures.earth)
sat_force_arrow = arrow(pos=sat.pos, axis=vector(1, 1, 1), color=color.red, shaftwidth=1, round=True)
sat_vel_arrow = arrow(pos=sat.pos, axis=vector(1, 1, 1), color=color.yellow, shaftwidth=1, round=True)


def move_sat(new_pos):
    old_pos = sat.pos
    sat.pos = new_pos * world_scale
    scene.center = sat.pos
    sat_force_arrow.pos = sat.pos
    sat_vel_arrow.pos = sat.pos

    for arrs_key in arrs:
        for arr in arrs[arrs_key]:
            arr.pos -= old_pos
            arr.pos += sat.pos


def rotation_matrix_to_eulerxyz(r):
    if r[0][2] < 1:
        if r[0][2] > -1:
            theta_y = asin(r[0][2])
            theta_x = atan2(-r[1][2], r[2][2])
            theta_z = atan2(-r[0][1], r[0][0])
        else:
            theta_y = -pi / 2
            theta_x = -atan2(r[1][0], r[1][1])
            theta_z = 0
    else:
        theta_y = pi / 2
        theta_x = atan2(r[1][0], r[1][1])
        theta_z = 0

    return theta_x, theta_y, theta_z


def set_force(force):
    sat_force_arrow.axis = force * vector_scale


def set_velocity(velocity):
    sat_vel_arrow.axis = velocity * vector_scale


old_rotate = None


def rotate_sat_matrix(r):
    global old_rotate
    old_rotate = r

    theta_xyz = rotation_matrix_to_eulerxyz(r)
    sat.rotate(theta_xyz[0], axis=vector(1, 0, 0))
    sat.rotate(theta_xyz[1], axis=vector(0, 1, 0))
    sat.rotate(theta_xyz[2], axis=vector(0, 0, 1))

    for arrs_key in arrs:
        for arr in arrs[arrs_key]:
            arr.rotate(theta_xyz[0], axis=vector(1, 0, 0), origin=sat.pos)
            arr.rotate(theta_xyz[1], axis=vector(0, 1, 0), origin=sat.pos)
            arr.rotate(theta_xyz[2], axis=vector(0, 0, 1), origin=sat.pos)


def unrotate_sat_matrix(r):
    theta_xyz = rotation_matrix_to_eulerxyz(r)
    sat.rotate(-theta_xyz[2], axis=vector(0, 0, 1))
    sat.rotate(-theta_xyz[1], axis=vector(0, 1, 0))
    sat.rotate(-theta_xyz[0], axis=vector(1, 0, 0))

    for arrs_key in arrs:
        for arr in arrs[arrs_key]:
            arr.rotate(-theta_xyz[2], axis=vector(0, 0, 1), origin=sat.pos)
            arr.rotate(-theta_xyz[1], axis=vector(0, 1, 0), origin=sat.pos)
            arr.rotate(-theta_xyz[0], axis=vector(1, 0, 0), origin=sat.pos)


R = [
    [-6.790363627287294E-16, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 6.790363627287294E-16, 0.0]
]

move_sat(vector(6742722.789864636, 1303167.605253255, 0.0))
set_force(vector(-8297.738461112745, -1603.705846491815, 0.0))
set_velocity(vector(-1445.647684201044, 7479.929841267291, 0.0))

rotate_sat_matrix(R)


# unrotate_sat_matrix(R)


def arr_handler(thruster, index, checkbx):
    print(thruster, index, checkbx.checked)
    arrs[thruster][index].visible = checkbx.checked
    client_socket.send(f"dyn.satellite.thruster_{thruster}{index+1}.on = {checkbx.checked} \n".encode())


def gen_handler(thruster, index):
    def handler(c):
        return arr_handler(thruster, index, c)

    return handler


# a miracle, dont touch
scene.append_to_caption('\n                ')
scene.append_to_caption('          X+')

wt = wtext(text='')


def setthrust(s):
    wt.text = '                Thrust: {:1.2f}'.format(s.value)


thrust_sl = slider(min=0.0, max=500.0, value=100.0, length=220, bind=setthrust)

setthrust(thrust_sl)

scene.append_to_caption('\n                ')
scene.append_to_caption('         ')
checkbox(bind=gen_handler('T', 0))

scene.append_to_caption('\n')
scene.append_to_caption('                ')
scene.append_to_caption('Y- ')
checkbox(bind=gen_handler('T', 3))
scene.append_to_caption('T ')
checkbox(bind=gen_handler('T', 1), text='Y+')
scene.append_to_caption('\n')

scene.append_to_caption('                ')
scene.append_to_caption('         ')
checkbox(bind=gen_handler('T', 2))
scene.append_to_caption('\n          ')
scene.append_to_caption('                ')
scene.append_to_caption('X-\n\n')

scene.append_to_caption('          X+                       X+\n')
scene.append_to_caption('         ')
checkbox(bind=gen_handler('L', 0))
scene.append_to_caption('                      ')
checkbox(bind=gen_handler('R', 0))

scene.append_to_caption('\n')
scene.append_to_caption('Z- ')
checkbox(bind=gen_handler('L', 3))
scene.append_to_caption('L ')
checkbox(bind=gen_handler('L', 1), text='Z+')

scene.append_to_caption('    ')
scene.append_to_caption('Z- ')
checkbox(bind=gen_handler('R', 1))
scene.append_to_caption('R ')
checkbox(bind=gen_handler('R', 3), text='Z+')
scene.append_to_caption('\n')

scene.append_to_caption('         ')
checkbox(bind=gen_handler('L', 2))
scene.append_to_caption('                      ')
checkbox(bind=gen_handler('R', 2))
scene.append_to_caption('\n          X-                         X-\n')

scene.append_to_caption('                ')
scene.append_to_caption('          X+\n')
scene.append_to_caption('                ')
scene.append_to_caption('         ')
checkbox(bind=gen_handler('B', 0))

scene.append_to_caption('\n')
scene.append_to_caption('                ')
scene.append_to_caption('Y- ')
checkbox(bind=gen_handler('B', 3))
scene.append_to_caption('B ')
checkbox(bind=gen_handler('B', 1), text='Y+')
scene.append_to_caption('\n')

scene.append_to_caption('                ')
scene.append_to_caption('         ')
checkbox(bind=gen_handler('B', 2))
scene.append_to_caption('\n          ')
scene.append_to_caption('                ')
scene.append_to_caption('X-\n\n')

# Connect to the variable server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", trick_varserver_port))
insock = client_socket.makefile("r")

client_socket.send(b"trick.var_pause()\n")

client_socket.send(b"trick.var_ascii()\n")
# tell var server what data we want

# Satellite position
client_socket.send(b"trick.var_add(\"dyn.satellite.pos[0]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.pos[1]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.pos[2]\") \n")

# Satellite velocity
client_socket.send(b"trick.var_add(\"dyn.satellite.vel[0]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.vel[1]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.vel[2]\") \n")

# Force on Satellite
client_socket.send(b"trick.var_add(\"dyn.satellite.force[0]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.force[1]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.force[2]\") \n")

# Rotation matrix
client_socket.send(b"trick.var_add(\"dyn.satellite.R[0][0]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[0][1]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[0][2]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[1][0]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[1][1]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[1][2]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[2][0]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[2][1]\") \n")
client_socket.send(b"trick.var_add(\"dyn.satellite.R[2][2]\") \n")

#
# client_socket.send(b"trick.var_add(\"dyn.satellite.main_engine.thrust[0]\") \n")
client_socket.send(b"trick.var_unpause()\n")

# # send a thrust value
# client_socket.send(b"dyn.satellite.main_engine.thrust[0] = " + (str(main_thrust).encode()) + b"\n")


# Repeatedly read and process the responses from the variable server.
while True:
    line = insock.readline()
    if line == '':
        break

    print(line)

    data = list(map(float, line.split('\t')))
    sat_pos = data[1:4]
    sat_vel = data[4:7]
    sat_force = data[7:10]
    R = [
        data[10:13],
        data[13:16],
        data[16:19],
    ]
    print(sat_pos)
    print(sat_vel)
    print(sat_force)
    move_sat(vector(*sat_pos))
    set_velocity(vector(*sat_vel))
    set_force(vector(*sat_force))

    unrotate_sat_matrix(old_rotate)
    rotate_sat_matrix(R)
