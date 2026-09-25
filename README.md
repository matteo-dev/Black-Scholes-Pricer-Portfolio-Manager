# Black-Scholes Option Pricer & Portfolio Manager

Application interactive construite en Python pour la tarification d'options financières, l'analyse des sensibilités (Greeks) et l'optimisation de portefeuille[cite: 1, 2].

## 🚀 Fonctionnalités

1. **Option Pricer :**
   - Tarification des options Call et Put via le modèle de Black-Scholes[cite: 1, 2].
   - Calcul des 5 principaux Greeks : $\Delta$ (Delta), $\Gamma$ (Gamma), $\text{Vega}$, $\Theta$ (Theta), $\rho$ (Rho)[cite: 1, 2].
   - Graphiques interactifs dynamiques (variation du sous-jacent $S_0$, de la volatilité $\sigma$ ou de la maturité $T$)[cite: 1, 2].
   - Connexion optionnelle aux données de marché en temps réel via `yfinance`[cite: 1, 2].

2. **Portfolio Manager :**
   - Gestion multi-actifs (actions, calls, puts).
   - Heuristique d'optimisation par grille (Strike $K$, Maturité $T$) pour minimiser le Delta net global du portefeuille[cite: 2].
   - Simulation visuelle de la distribution du PnL sous approximation normale[cite: 2].

---

## 🛠️ Installation et Lancement

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/votre-nom-d-utilisateur/black-scholes-portfolio-manager.git](https://github.com/votre-nom-d-utilisateur/black-scholes-portfolio-manager.git)
   cd black-scholes-portfolio-manager
