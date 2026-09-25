# Black-Scholes Option Pricer & Portfolio Manager

Application interactive construite en Python pour la tarification d'options financières, l'analyse des sensibilités (Greeks) et l'optimisation de portefeuille.

## 🚀 Fonctionnalités

1. **Option Pricer :**
   - Tarification des options Call et Put via le modèle de Black-Scholes.
   - Calcul des 5 principaux Greeks : $\Delta$ (Delta), $\Gamma$ (Gamma), $\text{Vega}$, $\Theta$ (Theta), $\rho$ (Rho).
   - Graphiques interactifs dynamiques (variation du sous-jacent $S_0$, de la volatilité $\sigma$ ou de la maturité $T$).
   - Connexion optionnelle aux données de marché en temps réel via `yfinance`.

2. **Portfolio Manager :**
   - Gestion multi-actifs (actions, calls, puts).
   - Heuristique d'optimisation par grille (Strike $K$, Maturité $T$) pour minimiser le Delta net global du portefeuille.
   - Simulation visuelle de la distribution du PnL sous approximation normale.

## English Below

Interactive application built in Python for financial option pricing, sensitivity analysis (Greeks), and portfolio optimization.

## 🚀 Features

1. **Option Pricer:**
   - Pricing of Call and Put options via the Black-Scholes model.
   - Calculation of the 5 main Greeks: $\Delta$ (Delta), $\Gamma$ (Gamma), $\text{Vega}$, $\Theta$ (Theta), $\rho$ (Rho).
   - Dynamic interactive charts (varying underlying price $S_0$, volatility $\sigma$, or maturity $T$).
   - Optional connection to real-time market data via `yfinance`.

2. **Portfolio Manager:**
   - Multi-asset management (equities, calls, puts).
   - Grid optimization heuristic (Strike $K$, Maturity $T$) to minimize the overall net portfolio Delta.
   - Visual simulation of the PnL distribution under a normal approximation.
   
---

## 🛠️ Installation et Lancement

1. **Cloner le dépôt / Clone the reposit :**
   ```bash
   git clone [https://github.com/votre-nom-d-utilisateur/black-scholes-portfolio-manager.git](https://github.com/votre-nom-d-utilisateur/black-scholes-portfolio-manager.git)
   cd black-scholes-portfolio-manager
2. **Installer les dépendances / Install requirements :**
   ```bash
   pip install -r requirements.txt
3. **Lancer l'application Streamlit / Run frontend :**
   ```bash
   streamlit run PricerappV2.py
