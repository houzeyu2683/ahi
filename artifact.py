import os
import time
import math
import json
import re
from typing import Optional, Literal
from dotenv import dotenv_values
from playwright.sync_api import sync_playwright
import logging
from logging.handlers import TimedRotatingFileHandler

class Screen:

    def __init__(self, headless: bool, checkpoint: str) -> None:
        self.headless = headless
        self.checkpoint = checkpoint
        return

    def setLog(self, title: str, path: str) -> bool:
        ''''''

        log = logging.getLogger(title)
        log.setLevel(logging.INFO)

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        style = TimedRotatingFileHandler(
            filename=path,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )

        # 3. 設定日誌格式
        rule = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        style.setFormatter(rule)

        # 4. 將 Handler 加入 Logger
        log.addHandler(style)

        # 測試寫入
        self.log = log
        log.info("Set log successful")
        return True

    def startClient(self) -> bool:
        """啟動客戶端"""

        self.client = sync_playwright().start()
        return True

    def openBrowser(self) -> bool:
        """打開瀏覽器"""

        self.browser = self.client.chromium.launch(headless=self.headless)
        return True

    def initiatePage(self, link: Optional[str] = None) -> bool:
        """初始頁面"""

        # self.page = self.browser.new_page()
        context = self.browser.new_context()
        context.add_init_script(
            'Object.defineProperty(navigator, "webdriver", {get: () => false})'
        )
        self.page = context.new_page()
        if link is not None: self.page.goto(link)
        return True

    def terminatePage(self) -> bool:
        """終止頁面"""

        self.page.close()
        return True

    def closeBrowser(self) -> bool:
        """關閉瀏覽器"""

        self.browser.close()
        return True

    def stopClient(self) -> bool:
        """終止客戶端"""

        self.client.stop()
        return True

    pass