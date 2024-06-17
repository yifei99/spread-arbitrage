from apexpro.helpers.util import round_size
import warnings

# 部分匹配消息内容来忽略警告
warnings.filterwarnings("ignore", message="This HTTP class is maintained for compatibility purposes.")

# 定义一个函数，用来发交易
async def send_order_apex(client, symbol, side, type, size, expirationEpochSeconds, price, limitFeeRate):
    # 优化订单的大小和价格
    symbolData = {}
    for k, v in enumerate(client.configs().get('data').get('perpetualContract')):
        if v.get('symbol') == symbol:
            symbolData = v
    size = round_size(size, symbolData.get('stepSize'))
    price = round_size(price, symbolData.get('tickSize'))
    # 创建订单
    createOrderRes = client.create_order(symbol=symbol, side=side,
                                           type=type, size=size, expirationEpochSeconds=expirationEpochSeconds,
                                           price=price, limitFeeRate=limitFeeRate)
    # 返回订单结果
    return createOrderRes


