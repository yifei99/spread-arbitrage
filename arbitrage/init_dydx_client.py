from configparser import ConfigParser
from dydx3 import Client

# 定义一个函数，用来初始化客户端
def init_dydx_client():
    # 创建配置对象
    config = ConfigParser()
    # 读取配置文件
    config.read('dydxconfig.ini')
    # 获取 dydx 部分的参数
    eth_private_key = config.get('dydx', 'eth_private_key')
    # 创建客户端对象
    client = Client(host='https://api.dydx.exchange',
                    eth_private_key=eth_private_key,
                    )
    # 设置dydx STARK 密钥
    stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
    client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
    (public_x, public_y) = (
    stark_key_pair_with_y_coordinate['public_key'],
    stark_key_pair_with_y_coordinate['public_key_y_coordinate'],
    )
    # 返回客户端对象
    return client
