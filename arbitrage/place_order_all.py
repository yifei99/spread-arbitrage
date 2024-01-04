from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD,MARKET_ETH_USD,MARKET_LINK_USD,MARKET_LTC_USD,MARKET_AVAX_USD,MARKET_ATOM_USD,MARKET_DOGE_USD,MARKET_BCH_USD,MARKET_MATIC_USD,MARKET_SOL_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_btc import calculate_spread as calculate_spread_btc
from get_depth_data_eth import calculate_spread as calculate_spread_eth
from get_depth_data_link import calculate_spread as calculate_spread_link
from get_depth_data_ltc import calculate_spread as calculate_spread_ltc
from get_depth_data_avax import calculate_spread as calculate_spread_avax
from get_depth_data_atom import calculate_spread as calculate_spread_atom
from get_depth_data_doge import calculate_spread as calculate_spread_doge
from get_depth_data_bch import calculate_spread as calculate_spread_bch
from get_depth_data_matic import calculate_spread as calculate_spread_matic
from get_depth_data_sol import calculate_spread as calculate_spread_sol
import time
import json



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

#初始化变量

dydx_take = 0.0005
apex_make = 0.0005
level = 4
#币种有：btc,eth,link,ltc,avax,atom,doge,bch,matic,sol
try:
    # 尝试从文件中读取变量
    with open('variables.json', 'r') as file:
        variables = json.loads(file.read())

    # 将读取的值赋给相应的变量
    arbitrage_count = variables['arbitrage_count']
    btc_count = variables['btc_count']
    eth_count = variables['eth_count']
    link_count = variables['link_count']
    ltc_count = variables['ltc_count']
    avax_count = variables['avax_count']
    atom_count = variables['atom_count']
    doge_count = variables['doge_count']
    bch_count = variables['bch_count']
    matic_count = variables['matic_count']
    sol_count = variables['sol_count']

except FileNotFoundError:
    # 如果文件不存在，则初始化变量
    arbitrage_count = 0
    btc_count = 0
    eth_count = 0
    link_count = 0
    ltc_count = 0
    avax_count = 0
    atom_count = 0
    doge_count = 0
    bch_count = 0
    matic_count = 0
    sol_count = 0

try:
    # 从文件中读取交易数据
    with open('trade_data.json', 'r') as file:
        trade_data = json.loads(file.read())

    # 将数据赋给相应的数组
    btc_trades = trade_data.get('btc_trades', [])
    eth_trades = trade_data.get('eth_trades', [])
    link_trades = trade_data.get('link_trades', [])
    ltc_trades = trade_data.get('ltc_trades', [])
    avax_trades = trade_data.get('avax_trades', [])
    atom_trades = trade_data.get('atom_trades', [])
    doge_trades = trade_data.get('doge_trades', [])
    bch_trades = trade_data.get('bch_trades', [])
    matic_trades = trade_data.get('matic_trades', [])
    sol_trades = trade_data.get('sol_trades', [])

except FileNotFoundError:
    # 初始化交易数据数组，如果文件不存在
    btc_trades = []
    eth_trades = []
    link_trades = []
    ltc_trades = []
    avax_trades = []
    atom_trades = []
    doge_trades = []
    bch_trades = []
    matic_trades = []
    sol_trades = []



