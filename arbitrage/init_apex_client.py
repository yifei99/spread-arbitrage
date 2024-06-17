from apexpro.constants import APEX_HTTP_TEST, NETWORKID_TEST, APEX_HTTP_MAIN, NETWORKID_MAIN
from apexpro.http_private_stark_key_sign import HttpPrivateStark
from configparser import ConfigParser

import warnings

# 部分匹配消息内容来忽略警告
warnings.filterwarnings("ignore", message="This HTTP class is maintained for compatibility purposes.")


# 定义一个函数，用来初始化客户端
def init_client():
    # 创建配置对象
    config = ConfigParser()
    # 读取配置文件
    config.read('apexconfig.ini')
    # 获取 apex 部分的参数
    public_key = config.get('apex', 'public_key')
    public_key_y_coordinate = config.get('apex', 'public_key_y_coordinate')
    private_key = config.get('apex', 'private_key')
    key = config.get('apex', 'key')
    secret = config.get('apex', 'secret')
    passphrase = config.get('apex', 'passphrase')
    # 创建客户端对象
    client = HttpPrivateStark(
        APEX_HTTP_MAIN,
        network_id=NETWORKID_MAIN,
        stark_public_key=public_key,
        stark_private_key=private_key,
        stark_public_key_y_coordinate=public_key_y_coordinate,
        api_key_credentials={"key": key, "secret": secret, "passphrase": passphrase},
    )
    # 返回客户端对象
    return client