import asyncio
from apexpro.constants import APEX_HTTP_MAIN
from apexpro.http_public import HttpPublic
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, \
    MARKET_AVAX_USD, MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, \
    MARKET_DOGE_USD, MARKET_LTC_USD, MARKET_BCH_USD
import csv
import time
import os

# 交易对和市场列表
symbols = ['BTCUSDC', 'ETHUSDC', 'LINKUSDC', 'AVAXUSDC', 'SOLUSDC', 'MATICUSDC', 'ATOMUSDC', 'DOGEUSDC', 'LTCUSDC', 'BCHUSDC']
markets = [MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, MARKET_AVAX_USD,
           MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, MARKET_DOGE_USD,
           MARKET_LTC_USD, MARKET_BCH_USD]

# 每次获取的订单数量
ORDER_LIMIT = 10

# 确保保存数据的文件夹存在
output_dir = 'depth-data'
os.makedirs(output_dir, exist_ok=True)

# 获取订单薄数据的函数
async def fetch_and_save_orderbook(apex_client, dydx_client, symbol, market):
    apex_csv_path = os.path.join(output_dir, f'order_book_{symbol}_apex.csv')
    dydx_csv_path = os.path.join(output_dir, f'order_book_{market}_dydx.csv')
    print(f'Starting data collection for {symbol} and {market}...')

    while True:
        # 获取当前时间戳
        timestamp = time.time()

        # 获取 Apex 订单薄数据
        apex_data = apex_client.depth(symbol=symbol)['data']
        apex_asks = apex_data['a'][:ORDER_LIMIT]
        apex_bids = apex_data['b'][:ORDER_LIMIT]

        # 获取 dYdX 订单薄数据
        dydx_response = dydx_client.public.get_orderbook(market=market)
        dydx_data = dydx_response.data
        dydx_asks = dydx_data['asks'][:ORDER_LIMIT]
        dydx_bids = dydx_data['bids'][:ORDER_LIMIT]

        # 打印数据进行调试
        print(f"Order book for {symbol} - Asks: {apex_asks}, Bids: {apex_bids}, Timestamp: {timestamp}")
        print(f"Order book for {market} - Asks: {dydx_asks}, Bids: {dydx_bids}, Timestamp: {timestamp}")

        # 保存 Apex 数据到 CSV
        with open(apex_csv_path, mode='a', newline='') as apex_file:
            apex_writer = csv.writer(apex_file)
            if apex_file.tell() == 0:
                apex_writer.writerow(['Price', 'Quantity', 'Type', 'Timestamp'])

            for ask in apex_asks:
                apex_writer.writerow([ask[0], ask[1], 'ask', timestamp])

            for bid in apex_bids:
                apex_writer.writerow([bid[0], bid[1], 'bid', timestamp])

        # 保存 dYdX 数据到 CSV
        with open(dydx_csv_path, mode='a', newline='') as dydx_file:
            dydx_writer = csv.writer(dydx_file)
            if dydx_file.tell() == 0:
                dydx_writer.writerow(['Size', 'Price', 'Type', 'Timestamp'])

            for ask in dydx_asks:
                dydx_writer.writerow([ask['size'], ask['price'], 'ask', timestamp])

            for bid in dydx_bids:
                dydx_writer.writerow([bid['size'], bid['price'], 'bid', timestamp])

        print(f"Order book for {symbol} saved to {apex_csv_path}")
        print(f"Order book for {market} saved to {dydx_csv_path}")

        # 每次获取后等待10秒
        await asyncio.sleep(10)

async def main():
    apex_client = HttpPublic(APEX_HTTP_MAIN)
    dydx_client = Client(host='https://api.dydx.exchange')

    # 启动任务
    tasks = [asyncio.create_task(fetch_and_save_orderbook(apex_client, dydx_client, symbols[i], markets[i])) for i in range(len(symbols))]

    # 等待所有任务完成
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
