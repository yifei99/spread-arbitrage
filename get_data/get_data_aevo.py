import asyncio
import configparser
from aevo import AevoClient
import csv
import os
import json

async def process_ticker(aevo, ticker, data_folder, initial_messages_to_skip=4):
    print(f"Subscribing to {ticker}")
    await aevo.subscribe_ticker(f"ticker:{ticker}:PERPETUAL")
    
    received_messages = 0
    last_timestamp = None  # Store the last processed timestamp

    # Ensure the data folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created folder: {data_folder}")

    # Construct the file path for the CSV file
    filename = os.path.join(data_folder, f"data_{ticker}_aevo.csv")
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        fieldnames = ['price', 'size', 'type', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            print(f"Created file and wrote header: {filename}")

        async for msg in aevo.read_messages():
            received_messages += 1

            if received_messages >= initial_messages_to_skip:

                # Check if the message is a JSON string and convert it to a dictionary if necessary
                if isinstance(msg, str):
                    try:
                        msg = json.loads(msg)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON message: {msg}. Error: {e}")
                        continue

                # Verify the structure of the message
                if 'data' in msg and 'tickers' in msg['data'] and len(msg['data']['tickers']) > 0:
                    data = msg['data']['tickers'][0]
                    timestamp_ns = int(msg['data']['timestamp'])  # Nanoseconds timestamp
                    timestamp_s = timestamp_ns // 1_000_000_000  # Convert to seconds

                    # Check if this timestamp is new (i.e., different from the last one processed)
                    if timestamp_s != last_timestamp:
                        # Prepare bid and ask data
                        bid_data = {
                            'price': data['bid']['price'],
                            'size': data['bid']['amount'],
                            'type': 'bid',
                            'timestamp': timestamp_s
                        }
                        ask_data = {
                            'price': data['ask']['price'],
                            'size': data['ask']['amount'],
                            'type': 'ask',
                            'timestamp': timestamp_s
                        }

                        # Write bid and ask data to CSV
                        writer.writerow(bid_data)
                        writer.writerow(ask_data)
                        
                        # Immediately flush the buffer to ensure data is written to disk
                        file.flush()
                        os.fsync(file.fileno())

                        print(f"Written to CSV: {bid_data} and {ask_data}")

                        # Update the last processed timestamp
                        last_timestamp = timestamp_s

                else:
                    print(f"Unexpected message structure: {msg}")

async def main():
    # Load configurations from aevo_config.ini
    config = configparser.ConfigParser()
    config.read('aevo_config.ini')

    tickers = ['SOL', 'DOGE', 'AVAX', 'MATIC', 'TRX', 'MKR', 'UMA', 'ATOM', 'CRV', 'BTC', 'NEAR', 'ETH', 'LINK', 
               'LTC', 'BCH', 'XRP', 'WLD', 'APT', 'ARB', 'TON', 'BLUR', 'BNB', 'DYDX', '1000PEPE', 'LDO', 'OP', 'TIA']
    clients = []
    tasks = []

    data_folder = 'depth-data'  # Define the folder for storing CSV files

    for ticker in tickers:
        try:
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
            task = process_ticker(aevo, ticker, data_folder)
            tasks.append(task)

        except Exception as e:
            print(f"Error initializing connection for {ticker}: {e}")

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
