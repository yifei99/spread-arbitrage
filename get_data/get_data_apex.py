# get_apex_data.py

import asyncio
import csv
import os
import time
from apexpro.constants import APEX_HTTP_MAIN
from apexpro.http_public import HttpPublic

# 定义交易对列表
symbols = ['BTCUSDC', 'ETHUSDC', 'LINKUSDC', 'AVAXUSDC', 'SOLUSDC', 'MATICUSDC', 'ATOMUSDC', 'DOGEUSDC',
            'LTCUSDC', 'BCHUSDC','LDOUSDC','OPUSDC','TIAUSDC','1000PEPEUSDC','TONUSDC',
           'BLURUSDC','BNBUSDC','WLDUSDC','DYDXUSDC','XRPUSDC','APTUSDC','ARBUSDC']

# 每次获取的订单数量
ORDER_LIMIT = 1

# 确保保存数据的文件夹存在
output_dir = 'depth-data'
os.makedirs(output_dir, exist_ok=True)

# 获取 Apex 订单薄数据的函数
async def fetch_and_save_orderbook_apex(apex_client, symbol):
    csv_path = os.path.join(output_dir, f'data_{symbol}_apex.csv')
    print(f'Starting data collection for {symbol} on Apex...')

    while True:
        # 获取当前时间戳，并将其转换为整数秒
        timestamp = int(time.time())

        # 获取 Apex 订单薄数据
        apex_data = apex_client.depth(symbol=symbol)['data']
        apex_asks = apex_data['a'][:ORDER_LIMIT]
        apex_bids = apex_data['b'][:ORDER_LIMIT]

        # 打印数据进行调试
        print(f"Order book for {symbol} - Timestamp: {timestamp}")

        # 保存 Apex 数据到 CSV
        with open(csv_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if csv_file.tell() == 0:
                writer.writerow(['Price', 'Size', 'Type', 'Timestamp'])

            for ask in apex_asks:
                writer.writerow([ask[0], ask[1], 'ask', timestamp])

            for bid in apex_bids:
                writer.writerow([bid[0], bid[1], 'bid', timestamp])

        # 每次获取后等待2秒
        await asyncio.sleep(2)

async def main():
    apex_client = HttpPublic(APEX_HTTP_MAIN)

    # 启动任务
    tasks = [asyncio.create_task(fetch_and_save_orderbook_apex(apex_client, symbol)) for symbol in symbols]

    # 等待所有任务完成
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
