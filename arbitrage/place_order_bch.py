from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BCH_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_bch import calculate_spread
import time

#价格设置需要更精确，不然发不出去！

# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()


# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']

async def arbitrage():
  arbitrage_count = 0
  apex_make = 0.0005
  dydx_take = 0.0002
  while True:
    # 计算价差
    s_first_price_apex, b_first_price_apex, s_first_price_dydx, b_first_price_dydx, _, _, _, _ = await calculate_spread()
    # 根据价差判断是否发送交易
    if float(b_first_price_apex)-float(s_first_price_dydx) > float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take:
          if arbitrage_count <8:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol="BCH-USDC", side="SELL",
                                type="MARKET", size="0.1", expirationEpochSeconds=currentTime+1000,
                                price=88, limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, MARKET_BCH_USD, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                False, '0.1', s_first_price_dydx, '0.0015', currentTime+1000)
            )

            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            arbitrage_count += 1
            if arbitrage_count >=8:
               print('above leverage ,stop')
            print(orderResult1,orderResult2)
    if float(b_first_price_dydx)-float(s_first_price_apex) > float(b_first_price_dydx)*dydx_take+float(s_first_price_apex)*apex_make:
      if arbitrage_count >-8:
        currentTime = time.time()
        # 异步地发送一个apex市价买单和一个dydx市价卖单
        limitFeeRate = client_apex.account['takerFeeRate']
        task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol="BCH-USDC", side="BUY",
                                type="MARKET", size="0.1", expirationEpochSeconds=currentTime+1000,
                                price=388, limitFeeRate=limitFeeRate)
            )
        task_dydx_sell = asyncio.create_task(
            send_order_dydx(client_dydx, position_id, MARKET_BCH_USD, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                            False, '0.1', b_first_price_dydx, '0.0015', currentTime+1000)
        )

        orderResult1 = await task_apex_buy
        orderResult2 = await task_dydx_sell
        arbitrage_count -= 1
        if arbitrage_count <=-8:
          print('above leverage ,stop')
        print(orderResult1,orderResult2)
    # 延时一秒，避免过于频繁
    await asyncio.sleep(1)

# 运行异步函数
asyncio.run(arbitrage())