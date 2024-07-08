import asyncio
import configparser
from aevo import AevoClient  # 假设 aevo.py 中包含 AevoClient 类
import csv
import os
import json
import websockets

# 定义一个锁来控制读写操作
connection_lock = asyncio.Lock()

# 用于跟踪每个 ticker 的连接状态
connection_states = {}

async def reconnect_all(tickers, data_folder, config, attempt=1, max_attempts=5):
    """尝试重新连接所有 WebSocket 连接。"""
    if attempt > max_attempts:
        print(f"Failed to reconnect all tickers after {max_attempts} attempts.")
        return None
    
    print(f"Reconnecting all tickers: {tickers} (Attempt {attempt})")
    # 指数回退策略，避免频繁重连
    await asyncio.sleep(min(5 * 2**attempt, 60))  # 最长等待时间为 60 秒

    tasks = []
    for ticker in tickers:
        aevo = await initialize_connection(ticker, data_folder, config)
        if aevo:
            task = process_ticker(aevo, ticker, data_folder)
            tasks.append(task)
    await asyncio.gather(*tasks)

async def initialize_connection(ticker, data_folder, config):
    """初始化连接并订阅 ticker。"""
    try:
        async with connection_lock:
            aevo = AevoClient(
                signing_key=config[ticker]['signing_key'],
                wallet_address=config[ticker]['wallet_address'],
                api_key=config[ticker]['api_key'],
                api_secret=config[ticker]['api_secret'],
                env=config[ticker]['env'],
            )
            await aevo.open_connection()  # 打开 WebSocket 连接
            connection_states[ticker] = True
            print(f"Initialized connection for {ticker}")
            return aevo
    except Exception as e:
        print(f"Error initializing connection for {ticker}: {e}")
        return None

async def process_ticker(aevo, ticker, data_folder):
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
                    if isinstance(msg, str):
                        try:
                            msg = json.loads(msg)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON message: {msg}. Error: {e}")
                            continue

                    # 处理成功连接确认消息
                    if 'data' in msg and 'success' in msg['data']:
                        if msg['data']['success'] is True:
                            print(f"Connection successful for account: {msg['data'].get('account')}")
                            continue  # 跳过这类消息的进一步处理

                    # 处理实际的数据消息
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

                            print(f"Written to CSV: {bid_data} and {ask_data}")

                            last_timestamp = timestamp_s

                    else:
                        # 在这里记录或处理意外的消息结构
                        print(f"Unexpected message structure: {msg}")

            except websockets.ConnectionClosedError as e:
                print(f"WebSocket connection closed for {ticker}: {e}")
                await aevo.close_connection()  # 确保连接关闭
                connection_states[ticker] = False
                break

            except asyncio.IncompleteReadError as e:
                print(f"Incomplete read error during message processing for {ticker}: {e}")
                await aevo.close_connection()
                connection_states[ticker] = False
                break

            except Exception as e:
                print(f"Error during message processing for {ticker}: {e}")
                await aevo.close_connection()
                connection_states[ticker] = False
                break

        # 检查是否所有连接都断开了
        if all(not state for state in connection_states.values()):
            print("All connections are closed. Reconnecting all tickers...")
            await reconnect_all(connection_states.keys(), data_folder, config)

async def main():
    # 从 aevo_config.ini 加载配置
    config = configparser.ConfigParser()
    config.read('aevo_config.ini')

    tickers = ['SOL']
    # , 'DOGE', 'AVAX', 'MATIC', 'TRX', 'MKR', 'UMA', 'ATOM', 'CRV', 'BTC', 'NEAR', 'ETH', 'LINK', 
    #          'LTC', 'BCH', 'XRP', 'WLD', 'APT', 'ARB', 'TON', 'BLUR', 'BNB', 'DYDX', '1000PEPE', 'LDO', 'OP', 'TIA'
    data_folder = 'depth-data'  # 定义存储 CSV 文件的文件夹

    tasks = []
    for ticker in tickers:
        aevo = await initialize_connection(ticker, data_folder, config)
        if aevo:
            task = process_ticker(aevo, ticker, data_folder)
            tasks.append(task)

    # 并发运行所有任务
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
