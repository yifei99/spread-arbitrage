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
