import time
import datetime
import robin_stocks.robinhood as r

stock = "None"
shares = 0

# Get setup information from file
with open('setup.txt') as f:
    lines = f.readlines()
    stock = lines[1].strip()
    shares = lines[3].strip()
    f.close()

print("Setting up with {} shares of {}".format(shares, stock))

# Log into robinhood
login = r.login("************************@gmail.com",
                "**********************************")

# Store global variables
high = None
current = None
low = None
start = None
stopTime = datetime.time(15, 55, 0) # 5 minutes before market close

# Buys a given number of stocks, sets low limit to sell
def setup():

    global high
    global current
    global low
    global start

    prices = r.get_latest_price(stock)

    current = prices[0]
    high = float(current)
    low = float(current) * 0.99
    start = float(current)

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

def exportFinal():

    # Total profit from all shares
    profit = (current - start) * float(shares)
    percent = (current - start) / float(start) * 100
    date = datetime.datetime.now()

    # Print statement
    f = open('spreadsheet.txt', 'a')
    f.write('{}\t\t\t{}\t\t\t{}\t\t\t{}\n'.format(date, stock, percent, profit))

def debug(currentTime):

    print("At {}, price is {}".format(currentTime, current))
 
# Program starts here
setup()

while True:

    # Update current time
    currentTime = datetime.datetime.now().time().replace(microsecond=0)

    # Get current price
    try:
        prices = r.get_latest_price(stock)
        current = float(prices[0])
    except:
        pass

    # debug(currentTime)

    # Increase in value or stays the same
    if (current > high):
        high = current
        print("At {}, price is {}".format(currentTime, current))
        setLow((low + high) / 2)

    # Decrease in value
    if (current <= low):
        sell()
        break

    # Sell everything before market close
    if (currentTime >= stopTime):
        sell()
        break

    # Wait 1 second
    time.sleep(0.2)

exportFinal()

k=input("press close to exit") 