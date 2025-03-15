import json

from playwright.sync_api import sync_playwright, expect

CONFIG_PATH = "config/config.json"


class Config:
    __slots__ = ["login_url", "redirect_url", "username", "password"]
    def __init__(self, config):
        self.login_url = config["login_url"]
        self.redirect_url = config["redirect_url"]
        self.username = config["username"]
        self.password = config["password"]


def run(playwright, config: Config):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(config.login_url)
    page.fill("input[name='username']", config.username)
    page.fill("input[name='password']", config.password)
    with page.expect_navigation() as response_info:
        page.click("button[id='kc-login']")
    try:
        page.wait_for_url(config.redirect_url, timeout=5000)
    except:
        print("[error] Login failed! Timeout!")
        exit(1)
    response = response_info.value
    if response.status != 200:
        print("[error] Login failed!")
        exit(2)
    else:
        print("[info] Login success!")
    browser.close()

with sync_playwright() as playwright:
    with open(CONFIG_PATH) as f:
        config_file = json.load(f)
        config = Config(config_file)
    run(playwright, config)