#交易逻辑
async def execute_trade(client_apex, client_dydx, position_id, market,size,symbol,s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_fourth_price_apex,b_fourth_price_apex,s_fourth_price_dydx,b_fourth_price_dydx,coin_count,coin_trades):
    global arbitrage_count
    global dydx_take
    global apex_make
    global level
    print('arbitrage_count:',arbitrage_count)
    if float(b_first_price_apex)-float(s_first_price_dydx) > float(b_first_price_apex)*apex_make*2+float(s_first_price_dydx)*dydx_take*2:
        fp = open('spread.txt','a')
        print('count:',arbitrage_count,'symbol:',symbol,'as-db spread:',(float(b_first_price_apex)-float(s_first_price_dydx))/(float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take),file=fp)
        fp.close()
        if arbitrage_count<level:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="SELL",
                                type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                price=b_fourth_price_apex, limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                False, size, s_fourth_price_dydx, '0.0015', currentTime+1000)
            )
            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            margin_value = float(b_first_price_apex)-float(s_first_price_dydx)-float(b_first_price_apex)*apex_make-float(s_first_price_dydx)*dydx_take
            globals()[coin_count] += 1
            arbitrage_count += 1
            coin_trades.append([margin_value,0])
            fp = open('trades.txt','a')
            print('open position:',file=fp)
            print('apex order:',orderResult1,file=fp)
            print('dydx order:',orderResult2,file=fp)
            fp.close

    if float(b_first_price_dydx)-float(s_first_price_apex) > float(b_first_price_dydx)*dydx_take*2+float(s_first_price_apex)*apex_make*2:
        fp = open('spread.txt','a')
        print('count:',arbitrage_count,'symbol:',symbol,'ab-ds spread:',(float(b_first_price_apex)-float(s_first_price_dydx))/(float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take),file=fp)
        fp.close()
        if arbitrage_count >-level:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="BUY",
                                type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                price=s_fourth_price_apex, limitFeeRate=limitFeeRate)
            )
            task_dydx_sell = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                               False, size, b_first_price_dydx, '0.0015', currentTime+1000)
            )
            orderResult1 = await task_apex_buy
            orderResult2 = await task_dydx_sell
            margin_value = float(b_first_price_dydx)-float(s_first_price_apex)-float(b_first_price_dydx)*dydx_take-float(s_first_price_apex)*apex_make
            globals()[coin_count] -= 1
            arbitrage_count -= 1
            coin_trades.append([margin_value,1])
            fp = open('trades.txt','a')
            print('open position:',file=fp)
            print('apex order:',orderResult1,file=fp)
            print('dydx order:',orderResult2,file=fp)
            fp.close

async def close_position(client_apex, client_dydx, position_id, market,size, symbol,s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_fourth_price_apex,b_fourth_price_apex,s_fourth_price_dydx,b_fourth_price_dydx,coin_count,coin_trades):
        global dydx_take
        global apex_make
        global arbitrage_count
        if(globals()[coin_count]!=0):
            if(coin_trades[-1][1]==0):
                if (float(b_first_price_dydx)-float(s_first_price_apex) + coin_trades[-1][0])> (float(s_first_price_apex)*apex_make+float(b_first_price_dydx)*dydx_take):
                    currentTime = time.time()
                    limitFeeRate = client_apex.account['takerFeeRate']
                    task_apex_buy = asyncio.create_task(
                        send_order_apex(client_apex, symbol=symbol, side="BUY",
                                        type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                        price=s_fourth_price_apex, limitFeeRate=limitFeeRate)
                    )
                    task_dydx_sell = asyncio.create_task(
                        send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                                       False, size, b_fourth_price_dydx, '0.0015', currentTime+1000)
                    )
                    orderResult1 = await task_apex_buy
                    orderResult2 = await task_dydx_sell
                    arbitrage_count -=1
                    globals()[coin_count] -= 1
                    coin_trades.pop()
                    fp = open('trades.txt','a')
                    print('close position:',file=fp)
                    print('apex order:',orderResult1,file=fp)
                    print('dydx order:',orderResult2,file=fp)
                    fp.close()

            elif(coin_trades[-1][1]==1):
                if (float(b_first_price_apex)-float(s_first_price_dydx) + coin_trades[-1][0]) > (float(b_first_price_apex)*apex_make+float(s_first_price_dydx)*dydx_take):
                    currentTime = time.time()
                    limitFeeRate = client_apex.account['takerFeeRate']
                    task_apex_sell = asyncio.create_task(
                        send_order_apex(client_apex, symbol=symbol, side="SELL",
                                        type="LIMIT", size=size, expirationEpochSeconds=currentTime+1000,
                                        price=b_fourth_price_apex, limitFeeRate=limitFeeRate)
                    )
                    task_dydx_buy = asyncio.create_task(
                        send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                        False, size, s_fourth_price_dydx, '0.0015', currentTime+1000)
                    )
                    orderResult1 = await task_apex_sell
                    orderResult2 = await task_dydx_buy
                    arbitrage_count +=1
                    globals()[coin_count] += 1
                    coin_trades.pop()
                    fp = open('trades.txt','a')
                    print('close position:',file=fp)
                    print('apex order:',orderResult1,file=fp)
                    print('dydx order:',orderResult2,file=fp)
                    fp.close()

