from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
import time
from dydx3.constants import MARKET_ATOM_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_LIMIT
from get_depth_data_atom import  calculate_spread
import asyncio

# 初始化客户端
client_dydx = init_dydx_client()
 # 计算价差
async def main():
    s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,s_fourth_price_apex,b_fourth_price_apex,s_fourth_price_dydx,b_fourth_price_dydx  =await calculate_spread()
    # 获取我们的仓位 ID
    account_response = client_dydx.private.get_account()
    position_id = account_response.data['account']['positionId']

    # 发送一个市价买单
    currentTime = time.time()
    orderResult = await send_order_dydx(client_dydx, position_id, MARKET_ATOM_USD, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT, False, '1', s_fourth_price_dydx, '0.0015', currentTime+100)
    print('order_response',orderResult)

asyncio.run(main())