# BPhO Computational Challenge 2023
# Challenges 1 - 7

# LIBRARIES
from dataclasses import dataclass
import os
from io import StringIO, BytesIO
import base64

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

import numpy as np
from scipy.interpolate import interp1d

from .data import Planet, retrieve_planet_details, get_planet
from .cache import Cache


dir_path = os.path.abspath(os.path.dirname(__file__))
cache_path = os.path.join(dir_path, os.pardir, "cache")

cache = Cache()
cache.register_cache()

@dataclass
class PlanetCoordinates:
    x: float
    y: float
    z: float


## GRAPH FUNCTIONS

def plot_centre(centre_planet_name: str, axis) -> None: #TODO
    """
    Plot a planet at the centre of the planetary system
    """
    if centre_planet_name == "Sun":
        axis.plot(0, 0, "o", color = "yellow", label = centre_planet_name)
    else:
        axis.plot(0, 0, "o", label = centre_planet_name)


def figure_setup(is_3D_orbit: bool):
    fig = plt.figure()
    fig.set_figwidth(8)
    fig.set_figheight(8)
    ax = fig.add_subplot(projection = "3d") if is_3D_orbit else fig.add_subplot()
    return fig, ax


def finish_figure(ax, title: str) -> None:
    # SHOW THE GRAPH
    ax.legend()
    ax.set_title(title)
    ax.grid()

def generate_animation_filename(input_planets: list[str], is_3D_orbit: bool) -> str:
    filename = "3D-" if is_3D_orbit else "2D-"
    filename += "_".join([_.lower() for _ in input_planets])
    filename += ".gif"
    return filename

def save_animation(animation: FuncAnimation, filename: str) -> None:
    # Save the animation as a GIF file
    writer = PillowWriter(fps=15, bitrate=400)
    animation.save(os.path.join(cache_path, filename), writer=writer)

def get_animation_data(filename: str) -> str:
    with open(os.path.join(cache_path, filename), 'rb') as f:
        gif_data = f.read()

    # Create a BytesIO object from the binary data
    buffer = BytesIO(gif_data)

    # Use the BytesIO object as needed
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return base64_data

def get_figure_data(fig) -> str:
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    return imgdata.getvalue()
        
## ORBIT FUNCTIONS

# Calculate the elliptical orbits of each planet
def calculate_orbit_position(planet: Planet, theta, orbit_3D) -> PlanetCoordinates:
    """
    Calculates the x and y coordinates of the orbit of a planet at a given angle theta
    """

    def compute_r(a: float, ecc: float, theta: float):
        """
        Computes the radius of the orbit at a given angle theta
        """
        return (a*(1-ecc**2))/(1-ecc*np.cos(theta))

    # Calculate r
    r = compute_r(planet.a, planet.ecc, theta)

    # Calculate x coordinate
    x = r * np.cos(theta)

    # Calculate y coordinate
    y = r * np.sin(theta)

    # If 3D orbits are to be calculated
    x = x * np.cos(planet.beta * np.pi / 180) if orbit_3D else x
    z = x * np.sin(planet.beta * np.pi / 180) if orbit_3D else None

    return PlanetCoordinates(x, y, z)


# Task 1 - 2D
def kepler_correlation(planets: list[Planet]) -> None:
    """
    Plots the Kepler's Third Law correlation
    """

    def plot_kepler_correlation():
        plt.plot(x, y, marker="s", markerfacecolor="red", markeredgecolor="red", label="Kepler's Third Law")
        plt.title("Kepler's Third Law")
        plt.xlabel("(a/AU)^(3/2)")
        plt.ylabel("T/Yr")
    

    x = []
    y = []
    for planet in planets:
        x.append(planet.a ** (3 / 2))
        y.append(planet.p)

    plot_kepler_correlation()


# Task 2 - 2D

def plot_orbit(input_planets: list[Planet], has_sun: bool, is_3D_orbit: bool, ax) -> None:

    def plot_planet(planet: Planet, ax, is_3D_orbit):
        if is_3D_orbit:
            ax.plot(x, y, z, label = planet.name)
            ax.set_zlabel("z/AU")
        else:
            ax.plot(x, y, label = planet.name)
    
    def plot_sun(has_sun, ax):
        if has_sun:
            plot_centre("Sun", ax)

    def set_labels():
        ax.set_xlabel("x/AU")
        ax.set_ylabel("y/AU")


    for input_planet in input_planets:
        x = []
        y = []
        z = []
        theta = 0
        for _ in range(1000):
            coord = calculate_orbit_position(input_planet, theta, is_3D_orbit)
            x.append(coord.x)
            y.append(coord.y)

            if is_3D_orbit:
                z.append(coord.z)

            # Increase theta
            theta += (0.002*np.pi)

        plot_planet(input_planet, ax, is_3D_orbit)
    plot_sun(has_sun, ax)
    set_labels()
    

