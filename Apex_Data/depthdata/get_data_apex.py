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