async def trade_btc():
    s_first_pirce_apex_btc, b_first_price_apex_btc, s_first_price_dydx_btc, b_first_price_dydx_btc, _, _, _, _,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc = await calculate_spread_btc()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_BTC_USD, '0.001',  'BTC-USDC',s_first_pirce_apex_btc,b_first_price_apex_btc,s_first_price_dydx_btc,b_first_price_dydx_btc,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc,'btc_count',btc_trades)
    s_first_pirce_apex_btc, b_first_price_apex_btc, s_first_price_dydx_btc, b_first_price_dydx_btc, _, _, _, _,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc = await calculate_spread_btc()
    await close_position(client_apex, client_dydx, position_id, MARKET_BTC_USD, '0.001','BTC-USDC',s_first_pirce_apex_btc,b_first_price_apex_btc,s_first_price_dydx_btc,b_first_price_dydx_btc,s_fourth_price_apex_btc,b_fourth_price_apex_btc,s_fourth_price_dydx_btc,b_fourth_price_dydx_btc,'btc_count',btc_trades)

async def trade_eth():
    s_first_pirce_apex_eth, b_first_price_apex_eth, s_first_price_dydx_eth, b_first_price_dydx_eth, _, _, _, _,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth = await calculate_spread_eth()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_ETH_USD, '0.01',  'ETH-USDC',s_first_pirce_apex_eth,b_first_price_apex_eth,s_first_price_dydx_eth,b_first_price_dydx_eth,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth,'eth_count',eth_trades)
    s_first_pirce_apex_eth, b_first_price_apex_eth, s_first_price_dydx_eth, b_first_price_dydx_eth, _, _, _, _,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth = await calculate_spread_eth()
    await close_position(client_apex, client_dydx, position_id, MARKET_ETH_USD, '0.01','ETH-USDC',s_first_pirce_apex_eth,b_first_price_apex_eth,s_first_price_dydx_eth,b_first_price_dydx_eth,s_fourth_price_apex_eth,b_fourth_price_apex_eth,s_fourth_price_dydx_eth,b_fourth_price_dydx_eth,'eth_count',eth_trades)

async def trade_link():
    s_first_pirce_apex_link, b_first_price_apex_link, s_first_price_dydx_link, b_first_price_dydx_link, _, _, _, _,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link = await calculate_spread_link()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_LINK_USD, '1',  'LINK-USDC',s_first_pirce_apex_link,b_first_price_apex_link,s_first_price_dydx_link,b_first_price_dydx_link,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link,'link_count',link_trades)
    s_first_pirce_apex_link, b_first_price_apex_link, s_first_price_dydx_link, b_first_price_dydx_link, _, _, _, _,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link = await calculate_spread_link()
    await close_position(client_apex, client_dydx, position_id, MARKET_LINK_USD, '1','LINK-USDC',s_first_pirce_apex_link,b_first_price_apex_link,s_first_price_dydx_link,b_first_price_dydx_link,s_fourth_price_apex_link,b_fourth_price_apex_link,s_fourth_price_dydx_link,b_fourth_price_dydx_link,'link_count',link_trades)

async def trade_ltc():
    s_first_pirce_apex_ltc, b_first_price_apex_ltc, s_first_price_dydx_ltc, b_first_price_dydx_ltc, _, _, _, _,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc = await calculate_spread_ltc()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_LTC_USD, '0.5',  'LTC-USDC',s_first_pirce_apex_ltc,b_first_price_apex_ltc,s_first_price_dydx_ltc,b_first_price_dydx_ltc,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc,'ltc_count',ltc_trades)
    s_first_pirce_apex_ltc, b_first_price_apex_ltc, s_first_price_dydx_ltc, b_first_price_dydx_ltc, _, _, _, _,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc = await calculate_spread_ltc()
    await close_position(client_apex, client_dydx, position_id, MARKET_LTC_USD, '0.5','LTC-USDC',s_first_pirce_apex_ltc,b_first_price_apex_ltc,s_first_price_dydx_ltc,b_first_price_dydx_ltc,s_fourth_price_apex_ltc,b_fourth_price_apex_ltc,s_fourth_price_dydx_ltc,b_fourth_price_dydx_ltc,'ltc_count',ltc_trades)