def animate_orbit(input_planets: list[Planet], orbit_3D: bool, ax, fig, colour: list[str]):

    def animate(i: int, input_planets: list[Planet], markers: list[plt.Line2D]) -> list[plt.Line2D]:
        """
        Animate the markers for the animation
        """
        #print(i)
        for index, input_planet in enumerate(input_planets):
            #theta = (2 * np.pi * (i * 0.002)) / input_planet.modified_p
            # Earth and Jupiter should turn one full rotation in 60 frames
            num_frames = 15 * input_planet.modified_p
            theta = (2 * np.pi * ((i % num_frames) / num_frames))
            #print(theta)
            planet_coord = calculate_orbit_position(input_planet, theta, orbit_3D)

            markers[index].set_data(planet_coord.x, planet_coord.y)

            if orbit_3D:
                markers[index].set_3d_properties(planet_coord.z)
                
        return markers

    def get_markers(ax):
        # CREATE THE MARKERS FOR THE ANIMATIONS
        if orbit_3D:
            markers = [ax.plot([0], [0], [0], marker = "o", color = colour[_])[0] for _ in range(9)]
        else:
            markers = [ax.plot([0], [0], marker = "o", color = colour[_])[0] for _ in range(9)]
        
        return markers

    def init():
        """
        Initialise the markers for the animation
        """
        markers = get_markers(ax)
        for marker in markers:
            marker.set_data([], [])

        return markers

    plot_orbit(input_planets, True, orbit_3D, ax)
    final_frames = 15 * input_planets[-1].modified_p
    final_frames = int(np.ceil(final_frames))
    print(final_frames)
    return FuncAnimation(fig, animate, frames = final_frames, init_func = init,
                                fargs = (input_planets, get_markers(ax)), interval = 1, blit = True)


# Task 5
def angle_vs_time(ax, input_planet: Planet) -> None:

    def calculate_angle_vs_time(t, P, ecc, theta0) -> np.ndarray:

        # Angle step for Simpson's rule
        dtheta = 1/1000

        # Number of orbits
        N = np.ceil(t[-1] / P)
        
        # Define array of polar angles for orbits
        theta = np.arange(theta0, (2 * np.pi * N + theta0) + dtheta, dtheta)

        # Evaluate integrand of time integral
        f = (1 - ecc * np.cos(theta)) ** (-2)

        # Define Simpson rule coefficients c = [1, 4, 2, 4, 2, 4, ....1]
        L = len(theta)
        isodd = np.remainder(np.arange(1, L-1), 2)
        isodd[isodd == 1] = 4
        isodd[isodd == 0] = 2
        c = np.concatenate(([1], isodd, [1]))

        # Calculate array of times
        tt = P * ((1 - ecc ** 2) ** (3/2)) * (1 / (2 * np.pi)) * dtheta * (1 / 3) * np.cumsum(c * f)

        # Interpolate the polar angles for the eccentric orbit at the circular orbit times
        theta = interp1d(tt, theta, kind='cubic')
        theta = theta(t)
        
        return theta
    
    def plot_angle_vs_time(ax):
        ax.cla()
        ax.plot(t, theta_circ, label = "Circular")
        ax.plot(t, theta_ecc, label = "Eccentric")
        ax.set_xlabel("time/years")
        ax.set_ylabel("orbit polar angle/rad")


    t = np.linspace(1, 800, 800)

    theta_circ = calculate_angle_vs_time(t, input_planet.p, 0, 0)
    theta_ecc = calculate_angle_vs_time(t, input_planet.p, input_planet.ecc, 0)

    plot_angle_vs_time(ax)


# Task 6
def plot_spinograph(input_planets: list[Planet], is_3D_orbit: bool, ax) -> None:
    planet1 = input_planets[0]
    planet2 = input_planets[1]
    tmax = max([planet1.p, planet2.p])  # Max time /years
    dt = 10 * tmax / 1234  # Time interval in years
    t = 0

    while t < 10 * tmax:
        x = []
        y = []

        theta = (2 * np.pi * (t)) / planet1.p
        planet_coord = calculate_orbit_position(planet1, theta, is_3D_orbit)
        x.append(planet_coord.x)
        y.append(planet_coord.y)

        theta = (2* np.pi * (t)) / planet2.p
        planet_coord = calculate_orbit_position(planet2, theta, is_3D_orbit)
        x.append(planet_coord.x)
        y.append(planet_coord.y)
        
        ax.plot(x, y, color = "black", linewidth = 0.5)
        #Update time t /years
        t = t + dt

    plot_orbit(input_planets, False, False, ax)


