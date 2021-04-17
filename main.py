import matplotlib.pyplot as plt
import numpy as np
from data import vars


def create_planet(planet_radius):
    # Make planet data
    planet_u = np.linspace(0, 2 * np.pi, 10)
    planet_v = np.linspace(0, np.pi, 10)
    planet_x = planet_radius * np.outer(np.cos(planet_u), np.sin(planet_v))
    planet_y = planet_radius * np.outer(np.sin(planet_u), np.sin(planet_v))
    planet_z = planet_radius * np.outer(np.ones(np.size(planet_u)), np.cos(planet_v))
    return planet_x, planet_y, planet_z


def plot_planet(ax, planet_x, planet_y, planet_z, x, y, z):
    # Plot the surface
    ax.plot_surface(planet_x + x, planet_y + y, planet_z + z)


def rectangular_prism(min_coord, max_coord):
    minx, miny, minz = min_coord
    maxx, maxy, maxz = max_coord

    x = np.array([[[minx, minx],
                   [minx, minx]],

                  [[maxx, maxx],
                   [maxx, maxx]]])

    y = np.array([[[miny, miny],
                   [maxy, maxy]],

                  [[miny, miny],
                   [maxy, maxy]]])

    z = np.array([[[minz, maxz],
                   [minz, maxz]],

                  [[minz, maxz],
                   [minz, maxz]]])

    return x, y, z


def draw_rectangular_prism(ax, min_coord, max_coord):
    c = rectangular_prism(min_coord, max_coord)
    ax.voxels(
        c[0], c[1], c[2],
        np.array([[[True]]]),
    )


def main():
    satellite_pos = (
        vars["dyn.satellite.pos[0]"][0],
        vars["dyn.satellite.pos[1]"][0],
        vars["dyn.satellite.pos[2]"][0],
    )

    planet_pos = (
        vars["dyn.planet.pos[0]"][0],
        vars["dyn.planet.pos[1]"][0],
        vars["dyn.planet.pos[2]"][0],
    )

    planet_radius = vars["dyn.planet.radius"][0],

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    draw_rectangular_prism(ax, (0, 0, 0), (4, 4, 1))

    plt.show()


if __name__ == '__main__':
    main()
