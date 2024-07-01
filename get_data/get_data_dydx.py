# get_dydx_data.py

import asyncio
import csv
import os
import time
from dydx3 import Client
from dydx3.constants import MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, \
    MARKET_AVAX_USD, MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, \
    MARKET_DOGE_USD, MARKET_LTC_USD, MARKET_BCH_USD, MARKET_TRX_USD, \
    MARKET_MKR_USD, MARKET_UMA_USD, MARKET_CRV_USD, MARKET_NEAR_USD

# 定义市场列表
markets = [MARKET_BTC_USD, MARKET_ETH_USD, MARKET_LINK_USD, MARKET_AVAX_USD,
           MARKET_SOL_USD, MARKET_MATIC_USD, MARKET_ATOM_USD, MARKET_DOGE_USD,
           MARKET_LTC_USD, MARKET_BCH_USD, MARKET_TRX_USD, MARKET_MKR_USD,
           MARKET_UMA_USD, MARKET_CRV_USD, MARKET_NEAR_USD]

# 每次获取的订单数量
ORDER_LIMIT = 1

# 确保保存数据的文件夹存在
output_dir = 'depth-data'
os.makedirs(output_dir, exist_ok=True)

# 获取 dYdX 订单薄数据的函数
async def fetch_and_save_orderbook_dydx(dydx_client, market):
    csv_path = os.path.join(output_dir, f'data_{market}_dydx.csv')
    print(f'Starting data collection for {market} on dYdX...')

    while True:
        # 获取当前时间戳，并将其转换为整数秒
        timestamp = int(time.time())

        # 获取 dYdX 订单薄数据
        dydx_response = dydx_client.public.get_orderbook(market=market)
        dydx_data = dydx_response.data
        dydx_asks = dydx_data['asks'][:ORDER_LIMIT]
        dydx_bids = dydx_data['bids'][:ORDER_LIMIT]

        # 打印数据进行调试
        print(f"Order book for {market} - Timestamp: {timestamp}")

        # 保存 dYdX 数据到 CSV
        with open(csv_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if csv_file.tell() == 0:
                writer.writerow(['Price', 'Size', 'Type', 'Timestamp'])

            for ask in dydx_asks:
                writer.writerow([ask['price'], ask['size'], 'ask', timestamp])

            for bid in dydx_bids:
                writer.writerow([bid['price'], bid['size'], 'bid', timestamp])

        # 每次获取后等待1秒
        await asyncio.sleep(1)

async def main():
    dydx_client = Client(host='https://api.dydx.exchange')

    # 启动任务
    tasks = [asyncio.create_task(fetch_and_save_orderbook_dydx(dydx_client, market)) for market in markets]

    # 等待所有任务完成
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
