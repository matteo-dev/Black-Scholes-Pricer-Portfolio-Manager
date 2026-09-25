# Importing necessary libraries
import streamlit as st # Import Streamlit for the web interface
import numpy as np # Import NumPy for numerical calculations
from scipy.stats import norm # Import the normal distribution from SciPy
import plotly.graph_objects as go # Import Plotly for interactive charts
import yfinance as yf # Import yfinance to retrieve market data

# Black-Scholes functions and Greeks

# Function to calculate d1 and d2
def d1_d2(S0, K, T, r, sigma):
    eps = 1e-12 # Small value to avoid division by zero
    sigma = max(sigma, eps) # Minimum volatility
    T = max(T, eps) # Minimum maturity
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

# Function to calculate the price of a call option 
def black_scholes_call(S0, K, T, r, sigma):
    d1, d2 = d1_d2(S0, K, T, r, sigma)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Function to calculate the price of a put option
def black_scholes_put(S0, K, T, r, sigma):
    d1, d2 = d1_d2(S0, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

# Function to calculate Greeks
def black_scholes_greeks_scalar(S0, K, T, r, sigma, option_type="call"):
    d1, d2 = d1_d2(S0, K, T, r, sigma)
    pdf_d1 = norm.pdf(d1)

    # Compute Gamma
    Gamma = pdf_d1 / (S0 * sigma * np.sqrt(T)) # Gamma measures the sensitivity of Delta to the underlying price
    # It is the second derivative of the option price with respect to the underlying price

    # Compute Vega
    Vega = S0 * pdf_d1 * np.sqrt(T) # Vega measures the sensitivity of the price to volatility
    # It is the derivative of the price with respect to volatility

    # Compute Delta, Theta, Rho
    if option_type == "call": # Call option

        Delta = norm.cdf(d1) # Delta measures the sensitivity of the price to the underlying asset price
        # It is the derivative of the price with respect to the underlying asset price

        Theta = - (S0 * pdf_d1 * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2) # Theta measures the sensitivity of the price to time
        # It is the derivative of the price with respect to time

        Rho = K * T * np.exp(-r * T) * norm.cdf(d2) # Rho measures the sensitivity of the price to the interest rate
        # It is the derivative of the price with respect to the interest rate

    else: # Put option
        Delta = norm.cdf(d1) - 1
        Theta = - (S0 * pdf_d1 * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        Rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    return {"Delta": Delta, "Gamma": Gamma, "Vega": Vega, "Theta": Theta, "Rho": Rho}

# Vectorized function to compute price and Greeks while varying one parameter
def greek_vectorized(vary_on, vary_values, K, T, r, sigma, option_type="call", base_S0=100):
    # Initialize lists to store results
    prices, deltas, gammas, vegas, thetas, rhos = [], [], [], [], [], []

    # Loop through the parameter values
    for v in vary_values:
        if vary_on == "S0":
            S0_v = v; sigma_v = sigma; T_v = T
        elif vary_on == "sigma":
            S0_v = base_S0; sigma_v = v; T_v = T
        elif vary_on == "T":
            S0_v = base_S0; sigma_v = sigma; T_v = v
        else:
            raise ValueError("Unknown vary_on parameter.")

        # Compute the price and Greeks
        price = black_scholes_call(S0_v, K, T_v, r, sigma_v) if option_type=="call" else black_scholes_put(S0_v, K, T_v, r, sigma_v)
        greeks = black_scholes_greeks_scalar(S0_v, K, T_v, r, sigma_v, option_type)

        # Store the results
        prices.append(price)
        deltas.append(greeks["Delta"])
        gammas.append(greeks["Gamma"])
        vegas.append(greeks["Vega"])
        thetas.append(greeks["Theta"])
        rhos.append(greeks["Rho"])

    return {"price": np.array(prices), "Delta": np.array(deltas), "Gamma": np.array(gammas),
            "Vega": np.array(vegas), "Theta": np.array(thetas), "Rho": np.array(rhos)}

# Function to retrieve the latest price from yfinance
def get_last_price_from_ticker(ticker):
    try:
        data = yf.Ticker(ticker)
        last = data.info.get("regularMarketPrice", None)
        if last is None:
            hist = data.history(period="5d")
            if not hist.empty:
                last = float(hist["Close"].iloc[-1])
        return last
    except:
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Black-Scholes Pricer & Greeks", layout="wide")
st.title("Black-Scholes Pricer — Price & Greeks (Interactive)")

# Sidebar for option parameters
st.sidebar.header("Option Parameters")
option_type = st.sidebar.selectbox("Option type", ["call", "put"])
use_market = st.sidebar.checkbox("Fetch underlying price from yfinance", value=False)

default_S0 = 100.0
ticker = ""
# Retrieve underlying price if requested
if use_market:
    ticker = st.sidebar.text_input("Yfinance ticker (e.g., ^FCHI, EURUSD=X)", value="^FCHI")
    if ticker:
        last = get_last_price_from_ticker(ticker)
        if last is not None:
            default_S0 = float(last)
            st.sidebar.success(f"Fetched price: {default_S0:.4f}")
        else:
            st.sidebar.warning("Unable to retrieve price for this ticker.")

# Option parameters
S0 = st.sidebar.number_input("S0 (spot price)", value=float(default_S0), format="%.4f")
K = st.sidebar.number_input("K (strike)", value=100.0, format="%.4f")
T = st.sidebar.number_input("T (maturity in years)", value=1.0, min_value=0.0001, format="%.4f")
r = st.sidebar.number_input("r (risk-free rate)", value=0.05, format="%.4f")
sigma = st.sidebar.number_input("sigma (volatility)", value=0.2, min_value=0.0001, format="%.4f")

# Parameter to vary
st.sidebar.header("Parameter to vary for plots")
vary_on = st.sidebar.radio("Vary", ("S0", "sigma", "T"))
if vary_on == "S0":
    vmin = st.sidebar.number_input("S0 min", value=max(1.0, S0*0.5), format="%.4f")
    vmax = st.sidebar.number_input("S0 max", value=max(S0*1.5, vmin+1), format="%.4f")
elif vary_on == "sigma":
    vmin = st.sidebar.number_input("sigma min", value=0.01, format="%.4f")
    vmax = st.sidebar.number_input("sigma max", value=1.0, format="%.4f")
elif vary_on == "T":
    vmin = st.sidebar.number_input("T min", value=0.01, format="%.4f")
    vmax = st.sidebar.number_input("T max", value=max(5.0, T), format="%.4f")

# Number of points for the plot
n_points = st.sidebar.slider("Number of points", 10, 500, 200)

# Choice of Greeks to display
st.sidebar.header("Display")
show_price = st.sidebar.checkbox("Show price", value=True)
greeks_to_show = st.sidebar.multiselect("Greeks to display", ["Delta", "Gamma", "Vega", "Theta", "Rho"], default=["Delta","Gamma"])

# Calculations
price_val = black_scholes_call(S0, K, T, r, sigma) if option_type=="call" else black_scholes_put(S0, K, T, r, sigma)
greeks_val = black_scholes_greeks_scalar(S0, K, T, r, sigma, option_type)

# Display results
col1, col2 = st.columns([1,2])
with col1:
    st.subheader("Values (central point)")
    st.write(f"Option: **{option_type.upper()}**")
    st.write(f"S0 = {S0:.4f}, K = {K:.4f}, T = {T:.4f}, r = {r:.4f}, sigma = {sigma:.4f}")
    if show_price:
        st.metric("Theoretical price", f"{price_val:.4f}")
    st.markdown("**Greeks (central point)**")
    st.write({k: round(v, 4 if k!="Gamma" else 6) for k,v in greeks_val.items()})

# Display interactive plot
with col2:
    st.subheader("Interactive plot")
    vary_values = np.linspace(vmin, vmax, n_points)
    results = greek_vectorized(vary_on, vary_values, K, T, r, sigma, option_type, base_S0=S0)

    fig = go.Figure()
    if show_price:
        fig.add_trace(go.Scatter(x=vary_values, y=results["price"], name="Price", mode="lines",
                                 hovertemplate="%{x:.4f}: %{y:.4f}<extra></extra>"))
    for g in greeks_to_show:
        fig.add_trace(go.Scatter(x=vary_values, y=results[g], name=g, mode="lines",
                                 hovertemplate="%{x:.4f}: %{y:.6f}<extra></extra>"))
    xlabel = {"S0":"Underlying price (S0)", "sigma":"Volatility (sigma)", "T":"Maturity (years)"}[vary_on]
    fig.update_layout(title=f"Price and Greeks as a function of {vary_on}", xaxis_title=xlabel, yaxis_title="Value", height=520)
    st.plotly_chart(fig, use_container_width=True)