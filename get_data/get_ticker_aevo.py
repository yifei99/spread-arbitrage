import asyncio
import configparser
from aevo import AevoClient

async def process_ticker(aevo, ticker, initial_messages_to_skip=4):
    print(f"Subscribing to {ticker}")
    await aevo.subscribe_ticker(f"ticker:{ticker}:PERPETUAL")
    
    received_messages = 0

    async for msg in aevo.read_messages():
        received_messages += 1

        if received_messages >= initial_messages_to_skip:
            print(f"{ticker} (Message {received_messages}): {msg}")
            await asyncio.sleep(10)  # Wait for 10 second before processing the next message


async def main():
    # Load configurations from aevo_config.ini
    config = configparser.ConfigParser()
    config.read('aevo_config.ini')

    tickers = ['SOL', 'DOGE', 'AVAX','MATIC','TRX','MKR','UMA','ATOM','CRV','BTC','NEAR','ETH','LINK']
    clients = []
    tasks = []

    for ticker in tickers:
        # Initialize AevoClient with specific configuration for the ticker
        aevo = AevoClient(
            signing_key=config[ticker]['signing_key'],
            wallet_address=config[ticker]['wallet_address'],
            api_key=config[ticker]['api_key'],
            api_secret=config[ticker]['api_secret'],
            env=config[ticker]['env'],
        )
        await aevo.open_connection()  # Open WebSocket connection
        clients.append(aevo)

        # Create a task for processing messages from this ticker
        task = process_ticker(aevo, ticker)
        tasks.append(task)

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

    # No need to close connections, as we are keeping them open for ongoing message processing

if __name__ == "__main__":
    asyncio.run(main())
