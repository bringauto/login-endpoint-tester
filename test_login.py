import json

from playwright.sync_api import sync_playwright, Playwright # type: ignore

CONFIG_PATH = "config/config.json"
PAGE_LOAD_TIMEOUT = 10000
RETRY_ATTEMPTS = 3


class Config:
    __slots__ = ["login_url", "redirect_url", "username", "password"]
    def __init__(self, config):
        self.login_url = config["login_url"]
        self.redirect_url = config["redirect_url"]
        self.username = config["username"]
        self.password = config["password"]


def run(playwright: Playwright, config: Config):
    for i in range(RETRY_ATTEMPTS):
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(config.login_url)
            page.wait_for_selector("input[name='username']", timeout=PAGE_LOAD_TIMEOUT)
            page.wait_for_selector("input[name='password']", timeout=PAGE_LOAD_TIMEOUT)
            page.fill("input[name='username']", config.username)
            page.fill("input[name='password']", config.password)
            with page.expect_navigation() as response_info:
                page.click("button[id='kc-login']")
                page.wait_for_url(config.redirect_url, timeout=PAGE_LOAD_TIMEOUT)
                break
        except Exception as e:
            print("[WARNING] Login failed! Timeout!")
            print(e)
            if i == RETRY_ATTEMPTS - 1:
                print("[ERROR] Login failed!")
                exit(1)
            browser.close()

    response = response_info.value
    if response.status != 200:
        print("[ERROR] Login failed!")
        exit(2)
    else:
        print("[INFO] Login success!")
    browser.close()

with sync_playwright() as playwright:
    with open(CONFIG_PATH) as f:
        config_file = json.load(f)
        config = Config(config_file)
    run(playwright, config)
