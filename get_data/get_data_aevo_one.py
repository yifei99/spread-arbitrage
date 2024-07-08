import asyncio
from aevo import AevoClient

async def main():
    aevo = AevoClient(
        signing_key="0x47992f6bbba2c10404a383e8fdec49744ffd5e1e78012f13e88848a999494492",
        wallet_address="0xc0942fc10b2430b703527a2b596dfea3588025dc",
        api_key="z3vm6onVoLBHzR1wFfrtDSebS9Z52F5i",
        api_secret="589d39a43efbac4034f0af199967af0a99456d03e2771bdd7c4f6fc496f0424c",
        env="mainnet",
    )

    await aevo.open_connection() # need to do this first to open wss connections
    await aevo.subscribe_ticker("ticker:ETH:PERPETUAL")

    async for msg in aevo.read_messages():
        print(msg)

if __name__ == "__main__":
    asyncio.run(main())