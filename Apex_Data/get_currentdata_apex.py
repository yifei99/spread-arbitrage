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
