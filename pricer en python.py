import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# --- Black-Scholes Call et Put ---
def black_scholes_call(S0, K, T, r, sigma):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return round(call_price, 4)

def black_scholes_put(S0, K, T, r, sigma):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    return round(put_price, 4)

# --- Greeks ---
def black_scholes_greeks(S0, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    pdf_d1 = norm.pdf(d1)  # densité de la loi normale en d1

    # Commun aux deux
    Gamma = pdf_d1 / (S0 * sigma * np.sqrt(T))
    Vega = S0 * pdf_d1 * np.sqrt(T) / 100  # /100 pour être en "pour 1%"

    if option_type == "call":
        Delta = norm.cdf(d1)
        Theta = (- (S0 * pdf_d1 * sigma) / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        Rho = (K * T * np.exp(-r * T) * norm.cdf(d2)) / 100
    else:  # put
        Delta = norm.cdf(d1) - 1
        Theta = (- (S0 * pdf_d1 * sigma) / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        Rho = (-K * T * np.exp(-r * T) * norm.cdf(-d2)) / 100
    
    return {
        "Delta": round(Delta, 4),
        "Gamma": round(Gamma, 4),
        "Vega": round(Vega, 4),
        "Theta": round(Theta, 4),
        "Rho": round(Rho, 4)
    }

# --- Exemple de test ---
if __name__ == "__main__":
    # Paramètres
    S0 = 100     # prix de l'actif
    K = 100      # strike
    T = 1        # maturité (1 an)
    r = 0.05     # taux sans risque 5%
    sigma = 0.2  # volatilité 20%

    call_price = black_scholes_call(S0, K, T, r, sigma)
    put_price = black_scholes_put(S0, K, T, r, sigma)
    greeks_call = black_scholes_greeks(S0, K, T, r, sigma, option_type="call")
    greeks_put = black_scholes_greeks(S0, K, T, r, sigma, option_type="put")

    print("Prix Call :", call_price)
    print("Prix Put  :", put_price)
    print("\nGreeks (Call):", greeks_call)
    print("Greeks (Put) :", greeks_put)

# --- Tableaux de sensibilité ---
def sensitivity_table(S_range, K, T, r, sigma):
    """
    Génère un tableau (dict) du prix du call et Delta
    en fonction de S0 (prix du sous-jacent)
    """
    results = []
    for S0 in S_range:
        call_price = black_scholes_call(S0, K, T, r, sigma)
        greeks = black_scholes_greeks(S0, K, T, r, sigma, option_type="call")
        results.append({
            "S0": round(S0, 2),
            "Call": call_price,
            "Delta": greeks["Delta"],
            "Gamma": greeks["Gamma"],
            "Vega": greeks["Vega"],
            "Theta": greeks["Theta"],
            "Rho": greeks["Rho"]
        })
    return results

# Exemple : faire varier S0 de 80 à 120
if __name__ == "__main__":
    S_values = np.linspace(80, 120, 9)  # 9 valeurs entre 80 et 120
    table = sensitivity_table(S_values, K=100, T=1, r=0.05, sigma=0.2)
    print("\nTableau de sensibilite (Call en fonction de S0) :")
    for row in table:
        print(row)

def plot_option_prices(K, T, r, sigma):
    S_values = np.linspace(50, 150, 100)
    call_prices = [black_scholes_call(S, K, T, r, sigma) for S in S_values]
    put_prices  = [black_scholes_put(S, K, T, r, sigma) for S in S_values]

    plt.figure(figsize=(8,5))
    plt.plot(S_values, call_prices, label="Call", color="blue")
    plt.plot(S_values, put_prices, label="Put", color="red")
    plt.xlabel("Prix du sous-jacent (S0)")
    plt.ylabel("Valeur de l'option")
    plt.title("Prix des options (Black-Scholes)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Exemple : tracer les prix
if __name__ == "__main__":
    plot_option_prices(K=100, T=1, r=0.05, sigma=0.2)

def plot_delta(K, T, r, sigma):
    S_values = np.linspace(50, 150, 100)
    deltas = [black_scholes_greeks(S, K, T, r, sigma, option_type="call")["Delta"] for S in S_values]

    plt.figure(figsize=(8,5))
    plt.plot(S_values, deltas, label="Delta (Call)", color="green")
    plt.xlabel("Prix du sous-jacent (S0)")
    plt.ylabel("Delta")
    plt.title("Delta du Call en fonction de S0")
    plt.grid(True)
    plt.legend()
    plt.show()

# Exemple
if __name__ == "__main__":
    plot_delta(K=100, T=1, r=0.05, sigma=0.2)
