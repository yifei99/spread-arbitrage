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
