import asyncio
import configparser
from aevo import AevoClient  # 假设 aevo.py 中包含 AevoClient 类
import csv
import os
import json
import time
import websockets

async def reconnect(ticker, data_folder, config, attempt=1, max_attempts=5):
    """尝试重新连接 WebSocket 连接。"""
    if attempt > max_attempts:
        print(f"Failed to reconnect to {ticker} after {max_attempts} attempts.")
        return None
    
    print(f"Attempting to reconnect to {ticker}... (Attempt {attempt})")
    await asyncio.sleep(5 * attempt)  # 逐渐增加等待时间以避免频繁重连

    try:
        # 重新初始化 AevoClient
        aevo = AevoClient(
            signing_key=config[ticker]['signing_key'],
            wallet_address=config[ticker]['wallet_address'],
            api_key=config[ticker]['api_key'],
            api_secret=config[ticker]['api_secret'],
            env=config[ticker]['env'],
        )
        await aevo.open_connection()  # 打开 WebSocket 连接
        print(f"Reconnected to {ticker}.")
        # 开始处理这个 ticker 的消息
        asyncio.create_task(process_ticker(aevo, ticker, data_folder))
        return aevo
    except Exception as e:
        print(f"Reconnection attempt {attempt} failed for {ticker}: {e}")
        return await reconnect(ticker, data_folder, config, attempt + 1, max_attempts)

async def process_ticker(aevo, ticker, data_folder, initial_messages_to_skip=4):
    print(f"Subscribing to {ticker}")
    await aevo.subscribe_ticker(f"ticker:{ticker}:PERPETUAL")
    
    received_messages = 0
    last_timestamp = None  # 存储最后处理的时间戳

    # 确保数据文件夹存在
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created folder: {data_folder}")

    # 构建 CSV 文件的路径
    filename = os.path.join(data_folder, f"data_{ticker}_aevo.csv")
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        fieldnames = ['price', 'size', 'type', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            print(f"Created file and wrote header: {filename}")

        while True:
            try:
                async for msg in aevo.read_messages():
                    received_messages += 1

                    if received_messages >= initial_messages_to_skip:
                        if isinstance(msg, str):
                            try:
                                msg = json.loads(msg)
                            except json.JSONDecodeError as e:
                                print(f"Error decoding JSON message: {msg}. Error: {e}")
                                continue

                        if 'data' in msg and 'tickers' in msg['data'] and len(msg['data']['tickers']) > 0:
                            data = msg['data']['tickers'][0]
                            timestamp_ns = int(msg['data']['timestamp'])  # 纳秒时间戳
                            timestamp_s = timestamp_ns // 1_000_000_000  # 转换为秒

                            if timestamp_s != last_timestamp:
                                bid_data = {
                                    'price': data['bid']['price'],
                                    'size': data['bid']['amount'],
                                    'type': 'bid',
                                    'timestamp': timestamp_s
                                }
                                ask_data = {
                                    'price': data['ask']['price'],
                                    'size': data['ask']['amount'],
                                    'type': 'ask',
                                    'timestamp': timestamp_s
                                }

                                writer.writerow(bid_data)
                                writer.writerow(ask_data)
                                
                                file.flush()
                                os.fsync(file.fileno())

                                # print(f"Written to CSV: {bid_data} and {ask_data}")

                                last_timestamp = timestamp_s

                        else:
                            print(f"Unexpected message structure: {msg}")

            except websockets.exceptions.ConnectionClosedError as e:
                print(f"WebSocket connection closed for {ticker}: {e}")
                await aevo.close_connection()  # 确保连接关闭
                aevo = await reconnect(ticker, data_folder, config)
                if not aevo:
                    print(f"Stopping processing for {ticker} due to repeated connection issues.")
                    break

            except Exception as e:
                print(f"Error during message processing for {ticker}: {e}")
                await aevo.close_connection()
                aevo = await reconnect(ticker, data_folder, config)
                if not aevo:
                    print(f"Stopping processing for {ticker} due to repeated connection issues.")
                    break

async def main():
    # 从 aevo_config.ini 加载配置
    config = configparser.ConfigParser()
    config.read('aevo_config.ini')

    tickers = ['SOL', 'DOGE', 'AVAX', 'MATIC', 'TRX', 'MKR', 'UMA', 'ATOM', 'CRV', 'BTC', 'NEAR', 'ETH', 'LINK', 
               'LTC', 'BCH', 'XRP', 'WLD', 'APT', 'ARB', 'TON', 'BLUR', 'BNB', 'DYDX', '1000PEPE', 'LDO', 'OP', 'TIA']
    tasks = []
    data_folder = 'depth-data'  # 定义存储 CSV 文件的文件夹

    for ticker in tickers:
        try:
            aevo = AevoClient(
                signing_key=config[ticker]['signing_key'],
                wallet_address=config[ticker]['wallet_address'],
                api_key=config[ticker]['api_key'],
                api_secret=config[ticker]['api_secret'],
                env=config[ticker]['env'],
            )
            await aevo.open_connection()  # 打开 WebSocket 连接

            # 创建一个处理该 ticker 消息的任务
            task = process_ticker(aevo, ticker, data_folder)
            tasks.append(task)

        except Exception as e:
            print(f"Error initializing connection for {ticker}: {e}")

    # 并发运行所有任务
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
