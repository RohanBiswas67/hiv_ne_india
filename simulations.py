"""
Simulations: Baseline, Monte Carlo uncertainty, Scenario analysis
Author: Rohan Biswas
"""

import numpy as np
from model import STATES, run_model

T = np.linspace(0, 5, 61)  # 5 years, monthly steps
N_SIMULATIONS = 200
NOISE = 0.15  # ±15% parameter noise for Monte Carlo
np.random.seed(42)


# ── 1. Baseline projection ─────────────────────────────────────────────────────
def run_baseline():
    results = {}
    for state, cfg in STATES.items():
        sol = run_model(cfg, T)
        N   = cfg['N']
        results[state] = {
            'sol':  sol,
            'prev': (sol[:,1] + sol[:,2] + sol[:,3] + sol[:,4]) / N * 100,
            'R':    sol[:,4],
            'R0':   sol[0, 4]
        }
    return results


# ── 2. Monte Carlo uncertainty analysis ───────────────────────────────────────
def run_monte_carlo():
    results = {}
    for state, cfg in STATES.items():
        N        = cfg['N']
        prevs, Rs = [], []
        for _ in range(N_SIMULATIONS):
            noise  = 1 + np.random.uniform(-NOISE, NOISE, 4)
            b, s, g, w = (cfg['beta']*noise[0], cfg['sigma']*noise[1],
                          cfg['gamma']*noise[2], cfg['omega']*noise[3])
            sol    = run_model(cfg, T, beta_override=b, gamma_override=g, omega_override=w)
            prevs.append((sol[:,1]+sol[:,2]+sol[:,3]+sol[:,4]) / N * 100)
            Rs.append(sol[:,4])
        prevs, Rs = np.array(prevs), np.array(Rs)
        results[state] = {
            'prev_mean':  prevs.mean(axis=0),
            'prev_low':   np.percentile(prevs, 2.5, axis=0),
            'prev_high':  np.percentile(prevs, 97.5, axis=0),
            'R_mean':     Rs.mean(axis=0),
            'R_low':      np.percentile(Rs, 2.5, axis=0),
            'R_high':     np.percentile(Rs, 97.5, axis=0),
            'R0':         Rs[:, 0].mean()
        }
    return results


# ── 3. Scenario analysis ───────────────────────────────────────────────────────
SCENARIOS = {
    'status_quo':   {},
    'high_IDU':     {'beta_scale': 1.3},
    'intervention': {'gamma_override': 0.99, 'omega_override': 0.003}
}

def run_scenarios():
    results = {}
    for state, cfg in STATES.items():
        results[state] = {}
        for scen, overrides in SCENARIOS.items():
            beta  = cfg['beta'] * overrides.get('beta_scale', 1.0)
            gamma = overrides.get('gamma_override', None)
            omega = overrides.get('omega_override', None)
            sol   = run_model(cfg, T, beta_override=beta,
                              gamma_override=gamma, omega_override=omega)
            N     = cfg['N']
            results[state][scen] = {
                'prev':  (sol[:,1]+sol[:,2]+sol[:,3]+sol[:,4]) / N * 100,
                'R_end': sol[-1, 4]
            }
    return results


if __name__ == '__main__':
    print("Running baseline...")
    b = run_baseline()
    for s, r in b.items():
        print(f"{s}: 2029 prev = {r['prev'][-1]:.2f}%")

    print("\nRunning Monte Carlo (200 sims)...")
    mc = run_monte_carlo()
    for s, r in mc.items():
        print(f"{s}: prev {r['prev_mean'][-1]:.2f}% "
              f"[{r['prev_low'][-1]:.2f}–{r['prev_high'][-1]:.2f}]  "
              f"R growth ~{100*(r['R_mean'][-1]-r['R0'])/r['R0']:+.0f}%")

    print("\nRunning scenarios...")
    sc = run_scenarios()
    labels = {'status_quo': 'Status Quo', 'high_IDU': 'High-IDU', 'intervention': 'Intervention'}
    for state in sc:
        print(f"\n{state}")
        for scen, res in sc[state].items():
            print(f"  {labels[scen]:<14} | Prev: {res['prev'][-1]:.2f}%  R: {res['R_end']:.0f}")
