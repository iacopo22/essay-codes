# %%
import numpy as np
import matplotlib.pyplot as plt


# Parameters
np.random.seed(42)
N = 100  # number of trades
v_H = 225   # high asset value
v_L = 210   # low asset value
p0 = 0.5    # initial belief that value is high
alpha = 0.6  # probability a trader is informed
shock_trade = 50  # simulate a shock at this trade

# true value equal to v_L since it's a bad news


# %%
# Initialize storage
beliefs = []
bid_prices = []
ask_prices = []
mid_prices = []
spreads = []
orders = []
trades = []
trade_types = []

p = p0  # initial belief

# %%
def update_belief(p, order, alpha):

    if order == 'buy':
        num = float(p * 0.5 * (1 + alpha))
        denom = float(p * alpha + (1 - alpha) * 0.5)
    elif order == 'sell':
        num = float(p * 0.5 * (1 - alpha))
        denom = float(alpha * (1 - p) + 0.5 * (1 - alpha))
    return float(num / denom)

# %%
for t in range(N):

    # Decide trader type
    is_informed = np.random.rand() < alpha

    # Generate order before shock
    if t < shock_trade:  # before shock
        order = np.random.choice(['buy', 'sell'], p=[0.52, 0.48])
    elif t >= shock_trade and t <=52:  # after shock
        # Sudden info shock: change probability market thinks asset is L
        p = 0.1
        alpha = 0.1
        if is_informed:
            order = 'sell'  # Informed trader knows that asset value is low
        else:
            order = np.random.choice(['buy', 'sell'])
    else:
        p = 0.3
        alpha = 0.4
        v_H = 200
        v_L = 180
        if is_informed:
            order = 'sell'
        else:
            order = np.random.choice(['buy', 'sell'])



    # Update belief
    p = update_belief(p, order, alpha)

    # Compute bid and ask
    bid = ((1 - p) * v_L + p * v_H) - (alpha*p*(1 - p))/(alpha*p+(1-alpha)*0.5) * (v_H - v_L)  # bid discount
    ask = ((1 - p) * v_L + p * v_H) + (alpha*p*(1 - p))/(alpha*p+(1-alpha)*0.5) * (v_H - v_L) # ask premium
    mid = (bid + ask) / 2
    spread = ask - bid

    # Store
    if order == 'buy':
        trades.append(ask)
    elif order == 'sell':
        trades.append(bid)
    beliefs.append(p)
    bid_prices.append(bid)
    ask_prices.append(ask)
    mid_prices.append(mid)
    spreads.append(spread)
    orders.append(order)

# --- Plotting ---
# %%
plt.figure(figsize=(18, 9))
plt.plot(mid_prices, label='Mid Price')
plt.plot(bid_prices, linestyle='--', label='Bid Price')
plt.plot(ask_prices, linestyle='--', label='Ask Price')
plt.axvline(shock_trade, color='red', linestyle=':', label='Tariff Shock')
plt.title('Glosten-Milgrom Simulation of Market Reaction to News')
plt.xlabel('Trade Number')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

# %%
plt.figure(figsize=(10, 4))
plt.plot(spreads, color='orange')
plt.axvline(shock_trade, color='red', linestyle=':', label='Tariff Shock')
plt.title('Bid-Ask Spread Evolution')
plt.xlabel('Trade Number')
plt.ylabel('Spread')
plt.grid(True)
plt.show()

# %%

