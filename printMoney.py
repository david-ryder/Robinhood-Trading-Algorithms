import readline
import time
import datetime
import robin_stocks.robinhood as r

### ONLY TOUCH THESE ###
stock = "None"
shares = 0
### ---------------- ###

# Get setup information from file
with open('setup.txt') as f:
    lines = f.readlines()
    stock = lines[1].strip()
    shares = lines[3].strip()

# Login to robinhood
login = r.login("drw12512@gmail.com",
                "Knightro@123")

high = None
current = None
low = None
stopTime = datetime.time(15, 55, 0) # 5 minutes before market close

# Buys a given number of a in a b, sets low limit to sell
def setup():

    global high
    global current
    global low

    prices = r.get_latest_price(stock)

    current = prices[0]
    high = current
    low = current * 0.999

    # Buy the specified stock
    buy()

    # Initiate stop loss order
    setLow(low)

# Buys a number of whole stock
def buy():

    print("Buying {} share(s) of {} at {}".format(shares, stock, current))

    try:
        r.order_buy_market(stock, shares)
    except Exception as e:
        print(e)

# Sells a number of whole a of a b
def sell():

    print("Selling {} share(s) of {} at {}".format(shares, stock, current))

    try:
        r.order_sell_market(stock, shares)
    except Exception as e:
        print(e)

# Sets lowPrice for the stock
def setLow(val):

    print("Setting low-point at: {}".format(val))

    try:
        r.order_sell_stop_loss(stock, shares, val)
    except Exception as e:
        print(e)
 
# Program starts here
setup()

while True:

    # Update current time
    currentTime = datetime.datetime.now().time().replace(microsecond=0)

    # Get current price
    prices = r.get_latest_price(stock)

    current = prices[0]

    # Increase in value
    if (high < current):
        high = current
        setLow((low + high) / 2)

    # Sell everything before market close
    if (currentTime == stopTime):
        sell(shares, stock)
        break

    # Wait 1 second
    time.sleep(1)