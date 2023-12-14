# 一.DYDX、GMX、APEX简介

官方链接：

DYDX:https://dydx.exchange

GMX:https://gmx.io

APEX:https://www.apex.exchange



**1.GMX交易机制：**

**AMM模式**，GMX使用定制预言机从3个CEX（Binance、Coinbase和BitFinex）提取价格，**零滑点**，最高支持50倍杠杆。

与交易者进行博弈的不是交易者，而是LP提供者，可以理解为交易者获利，则LP提供者亏损，反之如是。



![GMX](photo\GMX.png)

**2.DYDX交易机制：**

**订单薄模式**，用户在 DYDX平台可以下市价单和限价单，DYDX 引入了做市商提供流动性，追求撮合效率，最高支持20倍杠杆。DYDX（ V3）是搭建在以太坊 L2 的 Starkware 网络上的 DeFi 衍生品交易平台。 DYDX 采用链下订单簿、链上结算模式，用户在DYDX 平台的交易体验几乎可以和CEX相媲美。而 DYDX V4 版本将会迁移到 Cosmos 网络上，创建一条独立的 L1 区块链 DYDX Chain，具有完全去中心化的链下订单簿和匹配引擎,目前已上线测试网。



**3.APEX交易机制：**

**订单薄模式**，类似于DYDX，基于L2的 Starkware ，链下订单薄，链上结算，最高支持30倍杠杆。



上述DEX支持链及品种对比如下：

![venn1](photo\venn1.svg)





![venn2 ](photo\venn2 .svg)

# 二.Public API调用

## 1.dydx

文档地址：https://dydxprotocol.github.io/v3-teacher/#terms-of-service-and-privacy-policy



### (1)安装client

**a.Python Client**

