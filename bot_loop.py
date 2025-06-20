import asyncio
import os
import random
from playwright.async_api import async_playwright

REELS_FOLDER = "reels"

async def upload_reel(playwright, reel_path):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(storage_state="cookies.json")
    page = await context.new_page()
    print(f"🌐 Navigating to Instagram...")
    await page.goto("https://www.instagram.com/")
    await page.wait_for_timeout(5000)

    try:
        print(f"📤 Uploading: {reel_path}")
        await page.click("svg[aria-label='New post']")
        await page.wait_for_timeout(2000)
        await page.locator("text=Post").click()
        await page.wait_for_timeout(2000)
        input_file = await page.query_selector("input[type='file']")
        await input_file.set_input_files(reel_path)
        await page.wait_for_timeout(10000)
        await page.locator("text=Next").click()
        await page.wait_for_timeout(3000)
        await page.locator("text=Next").click()
        await page.wait_for_timeout(3000)
        await page.locator("text=Share").click()
        await page.wait_for_timeout(10000)
        print(f"✅ Uploaded: {reel_path}")
        os.remove(reel_path)
    except Exception as e:
        print(f"❌ Error uploading {reel_path}: {e}")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        reel_files = [os.path.join(REELS_FOLDER, f) for f in os.listdir(REELS_FOLDER) if f.endswith(".mp4")]
        if not reel_files:
            print("📁 No reels found.")
            return
        random.shuffle(reel_files)
        to_upload = reel_files[:random.randint(10, 15)]
        for reel in to_upload:
            await upload_reel(playwright, reel)
            wait_time = random.randint(60, 600)
            print(f"⏳ Waiting {wait_time} seconds before next upload...")
            await asyncio.sleep(wait_time)

asyncio.run(main())
