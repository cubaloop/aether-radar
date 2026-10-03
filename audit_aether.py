import asyncio
from playwright.async_api import async_playwright
import shutil
import os

art_dir = 'C:/Users/Yo/.gemini/antigravity/brain/5ffd42c9-57c1-4bbb-be8b-eb9d301859b6'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Initial View
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto('http://localhost:8095/', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='aether_desktop.png', full_page=False)
        shutil.copy('aether_desktop.png', os.path.join(art_dir, 'aether_desktop.png'))
        print('Captured initial desktop')

        # 2. Trigger Scan on octane.rent
        await page.fill('#targetUrlInput', 'octane.rent')
        await page.click('#scanSubmitBtn')
        print('Triggered scan, waiting for neural decomposition...')
        
        # Wait for results to be visible
        await page.wait_for_selector('#resultsSection:not(.hidden)', timeout=30000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path='aether_scanned.png', full_page=False)
        shutil.copy('aether_scanned.png', os.path.join(art_dir, 'aether_scanned.png'))
        print('Captured scanned results')

        # 3. Trigger Instant Demo Unlock
        await page.click('button:has-text("Instant Unlock")')
        await page.wait_for_selector('#unlockedDossierContainer:not(.hidden)', timeout=10000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path='aether_unlocked.png', full_page=False)
        shutil.copy('aether_unlocked.png', os.path.join(art_dir, 'aether_unlocked.png'))
        print('Captured unlocked dossier')

        # 4. Mobile Viewport
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await mobile_page.goto('http://localhost:8095/', wait_until='networkidle')
        await mobile_page.wait_for_timeout(1000)
        await mobile_page.screenshot(path='aether_mobile.png', full_page=False)
        shutil.copy('aether_mobile.png', os.path.join(art_dir, 'aether_mobile.png'))
        print('Captured mobile initial')

        await browser.close()
        print('All test screenshots completed successfully.')

asyncio.run(main())