async def trade_avax():
    s_first_pirce_apex_avax, b_first_price_apex_avax, s_first_price_dydx_avax, b_first_price_dydx_avax, _, _, _, _,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax = await calculate_spread_avax()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_AVAX_USD, '1',  'AVAX-USDC',s_first_pirce_apex_avax,b_first_price_apex_avax,s_first_price_dydx_avax,b_first_price_dydx_avax,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax,'avax_count',avax_trades)
    s_first_pirce_apex_avax, b_first_price_apex_avax, s_first_price_dydx_avax, b_first_price_dydx_avax, _, _, _, _,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax = await calculate_spread_avax()
    await close_position(client_apex, client_dydx, position_id, MARKET_AVAX_USD, '1','AVAX-USDC',s_first_pirce_apex_avax,b_first_price_apex_avax,s_first_price_dydx_avax,b_first_price_dydx_avax,s_fourth_price_apex_avax,b_fourth_price_apex_avax,s_fourth_price_dydx_avax,b_fourth_price_dydx_avax,'avax_count',avax_trades)

async def trade_atom():
    s_first_pirce_apex_atom, b_first_price_apex_atom, s_first_price_dydx_atom, b_first_price_dydx_atom, _, _, _, _,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom = await calculate_spread_atom()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_ATOM_USD, '1',  'ATOM-USDC',s_first_pirce_apex_atom,b_first_price_apex_atom,s_first_price_dydx_atom,b_first_price_dydx_atom,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom,'atom_count',atom_trades)
    s_first_pirce_apex_atom, b_first_price_apex_atom, s_first_price_dydx_atom, b_first_price_dydx_atom, _, _, _, _,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom = await calculate_spread_atom()
    await close_position(client_apex, client_dydx, position_id, MARKET_ATOM_USD, '1','ATOM-USDC',s_first_pirce_apex_atom,b_first_price_apex_atom,s_first_price_dydx_atom,b_first_price_dydx_atom,s_fourth_price_apex_atom,b_fourth_price_apex_atom,s_fourth_price_dydx_atom,b_fourth_price_dydx_atom,'atom_count',atom_trades)

async def trade_doge():
    s_first_pirce_apex_doge, b_first_price_apex_doge, s_first_price_dydx_doge, b_first_price_dydx_doge, _, _, _, _,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge = await calculate_spread_doge()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_DOGE_USD, '300',  'DOGE-USDC',s_first_pirce_apex_doge,b_first_price_apex_doge,s_first_price_dydx_doge,b_first_price_dydx_doge,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge,'doge_count',doge_trades)
    s_first_pirce_apex_doge, b_first_price_apex_doge, s_first_price_dydx_doge, b_first_price_dydx_doge, _, _, _, _,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge = await calculate_spread_doge()
    await close_position(client_apex, client_dydx, position_id, MARKET_DOGE_USD, '300','DOGE-USDC',s_first_pirce_apex_doge,b_first_price_apex_doge,s_first_price_dydx_doge,b_first_price_dydx_doge,s_fourth_price_apex_doge,b_fourth_price_apex_doge,s_fourth_price_dydx_doge,b_fourth_price_dydx_doge,'doge_count',doge_trades)

async def trade_bch():
    s_first_pirce_apex_bch, b_first_price_apex_bch, s_first_price_dydx_bch, b_first_price_dydx_bch, _, _, _, _,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch = await calculate_spread_bch()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_BCH_USD, '0.2',  'BCH-USDC',s_first_pirce_apex_bch,b_first_price_apex_bch,s_first_price_dydx_bch,b_first_price_dydx_bch,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch,'bch_count',bch_trades)
    s_first_pirce_apex_bch, b_first_price_apex_bch, s_first_price_dydx_bch, b_first_price_dydx_bch, _, _, _, _,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch = await calculate_spread_bch()
    await close_position(client_apex, client_dydx, position_id, MARKET_BCH_USD, '0.2','BCH-USDC',s_first_pirce_apex_bch,b_first_price_apex_bch,s_first_price_dydx_bch,b_first_price_dydx_bch,s_fourth_price_apex_bch,b_fourth_price_apex_bch,s_fourth_price_dydx_bch,b_fourth_price_dydx_bch,'bch_count',bch_trades)

