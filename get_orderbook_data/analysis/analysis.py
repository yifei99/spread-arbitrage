import os
import pandas as pd

data_folder = "/home/dex-arb/spread-arbitrage/get_orderbook_data/depth-data"
symbol = "DOGE"
filename_apex = os.path.join(data_folder, f"order_book_{symbol}USDC_apex.csv")
filename_dydx = os.path.join(data_folder, f"order_book_{symbol}-USD_dydx.csv")

df_apex = pd.read_csv(filename_apex, header = 0)
df_dydx = pd.read_csv(filename_dydx, header = 0)

print ("duration = {}".format(df_apex.iloc[-1]["Timestamp"] - df_apex.iloc[0]["Timestamp"]))
print ("duration in hour = {}".format((df_apex.iloc[-1]["Timestamp"] - df_apex.iloc[0]["Timestamp"]) / 3600))

# 1. 评估一档行情交叉的机会
df_bid1_apex_dydx = pd.merge(left = df_apex.iloc[10::20][["Price", "Timestamp", "Quantity"]].rename(columns = {"Price": "bid1_px_apex",
                                                                                                               "Quantity": "bid1_sz_apex"}),
                             right = df_dydx.iloc[10::20][["Price", "Timestamp", "Size"]].rename(columns = {"Price": "bid1_px_dydx",
                                                                                                            "Size": "bid1_sz_dydx"}),
                             left_on = ["Timestamp"],
                             right_on = ["Timestamp"],
                             how = "outer")
df_ask1_apex_dydx = pd.merge(left = df_apex.iloc[::20][["Price", "Timestamp", "Quantity"]].rename(columns = {"Price": "ask1_px_apex",
                                                                                                             "Quantity": "ask1_sz_apex"}),
                             right = df_dydx.iloc[::20][["Price", "Timestamp", "Size"]].rename(columns = {"Price": "ask1_px_dydx",
                                                                                                          "Size": "ask1_sz_dydx"}),
                             left_on = ["Timestamp"],
                             right_on = ["Timestamp"],
                             how = "outer")
df_bs1_apex_dydx = pd.merge(left = df_bid1_apex_dydx,
                            right = df_ask1_apex_dydx,
                            left_on = ["Timestamp"],
                            right_on = ["Timestamp"],
                            how = "outer").set_index("Timestamp")

offset_ratio = 0.0025
df_bs1_apex_dydx["dydx_above_apex"] = (df_bs1_apex_dydx["bid1_px_dydx"] > df_bs1_apex_dydx["ask1_px_apex"] * (1 + offset_ratio)).astype(int)
df_bs1_apex_dydx["apex_above_dydx"] = (df_bs1_apex_dydx["bid1_px_apex"] > df_bs1_apex_dydx["ask1_px_dydx"] * (1 + offset_ratio)).astype(int)

print ("# samples = {}".format(df_bs1_apex_dydx.shape[0]))
print ("# samples with dydx above apex = {}".format(df_bs1_apex_dydx["dydx_above_apex"].sum()))
print ("# samples with apex above dydx = {}".format(df_bs1_apex_dydx["apex_above_dydx"].sum()))

print (df_bs1_apex_dydx.head(20))