# Singularity and chaos: a toy visualization

This visualization makes a narrow mathematical analogy:

- The “singularity” is represented by the exact Lorenz state `(0, 0, 0)`.
- The exact state remains a point because it is an equilibrium.
- A second trajectory begins only `1e-12` away.
- Nonlinear dynamics amplify the distinction until the perturbed trajectory
  occupies the Lorenz strange attractor.

This does **not** claim that the Lorenz equations describe the universe or
the Big Bang. It illustrates why a single exact state and a nearby perturbed
state can have radically different long-term behavior in a chaotic system.

## Run

```bash
cd singularity_chaos
python3 -m pip install numpy matplotlib
python3 singularity_chaos.py
```

The left panel animates the trajectories in phase space. The right panel
plots their separation on a logarithmic scale.