async def trade_matic():
    s_first_pirce_apex_matic, b_first_price_apex_matic, s_first_price_dydx_matic, b_first_price_dydx_matic, _, _, _, _,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic = await calculate_spread_matic()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_MATIC_USD, '30',  'MATIC-USDC',s_first_pirce_apex_matic,b_first_price_apex_matic,s_first_price_dydx_matic,b_first_price_dydx_matic,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic,'matic_count',matic_trades)
    s_first_pirce_apex_matic, b_first_price_apex_matic, s_first_price_dydx_matic, b_first_price_dydx_matic, _, _, _, _,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic = await calculate_spread_matic()
    await close_position(client_apex, client_dydx, position_id, MARKET_MATIC_USD, '30','MATIC-USDC',s_first_pirce_apex_matic,b_first_price_apex_matic,s_first_price_dydx_matic,b_first_price_dydx_matic,s_fourth_price_apex_matic,b_fourth_price_apex_matic,s_fourth_price_dydx_matic,b_fourth_price_dydx_matic,'matic_count',matic_trades)

async def trade_sol():
    s_first_pirce_apex_sol, b_first_price_apex_sol, s_first_price_dydx_sol, b_first_price_dydx_sol, _, _, _, _,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol = await calculate_spread_sol()
    await execute_trade(client_apex, client_dydx, position_id, MARKET_SOL_USD, '1',  'SOL-USDC',s_first_pirce_apex_sol,b_first_price_apex_sol,s_first_price_dydx_sol,b_first_price_dydx_sol,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol,'sol_count',sol_trades)
    s_first_pirce_apex_sol, b_first_price_apex_sol, s_first_price_dydx_sol, b_first_price_dydx_sol, _, _, _, _,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol = await calculate_spread_sol()
    await close_position(client_apex, client_dydx, position_id, MARKET_SOL_USD, '1','SOL-USDC',s_first_pirce_apex_sol,b_first_price_apex_sol,s_first_price_dydx_sol,b_first_price_dydx_sol,s_fourth_price_apex_sol,b_fourth_price_apex_sol,s_fourth_price_dydx_sol,b_fourth_price_dydx_sol,'sol_count',sol_trades)

async def arbitrage():
    while True:
        btc_task = trade_btc()
        eth_task = trade_eth()
        link_task = trade_link()
        ltc_task = trade_ltc()
        avax_task = trade_avax()
        atom_task = trade_atom()
        doge_task = trade_doge()
        bch_task = trade_bch()
        matic_task = trade_matic()
        sol_task = trade_sol()
        await asyncio.gather(btc_task,eth_task,link_task,ltc_task,avax_task,atom_task,doge_task,bch_task,matic_task,sol_task)

       # 将所有变量组织成一个字典
        variables = {
            'btc_count': btc_count,
            'eth_count': eth_count,
            'link_count': link_count,
            'ltc_count': ltc_count,
            'avax_count': avax_count,
            'atom_count': atom_count,
            'doge_count': doge_count,
            'bch_count': bch_count,
            'matic_count': matic_count,
            'sol_count': sol_count,
            'arbitrage_count': arbitrage_count
        }

        # 将字典存储为JSON格式到文件
        with open('variables.json', 'w') as file:
            file.write(json.dumps(variables, indent=4))
        
        # 将所有交易数组组织成一个字典
        trade_data = {
            'btc_trades': btc_trades,
            'eth_trades': eth_trades,
            'link_trades': link_trades,
            'ltc_trades': ltc_trades,
            'avax_trades': avax_trades,
            'atom_trades': atom_trades,
            'doge_trades': doge_trades,
            'bch_trades': bch_trades,
            'matic_trades': matic_trades,
            'sol_trades': sol_trades
        }

        # 将字典存储为JSON格式到文件
        with open('trade_data.json', 'w') as file:
            file.write(json.dumps(trade_data, indent=4))  # 使用indent参数使JSON文件更易读

# 运行异步函数
asyncio.run(arbitrage())