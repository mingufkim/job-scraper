from playwright.sync_api import sync_playwright

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://playwright.dev")

page.screenshot(path="playwright.png")

browser.close()

p.stop()