Install `dydx-v3-python` from [PyPI](https://pypi.org/project/dydx-v3-python) using `pip`:

`pip install dydx-v3-python`

**b.TypeScript Client**

Install `@dydxprotocol/v3-client` from [NPM](https://www.npmjs.com/package/@dydxprotocol/v3-client):

```
npm i -s @dydxprotocol/v3-client
```

### (2)client初始化

| Module     | Description                                                  |
| ---------- | ------------------------------------------------------------ |
| public     | Public API endpoints. Does not require authentication.       |
| onboarding | Endpoint to create a new user, authenticated via Ethereum key. |
| api_keys   | Endpoints for managing API keys, authenticated via Ethereum key. |
| private    | All other private endpoints, authenticated via API key.      |
| eth        | Calling and querying L1 Ethereum smart contracts.            |

The following configuration options are available:

| Parameter                | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| host                     | The HTTP API host.                                           |
| api_timeout              | Timeout for HTTP requests, in milliseconds.                  |
| default_ethereum_address | (Optional) The default account for Ethereum key auth and sending Ethereum transactions. |
| eth_private_key          | (Optional) May be used for Ethereum key auth.                |
| eth_send_options         | (Optional) Options for Ethereum transactions, see [`sendTransaction`](https://web3py.readthedocs.io/en/stable/web3.eth.html?highlight=signTransaction#web3.eth.Eth.sendTransaction). |
| network_id               | (Optional) Chain ID for Ethereum key auth and smart contract addresses. Defaults to `web3.net.version` if available, or `1` (mainnet). |
| stark_private_key        | (Optional) STARK private key, used to sign orders and withdrawals. |
| web3                     | (Optional) Web3 object used for Ethereum key auth and/or smart contract interactions. |
| web3_account             | (Optional) May be used for Ethereum key auth.                |
| web3_provider            | (Optional) Web3 provider object, same usage as `web3`.       |
| api_key_credentials      | (Optional) Dictionary containing the key, secret and passphrase required for the private module to sign requests. |
| crypto_c_exports_path    | (Optional) For python only, will use faster C++ code to run hashing, signing and verifying. It's expected to be compiled from the `crypto_c_exports` target from Starkware's [repository](https://github.com/starkware-libs/crypto-cpp/blob/master/src/starkware/crypto/ffi/CMakeLists.txt). See [section on this below for more information](https://dydxprotocol.github.io/v3-teacher/#c-methods-for-faster-stark-signing). |



**python examples：**

https://github.com/dydxprotocol/dydx-v3-python/blob/master/examples/onboard.py



**js examples：**

https://github.com/dydxprotocol/v3-client/tree/master/examples



### (3).调用对应API获取价格数据

获取订单薄：

**HTTP Request**

```
GET v3/orderbook/:market
```

 Returns bids and asks which are each Orderbook order arrays (price and size).

Description: Returns the active orderbook for a market. All bids and asks that are fillable are returned.

**Request**

| Parameter | Description              |
| --------- | ------------------------ |
| market    | Market of the Orderbook. |

**Response**

| Parameter | Description                                                  |
| --------- | ------------------------------------------------------------ |
| bids      | See Orderbook Order below. Sorted by price in descending order. |
| asks      | See Orderbook Order below. Sorted by price in ascending order. |

**Orderbook Order**

| Parameter | Description                                        |
| --------- | -------------------------------------------------- |
| price     | The price of the order (in quote / base currency). |
| size      | The size of the order (in base currency).          |

**examples：**

**python：**

```python
from dydx3.constants import MARKET_BTC_USD

orderbook = client.public.get_orderbook(
  market=MARKET_BTC_USD,
)

```



**js：**

```javascript
const orderbook: OrderbookResponseObject = await client.public.getOrderbook(
  Market.BTC_USD,
);

```



**python版本运行测试如下：**

![get_data_dydx](photo\get_data_dydx.png)



**bug：**

刚运行时报错：

`ImportError: cannot import name 'getargspec' from 'inspect'`

解决方法：

`goto => site-packages/parsimonious/expressions.py and change import line to say..... from inspect import getfullargspec`



**代码更新，获取所有市场的订单薄**：

使用前先安装`pip install asyncio`

```python
import asyncio
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, \
    MARKET_AVAX_USD, MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, \
    MARKET_DOGE_USD, MARKET_LTC_USD, MARKET_BCH_USD

# List of markets to track
markets = [MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, MARKET_AVAX_USD, 
           MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, MARKET_DOGE_USD, 
           MARKET_LTC_USD, MARKET_BCH_USD]

# Function to fetch orderbook data for a market 
async def fetch_and_save_orderbook(client, market):
    while True:
        orderbook_response = client.public.get_orderbook(market=market)
        orderbook_data = orderbook_response.data
    
        print(f'Order book for {market}:{orderbook_data}')

        # Wait for 10 seconds before fetching data again
        await asyncio.sleep(10)

async def main():
    client = Client(host='https://api.dydx.exchange')

    # Start tasks for each market
    tasks = [asyncio.create_task(fetch_and_save_orderbook(client, market)) for market in markets]

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

```

**代码更新，将数据存入csv文件：**

```python
import asyncio
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, \
    MARKET_AVAX_USD, MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, \
    MARKET_DOGE_USD, MARKET_LTC_USD, MARKET_BCH_USD
import csv
import time

# 要追踪的市场列表
markets = [MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, MARKET_AVAX_USD,
           MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, MARKET_DOGE_USD,
           MARKET_LTC_USD, MARKET_BCH_USD]

# 获取市场订单薄数据的函数
async def fetch_and_save_orderbook(client, market):
    csv_file_path = f'order_book_{market}_dydx.csv'
    print(f'starting collect data of {market}...')

    while True:
        orderbook_response = client.public.get_orderbook(market=market)
        orderbook_data = orderbook_response.data

        # 提取卖单和买单数据
        asks = orderbook_data['asks']
        bids = orderbook_data['bids']

        # 获取当前时间戳
        timestamp = int(time.time())

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(['Size', 'Price', 'Type', 'Timestamp', 'Market'])

            # Write ask data to CSV
            for ask in asks:
                writer.writerow([ask['size'], ask['price'], 'ask', timestamp, market])

            # Write bid data to CSV
            for bid in bids:
                writer.writerow([bid['size'], bid['price'], 'bid', timestamp, market])

        print(f"Order book for {market} saved to {csv_file_path}")
        # Wait for 10 seconds before fetching data again
        await asyncio.sleep(10)

async def main():
    client = Client(host='https://api.dydx.exchange')

    # 为每个市场启动一个任务
    tasks = [asyncio.create_task(fetch_and_save_orderbook(client, market)) for market in markets]

    # 等待所有任务完成
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

```





**获取不同交易市场的交易数据：**

API说明：

**Request**

| Parameter          | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| market             | Market of the trades.                                        |
| startingBeforeOrAt | (Optional): Set a date by which the trades had to be created. |
| limit              | (Optional): The number of candles to fetch (Max 100).        |

**Response**

| Parameter | Description                         |
| --------- | ----------------------------------- |
| trades    | An array of trades. See trade below |

**Trade**

| Parameter   | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| side        | Either `BUY` or `SELL.`                                      |
| size        | The size of the trade.                                       |
| price       | The price of the trade.                                      |
| createdAt   | The time of the trade.                                       |
| liquidation | `true` if the trade was the result of a liquidation. `false` otherwise. |



代码如下：

```python
import csv
import time
import hashlib
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, \
    MARKET_AVAX_USD, MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, \
    MARKET_DOGE_USD, MARKET_LTC_USD, MARKET_BCH_USD

# 初始化 dydx 客户端
client = Client(host='https://api.dydx.exchange')

# 定义不同加密货币对应的 CSV 文件路径
csv_files = {
    MARKET_BTC_USD: 'trades_data_BTCUSD_dydx.csv',
    MARKET_ETH_USD: 'trades_data_ETHUSD_dydx.csv',
    MARKET_LINK_USD: 'trades_data_LINKUSD_dydx.csv',
    MARKET_AVAX_USD: 'trades_data_AVAXUSD_dydx.csv',
    MARKET_SOL_USD: 'trades_data_SOLUSD_dydx.csv',
    MARKET_MATIC_USD: 'trades_data_MATICUSD_dydx.csv',
    MARKET_ATOM_USD: 'trades_data_ATOMUSD_dydx.csv',
    MARKET_DOGE_USD: 'trades_data_DOGEUSD_dydx.csv',
    MARKET_LTC_USD: 'trades_data_LTCUSD_dydx.csv',
    MARKET_BCH_USD: 'trades_data_BCHUSD_dydx.csv'
}

# 函数：使用 SHA-256 哈希生成交易的唯一标识
def generate_trade_id(trade):
    trade_info = f"{trade['side']}_{trade['size']}_{trade['price']}_{trade['createdAt']}"
    return hashlib.sha256(trade_info.encode()).hexdigest()

# 函数：过滤出新交易数据
def filter_new_trades(all_trades, existing_trade_ids):
    new_trades_data = []
    for trade in all_trades:
        trade_id = generate_trade_id(trade)
        if trade_id not in existing_trade_ids:
            existing_trade_ids.add(trade_id)
            trade['TradeID'] = trade_id
            new_trades_data.append(trade)
    return new_trades_data

# 初始化所有市场的 existing_trade_ids
existing_trade_ids = {market: set() for market in csv_files.keys()}

# 无限循环，每隔一分钟查询数据并存入对应 CSV 文件
while True:
    for market, csv_file_path in csv_files.items():
        # 获取交易数据
        all_trades = client.public.get_trades(market=market).data['trades']

        # 获取当前市场的 existing_trade_ids
        existing_trade_ids_current = existing_trade_ids[market]

        # 过滤出新交易数据
        new_trades_data = filter_new_trades(all_trades, existing_trade_ids_current)

        # 将新交易数据写入当前市场对应的 CSV 文件
        with open(csv_file_path, mode='a', newline='') as file:
            fieldnames = ['TradeID', 'Side', 'Size', 'Price', 'CreatedAt', 'Liquidation']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for trade in new_trades_data:
                writer.writerow({
                    'TradeID': trade['TradeID'],
                    'Side': trade['side'],
                    'Size': trade['size'],
                    'Price': trade['price'],
                    'CreatedAt': trade['createdAt'],
                    'Liquidation': trade['liquidation']
                })

        print(f'{len(new_trades_data)} new trades data saved to {csv_file_path}')

    # 等待三分钟
    time.sleep(180)

```

由于dydx的交易没有标识符，无法去重，故而我给每个交易生成了一个hash编码，方便去重

运行结果如下：

![get_currentdata_all_dydx](D:\学习资料\实习\量道投资\图片\get_currentdata_all_dydx.png)

dydx每次只能获取100笔交易，按照目前的频率，隔3分钟获取一次为佳。



## 2.apex

参考地址：https://api-docs.pro.apex.exchange/#introduction

python-examples：https://github.com/ApeX-Protocol/apexpro-openapi/blob/main/tests/demo_ws.py



### (1).安装

`pip install apexpro`





### (2).调用对应API获取数据

**GET Market Depth**

```
GET /v1/depth
```

Retrieve all active orderbook for one symbol, inclue all bids and asks.

Request Parameters

| Parameter | Position | type   | required | comment                                                      |
| --------- | -------- | ------ | -------- | ------------------------------------------------------------ |
| symbol    | query    | string | true     | use `crossSymbolName` responded from [All Config Data](https://api-docs.pro.apex.exchange/?python#publicapi-get-all-config-data) |
| limit     | query    | string | false    | Default at 100                                               |

**Response Status Code**

| status code | value | comment | data model |
| ----------- | ----- | ------- | ---------- |
| 200         | OK    | success | Inline     |

**Response Parameters**

status code **200**

| Parameter | type     | required | limit | comment |
| --------- | -------- | -------- | ----- | ------- |
| » data    | [object] | true     | none  | none    |
| »» a      | [array]  | false    | none  | Sell    |
| »» b      | [array]  | false    | none  | Buy     |
| »» s      | string   | false    | none  | Symbol  |
| »» u      | integer  | false    | none  | none    |



**Python版本运行测试如下：**

![get_data_apex](photo\get_data_apex.png)



**代码更新，获取所有市场订单薄数据，依赖安装同dydx：**

```python
import asyncio
from apexpro.constants import APEX_HTTP_MAIN
from apexpro.http_public import HttpPublic

symbols = ['BTCUSDC', 'ETHUSDC', 'LINKUSDC', 'AVAXUSDC', 'SOLUSDC', 'MATICUSDC', 'ATOMUSDC', 'DOGEUSDC', 'LTCUSDC', 'BCHUSDC']

async def fetch_order_book(symbol, client):
    while True:
        data = client.depth(symbol=symbol)
        print(f"Order book for {symbol}: {data}")

        # 每次获取后等待10秒
        await asyncio.sleep(10)

async def main():
    client = HttpPublic(APEX_HTTP_MAIN)

    # 为每个交易对启动一个任务
    tasks = [asyncio.create_task(fetch_order_book(symbol, client)) for symbol in symbols]

    # 等待所有任务完成（实际上永远不会完成）
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

```

**代码更新，将数据存入csv文件：**

```python
import asyncio
from apexpro.constants import APEX_HTTP_MAIN
from apexpro.http_public import HttpPublic
import csv
import time

symbols = ['BTCUSDC', 'ETHUSDC', 'LINKUSDC', 'AVAXUSDC', 'SOLUSDC', 'MATICUSDC', 'ATOMUSDC', 'DOGEUSDC', 'LTCUSDC', 'BCHUSDC']

async def fetch_order_book(symbol, client):
    csv_file_path = f'order_book_{symbol}_apex.csv'
    print(f'Starting data collection for {symbol}...')

    while True:
        # Get order book data
        data = client.depth(symbol=symbol)['data']

        # Extract ask and bid data
        asks = data['a']
        bids = data['b']

        # Get the current timestamp
        timestamp = time.time()

        # Print data for debugging
        print(f"Order book for {symbol} - Asks: {asks}, Bids: {bids}, Timestamp: {timestamp}")

        # Open the CSV file in append mode
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(['Price', 'Quantity', 'Type', 'Timestamp'])

            # Write data to CSV
            for ask in asks:
                writer.writerow([ask[0], ask[1], 'ask', timestamp])

            for bid in bids:
                writer.writerow([bid[0], bid[1], 'bid', timestamp])

        print(f"Order book for {symbol} saved to {csv_file_path}")
        # 每次获取后等待10秒
        await asyncio.sleep(10)

async def main():
    client = HttpPublic(APEX_HTTP_MAIN)

    # 为每个交易对启动一个任务
    tasks = [asyncio.create_task(fetch_order_book(symbol, client)) for symbol in symbols]

    # 等待所有任务完成（实际上永远不会完成）
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

```



### (3).持续获取交易数据

**API说明**：

**GET Newest Trading Data**

Retrieve trading data.

**Request Parameters**

| Parameter | Position | type   | required | comment                                                      |
| --------- | -------- | ------ | -------- | ------------------------------------------------------------ |
| symbol    | query    | string | true     | use `crossSymbolName` responded from [All Config Data](https://api-docs.pro.apex.exchange/#publicapi-get-all-config-data) |
| limit     | query    | string | false    | Limit                                                        |
| from      | query    | string | false    | Return to latest data as default                             |

**Response Status Code**

| status code | value | comment | data model |
| ----------- | ----- | ------- | ---------- |
| 200         | OK    | success | Inline     |

**Response Parameters**

status code **200**

| Parameter | type     | required | limit | comment    |
| --------- | -------- | -------- | ----- | ---------- |
| » data    | [object] | true     | none  | none       |
| »» S      | string   | false    | none  | Side       |
| »» v      | string   | false    | none  | Size       |
| »» p      | string   | false    | none  | Price      |
| »» s      | string   | false    | none  | Symbol     |
| »» T      | integer  | false    | none  | Trade time |

```python
import csv
import time
from apexpro.http_public import HttpPublic

# 初始化API客户端
client = HttpPublic("https://pro.apex.exchange")

# 定义CSV文件路径
csv_file_path = 'trades_data_BTCUSDC_apex.csv'

# 获取已存在的Trade IDs
existing_trade_ids = set()

# 无限循环，每隔一分钟获取数据并存入CSV
while True:
    # 获取交易数据
    trades_data = client.trades(symbol="BTCUSDC")['data']

    # 过滤出新数据
    new_trades_data = [entry for entry in trades_data if entry['i'] not in existing_trade_ids]

    # 更新已存在的Trade IDs
    existing_trade_ids.update(entry['i'] for entry in new_trades_data)

    # 写入CSV文件
    with open(csv_file_path, mode='a', newline='') as file:
        fieldnames = ['Trade ID', 'Price', 'Side', 'Quantity', 'Symbol', 'Timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # 将新获取的数据写入CSV
        for entry in new_trades_data:
            writer.writerow({
                'Trade ID': entry['i'],
                'Price': float(entry['p']),
                'Side': entry['S'],
                'Quantity': float(entry['v']),
                'Symbol': entry['s'],
                'Timestamp': entry['T']
            })

    print(f'{len(new_trades_data)} new trades data saved to {csv_file_path}')

    # 等待一分钟
    time.sleep(60)

```

运行结果如下：![get_currentdata_btc_apex](photo\get_currentdata_btc_apex.png)

![get_currendata_btc_apex_2](photo\get_currendata_btc_apex_2.png)



每分钟大概有20笔新交易，调用一次API是获取500笔最近的交易，那么过20分钟左右发送一次新的查询请求即可。



**代码更新：**

观察到相同交易去重部分每次程序重启就会初始为空，如果程序重启间隔较短，会往表里插入相同的数据，故而进行了修改：

```python
# 读取已存在的Trade IDs并放入集合
existing_trade_ids = set()
try:
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                existing_trade_ids.add(row[0])  # Trade ID是第一列
except FileNotFoundError:
    pass  # 如果文件不存在，可以忽略
```

目前问题已解决。

**获取不同交易市场的交易数据：**

目前只需要获取与DYDX公共的交易对，可修改symbol为：

BTCUSDC、ETHUSDC、LINKUSDC、AVAXUSDC、SOLUSDC、MATICUSDC、ATOMUSDC、DOGEUSDC、LTCUSDC、BCHUSDC

将这些数据存入不同的表里，修改后完整代码为：

```python
import csv
import time
from apexpro.http_public import HttpPublic

# 初始化API客户端
client = HttpPublic("https://pro.apex.exchange")

# 定义交易对列表
symbols = ['BTCUSDC', 'ETHUSDC', 'LINKUSDC', 'AVAXUSDC', 'SOLUSDC', 'MATICUSDC', 'ATOMUSDC', 'DOGEUSDC', 'LTCUSDC', 'BCHUSDC']

# 无限循环，每隔一分钟获取数据并存入对应的CSV
while True:
    for symbol in symbols:
        # 定义CSV文件路径
        csv_file_path = f'trades_data_{symbol}_apex.csv'

        # 读取已存在的Trade IDs并放入集合
        existing_trade_ids = set()
        try:
            with open(csv_file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        existing_trade_ids.add(row[0])  # Trade ID是第一列
        except FileNotFoundError:
            pass  # 如果文件不存在，可以忽略

        # 获取交易数据
        trades_data = client.trades(symbol=symbol)['data']

        # 过滤出新数据
        new_trades_data = [entry for entry in trades_data if entry['i'] not in existing_trade_ids]

        # 更新已存在的Trade IDs
        existing_trade_ids.update(entry['i'] for entry in new_trades_data)

        # 写入CSV文件
        with open(csv_file_path, mode='a', newline='') as file:
            fieldnames = ['Trade ID', 'Price', 'Side', 'Quantity', 'Symbol', 'Timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # 将新获取的数据写入CSV
            for entry in new_trades_data:
                writer.writerow({
                    'Trade ID': entry['i'],
                    'Price': float(entry['p']),
                    'Side': entry['S'],
                    'Quantity': float(entry['v']),
                    'Symbol': entry['s'],
                    'Timestamp': entry['T']
                })

        print(f'{len(new_trades_data)} new trades data for {symbol} saved to {csv_file_path}')

    # 等待十分钟
    time.sleep(600)

```

结果如下：

![get_currentdata_all_apex](photo\get_currentdata_all_apex.png)

可以看到，目前可以稳定收录所有数据，按照目前的交易频率，设置等待时间为10分钟比较合适



# 三.Private API调用

## 1.dydx

参考文档：

1.Programmatic Trading on dYdX：https://medium.com/dydxderivatives/programatic-trading-on-dydx-4c74b8e86d88

2.https://github.com/dydxprotocol/dydx-v3-python/blob/master/examples/onboard.py



在主网上需要获取STARK key来执行Private API

```python
from dydx3 import Client

# initial dydx client
client = Client(host='https://api.dydx.exchange',
                eth_private_key='', #换成钱包私钥
                )



# Set STARK key.
stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
(public_x, public_y) = (
    stark_key_pair_with_y_coordinate['public_key'],
    stark_key_pair_with_y_coordinate['public_key_y_coordinate'],
)

#  Onboard the account.
onboarding_response = client.onboarding.create_user(
    stark_public_key=public_x,
    stark_public_key_y_coordinate=public_y,
)
print('onboarding_response', onboarding_response)

# Query a private endpoint.
accounts_response = client.private.get_accounts()
print('accounts_response', accounts_response.data)
```

**Create A New Order**

> Create Order

```python
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_LIMIT
from dydx3.constants import TIME_IN_FORCE_GTT

placed_order = client.private.create_order(
  position_id=1, # required for creating the order signature
  market=MARKET_BTC_USD,
  side=ORDER_SIDE_SELL,
  order_type=ORDER_TYPE_LIMIT,
  post_only=False,
  size='100',
  price='18000',
  limit_fee='0.015',
  expiration_epoch_seconds=1613988637,
  time_in_force=TIME_IN_FORCE_GTT,
)
```



**HTTP Request**

```
POST v3/orders
```

Description: Create a new order.

**Request**

| Parameter       | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| market          | Market of the order.                                         |
| side            | Either `BUY` or `SELL.`                                      |
| type            | The type of order. This can be `MARKET`, `LIMIT`, `STOP_LIMIT`, `TRAILING_STOP` or `TAKE_PROFIT`. |
| postOnly        | Whether the order should be canceled if it would fill immediately on reaching the matching-engine. |
| size            | Size of the order, in base currency (i.e. an ETH-USD position of size 1 represents 1 ETH). |
| price           | Worst accepted price of the base asset in USD.               |
| limitFee        | Is the highest accepted fee for the trade. See [below](https://dydxprotocol.github.io/v3-teacher/?python#order-limitfee) for more information. |
| expiration      | Time at which the order will expire if not filled. This is the Good-Til-Time and is accurate to a granularity of about 15 seconds. |
| timeInForce     | (Optional) One of `GTT` (Good til time), `FOK`(Fill or kill) or `IOC` (Immediate or cancel). This will default to `GTT`. |
| cancelId        | (Optional) The id of the order that is being replaced by this one. |
| triggerPrice    | (Optional) The triggerPrice at which this order will go to the matching-engine. |
| trailingPercent | (Optional) The percent that the triggerPrice trails the [index price](https://dydxprotocol.github.io/v3-teacher/?python#index-price-sources) of the market. |
| reduceOnly      | (Optional) Whether the order should be [reduce-only](https://dydxprotocol.github.io/v3-teacher/?python#reduce-only). Only supported on `FOK`(Fill or kill) or `IOC` (Immediate or cancel) orders. |
| clientId        | Unique id of the client associated with the order. Must be <= 40 characters. When using the client, if not included, will be randomly generated by the client. |
| signature       | Signature for the order, signed with the account's STARK private key. When using the client, if not included, will be done by the client. For more information see [above](https://dydxprotocol.github.io/v3-teacher/?python#creating-and-signing-requests). |



**发交易**：

```python
import time

from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_BUY
from dydx3.constants import ORDER_TYPE_LIMIT

# 初始化 dydx 客户端
client = Client(host='https://api.dydx.exchange',
                eth_private_key='your private eth key',
                )



# Set STARK key.
stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
(public_x, public_y) = (
    stark_key_pair_with_y_coordinate['public_key'],
    stark_key_pair_with_y_coordinate['public_key_y_coordinate'],
)

# #  Onboard the account.
# onboarding_response = client.onboarding.create_user(
#     stark_public_key=public_x,
#     stark_public_key_y_coordinate=public_y,
# )
# print('onboarding_response', onboarding_response)

# Get our position ID.
account_response = client.private.get_account()
position_id = account_response.data['account']['positionId']


# Post an bid at a price that is unlikely to match.
order_params = {
    'position_id': position_id,
    'market': MARKET_BTC_USD,
    'side': ORDER_SIDE_BUY,
    'order_type': ORDER_TYPE_LIMIT,
    'post_only': True,
    'size': '0.0777',
    'price': '20',
    'limit_fee': '0.0015',
    'expiration_epoch_seconds': time.time() + 100,
}

order_response = client.private.create_order(**order_params)
order_id = order_response['order']['id']

print('order_response',order_response.data)

# Cancel all orders.
client.private.cancel_all_orders()
```



**bug：**

1.VPN地区不能设在美国

2.`'Order expiration cannot be less than 1 minute(s) in the future'`

```python
 'expiration_epoch_seconds': time.time() + 100 #这一行一开始写的+5，不行，改成+100就行
```

3.`get position_id error`

```python
position_id = account_response['account']['positionId']
=>
position_id = account_response.data['account']['positionId']
```





## 2.apex

参考文档：https://github.com/ApeX-Protocol/apexpro-openapi/blob/main/tests/demo_private.py



```python
from apexpro.http_private import HttpPrivate
from apexpro.constants import APEX_HTTP_TEST, NETWORKID_TEST, APEX_HTTP_MAIN, NETWORKID_MAIN


priKey = "your eth_prikey"

client = HttpPrivate(APEX_HTTP_MAIN, network_id=NETWORKID_MAIN, eth_private_key=priKey)
configs = client.configs()

stark_key_pair_with_y_coordinate = client.derive_stark_key(client.default_address)

nonceRes = client.generate_nonce(starkKey=stark_key_pair_with_y_coordinate['public_key'],ethAddress=client.default_address,chainId=NETWORKID_MAIN)

#api_key = client.recover_api_key_credentials(nonce=nonceRes['data']['nonce'], ethereum_address=client.default_address)
#print(api_key)
regRes = client.register_user(nonce=nonceRes['data']['nonce'],starkKey=stark_key_pair_with_y_coordinate['public_key'],stark_public_key_y_coordinate=stark_key_pair_with_y_coordinate['public_key_y_coordinate'],ethereum_address=client.default_address)
key = regRes['data']['apiKey']['key']
secret = regRes['data']['apiKey']['secret']
passphrase = regRes['data']['apiKey']['passphrase']

#back stark_key_pair, apiKey,and accountId for private Api or create-oreder or withdraw
# print(stark_key_pair_with_y_coordinate)
# print(regRes['data']['account']['positionId'])
# print(regRes['data']['apiKey'])

client = HttpPrivate(APEX_HTTP_MAIN, network_id=NETWORKID_MAIN, api_key_credentials={'key': key,'secret': secret, 'passphrase': passphrase})

userRes = client.get_user()

print(userRes)


```



**POST Creating Orders**

> example



```python
from apexpro.http_private_stark_key_sign import HttpPrivateStark
from apexpro.constants import APEX_HTTP_MAIN, NETWORKID_MAIN

key = 'f16ddxxxxxxxxxxx'
secret = 'Kvckxxxxxxxxxxx'
passphrase = 'Yjjd1xxxxxxxxxx'

public_key = '0x1cf0000000000'
public_key_y_coordinate = '0x7615000000000'
private_key = '0x488a6000000000'

client = HttpPrivateStark(APEX_HTTP_MAIN, network_id=NETWORKID_MAIN,
                     stark_public_key=public_key,
                     stark_private_key=private_key,
                     stark_public_key_y_coordinate=public_key_y_coordinate,
                     api_key_credentials={'key': key, 'secret': secret, 'passphrase': passphrase})

currentTime = time.time()

createOrderRes = client.create_order(symbol="BTC-USDC", side="BUY",
                                           type="LIMIT", size="0.01",
                                           price="20001", limitFee="0.001",
                                            accountId="330547708362228116",reduceOnly=False,
                                     expirationEpochSeconds= currentTime, timeInForce="GOOD_TIL_CANCEL")
```

**Request Parameters**

| Parameter         | Position | Type   | Required | Comment                                                      |
| ----------------- | -------- | ------ | -------- | ------------------------------------------------------------ |
| APEX-SIGNATURE    | header   | string | true     | Request signature                                            |
| APEX-TIMESTAMP    | header   | string | true     | Request timestamp                                            |
| APEX-API-KEY      | header   | string | true     | apiKeyCredentials.key                                        |
| APEX-PASSPHRASE   | header   | string | true     | apiKeyCredentials.passphrase                                 |
| body              | body     | object | false    | none                                                         |
| » symbol          | body     | string | true     | Symbol                                                       |
| » side            | body     | string | true     | BUY or SELL                                                  |
| » type            | body     | string | true     | "LIMIT", "MARKET","STOP_LIMIT", "STOP_MARKET", "TAKE_PROFIT_LIMIT", "TAKE_PROFIT_MARKET" |
| » size            | body     | string | true     | Size                                                         |
| » price           | body     | string | true     | Price                                                        |
| » limitFee        | body     | string | true     | limitFee = price * size * takerFeeRate( from GET /v1/account) |
| » expiration      | body     | string | true     | Order expiry time                                            |
| » timeInForce     | body     | string | false    | "GOOD_TIL_CANCEL", "FILL_OR_KILL", "IMMEDIATE_OR_CANCEL", "POST_ONLY" |
| » triggerPrice    | body     | string | false    | Trigger price                                                |
| » trailingPercent | body     | string | false    | Conditional order trailing-stop                              |
| » clientOrderId   | body     | string | true     | Randomized client id                                         |
| » signature       | body     | string | true     | starkKey signature                                           |
| » reduceOnly      | body     | string | false    | Reduce-only                                                  |

> Successful Response Generation

```json
{
  "id": "1234",
  "clientOrderId": "1234",
  "accountId": "12345",
  "symbol": "BTC-USD",
  "side": "SELL",
  "price": "18000",
  "limitFee": "100",
  "fee": "100",
  "triggerPrice": "1.2",
  "trailingPercent": "0.12",
  "size": "100",
  "type": "LIMIT",
  "createdAt": 1647502440973,
  "updatedTime": 1647502440973,
  "expiresAt": 1647502440973,
  "status": "PENDING",
  "timeInForce": "GOOD_TIL_CANCEL",
  "postOnly": false,
  "reduceOnly": false,
  "latestMatchFillPrice": "reason",
  "cumMatchFillSize": "0.1",
  "cumMatchFillValue": "1000",
  "cumMatchFillFee": "1",
  "cumSuccessFillSize": "0.1",
  "cumSuccessFillValue": "1000",
  "cumSuccessFillFee": "1"
}
```

**Response Status Code**

| Status Code | Definition | Comment | Data Model |
| ----------- | ---------- | ------- | ---------- |
| 200         | OK         | Success | Inline     |

**Response Parameters**

Status Code **200**

| Parameter              | Type    | Required | Limit | Comment                         |
| ---------------------- | ------- | -------- | ----- | ------------------------------- |
| » id                   | string  | false    | none  | Order id                        |
| »» orderId             | string  | false    | none  | Order id                        |
| » clientOrderId        | string  | false    | none  | Client create the Randomized id |
| » accountId            | string  | false    | none  | Account ID                      |
| » symbol               | string  | false    | none  | Symbol                          |
| » side                 | string  | false    | none  | BUY or SELL                     |
| » price                | string  | false    | none  | Order open price                |
| » limitFee             | string  | false    | none  | Order open max. fee             |
| » fee                  | string  | false    | none  | Order open actual fee           |
| » triggerPrice         | string  | false    | none  | Conditional order trigger price |
| » trailingPercent      | string  | false    | none  | Conditional order trailing-stop |
| » size                 | string  | false    | none  | Order open size                 |
| » type                 | string  | false    | none  | Order type                      |
| » createdAt            | integer | false    | none  | Order create at                 |
| » updatedTime          | integer | false    | none  | Order update time               |
| » expiresAt            | integer | false    | none  | Order expires at                |
| » status               | string  | false    | none  | Order status                    |
| » timeInForce          | string  | false    | none  | Open order timeInForce          |
| » postOnly             | boolean | false    | none  | Open Post-only order            |
| » reduceOnly           | boolean | false    | none  | Open Reduce-only order          |
| » latestMatchFillPrice | string  | false    | none  | Latest match fill price         |
| » cumMatchFillSize     | string  | false    | none  | Cumulative match fill size      |
| » cumMatchFillValue    | string  | false    | none  | Cumulative match fill value     |
| » cumMatchFillFee      | string  | false    | none  | Cumulative match fill fee       |
| » cumSuccessFillSize   | string  | false    | none  | Cumulative success fill size    |
| » cumSuccessFillValue  | string  | false    | none  | Cumulative success fill value   |
| » cumSuccessFillFee    | string  | false    | none  | Cumulative success fill fee     |



**发交易：**

参考文档：https://github.com/ApeX-Protocol/apexpro-openapi/blob/main/tests/demo_stark_key_sign.py



```python
from apexpro.helpers.util import round_size
from apexpro.http_private_stark_key_sign import HttpPrivateStark
from apexpro.constants import APEX_HTTP_TEST, NETWORKID_TEST, APEX_HTTP_MAIN, NETWORKID_MAIN
import time


# priKey = "your eth_prikey"

# client = HttpPrivate(APEX_HTTP_MAIN, network_id=NETWORKID_MAIN, eth_private_key=priKey)
# # configs = client.configs()

# stark_key_pair_with_y_coordinate = client.derive_stark_key(client.default_address)

# nonceRes = client.generate_nonce(starkKey=stark_key_pair_with_y_coordinate['public_key'],ethAddress=client.default_address,chainId=NETWORKID_MAIN)

# api_key = client.recover_api_key_credentials(nonce=nonceRes['data']['nonce'], ethereum_address=client.default_address)
# # print(api_key)
# regRes = client.register_user(nonce=nonceRes['data']['nonce'],starkKey=stark_key_pair_with_y_coordinate['public_key'],stark_public_key_y_coordinate=stark_key_pair_with_y_coordinate['public_key_y_coordinate'],ethereum_address=client.default_address)

# back stark_key_pair, apiKey,and accountId for private Api or create-oreder or withdraw
# print(stark_key_pair_with_y_coordinate)
# print(regRes['data']['account']['positionId'])
# print(regRes['data']['apiKey'])

public_key = "your public_key"
public_key_y_coordinate = (
    "your public_key_y_coordinate"
)
private_key = "your private_key"
positionId = "your position id"
key = "your key"
secret = "your secret"
passphrase = "your passphrase"


client = HttpPrivateStark(
    APEX_HTTP_MAIN,
    network_id=NETWORKID_MAIN,
    stark_public_key=public_key,
    stark_private_key=private_key,
    stark_public_key_y_coordinate=public_key_y_coordinate,
    api_key_credentials={"key": key, "secret": secret, "passphrase": passphrase},
)
configs = client.configs()
client.get_user()
print(client.get_account())


# sample1
# When create an order, optimize the size of the order according to the stepSize of the currency symbol,
# and optimize the price of the order according to the tickSize
symbolData = {}
for k, v in enumerate(configs.get('data').get('perpetualContract')):
    if v.get('symbol') == "BTC-USDC":
        symbolData = v

print(round_size("0.0116", symbolData.get('stepSize')))
print(round_size("25555.8", symbolData.get('tickSize')))

# Create a limit order
currentTime = time.time()
limitFeeRate = client.account['takerFeeRate']

size = round_size("0.01", symbolData.get('stepSize'))
price = round_size("28888.5", symbolData.get('tickSize'))
createOrderRes = client.create_order(symbol="BTC-USDC", side="BUY",
                                           type="LIMIT", size=size, expirationEpochSeconds= currentTime,
                                           price=price, limitFeeRate=limitFeeRate)
print(createOrderRes)

```



# 四.实现

## 1.价差图分析

**首先清洗数据，保留前3的ask和bid**

```python
import os
import pandas as pd

# 输入文件夹和输出文件夹的相对路径
input_folder = 'D:\学习资料\实习\DYDX_data\depthdata'  # 输入文件夹位于当前工作目录下
output_folder = 'D:\学习资料\实习\DYDX_data\depthdata\datafilter'  # 输出文件夹位于当前工作目录下

# 获取输入文件夹中的所有CSV文件
input_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 遍历每个CSV文件
for input_file in input_files:
    input_file_path = os.path.join(input_folder, input_file)

    # 从CSV文件加载数据
    df = pd.read_csv(input_file_path)

    # 使用groupby和cumcount来分组并获取前3个bid和ask
    df['row_num'] = df.groupby(['Timestamp', 'Type']).cumcount() + 1
    result = df[df['row_num'] <= 3]

    # 删除辅助列row_num
    result = result.drop(columns=['row_num'])

    # 更改输出文件名，加上'_filter'前缀
    output_file = input_file.replace('.csv', '_filter.csv')
    output_file_path = os.path.join(output_folder, output_file)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 将处理后的数据保存到新的CSV文件
    result.to_csv(output_file_path, index=False)

    print(f"Processed {input_file} and saved as {output_file}")

print("All files processed.")

```

**而后生成价差图**

```python
import pandas as pd
import matplotlib.pyplot as plt

# 读取第一个表的数据
data1 = pd.read_csv("order_book_BTC-USD_dydx_filter.csv")  # 替换为第一个表格文件的路径

# 读取第二个表的数据
data2 = pd.read_csv("order_book_BTCUSDC_apex_filter.csv")  # 替换为第二个表格文件的路径

# 分别获取ask和bid的数据
ask_data1 = data1[data1["Type"] == "ask"]
ask_data2 = data2[data2["Type"] == "ask"]
bid_data1 = data1[data1["Type"] == "bid"]
bid_data2 = data2[data2["Type"] == "bid"]

# 确定处理的数据量，以数据较少的表为基准
min_data_length = min(len(ask_data1), len(ask_data2), len(bid_data1), len(bid_data2))

# 仅保留相同数量的数据，并按每3个ask和3个bid为一组
ask_data1 = ask_data1[:min_data_length].iloc[::3]
bid_data1 = bid_data1[:min_data_length].iloc[::3]
ask_data2 = ask_data2[:min_data_length].iloc[::3]
bid_data2 = bid_data2[:min_data_length].iloc[::3]

# 将Unix时间戳转换为标准时间
ask_data1["Timestamp"] = pd.to_datetime(ask_data1["Timestamp"], unit='s')
bid_data2["Timestamp"] = pd.to_datetime(bid_data2["Timestamp"], unit='s')
ask_data2["Timestamp"] = pd.to_datetime(ask_data2["Timestamp"], unit='s')
bid_data1["Timestamp"] = pd.to_datetime(bid_data1["Timestamp"], unit='s')

# 计算价格差值
dydx_apex_diff = ask_data1["Price"].values - bid_data2["Price"].values
apex_dydx_diff = ask_data2["Price"].values - bid_data1["Price"].values

# 绘制价差图
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(ask_data1["Timestamp"], dydx_apex_diff, label="Price Difference")
plt.title("DYDX-APEX Price Difference Chart")
plt.xlabel("Timestamp")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(ask_data2["Timestamp"], apex_dydx_diff, label="Price Difference")
plt.title("APEX-DYDX Price Difference Chart")
plt.xlabel("Timestamp")
plt.legend()

plt.tight_layout()
plt.show()

```

**小问题**：

价差应是A的买一价-B的卖一价，一开始我写的A的买一价-B的买一价。



BTC价差图如下图：

![BTC_price_difference](photo\BTC_price_difference.png)



ETH价差图如下图：

![ETH_price_difference](photo\ETH_price_difference.png)



**对价差分布区间进行分析：**

```python
import pandas as pd
import matplotlib.pyplot as plt

# 读取第一个表的数据
data1 = pd.read_csv("order_book_ETH-USD_dydx_filter.csv")  # 替换为第一个表格文件的路径

# 读取第二个表的数据
data2 = pd.read_csv("order_book_ETHUSDC_apex_filter.csv")  # 替换为第二个表格文件的路径

# 分别获取ask和bid的数据
ask_data1 = data1[data1["Type"] == "ask"]
ask_data2 = data2[data2["Type"] == "ask"]
bid_data1 = data1[data1["Type"] == "bid"]
bid_data2 = data2[data2["Type"] == "bid"]

# 确定处理的数据量，以数据较少的表为基准
min_data_length = min(len(ask_data1), len(ask_data2), len(bid_data1), len(bid_data2))

# 仅保留相同数量的数据，并按每3个ask和3个bid为一组
ask_data1 = ask_data1[:min_data_length].iloc[::3]
bid_data1 = bid_data1[:min_data_length].iloc[::3]
ask_data2 = ask_data2[:min_data_length].iloc[::3]
bid_data2 = bid_data2[:min_data_length].iloc[::3]

# 将Unix时间戳转换为标准时间
ask_data1["Timestamp"] = pd.to_datetime(ask_data1["Timestamp"], unit='s')
bid_data2["Timestamp"] = pd.to_datetime(bid_data2["Timestamp"], unit='s')
ask_data2["Timestamp"] = pd.to_datetime(ask_data2["Timestamp"], unit='s')
bid_data1["Timestamp"] = pd.to_datetime(bid_data1["Timestamp"], unit='s')

# 计算价格差值
dydx_apex_diff = ask_data1["Price"].values - bid_data2["Price"].values
apex_dydx_diff = ask_data2["Price"].values - bid_data1["Price"].values

# 绘制价差直方图 ，range根据具体品种调整
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.hist(dydx_apex_diff, bins=100, range=(-5, 5), edgecolor='k')
plt.title("DYDX-APEX Price Difference Distribution ")
plt.xlabel("Price Difference")
plt.ylabel("Frequency")

plt.subplot(2, 1, 2)
plt.hist(apex_dydx_diff, bins=100, range=(-5, 5), edgecolor='k')
plt.title("APEX-DYDX Price Difference Distribution ")
plt.xlabel("Price Difference")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

```

生成的价差分布图如下：

![ETH_Price Difference_2](photo\ETH_Price Difference_2.png)

![BTC_Price Difference_2](photo\BTC_Price Difference_2.png)

由于DYDX和APEX基于以太坊二层，gas费用较低，故而是有利可图的，具体gas得发交易测试一下。



## 2.gas费

ETH-USDC swap ~10U

**DYDX**

authorization ~5U （一次性花费）

deposit  8~15U （ >500U的存款免gas费，每周限免3次）

交易费率（无gas费，只收手续费）：

![dydx交易费率](photo\dydx交易费率.png)



**APEX**

authorization ~5U

deposit  8~15U

交易费率（无gas费，只收手续费）：

Maker fees are at **0.02%** and taker fees are at **0.05%**. 



## 3.实时价差计算

**BTC**

```python
import asyncio
from apexpro.http_public import HttpPublic
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD

# 定义交易对列表
symbol = 'BTCUSDC'
market = MARKET_BTC_USD

# 定义异步函数来获取 APEX 的价格
async def get_apex_price():
    # 初始化API客户端
    apexclient = HttpPublic("https://pro.apex.exchange")
    # 获取深度数据
    trades_data = apexclient.depth(symbol=symbol)['data']
    # 返回卖一价和买一价
    return trades_data['a'][0][0], trades_data['b'][0][0], trades_data['a'][0][1], trades_data['b'][0][1]

# 定义异步函数来获取 dydx 的价格
async def get_dydx_price():
    # 初始化API客户端
    dydxclient = Client(host='https://api.dydx.exchange')
    # 获取深度数据
    orderbook_response = dydxclient.public.get_orderbook(market=market)
    orderbook_data = orderbook_response.data
    # 返回卖一价和买一价
    return orderbook_data['asks'][0]['price'], orderbook_data['bids'][0]['price'], orderbook_data['asks'][0]['size'], orderbook_data['bids'][0]['size']

# 定义异步函数来计算价差
async def calculate_spread():
    # 创建两个任务，分别获取 APEX 和 dydx 的价格
    task1 = asyncio.create_task(get_apex_price())
    task2 = asyncio.create_task(get_dydx_price())
    # 等待两个任务完成，并获取结果
    s_first_price_apex, b_first_price_apex,s_first_size_apex,b_first_size_apex = await task1
    s_first_price_dydx, b_first_price_dydx,s_first_size_dydx,b_first_size_dydx   = await task2
    # 计算价差
    spread1 = float(s_first_price_apex) - float(b_first_price_dydx)
    spread2 = float(s_first_price_dydx) - float(b_first_price_apex)
    # 打印结果
    print('apex-dydx price gap: ',spread1,'price gap ratio:',(spread1/float(s_first_price_apex))*100,'%','apex size:',s_first_size_apex,'dydx size:',b_first_size_dydx)
    print('dydx-apex price gap: ',spread2,'price gap ratio:',(spread2/float(s_first_price_dydx))*100,'%', 'apex size:',b_first_size_apex,'dydx size:',s_first_size_dydx)

# 创建事件循环
loop = asyncio.get_event_loop()
# 运行异步函数
loop.run_until_complete(calculate_spread())
# 关闭事件循环
loop.close()

```

运行结果如图：

![price gap cal](photo\price gap cal.png)



**注意：**

编写异步代码确保时间误差小。



## 4.代码重构

**1.设置**

apexconfig.ini

```ini
[apex]
public_key = 
public_key_y_coordinate = 
private_key = 
key = 
secret = 
passphrase = 
```

dydxconfig.ini

```ini
[dydx]
eth_private_key = 
```

**2.获取价差**

get_depth_data_btc.py

```python
"""
这是一个用来计算 APEX 和 dydx 之间的 BTCUSDC 价差的模块。
可以调用 calculate_spread 函数来返回两个交易所的卖一价、买一价和价差。
"""



import asyncio
from apexpro.http_public import HttpPublic
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD


# 定义交易对列表
symbol = 'BTCUSDC'
market = MARKET_BTC_USD

# 定义异步函数来获取 APEX 的价格
async def get_apex_price():
    # 初始化API客户端
    apexclient = HttpPublic("https://pro.apex.exchange")
    # 获取深度数据
    trades_data = apexclient.depth(symbol=symbol)['data']
    # 返回卖一价和买一价
    return trades_data['a'][0][0], trades_data['b'][0][0], trades_data['a'][0][1], trades_data['b'][0][1]

# 定义异步函数来获取 dydx 的价格
async def get_dydx_price():
    # 初始化API客户端
    dydxclient = Client(host='https://api.dydx.exchange')
    # 获取深度数据
    orderbook_response = dydxclient.public.get_orderbook(market=market)
    orderbook_data = orderbook_response.data
    # 返回卖一价和买一价
    return orderbook_data['asks'][0]['price'], orderbook_data['bids'][0]['price'], orderbook_data['asks'][0]['size'], orderbook_data['bids'][0]['size']

# 定义异步函数来计算价差
async def calculate_spread():
    # 创建两个任务，分别获取 APEX 和 dydx 的价格
    task1 = asyncio.create_task(get_apex_price())
    task2 = asyncio.create_task(get_dydx_price())
    # 等待两个任务完成，并获取结果
    s_first_price_apex, b_first_price_apex,s_first_size_apex,b_first_size_apex = await task1
    s_first_price_dydx, b_first_price_dydx,s_first_size_dydx,b_first_size_dydx   = await task2
    # 计算价差
    spread1 = ((float(s_first_price_apex) - float(b_first_price_dydx))/float(s_first_price_apex))*100
    spread2 = ((float(s_first_price_dydx) - float(b_first_price_apex))/float(s_first_price_dydx))*100
    return s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2


if __name__ == '__main__':
    # 创建事件循环
    loop = asyncio.get_event_loop()
    # 运行异步函数
    loop.run_until_complete(calculate_spread())
    # 关闭事件循环
    loop.close()

```

**3.apex**

（1）init_apex_client.py

```python
from apexpro.constants import APEX_HTTP_TEST, NETWORKID_TEST, APEX_HTTP_MAIN, NETWORKID_MAIN
from apexpro.http_private_stark_key_sign import HttpPrivateStark
from configparser import ConfigParser

# 定义一个函数，用来初始化客户端
def init_client():
    # 创建配置对象
    config = ConfigParser()
    # 读取配置文件
    config.read('apexconfig.ini')
    # 获取 apex 部分的参数
    public_key = config.get('apex', 'public_key')
    public_key_y_coordinate = config.get('apex', 'public_key_y_coordinate')
    private_key = config.get('apex', 'private_key')
    key = config.get('apex', 'key')
    secret = config.get('apex', 'secret')
    passphrase = config.get('apex', 'passphrase')
    # 创建客户端对象
    client = HttpPrivateStark(
        APEX_HTTP_MAIN,
        network_id=NETWORKID_MAIN,
        stark_public_key=public_key,
        stark_private_key=private_key,
        stark_public_key_y_coordinate=public_key_y_coordinate,
        api_key_credentials={"key": key, "secret": secret, "passphrase": passphrase},
    )
    # 返回客户端对象
    return client
```

(2)send_order_apex.py

```python
from apexpro.helpers.util import round_size

# 定义一个函数，用来发交易
def send_order_apex(client, symbol, side, type, size, expirationEpochSeconds, price, limitFeeRate):
    # 优化订单的大小和价格
    symbolData = {}
    for k, v in enumerate(client.configs().get('data').get('perpetualContract')):
        if v.get('symbol') == symbol:
            symbolData = v
    size = round_size(size, symbolData.get('stepSize'))
    price = round_size(price, symbolData.get('tickSize'))
    # 创建订单
    createOrderRes = client.create_order(symbol=symbol, side=side,
                                           type=type, size=size, expirationEpochSeconds=expirationEpochSeconds,
                                           price=price, limitFeeRate=limitFeeRate)
    # 返回订单结果
    return createOrderRes



```

(3)place_order_apex.py

```python
from init_apex_client import init_client
from send_order_apex import send_order_apex
import time

# 初始化客户端
client_apex = init_client()
configs = client_apex.configs()

# 获取用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 发送一个市价买单
currentTime = time.time()
limitFeeRate = client_apex.account['takerFeeRate']
orderResult = send_order_apex(client_apex, symbol="BTC-USDC", side="BUY",
                                           type="MARKET", size="0.001", expirationEpochSeconds= currentTime,
                                           price="28888.5", limitFeeRate=limitFeeRate)
print(orderResult)
```

**4.dydx**

(1)init_dydx_client.py

```python
from configparser import ConfigParser
from dydx3 import Client

# 定义一个函数，用来初始化客户端
def init_dydx_client():
    # 创建配置对象
    config = ConfigParser()
    # 读取配置文件
    config.read('dydxconfig.ini')
    # 获取 dydx 部分的参数
    eth_private_key = config.get('dydx', 'eth_private_key')
    # 创建客户端对象
    client = Client(host='https://api.dydx.exchange',
                    eth_private_key=eth_private_key,
                    )
    # 设置dydx STARK 密钥
    stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
    client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
    (public_x, public_y) = (
    stark_key_pair_with_y_coordinate['public_key'],
    stark_key_pair_with_y_coordinate['public_key_y_coordinate'],
    )
    # 返回客户端对象
    return client

```

(2)send_order_dydx.py

```python
# 定义一个函数，用来发交易
def send_order_dydx(client, position_id, market, side, order_type, post_only, size, price, limit_fee, expiration_epoch_seconds):
    # 创建订单参数
    order_params = {
        'position_id': position_id,
        'market': market,
        'side': side,
        'order_type': order_type,
        'post_only': post_only,
        'size': size,
        'price': price,
        'limit_fee': limit_fee,
        'expiration_epoch_seconds': expiration_epoch_seconds,
    }
    # 创建订单
    order_response = client.private.create_order(**order_params)
    # 返回订单结果
    return order_response

```

(3)place_order_dydx.py

```python
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
import time
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET


# 初始化客户端
client_dydx = init_dydx_client()

# 获取我们的仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

# 发送一个市价买单
currentTime = time.time()
orderResult = send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_BUY, ORDER_TYPE_MARKET, True, '0.001', '28888', '0.0015', currentTime)
print('order_response',orderResult.data)

```

##  5.代码整合

btc目前的策略如下：价差超过百1则两边同时make

代码如下：

```python
from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET
from get_depth_data_btc import calculate_spread
import time

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

async def arbitrage():
  while True:
    # 计算价差
    spread1,spread2 = await calculate_spread()
    # 根据价差判断是否发送交易
    if spread1 > 1:
      currentTime = time.time()
      # 异步地发送一个apex市价卖单和一个dydx市价买单
      limitFeeRate = client_apex.account['takerFeeRate']
      orderResult1, orderResult2 = await asyncio.gather(
        send_order_apex(client_apex, symbol="BTC-USDC", side="SELL",
                                           type="MARKET", size="0.001", expirationEpochSeconds= currentTime,
                                           price="28888.5", limitFeeRate=limitFeeRate),
        send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_BUY, ORDER_TYPE_MARKET, True, '0.001', '28888', '0.0015', currentTime)
      )
      print(orderResult1)
      print('order_response', orderResult2.data)
    if spread2 > 1:
      currentTime = time.time()
      # 异步地发送一个apex市价买单和一个dydx市价卖单
      limitFeeRate = client_apex.account['takerFeeRate']
      orderResult1, orderResult2 = await asyncio.gather(
        send_order_apex(client_apex, symbol="BTC-USDC", side="BUY",
                                           type="MARKET", size="0.001", expirationEpochSeconds= currentTime,
                                           price="28888.5", limitFeeRate=limitFeeRate),
        send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_SELL, ORDER_TYPE_MARKET, True, '0.001', '28888', '0.0015', currentTime)
      )
      print(orderResult1)
      print('order_response', orderResult2.data)
    # 延时一秒，避免过于频繁
    await asyncio.sleep(1)

# 运行异步函数
asyncio.run(arbitrage())
```

## 6.bug

dydx发市价单不知道参数怎么设置，文档也不详细，故而改成了发限价单。

还有一些同步异步的问题，要把发交易的函数前加上async。现在修改以及整合的代码部分如下：

1.send_order_apex

```python
from apexpro.helpers.util import round_size

# 定义一个函数，用来发交易
async def send_order_apex(client, symbol, side, type, size, expirationEpochSeconds, price, limitFeeRate):
    # 优化订单的大小和价格
    symbolData = {}
    for k, v in enumerate(client.configs().get('data').get('perpetualContract')):
        if v.get('symbol') == symbol:
            symbolData = v
    size = round_size(size, symbolData.get('stepSize'))
    price = round_size(price, symbolData.get('tickSize'))
    # 创建订单
    createOrderRes = client.create_order(symbol=symbol, side=side,
                                           type=type, size=size, expirationEpochSeconds=expirationEpochSeconds,
                                           price=price, limitFeeRate=limitFeeRate)
    # 返回订单结果
    return createOrderRes



```

2.send_order_dydx.py

```python
# 定义一个函数，用来发交易
async def send_order_dydx(client, position_id, market, side, order_type, post_only, size, price, limit_fee, expiration_epoch_seconds):
    # 创建订单参数
    order_params = {
        'position_id': position_id,
        'market': market,
        'side': side,
        'order_type': order_type,
        'post_only': post_only,
        'size': size,
        'price': price,
        'limit_fee': limit_fee,
        'expiration_epoch_seconds': expiration_epoch_seconds
    }
    # 创建订单
    order_response = client.private.create_order(**order_params)
    # 返回订单结果
    return order_response.data

```

3.place_order_btc.py

```python
from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_btc import calculate_spread
import time

#价格设置需要更精确，不然发不出去！

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

async def arbitrage():
  while True:
    # 计算价差
    s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2 = await calculate_spread()
    # 根据价差判断是否发送交易
    if spread1 > 0.7:
          currentTime = time.time()
          limitFeeRate = client_apex.account['takerFeeRate']
          task_apex_sell = asyncio.create_task(
              send_order_apex(client_apex, symbol="BTC-USDC", side="SELL",
                              type="MARKET", size="0.001", expirationEpochSeconds=currentTime,
                              price=b_first_price_apex, limitFeeRate=limitFeeRate)
          )
          task_dydx_buy = asyncio.create_task(
              send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                              True, '0.001', b_first_price_dydx, '0.0015', currentTime+100)
          )

          orderResult1 = await task_apex_sell
          orderResult2 = await task_dydx_buy
          print(orderResult1,orderResult2)
    if spread2 > 0.7: 
      currentTime = time.time()
      # 异步地发送一个apex市价买单和一个dydx市价卖单
      limitFeeRate = client_apex.account['takerFeeRate']
      task_apex_buy = asyncio.create_task(
              send_order_apex(client_apex, symbol="BTC-USDC", side="BUY",
                              type="MARKET", size="0.001", expirationEpochSeconds=currentTime,
                              price=s_first_price_apex, limitFeeRate=limitFeeRate)
          )
      task_dydx_sell = asyncio.create_task(
          send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                          True, '0.001', s_first_price_dydx, '0.0015', currentTime+100)
      )

      orderResult1 = await task_apex_buy
      orderResult2 = await task_dydx_sell
      print(orderResult1,orderResult2)
    # 延时一秒，避免过于频繁
    await asyncio.sleep(1)

# 运行异步函数
asyncio.run(arbitrage())
```



## 7.补充

**风险控制：**

需要将仓位杠杆控制到3倍以内，由于dydx与apex没有获取仓位杠杆的接口，但是每次发送交易的数额可以决定，故而可以设置每次发送总仓位1.5倍杠杆的数额，然后设置一个变量保证每个方向上的交易不超过2次，即可保证总仓位始终小于3倍杠杆



**细节：**

```python
send_order_apex(client_apex, symbol=“BTC-USDC”, side=“BUY”,type=“MARKET”,size=“0.004”, expirationEpochSeconds=currentTime+100,price=’58888’, limitFeeRate=limitFeeRate)
```

在apex市价交易参数里，price代表可接受的价格，故而当卖出时，此price要尽可能的调低，否则会失败，同理买进时要尽可能的高。



同时将价差计算修改为：

```python
 # 计算价差
    spread1 = ((float(b_first_price_apex) -float(s_first_price_dydx))/float(b_first_price_apex))*100
    spread2 = ((float(b_first_price_dydx) - float(s_first_price_apex))/float(b_first_price_dydx))*100
```

因为如果在apex卖，dydx买的话，apex的卖价应该大于dydx的买价，apex的卖价由apex买一价决定，dydx买价由dydx卖一价决定。反之同理。



代码修改如下：

get_depth_data_btc.py

```python
"""
这是一个用来计算 APEX 和 dydx 之间的 BTCUSDC 价差的模块。
可以调用 calculate_spread 函数来返回两个交易所的卖一价、买一价和价差。
"""



import asyncio
from apexpro.http_public import HttpPublic
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD


# 定义交易对列表
symbol = 'BTCUSDC'
market = MARKET_BTC_USD

# 定义异步函数来获取 APEX 的价格
async def get_apex_price():
    # 初始化API客户端
    apexclient = HttpPublic("https://pro.apex.exchange")
    # 获取深度数据
    trades_data = apexclient.depth(symbol=symbol)['data']
    # 返回卖一价和买一价
    return trades_data['a'][0][0], trades_data['b'][0][0], trades_data['a'][0][1], trades_data['b'][0][1]

# 定义异步函数来获取 dydx 的价格
async def get_dydx_price():
    # 初始化API客户端
    dydxclient = Client(host='https://api.dydx.exchange')
    # 获取深度数据
    orderbook_response = dydxclient.public.get_orderbook(market=market)
    orderbook_data = orderbook_response.data
    # 返回卖一价和买一价
    return orderbook_data['asks'][0]['price'], orderbook_data['bids'][0]['price'], orderbook_data['asks'][0]['size'], orderbook_data['bids'][0]['size']

# 定义异步函数来计算价差
async def calculate_spread():
    # 创建两个任务，分别获取 APEX 和 dydx 的价格
    task1 = asyncio.create_task(get_apex_price())
    task2 = asyncio.create_task(get_dydx_price())
    # 等待两个任务完成，并获取结果
    s_first_price_apex, b_first_price_apex,s_first_size_apex,b_first_size_apex = await task1
    s_first_price_dydx, b_first_price_dydx,s_first_size_dydx,b_first_size_dydx   = await task2
    # 计算价差
    spread1 = ((float(b_first_price_apex) - float(s_first_price_dydx))/float(b_first_price_apex))*100
    spread2 = ((float(b_first_price_dydx) - float(s_first_price_apex))/float(b_first_price_dydx))*100
    return s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2


if __name__ == '__main__':
    # 创建事件循环
    loop = asyncio.get_event_loop()
    # 运行异步函数
    loop.run_until_complete(calculate_spread())
    # 关闭事件循环
    loop.close()

```



place_order_btc.py

```python
from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_btc import calculate_spread
import time

#价格设置需要更精确，不然发不出去！

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

async def arbitrage():
  arbitrage_count = 0
  while True:
    # 计算价差
    s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2 = await calculate_spread()
    # 根据价差判断是否发送交易
    if spread1 > 0.7:
          if arbitrage_count <2:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol="BTC-USDC", side="SELL",
                                type="MARKET", size="0.004", expirationEpochSeconds=currentTime+100,
                                price='18888', limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                True, '0.004', b_first_price_dydx, '0.0015', currentTime+100)
            )

            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            arbitrage_count += 1
            if arbitrage_count >=2:
               print('above leverage ,stop')
            print(orderResult1,orderResult2)
    if spread2 > 0.7: 
      if arbitrage_count >-2:
        currentTime = time.time()
        # 异步地发送一个apex市价买单和一个dydx市价卖单
        limitFeeRate = client_apex.account['takerFeeRate']
        task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol="BTC-USDC", side="BUY",
                                type="MARKET", size="0.004", expirationEpochSeconds=currentTime+100,
                                price='58888', limitFeeRate=limitFeeRate)
            )
        task_dydx_sell = asyncio.create_task(
            send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                            True, '0.004', s_first_price_dydx, '0.0015', currentTime+100)
        )

        orderResult1 = await task_apex_buy
        orderResult2 = await task_dydx_sell
        arbitrage_count -= 1
        if arbitrage_count <=-2:
          print('above leverage ,stop')
        print(orderResult1,orderResult2)
    # 延时一秒，避免过于频繁
    await asyncio.sleep(1)

# 运行异步函数
asyncio.run(arbitrage())
```



**持续运行：**

写一个脚本确保因为各种异常程序退出后能够重启：

```python
import subprocess
import time

def run_program():
    # 这里替换为你需要执行的程序命令
    process = subprocess.Popen(["python", "place_order_btc.py"])  # 例如：python your_program.py
    return process

if __name__ == "__main__":
    while True:
        program = run_program()
        while program.poll() is None:
            # 程序正在运行
            time.sleep(5)  # 每5秒检查一次程序状态
        # 程序已终止，等待一段时间后重启
        print("程序已终止，重新启动中...")
        time.sleep(3)  # 等待3秒

```



# 五.分析优化





## 1.其他品种

扩展到其他币种的价差套利

1.eth

新建文件get_depth_data_eth.py

```python
import asyncio
from apexpro.http_public import HttpPublic
from dydx3 import Client
from dydx3.constants import MARKET_ETH_USD


# 定义交易对列表
symbol = 'ETHUSDC'
market = MARKET_ETH_USD

# 定义异步函数来获取 APEX 的价格
async def get_apex_price():
    # 初始化API客户端
    apexclient = HttpPublic("https://pro.apex.exchange")
    # 获取深度数据
    trades_data = apexclient.depth(symbol=symbol)['data']
    # 返回卖一价和买一价
    return trades_data['a'][0][0], trades_data['b'][0][0], trades_data['a'][0][1], trades_data['b'][0][1]

# 定义异步函数来获取 dydx 的价格
async def get_dydx_price():
    # 初始化API客户端
    dydxclient = Client(host='https://api.dydx.exchange')
    # 获取深度数据
    orderbook_response = dydxclient.public.get_orderbook(market=market)
    orderbook_data = orderbook_response.data
    # 返回卖一价和买一价
    return orderbook_data['asks'][0]['price'], orderbook_data['bids'][0]['price'], orderbook_data['asks'][0]['size'], orderbook_data['bids'][0]['size']

# 定义异步函数来计算价差
async def calculate_spread():
    # 创建两个任务，分别获取 APEX 和 dydx 的价格
    task1 = asyncio.create_task(get_apex_price())
    task2 = asyncio.create_task(get_dydx_price())
    # 等待两个任务完成，并获取结果
    s_first_price_apex, b_first_price_apex,s_first_size_apex,b_first_size_apex = await task1
    s_first_price_dydx, b_first_price_dydx,s_first_size_dydx,b_first_size_dydx   = await task2
    # 计算价差
    spread1 = ((float(b_first_price_apex) - float(s_first_price_dydx))/float(s_first_price_apex))*100
    spread2 = ((float(b_first_price_dydx) - float(s_first_price_apex))/float(s_first_price_dydx))*100
    return s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2


if __name__ == '__main__':
    # 创建事件循环
    loop = asyncio.get_event_loop()
    # 运行异步函数
    loop.run_until_complete(calculate_spread())
    # 关闭事件循环
    loop.close()

```

新建文件place_order_eth.py

```python
from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_ETH_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_eth import calculate_spread
import time

#价格设置需要更精确，不然发不出去！

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

async def arbitrage():
  arbitrage_count = 0
  while True:
    # 计算价差
    s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2 = await calculate_spread()
    # 根据价差判断是否发送交易
    if spread1 > 0.7:
          if arbitrage_count <8:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol="ETH-USDC", side="SELL",
                                type="MARKET", size="0.001", expirationEpochSeconds=currentTime+100,
                                price=b_first_price_apex, limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, MARKET_ETH_USD, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                True, '0.001', b_first_price_dydx, '0.0015', currentTime+100)
            )

            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            arbitrage_count += 1
            if arbitrage_count >=8:
               print('above leverage ,stop')
            print(orderResult1,orderResult2)
    if spread2 > 0.7: 
      if arbitrage_count >-8:
        currentTime = time.time()
        # 异步地发送一个apex市价买单和一个dydx市价卖单
        limitFeeRate = client_apex.account['takerFeeRate']
        task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol="ETH-USDC", side="BUY",
                                type="MARKET", size="0.001", expirationEpochSeconds=currentTime+100,
                                price=s_first_price_apex, limitFeeRate=limitFeeRate)
            )
        task_dydx_sell = asyncio.create_task(
            send_order_dydx(client_dydx, position_id, MARKET_ETH_USD, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                            True, '0.001', s_first_price_dydx, '0.0015', currentTime+100)
        )

        orderResult1 = await task_apex_buy
        orderResult2 = await task_dydx_sell
        arbitrage_count -= 1
        if arbitrage_count <=-8:
          print('above leverage ,stop')
        print(orderResult1,orderResult2)
    # 延时一秒，避免过于频繁
    await asyncio.sleep(5)

# 运行异步函数
asyncio.run(arbitrage())
```



其他文件不变，文件结构如下：

**初始化api端口**

init_apex.client.py

init_dydx.client.py

**发送交易**

send_order_apex.py

send_order_dydx.py

**测试发送交易**

place_order_dydx.py

place_order_apex.py



其他品种同理。修改对应部分以及注意发送交易的size即可。



**所有品种同时运行**：

```python
from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD,MARKET_ETH_USD,MARKET_LINK_USD,MARKET_LTC_USD,MARKET_AVAX_USD,MARKET_ATOM_USD,MARKET_DOGE_USD,MARKET_BCH_USD,MARKET_MATIC_USD,MARKET_SOL_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_btc import calculate_spread as calculate_spread_btc
from get_depth_data_eth import calculate_spread as calculate_spread_eth
from get_depth_data_link import calculate_spread as calculate_spread_link
from get_depth_data_ltc import calculate_spread as calculate_spread_ltc
from get_depth_data_avax import calculate_spread as calculate_spread_avax
from get_depth_data_atom import calculate_spread as calculate_spread_atom
from get_depth_data_doge import calculate_spread as calculate_spread_doge
from get_depth_data_bch import calculate_spread as calculate_spread_bch
from get_depth_data_matic import calculate_spread as calculate_spread_matic
from get_depth_data_sol import calculate_spread as calculate_spread_sol
import time




#价格设置需要更精确，不然发不出去！

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

# 读取存储 arbitrage_count 的文件，如果存在则读取值
try:
    with open('arbitrage_count.txt', 'r') as file:
        arbitrage_count = int(file.read())
except FileNotFoundError:
    arbitrage_count = 0

dydx_take = 0.0002
apex_make = 0.0005


async def execute_trade(client_apex, client_dydx, position_id, market,size, price1,price2, symbol,s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx):
    global arbitrage_count
    global dydx_take
    global apex_make
    print('arbitrage_count:',arbitrage_count)
    print('float(b_first_price_apex)-float(s_first_price_dydx)',float(b_first_price_apex)-float(s_first_price_dydx))
    print('float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take',float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take)
    if float(b_first_price_apex)-float(s_first_price_dydx) > float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take:
        if arbitrage_count<8:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="SELL",
                                type="MARKET", size=size, expirationEpochSeconds=currentTime+1000,
                                price=price1, limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                True, size, b_first_price_dydx, '0.0015', currentTime+1000)
            )
            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            arbitrage_count += 1
            print('apex order:',orderResult1)
            print('dydx order:',orderResult2)

    if float(b_first_price_dydx)-float(s_first_price_apex) > float(b_first_price_dydx)*dydx_take+float(s_first_price_apex)*apex_make:
        if arbitrage_count >-8:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="BUY",
                                type="MARKET", size=size, expirationEpochSeconds=currentTime+1000,
                                price=price2, limitFeeRate=limitFeeRate)
            )
            task_dydx_sell = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                                True, size, s_first_price_dydx, '0.0015', currentTime+1000)
            )
            orderResult1 = await task_apex_buy
            orderResult2 = await task_dydx_sell
            arbitrage_count -= 1
            print('apex order:',orderResult1)
            print('dydx order:',orderResult2)


async def arbitrage():
    while True:
        # 计算价差
        s_first_pirce_apex_btc, b_first_price_apex_btc, s_first_price_dydx_btc, b_first_price_dydx_btc, _, _, _, _ = await calculate_spread_btc()
        s_first_price_apex_eth, b_first_price_apex_eth, s_first_price_dydx_eth, b_first_price_dydx_eth, _, _, _, _ = await calculate_spread_eth()
        s_first_price_apex_link, b_first_price_apex_link, s_first_price_dydx_link, b_first_price_dydx_link, _, _, _, _ = await calculate_spread_link()
        s_first_price_apex_ltc, b_first_price_apex_ltc, s_first_price_dydx_ltc, b_first_price_dydx_ltc, _, _, _, _ = await calculate_spread_ltc()
        s_first_price_apex_avax, b_first_price_apex_avax, s_first_price_dydx_avax, b_first_price_dydx_avax, _, _, _, _ = await calculate_spread_avax()
        s_first_price_apex_atom, b_first_price_apex_atom, s_first_price_dydx_atom, b_first_price_dydx_atom, _, _, _, _ = await calculate_spread_atom()
        s_first_price_apex_doge, b_first_price_apex_doge, s_first_price_dydx_doge, b_first_price_dydx_doge, _, _, _, _ = await calculate_spread_doge()
        s_first_price_apex_bch, b_first_price_apex_bch, s_first_price_dydx_bch, b_first_price_dydx_bch, _, _, _, _ = await calculate_spread_bch()
        s_first_price_apex_matic, b_first_price_apex_matic, s_first_price_dydx_matic, b_first_price_dydx_matic, _, _, _, _ = await calculate_spread_matic()
        s_first_price_apex_sol, b_first_price_apex_sol, s_first_price_dydx_sol, b_first_price_dydx_sol, _, _, _, _ = await calculate_spread_sol()
        
        # 调用 execute_trade 处理所有币种的交易逻辑
        await execute_trade(client_apex, client_dydx, position_id, MARKET_BTC_USD, '0.001', '18888','48888', 'BTC-USDC',s_first_pirce_apex_btc,b_first_price_apex_btc,s_first_price_dydx_btc,b_first_price_dydx_btc)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_ETH_USD,'0.01', '888','2888', 'ETH-USDC',s_first_price_apex_eth,b_first_price_apex_eth,s_first_price_dydx_eth,b_first_price_dydx_eth)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_LINK_USD, '1', '8','28', 'LINK-USDC',s_first_price_apex_link,b_first_price_apex_link,s_first_price_dydx_link,b_first_price_dydx_link)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_LTC_USD,  '0.5', '48', '188','LTC-USDC',s_first_price_apex_ltc,b_first_price_apex_ltc,s_first_price_dydx_ltc,b_first_price_dydx_ltc)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_AVAX_USD,  '1', '8', '48','AVAX-USDC',s_first_price_apex_avax,b_first_price_apex_avax,s_first_price_dydx_avax,b_first_price_dydx_avax)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_ATOM_USD,  '3', '4', '18','ATOM-USDC',s_first_price_apex_atom,b_first_price_apex_atom,s_first_price_dydx_atom,b_first_price_dydx_atom)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_DOGE_USD,  '300', '0.04', '0.3','DOGE-USDC',s_first_price_apex_doge,b_first_price_apex_doge,s_first_price_dydx_doge,b_first_price_dydx_doge)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_BCH_USD,  '0.1', '88', '388','BCH-USDC',s_first_price_apex_bch,b_first_price_apex_bch,s_first_price_dydx_bch,b_first_price_dydx_bch)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_MATIC_USD, '30', '0.1', '2','MATIC-USDC',s_first_price_apex_matic,b_first_price_apex_matic,s_first_price_dydx_matic,b_first_price_dydx_matic)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_SOL_USD,  '1', '48', '188','SOL-USDC',s_first_price_apex_sol,b_first_price_apex_sol,s_first_price_dydx_sol,b_first_price_dydx_sol)
        
        # 在适当的时候将 arbitrage_count 的值写入文件，以便下次读取
        with open('arbitrage_count.txt', 'w') as file:
            file.write(str(arbitrage_count))
        # 等待 1 秒
        await asyncio.sleep(1)


# 运行异步函数
asyncio.run(arbitrage())
```



**重写运行文件：**

```python
import subprocess
import time

def run_program(file_choice):
    if file_choice == "1":
        process = subprocess.Popen(["python", "place_order_btc.py"])
    elif file_choice == "2":
        process = subprocess.Popen(["python", "place_order_eth.py"])
    elif file_choice == "3":
        process = subprocess.Popen(["python", "place_order_link.py"])
    elif file_choice == "4":
        process = subprocess.Popen(["python", "place_order_ltc.py"])
    elif file_choice == "5":
        process = subprocess.Popen(["python", "place_order_avax.py"])
    elif file_choice == "6":
        process = subprocess.Popen(["python", "place_order_atom.py"])
    elif file_choice == "7":
        process = subprocess.Popen(["python", "place_order_doge.py"])
    elif file_choice == "8":
        process = subprocess.Popen(["python", "place_order_bch.py"])
    elif file_choice == "9":
        process = subprocess.Popen(["python", "place_order_matic.py"])
    elif file_choice == "10":
        process = subprocess.Popen(["python", "place_order_sol.py"])
    elif file_choice == "11":
        process = subprocess.Popen(["python","place_order_all.py"])
    else:
        print("无效的选择")
        return None
    return process

if __name__ == "__main__":
    while True:
        choice = input("请输入要运行的文件(1-btc,2-eth,3-link,4-ltc,5-avax,6-atom,7-doge,8-bch,9-matic,10-sol,11-all ):")
        program = run_program(choice)
        if program:
            while program.poll() is None:
                time.sleep(5)
            print("程序已终止，重新启动中...")
            time.sleep(3)

```



## 2.优化

**优化触发条件：**

之前的触发条件有问题，导致迟迟不能触发，优化后触发条件如下：

```python
dydx_take = 0.0002
apex_make = 0.0005

float(b_first_price_apex)-float(s_first_price_dydx) > float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take
```



**优化风险控制：**

每次异常退出再重启杠杆都会从0开始计算，这导致杠杆越拉越高，故而采用全局文件的方式存储arbitrage_count



place_order_all.py

```python
# 其他导入和函数定义...

# 读取存储 arbitrage_count 的文件，如果存在则读取值
try:
    with open('arbitrage_count.txt', 'r') as file:
        arbitrage_count = int(file.read())
except FileNotFoundError:
    arbitrage_count = 0

async def arbitrage():
    global arbitrage_count
    # 其他代码...
    
    while True:
        # 计算价差和交易逻辑
        # ...

        # 在合适的地方，更新 arbitrage_count 的值
        # 比如：
        arbitrage_count += 1  # 或者根据你的逻辑修改 arbitrage_count
        
        # 在适当的时候将 arbitrage_count 的值写入文件，以便下次读取
        with open('arbitrage_count.txt', 'w') as file:
            file.write(str(arbitrage_count))
        
        # 等待 1 秒
        await asyncio.sleep(1)

# 其他代码...

# 运行异步函数
asyncio.run(arbitrage())

```



run.py

```python
# 其他代码...

if __name__ == "__main__":
    choice = input("请输入要运行的文件(1-btc,2-eth,3-link,4-ltc,5-avax,6-atom,7-doge,8-bch,9-matic,10-sol,11-all ):")
    with open('arbitrage_count.txt', 'w') as file:
            file.write(str(0))
    while True:
        program = run_program(choice)
        if program:
            while program.poll() is None:
                time.sleep(5)
            print("程序已终止，重新启动中...")
            time.sleep(1)
```



**apex买卖价设置**

要尽可能大和尽可能小，但不能太大，不然会触发报错：

> {'code': 3, 'msg': 'If order is filled, your account may be liquidated.', 'key': 'ORDER_POSSIBLE_LEAD_TO_ACCOUNT_LIQUIDATED'}



**dydx参数设置**

post-only一定要设置成false，改正后买单的price可设置成卖一价，卖单的price可设置成买一价，保证立刻成交！

否则极其容易订单发出去就被取消！

time 设置为currentTime+1000比较好，大约15分钟。



## 3.结果分析

**时间：**

大概10s达到杠杆上限

![time](photo\time.png)

**仓位对比**：

apex：

![position_apex](photo\position_apex.png)

dydx：

![position_dydx](photo\position_dydx.png)



收益为：0.05764U

初始资金为：

apex：100U

dydx：100U

按此频率，如果持续交易，则每日收益为498U



## 4.平仓机制

现在的套利机制为价差大于手续费，可改为价差大于2倍手续费，利润为价差-手续费

假设当前仓位为dydx买，apex卖

那么平仓的判断条件为**dydx卖价大于apex买价且利润大于当前手续费**

同时优化代码的并行机制，一个币种的交易分成四个模块：

1. 获取当前价格数据
2. 执行套利
3. 获取当前价格数据
4. 执行平仓

将每个币种设计成一个task，然后并行处理，尽可能减少延时。

同时获取价格数据返回买四价和卖四价，避免人工设置交易的价格参数。

代码如下：

place_order_all.py

```python
from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD,MARKET_ETH_USD,MARKET_LINK_USD,MARKET_LTC_USD,MARKET_AVAX_USD,MARKET_ATOM_USD,MARKET_DOGE_USD,MARKET_BCH_USD,MARKET_MATIC_USD,MARKET_SOL_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_btc import calculate_spread as calculate_spread_btc
from get_depth_data_eth import calculate_spread as calculate_spread_eth
from get_depth_data_link import calculate_spread as calculate_spread_link
from get_depth_data_ltc import calculate_spread as calculate_spread_ltc
from get_depth_data_avax import calculate_spread as calculate_spread_avax
from get_depth_data_atom import calculate_spread as calculate_spread_atom
from get_depth_data_doge import calculate_spread as calculate_spread_doge
from get_depth_data_bch import calculate_spread as calculate_spread_bch
from get_depth_data_matic import calculate_spread as calculate_spread_matic
from get_depth_data_sol import calculate_spread as calculate_spread_sol
import time




#价格设置需要更精确，不然发不出去！

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

# 读取存储 arbitrage_count 的文件，如果存在则读取值
try:
    with open('arbitrage_count.txt', 'r') as file:
        arbitrage_count = int(file.read())
except FileNotFoundError:
    arbitrage_count = 0

dydx_take = 0.0005
apex_make = 0.0005
level = 4
#币种有：btc,eth,link,ltc,avax,atom,doge,bch,matic,sol
btc_count = 0
eth_count = 0
link_count = 0
ltc_count = 0
avax_count = 0
atom_count = 0
doge_count = 0
bch_count = 0
matic_count = 0
sol_count = 0
btc_trades = []
eth_trades = []
link_trades = []
ltc_trades = []
avax_trades = []
atom_trades = []
doge_trades = []
bch_trades = []
matic_trades = []
sol_trades = []


#交易逻辑
async def execute_trade(client_apex, client_dydx, position_id, market,size,symbol,s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_fourth_price_apex,b_fourth_price_apex,s_fourth_price_dydx,b_fourth_price_dydx,coin_count,coin_trades):
    global arbitrage_count
    global dydx_take
    global apex_make
    global level
    print('arbitrage_count:',arbitrage_count)
    if float(b_first_price_apex)-float(s_first_price_dydx) > float(b_first_price_apex)*apex_make*2+float(s_first_price_dydx)*dydx_take*2:
        fp = open('spread.txt','a')
        print('count:',arbitrage_count,'symbol:',symbol,'as-db spread:',(float(b_first_price_apex)-float(s_first_price_dydx))/(float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take),file=fp)
        fp.close()
        if arbitrage_count<level:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="SELL",
                                type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                price=b_fourth_price_apex, limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                False, size, s_fourth_price_dydx, '0.0015', currentTime+1000)
            )
            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            margin_value = float(b_first_price_apex)-float(s_first_price_dydx)-float(b_first_price_apex)*apex_make-float(s_first_price_dydx)*dydx_take
            globals()[coin_count] += 1
            arbitrage_count += 1
            coin_trades.append([margin_value,0])
            fp = open('trades.txt','a')
            print('open position:',file=fp)
            print('apex order:',orderResult1,file=fp)
            print('dydx order:',orderResult2,file=fp)
            fp.close

    if float(b_first_price_dydx)-float(s_first_price_apex) > float(b_first_price_dydx)*dydx_take*2+float(s_first_price_apex)*apex_make*2:
        fp = open('spread.txt','a')
        print('count:',arbitrage_count,'symbol:',symbol,'ab-ds spread:',(float(b_first_price_apex)-float(s_first_price_dydx))/(float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take),file=fp)
        fp.close()
        if arbitrage_count >-level:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="BUY",
                                type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                price=s_fourth_price_apex, limitFeeRate=limitFeeRate)
            )
            task_dydx_sell = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                               False, size, b_first_price_dydx, '0.0015', currentTime+1000)
            )
            orderResult1 = await task_apex_buy
            orderResult2 = await task_dydx_sell
            margin_value = float(b_first_price_dydx)-float(s_first_price_apex)-float(b_first_price_dydx)*dydx_take-float(s_first_price_apex)*apex_make
            globals()[coin_count] -= 1
            arbitrage_count -= 1
            coin_trades.append([margin_value,1])
            fp = open('trades.txt','a')
            print('open position:',file=fp)
            print('apex order:',orderResult1,file=fp)
            print('dydx order:',orderResult2,file=fp)
            fp.close

async def close_position(client_apex, client_dydx, position_id, market,size, symbol,s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_fourth_price_apex,b_fourth_price_apex,s_fourth_price_dydx,b_fourth_price_dydx,coin_count,coin_trades):
        global dydx_take
        global apex_make
        global arbitrage_count
        if(globals()[coin_count]!=0):
            if(coin_trades[-1][1]==0):
                if (s_first_price_apex>b_first_price_dydx) and (coin_trades[-1][0]>float(s_first_price_apex)*apex_make+float(b_first_price_dydx)*dydx_take):
                    currentTime = time.time()
                    limitFeeRate = client_apex.account['takerFeeRate']
                    task_apex_buy = asyncio.create_task(
                        send_order_apex(client_apex, symbol=symbol, side="BUY",
                                        type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                        price=s_fourth_price_apex, limitFeeRate=limitFeeRate)
                    )
                    task_dydx_sell = asyncio.create_task(
                        send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                                       False, size, b_fourth_price_dydx, '0.0015', currentTime+1000)
                    )
                    orderResult1 = await task_apex_buy
                    orderResult2 = await task_dydx_sell
                    arbitrage_count -=1
                    globals()[coin_count] -= 1
                    coin_trades.pop()
                    fp = open('trades.txt','a')
                    print('close position:',file=fp)
                    print('apex order:',orderResult1,file=fp)
                    print('dydx order:',orderResult2,file=fp)
                    fp.close()

            elif(coin_trades[-1][1]==1):
                if (s_first_price_dydx>b_first_price_apex) and (coin_trades[-1][0]>float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take):
                    currentTime = time.time()
                    limitFeeRate = client_apex.account['takerFeeRate']
                    task_apex_sell = asyncio.create_task(
                        send_order_apex(client_apex, symbol=symbol, side="SELL",
                                        type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                        price=b_fourth_price_apex, limitFeeRate=limitFeeRate)
                    )
                    task_dydx_buy = asyncio.create_task(
                        send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                        False, size, s_fourth_price_dydx, '0.0015', currentTime+1000)
                    )
                    orderResult1 = await task_apex_sell
                    orderResult2 = await task_dydx_buy
                    arbitrage_count +=1
                    globals()[coin_count] += 1
                    coin_trades.pop()
                    fp = open('trades.txt','a')
                    print('close position:',file=fp)
                    print('apex order:',orderResult1,file=fp)
                    print('dydx order:',orderResult2,file=fp)
                    fp.close()

async def trade_btc():
    s_first_pirce_apex_btc, b_first_price_apex_btc, s_first_price_dydx_btc, b_first_price_dydx_btc, _, _, _, _,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc = await calculate_spread_btc()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_BTC_USD, '0.001',  'BTC-USDC',s_first_pirce_apex_btc,b_first_price_apex_btc,s_first_price_dydx_btc,b_first_price_dydx_btc,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc,'btc_count',btc_trades)
    s_first_pirce_apex_btc, b_first_price_apex_btc, s_first_price_dydx_btc, b_first_price_dydx_btc, _, _, _, _,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc = await calculate_spread_btc()
    await close_position(client_apex, client_dydx, position_id, MARKET_BTC_USD, '0.001','BTC-USDC',s_first_pirce_apex_btc,b_first_price_apex_btc,s_first_price_dydx_btc,b_first_price_dydx_btc,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc,'btc_count',btc_trades)

async def trade_eth():
    s_first_pirce_apex_eth, b_first_price_apex_eth, s_first_price_dydx_eth, b_first_price_dydx_eth, _, _, _, _,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth = await calculate_spread_eth()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_ETH_USD, '0.01',  'ETH-USDC',s_first_pirce_apex_eth,b_first_price_apex_eth,s_first_price_dydx_eth,b_first_price_dydx_eth,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth,'eth_count',eth_trades)
    s_first_pirce_apex_eth, b_first_price_apex_eth, s_first_price_dydx_eth, b_first_price_dydx_eth, _, _, _, _,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth = await calculate_spread_eth()
    await close_position(client_apex, client_dydx, position_id, MARKET_ETH_USD, '0.01','ETH-USDC',s_first_pirce_apex_eth,b_first_price_apex_eth,s_first_price_dydx_eth,b_first_price_dydx_eth,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth,'eth_count',eth_trades)

async def trade_link():
    s_first_pirce_apex_link, b_first_price_apex_link, s_first_price_dydx_link, b_first_price_dydx_link, _, _, _, _,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link = await calculate_spread_link()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_LINK_USD, '1',  'LINK-USDC',s_first_pirce_apex_link,b_first_price_apex_link,s_first_price_dydx_link,b_first_price_dydx_link,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link,'link_count',link_trades)
    s_first_pirce_apex_link, b_first_price_apex_link, s_first_price_dydx_link, b_first_price_dydx_link, _, _, _, _,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link = await calculate_spread_link()
    await close_position(client_apex, client_dydx, position_id, MARKET_LINK_USD, '1','LINK-USDC',s_first_pirce_apex_link,b_first_price_apex_link,s_first_price_dydx_link,b_first_price_dydx_link,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link,'link_count',link_trades)

async def trade_ltc():
    s_first_pirce_apex_ltc, b_first_price_apex_ltc, s_first_price_dydx_ltc, b_first_price_dydx_ltc, _, _, _, _,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc = await calculate_spread_ltc()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_LTC_USD, '0.5',  'LTC-USDC',s_first_pirce_apex_ltc,b_first_price_apex_ltc,s_first_price_dydx_ltc,b_first_price_dydx_ltc,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc,'ltc_count',ltc_trades)
    s_first_pirce_apex_ltc, b_first_price_apex_ltc, s_first_price_dydx_ltc, b_first_price_dydx_ltc, _, _, _, _,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc = await calculate_spread_ltc()
    await close_position(client_apex, client_dydx, position_id, MARKET_LTC_USD, '0.5','LTC-USDC',s_first_pirce_apex_ltc,b_first_price_apex_ltc,s_first_price_dydx_ltc,b_first_price_dydx_ltc,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc,'ltc_count',ltc_trades)

async def trade_avax():
    s_first_pirce_apex_avax, b_first_price_apex_avax, s_first_price_dydx_avax, b_first_price_dydx_avax, _, _, _, _,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax = await calculate_spread_avax()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_AVAX_USD, '1',  'AVAX-USDC',s_first_pirce_apex_avax,b_first_price_apex_avax,s_first_price_dydx_avax,b_first_price_dydx_avax,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax,'avax_count',avax_trades)
    s_first_pirce_apex_avax, b_first_price_apex_avax, s_first_price_dydx_avax, b_first_price_dydx_avax, _, _, _, _,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax = await calculate_spread_avax()
    await close_position(client_apex, client_dydx, position_id, MARKET_AVAX_USD, '1','AVAX-USDC',s_first_pirce_apex_avax,b_first_price_apex_avax,s_first_price_dydx_avax,b_first_price_dydx_avax,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax,'avax_count',avax_trades)

async def trade_atom():
    s_first_pirce_apex_atom, b_first_price_apex_atom, s_first_price_dydx_atom, b_first_price_dydx_atom, _, _, _, _,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom = await calculate_spread_atom()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_ATOM_USD, '1',  'ATOM-USDC',s_first_pirce_apex_atom,b_first_price_apex_atom,s_first_price_dydx_atom,b_first_price_dydx_atom,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom,'atom_count',atom_trades)
    s_first_pirce_apex_atom, b_first_price_apex_atom, s_first_price_dydx_atom, b_first_price_dydx_atom, _, _, _, _,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom = await calculate_spread_atom()
    await close_position(client_apex, client_dydx, position_id, MARKET_ATOM_USD, '1','ATOM-USDC',s_first_pirce_apex_atom,b_first_price_apex_atom,s_first_price_dydx_atom,b_first_price_dydx_atom,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom,'atom_count',atom_trades)

async def trade_doge():
    s_first_pirce_apex_doge, b_first_price_apex_doge, s_first_price_dydx_doge, b_first_price_dydx_doge, _, _, _, _,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge = await calculate_spread_doge()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_DOGE_USD, '300',  'DOGE-USDC',s_first_pirce_apex_doge,b_first_price_apex_doge,s_first_price_dydx_doge,b_first_price_dydx_doge,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge,'doge_count',doge_trades)
    s_first_pirce_apex_doge, b_first_price_apex_doge, s_first_price_dydx_doge, b_first_price_dydx_doge, _, _, _, _,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge = await calculate_spread_doge()
    await close_position(client_apex, client_dydx, position_id, MARKET_DOGE_USD, '300','DOGE-USDC',s_first_pirce_apex_doge,b_first_price_apex_doge,s_first_price_dydx_doge,b_first_price_dydx_doge,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge,'doge_count',doge_trades)

async def trade_bch():
    s_first_pirce_apex_bch, b_first_price_apex_bch, s_first_price_dydx_bch, b_first_price_dydx_bch, _, _, _, _,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch = await calculate_spread_bch()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_BCH_USD, '0.2',  'BCH-USDC',s_first_pirce_apex_bch,b_first_price_apex_bch,s_first_price_dydx_bch,b_first_price_dydx_bch,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch,'bch_count',bch_trades)
    s_first_pirce_apex_bch, b_first_price_apex_bch, s_first_price_dydx_bch, b_first_price_dydx_bch, _, _, _, _,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch = await calculate_spread_bch()
    await close_position(client_apex, client_dydx, position_id, MARKET_BCH_USD, '0.2','BCH-USDC',s_first_pirce_apex_bch,b_first_price_apex_bch,s_first_price_dydx_bch,b_first_price_dydx_bch,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch,'bch_count',bch_trades)

async def trade_matic():
    s_first_pirce_apex_matic, b_first_price_apex_matic, s_first_price_dydx_matic, b_first_price_dydx_matic, _, _, _, _,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic = await calculate_spread_matic()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_MATIC_USD, '30',  'MATIC-USDC',s_first_pirce_apex_matic,b_first_price_apex_matic,s_first_price_dydx_matic,b_first_price_dydx_matic,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic,'matic_count',matic_trades)
    s_first_pirce_apex_matic, b_first_price_apex_matic, s_first_price_dydx_matic, b_first_price_dydx_matic, _, _, _, _,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic = await calculate_spread_matic()
    await close_position(client_apex, client_dydx, position_id, MARKET_MATIC_USD, '30','MATIC-USDC',s_first_pirce_apex_matic,b_first_price_apex_matic,s_first_price_dydx_matic,b_first_price_dydx_matic,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic,'matic_count',matic_trades)

async def trade_sol():
    s_first_pirce_apex_sol, b_first_price_apex_sol, s_first_price_dydx_sol, b_first_price_dydx_sol, _, _, _, _,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol = await calculate_spread_sol()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_SOL_USD, '1',  'SOL-USDC',s_first_pirce_apex_sol,b_first_price_apex_sol,s_first_price_dydx_sol,b_first_price_dydx_sol,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol,'sol_count',sol_trades)
    s_first_pirce_apex_sol, b_first_price_apex_sol, s_first_price_dydx_sol, b_first_price_dydx_sol, _, _, _, _,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol = await calculate_spread_sol()
    await close_position(client_apex, client_dydx, position_id, MARKET_SOL_USD, '1','SOL-USDC',s_first_pirce_apex_sol,b_first_price_apex_sol,s_first_price_dydx_sol,b_first_price_dydx_sol,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol,'sol_count',sol_trades)

async def arbitrage():
    while True:
        btc_task = trade_btc()
        eth_task = trade_eth()
        link_task = trade_link()
        ltc_task = trade_ltc()
        avax_task = trade_avax()
        atom_task = trade_atom()
        doge_task = trade_doge()
        bch_task = trade_bch()
        matic_task = trade_matic()
        sol_task = trade_sol()
        await asyncio.gather(btc_task,eth_task,link_task,ltc_task,avax_task,atom_task,doge_task,bch_task,matic_task,sol_task)

        # 在适当的时候将 arbitrage_count 的值写入文件，以便下次读取
        with open('arbitrage_count.txt', 'w') as file:
            file.write(str(arbitrage_count))
        # 等待 1 秒
        await asyncio.sleep(1)


# 运行异步函数
asyncio.run(arbitrage())
```

​     