# Task 7
def plot_imaginary_orbit(input_centre_planet: Planet, input_planets: list[Planet], is_3D_orbit: bool, ax) -> None:

    def calculate_planet_orbit(centre_planet: Planet, 
                                planet: Planet
                                ) -> (list[float], list[float], list[float]):
        
        # Calculate the position of planet 1 (eg. Earth, which will be at the centre of the solar system)
        coord_x = []
        coord_y = []
        coord_z = []
            
        tmax = max([centre_planet.p, planet.p])  # Max time /years
        dt = 10*tmax/1234  # Time interval in years
        t = 0

        for _ in range(1000):

            theta = (2 * np.pi * (t)) / centre_planet.p
            planet1 = calculate_orbit_position(centre_planet, theta, is_3D_orbit)
            
            theta = (2 * np.pi * (t)) / planet.p
            planet2 = calculate_orbit_position(planet, theta, is_3D_orbit)
            
            coord_x.append(planet2.x - planet1.x)
            coord_y.append(planet2.y - planet1.y)
            
            if is_3D_orbit:
                coord_z.append(planet2.z - planet1.z)
            
            # Update time t /years
            t = t + dt
        return coord_x, coord_y, coord_z

    def set_labels(is_3D_orbit: bool):
        ax.set_xlabel("x/AU")
        ax.set_ylabel("y/AU")
        if is_3D_orbit:
            ax.set_zlabel("z/AU")

    # Plot the centre planet
    plot_centre(input_centre_planet.name, ax)

    # Plot the orbits of the other planets
    for planet in input_planets:
        coord_x, coord_y, coord_z = calculate_planet_orbit(input_centre_planet, planet)

        if is_3D_orbit:
            ax.plot(coord_x, coord_y, coord_z, label = planet.name)
        else:
            ax.plot(coord_x, coord_y, label = planet.name)
    
    set_labels(is_3D_orbit)


colour = ["royalblue", "orange", "green", "red", "mediumpurple", "blue", "orange", "green", "yellow"]

def task1():
    # Initialise figure
    fig, ax = figure_setup(is_3D_orbit=False)

    # Plot Kepler's Third Law
    kepler_correlation(retrieve_planet_details())

    # Finalise figure
    finish_figure(ax, "Kepler's Third Law")

    return get_figure_data(fig)

    
def task2(input_planets: list[str], is_3D_orbit: bool):
    # Initialise figure
    fig, ax = figure_setup(is_3D_orbit=is_3D_orbit)
    input_planets = [get_planet(_) for _ in input_planets]

    # Plot orbits
    plot_orbit(input_planets, True, is_3D_orbit, ax)

    # Finalise figure
    finish_figure(ax, "2D Planet Orbits")

    return get_figure_data(fig)

def task3(input_planets: list[str]):
    #Generate filename
    filename = generate_animation_filename(input_planets, is_3D_orbit=False)

    if cache.get(filename) is None:
        # Initialise figure
        fig, ax = figure_setup(is_3D_orbit=False)
        input_planets = [get_planet(_) for _ in input_planets]

        # Generate animation
        animation = animate_orbit(input_planets, False, ax, fig, colour)

        # Finalise figure
        finish_figure(ax, "2D Planet Orbits")
        
        # Save animation
        save_animation(animation, filename)
        cache.set(filename, True)

    return get_animation_data(filename)


def task4(input_planets: list[str]):
    # Generate filename
    filename = generate_animation_filename(input_planets, is_3D_orbit=True)

    # Check if animation has already been generated
    if cache.get(filename) is None:
        # Initialise animation
        fig, ax = figure_setup(is_3D_orbit=True)
        input_planets = [get_planet(_) for _ in input_planets]

        # Generate animation
        animation = animate_orbit(input_planets, True, ax, fig, colour)

        # Finalise animation
        finish_figure(ax, "3D Planet Orbits")

        # Save animation
        save_animation(animation, filename)
        cache.set(filename, True)
    
    return get_animation_data(filename)

def task5(input_planet: str):
    # Initialise figure
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planet = get_planet(input_planet)

    # Plot angle vs time
    angle_vs_time(ax, input_planet)

    # Finalise figure
    finish_figure(ax, "Angle vs Time")

    return get_figure_data(fig)


def task6(input_planets: list[str]):
    # Initialise figure
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planets = [get_planet(_) for _ in input_planets]

    # Plot spinograph
    plot_spinograph(input_planets, False, ax)

    # Finalise figure
    finish_figure(ax, "Spirograph")

    return get_figure_data(fig)

def task7A(input_centre_planet: str, input_planets: list[str], is_3D_orbit: bool):
    # Initialise figure
    fig, ax = figure_setup(is_3D_orbit=is_3D_orbit)
    input_planets = [get_planet(_) for _ in input_planets]
    input_centre_planet = get_planet(input_centre_planet)

    # Plot imaginary orbit
    plot_imaginary_orbit(input_centre_planet, input_planets, is_3D_orbit, ax)

    # Finalise figure
    finish_figure(ax, "Plot Imaginary Orbit")

    return get_figure_data(fig)