"""Toy visualization: an exact singular state versus a tiny perturbation.

This is not a cosmological model. It uses the Lorenz equations as a
mathematical analogy for how nonlinear dynamics can amplify an initially
tiny distinction:

    dx/dt = sigma * (y - x)
    dy/dt = x * (rho - z) - y
    dz/dt = x * y - beta * z

The exact state (0, 0, 0) remains a single point forever. A trajectory
starting 1e-12 away from it eventually separates and forms the Lorenz
strange attractor.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0
DT = 0.005
STEPS = 16_000
PERTURBATION = 1e-12


def lorenz(state: np.ndarray) -> np.ndarray:
    x, y, z = state
    return np.array(
        [
            SIGMA * (y - x),
            x * (RHO - z) - y,
            x * y - BETA * z,
        ]
    )


def integrate(initial: np.ndarray) -> np.ndarray:
    """Integrate the Lorenz system with fourth-order Runge–Kutta."""
    states = np.empty((STEPS, 3), dtype=float)
    states[0] = initial
    for index in range(1, STEPS):
        current = states[index - 1]
        k1 = lorenz(current)
        k2 = lorenz(current + DT * k1 / 2)
        k3 = lorenz(current + DT * k2 / 2)
        k4 = lorenz(current + DT * k3)
        states[index] = current + DT * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return states


def main() -> None:
    exact = integrate(np.array([0.0, 0.0, 0.0]))
    perturbed = integrate(np.array([PERTURBATION, 0.0, 0.0]))
    separation = np.linalg.norm(perturbed - exact, axis=1)

    figure = plt.figure(figsize=(13, 7))
    attractor_axes = figure.add_subplot(121, projection="3d")
    separation_axes = figure.add_subplot(122)
    attractor_axes.set(
        title="From one point to a chaotic attractor",
        xlabel="x",
        ylabel="y",
        zlabel="z",
        xlim=(-22, 22),
        ylim=(-30, 30),
        zlim=(0, 55),
    )
    separation_axes.set(
        title="Amplification of the initial distinction",
        xlabel="Time",
        ylabel="Distance from exact trajectory (log scale)",
        yscale="log",
        xlim=(0, STEPS * DT),
        ylim=(1e-14, 100),
    )
    separation_axes.grid(alpha=0.25)

    exact_line, = attractor_axes.plot([], [], [], color="black", lw=2, label="exact point")
    perturbed_line, = attractor_axes.plot([], [], [], color="#cc4b37", lw=1, label="1e-12 perturbation")
    marker, = attractor_axes.plot([], [], [], "o", color="#cc4b37", ms=5)
    separation_line, = separation_axes.plot([], [], color="#cc4b37", lw=1.5)
    attractor_axes.legend(loc="upper left")

    time = np.arange(STEPS) * DT

    def update(frame: int):
        exact_line.set_data(exact[: frame + 1, 0], exact[: frame + 1, 1])
        exact_line.set_3d_properties(exact[: frame + 1, 2])
        perturbed_line.set_data(perturbed[: frame + 1, 0], perturbed[: frame + 1, 1])
        perturbed_line.set_3d_properties(perturbed[: frame + 1, 2])
        marker.set_data([perturbed[frame, 0]], [perturbed[frame, 1]])
        marker.set_3d_properties([perturbed[frame, 2]])
        separation_line.set_data(time[: frame + 1], separation[: frame + 1])
        return exact_line, perturbed_line, marker, separation_line

    animation = FuncAnimation(
        figure,
        update,
        frames=range(0, STEPS, 8),
        interval=20,
        blit=False,
        repeat=True,
        cache_frame_data=False,
    )
    # Keep a strong reference while the GUI event loop is running.
    figure._singularity_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
