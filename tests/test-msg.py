import asyncio
import aiohttp

# PASTE YOUR URL HERE
WEBHOOK_URL = "https://discord.com/api/webhooks/1450192357516644544/zVu9R6WhWntS8erCu7INqxQ40WdiADZFvWPUFIB61GN2XB21EtM5Epm_oWCchatGgdTD"


async def test():
    async with aiohttp.ClientSession() as session:
        await session.post(WEBHOOK_URL, json={"content": "Test Message"})
        print("Sent!")

# Run the test
if __name__ == "__main__":
    # Fix for Python 3.14/3.12 loop issue
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test())