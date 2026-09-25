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

---

## 🛠️ Installation et Lancement

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/votre-nom-d-utilisateur/black-scholes-portfolio-manager.git](https://github.com/votre-nom-d-utilisateur/black-scholes-portfolio-manager.git)
   cd black-scholes-portfolio-manager
2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
3. **Lancer l'application Streamlit :**
   ```bash
   streamlit run PricerappV2.py
