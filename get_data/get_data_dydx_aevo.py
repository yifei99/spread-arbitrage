import asyncio
import configparser
from aevo import AevoClient

async def main():
    # Load configurations from aevo_config.ini
    config = configparser.ConfigParser()
    config.read('aevo_config.ini')

    aevo = AevoClient(
        signing_key=config['aevo']['signing_key'],
        wallet_address=config['aevo']['wallet_address'],
        api_key=config['aevo']['api_key'],
        api_secret=config['aevo']['api_secret'],
        env=config['aevo']['env'],
    )
    
    await aevo.open_connection()  # Open WebSocket connection
    await aevo.subscribe_ticker("ticker:SOL:PERPETUAL")
    
    initial_messages_to_skip = 4
    received_messages = 0

    async for msg in aevo.read_messages():
        if received_messages < initial_messages_to_skip:
            received_messages += 1
            continue
        
        print(msg)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
