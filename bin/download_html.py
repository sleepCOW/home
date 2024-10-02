import sys
import asyncio
from playwright.async_api import async_playwright
import requests


async def save_page_html(url: str, output_file: str, take_screenshot: bool):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await asyncio.sleep(4)  # Wait for 4 seconds
        html_content = await page.content()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        if take_screenshot:
            screenshot_file = output_file.rsplit('.', 1)[0] + '.png'
            await page.screenshot(path=screenshot_file)
        await browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python download_html.py <url> <output_file> <use_playwright> <take_screenshot>')
        print("Options:")
        print("[-js] - load page with javascript as a real browser (using playwright)")
        print("[-s] - take screenshot (works only when using playwright)")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]
    use_playwright = '-js' in sys.argv or '-playwright' in sys.argv
    take_screenshot = '-s' in sys.argv or '-screenshot' in sys.argv

    if use_playwright:
        asyncio.run(save_page_html(url, output_file, take_screenshot))
    else:
        r = requests.get(url)
        if r.status_code == 200:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(r.text)
        else:
            print(f'Bad status code: {r.status_code}')