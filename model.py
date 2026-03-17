"""
S-I-D-T-R Compartmental Model for HIV Transmission & Drug Resistance
North-East India | Based on NACO 2024/2025 Data
Author: Rohan Biswas
"""

import numpy as np
from scipy.integrate import odeint

# -- Fixed biological parameters (literature-derived)
DELTA_D = 0.75   # relative infectivity of diagnosed-untreated
DELTA_R = 1.15   # relative infectivity of resistant cases
MU      = 0.0095 # natural mortality rate
ALPHA   = 0.11   # disease-related mortality (untreated/failed)

# -- State configurations (NACO 2024/2025)
STATES = {
    'Mizoram': {
        'N': 1_300_000, 'PLHIV': 26_320, 'prev_pct': 2.75,
        'beta': 0.28, 'sigma': 0.35, 'gamma': 0.983, 'omega': 0.0051,
        'I_frac': 0.19, 'R_frac': 0.031
    },
    'Nagaland': {
        'N': 2_200_000, 'PLHIV': 23_730, 'prev_pct': 1.37,
        'beta': 0.32, 'sigma': 0.32, 'gamma': 0.981, 'omega': 0.0071,
        'I_frac': 0.20, 'R_frac': 0.04
    },
    'Manipur': {
        'N': 3_200_000, 'PLHIV': 23_460, 'prev_pct': 0.81,
        'beta': 0.25, 'sigma': 0.30, 'gamma': 0.983, 'omega': 0.0212,
        'I_frac': 0.18, 'R_frac': 0.06
    },
    'Assam': {
        'N': 35_000_000, 'PLHIV': 33_150, 'prev_pct': 0.13,
        'beta': 0.12, 'sigma': 0.28, 'gamma': 0.975, 'omega': 0.0073,
        'I_frac': 0.15, 'R_frac': 0.03
    }
}


def hiv_model(y, t, params):
    """ODE system for S-I-D-T-R model."""
    S, I, D, T, R = y
    beta, sigma, gamma, omega, delta_D, delta_R, Lambda, mu, alpha, N = params
    force  = beta * (I + delta_D * D + delta_R * R) / N
    dSdt   = Lambda - force * S - mu * S
    dIdt   = force * S - (sigma + mu + alpha) * I
    dDdt   = sigma * I - (gamma + mu + alpha) * D
    dTdt   = gamma * D - (omega + mu) * T
    dRdt   = omega * T - (mu + alpha) * R
    return [dSdt, dIdt, dDdt, dTdt, dRdt]


def get_initial_conditions(cfg):
    """Derive initial compartment values from state config."""
    N, PLHIV = cfg['N'], cfg['PLHIV']
    I0 = cfg['I_frac'] * PLHIV
    R0 = cfg['R_frac'] * PLHIV
    T0 = PLHIV * 0.90
    D0 = PLHIV * 0.05
    S0 = N - (I0 + D0 + T0 + R0)
    return [S0, I0, D0, T0, R0]


def run_model(cfg, t, beta_override=None, gamma_override=None, omega_override=None):
    """Run ODE model for a single state config. Override params for scenarios."""
    N      = cfg['N']
    Lambda = 15_000 if N > 10_000_000 else 12_000
    beta   = beta_override  if beta_override  is not None else cfg['beta']
    gamma  = gamma_override if gamma_override is not None else cfg['gamma']
    omega  = omega_override if omega_override is not None else cfg['omega']
    params = [beta, cfg['sigma'], gamma, omega, DELTA_D, DELTA_R, Lambda, MU, ALPHA, N]
    y0     = get_initial_conditions(cfg)
    return odeint(hiv_model, y0, t, args=(params,))
