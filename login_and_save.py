import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.instagram.com/accounts/login/")
        await page.fill("input[name='username']", "YOUR_USERNAME")
        await page.fill("input[name='password']", "YOUR_PASSWORD")
        await page.press("input[name='password']", "Enter")
        print("⚠️ Enter OTP manually if asked...")
        await page.wait_for_timeout(30000)
        await context.storage_state(path="cookies.json")
        print("✅ Session saved to cookies.json")
        await browser.close()

asyncio.run(main())
