# HIV Transmission & Drug Resistance Modeling — North-East India

**Rohan Biswas** | Presented at EDNEIHA-2026, Tezpur University (March 2026)

A compartmental mathematical model (S-I-D-T-R ODE system) analyzing HIV transmission dynamics and antimicrobial resistance (AMR) risk in four high-burden North-Eastern Indian states: Mizoram, Nagaland, Manipur, and Assam.

---

## Key Findings

| State | 2024 Prevalence | 2029 Projected | Resistant Compartment Growth |
|-------|----------------|----------------|------------------------------|
| Mizoram | 2.75% | ~2.64% | +17% |
| Nagaland | 1.37% | ~1.57% | +23% |
| Manipur | 0.81% | ~0.98% | **+82%** |
| Assam | 0.13% | ~0.10% | +42% |

**Bottom line:** Even when ART linkage is strong, small virologic failure rates accumulate into a rapidly growing resistant reservoir especially in IDU-dominated states. Standard cascade metrics miss this risk.

---

## Model Structure

Five compartments tracking population flow:

```
S (Susceptible) -> I (Infected, undiagnosed) -> D (Diagnosed, not on ART)
                                             -> T (On ART, virally suppressed)
                                             -> R (Virologic failure / Resistance)
```

Parameters are fully empirical, calibrated to **NACO 2024/2025 state-level surveillance data**.

---

## Repository Structure

```
├── model.py          # ODE system, state configs, solver
├── simulations.py    # Baseline, Monte Carlo (200 sims, ±15% noise), scenario analysis
├── plots.py          # All figures (run to regenerate)
├── outputs/          # Generated plots
├── data/ 	          # Datasets generated from NACO state-level surveillance data
└── README.md
```

---

## Usage

```bash
pip install numpy scipy matplotlib
python plots.py        # generates all three figures in outputs/
python simulations.py  # prints projection summaries to console
```

---

## Data Sources

- NACO. *HIV Estimation 2025 Technical Report.* Ministry of Health & Family Welfare, Government of India, 2025.
- State-level PLHIV estimates, ART cascade indicators, and new infection counts from NACO state dashboards.

---

## Citation

If you use this model, please cite:

> Biswas, R. (2026). *Decoupling the HIV Care Cascade: A Data-Driven Mathematical Model for Transmission Dynamics and Anti-Microbial Resistance (AMR) Risks in North-East India.* Poster presented at EDNEIHA-2026: Emerging Diseases in North-East India: A Data-Driven One Health Approach, Tezpur University, India. DOI: 10.13140/RG.2.2.22730.22729

---

*Contact: rohanbiswas031@gmail.com*
