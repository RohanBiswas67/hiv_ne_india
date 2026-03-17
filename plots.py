"""
Plots: Baseline, Monte Carlo uncertainty, Scenario comparison
Author: Rohan Biswas
Run: python plots.py
"""

import numpy as np
import matplotlib.pyplot as plt
from model import STATES
from simulations import T, run_baseline, run_monte_carlo, run_scenarios, SCENARIOS

SCENARIO_COLORS = {'status_quo': 'blue', 'high_IDU': 'orange', 'intervention': 'green'}
SCENARIO_LABELS = {'status_quo': 'Status Quo', 'high_IDU': 'High-IDU Shock (beta*1.3)', 'intervention': 'Intervention Success'}


def plot_baseline(results):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axs = axs.flatten()
    for i, (state, res) in enumerate(results.items()):
        ax  = axs[i]
        cfg = STATES[state]
        ax.plot(T, res['prev'], 'b-', lw=2.5, label='Projected Prevalence (%)')
        ax.axhline(cfg['prev_pct'], color='r', ls='--', label=f"2024 NACO ({cfg['prev_pct']}%)")
        inset = ax.inset_axes([0.65, 0.55, 0.3, 0.35])
        inset.plot(T, res['R'], 'r-', lw=1.8)
        inset.set_title('Resistant R (AMR)', fontsize=9)
        inset.grid(True, alpha=0.6)
        ax.set_title(f'{state} (2024–2029)')
        ax.set_ylabel('Prevalence (%)')
        ax.legend(); ax.grid(True)
    for ax in axs: ax.set_xlabel('Years')
    plt.tight_layout()
    plt.savefig('outputs/baseline_projections.png', dpi=300)
    plt.show()
    print("Saved: outputs/baseline_projections.png")


def plot_monte_carlo(results):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axs = axs.flatten()
    for i, (state, res) in enumerate(results.items()):
        ax  = axs[i]
        cfg = STATES[state]
        ax.plot(T, res['prev_mean'], 'b-', lw=2, label='Mean Prevalence')
        ax.fill_between(T, res['prev_low'], res['prev_high'], alpha=0.25, color='blue', label='95% CI')
        ax.axhline(cfg['prev_pct'], color='r', ls='--', label=f"2024 NACO ({cfg['prev_pct']}%)")
        ax.set_title(f'{state} — Uncertainty (200 MC sims)')
        ax.set_ylabel('Prevalence (%)')
        ax.legend(fontsize=9); ax.grid(True, alpha=0.5)
    for ax in axs: ax.set_xlabel('Years from 2024')
    plt.tight_layout()
    plt.savefig('outputs/monte_carlo_uncertainty.png', dpi=300)
    plt.show()
    print("Saved: outputs/monte_carlo_uncertainty.png")


def plot_scenarios(results):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axs = axs.flatten()
    for i, (state, scen_results) in enumerate(results.items()):
        ax  = axs[i]
        cfg = STATES[state]
        for scen, res in scen_results.items():
            ax.plot(T, res['prev'], color=SCENARIO_COLORS[scen], label=SCENARIO_LABELS[scen])
        ax.axhline(cfg['prev_pct'], color='red', ls='--', lw=1.5, label=f"2024 NACO ({cfg['prev_pct']}%)")
        ax.set_title(f'{state} (2024–2029 Scenarios)')
        ax.set_ylabel('Prevalence (%)')
        ax.legend(fontsize=9); ax.grid(True, alpha=0.5)
    for ax in axs: ax.set_xlabel('Years from 2024')
    plt.tight_layout()
    plt.savefig('outputs/scenario_projections.png', dpi=300)
    plt.show()
    print("Saved: outputs/scenario_projections.png")


if __name__ == '__main__':
    import os; os.makedirs('outputs', exist_ok=True)
    print("Generating baseline plot...")
    plot_baseline(run_baseline())
    print("Generating Monte Carlo plot...")
    plot_monte_carlo(run_monte_carlo())
    print("Generating scenario plot...")
    plot_scenarios(run_scenarios())
