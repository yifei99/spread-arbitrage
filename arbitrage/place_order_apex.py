from init_apex_client import init_client
from send_order_apex import send_order_apex
import time
from get_depth_data_atom import  calculate_spread
import asyncio

# 初始化客户端
client_apex = init_client()
configs = client_apex.configs()

# 获取用户和账户信息
client_apex.get_user()
client_apex.get_account()

async def main():
    # 发送一个市价买单
    s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,s_fourth_price_apex,b_fourth_price_apex,s_fourth_price_dydx,b_fourth_price_dydx =await calculate_spread()
    currentTime = time.time()
    limitFeeRate = client_apex.account['takerFeeRate']
    orderResult = await send_order_apex(client_apex, symbol="ATOM-USDC", side="BUY",
                                            type="LIMIT", size="0.5", expirationEpochSeconds= currentTime+1000,
                                            price='1', limitFeeRate=limitFeeRate)
    print(orderResult)
    print(s_first_price_apex,s_fourth_price_apex)

asyncio.run(main())