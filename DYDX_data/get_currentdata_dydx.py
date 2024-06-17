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
