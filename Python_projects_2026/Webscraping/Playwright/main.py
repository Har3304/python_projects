from playwright.sync_api import sync_playwright
import time

with sync_playwright() as playwright:
    #Launch a browser
    browser = playwright.chromium.launch(headless=False)

    #Create a new page or tab
    page = browser.new_page()

    #Visit playwright website
    page.goto("https://playwright.dev/python")

    #Locate a link element with "Docs" text

    docs_button = page.get_by_role(('link', name='Get Started'))
    docs_button.click()

    #Get the page url
    print(page.url)

    time.sleep(10)