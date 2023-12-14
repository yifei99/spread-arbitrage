# 定义一个函数，用来发交易
async def send_order_dydx(client, position_id, market, side, order_type, post_only, size, price, limit_fee, expiration_epoch_seconds):
    # 创建订单参数
    order_params = {
        'position_id': position_id,
        'market': market,
        'side': side,
        'order_type': order_type,
        'post_only': post_only,
        'size': size,
        'price': price,
        'limit_fee': limit_fee,
        'expiration_epoch_seconds': expiration_epoch_seconds
    }
    # 创建订单
    order_response = client.private.create_order(**order_params)
    # 返回订单结果
    return order_response.data
