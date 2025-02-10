from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class WhatsAppDriver:
    def __init__(self):
        self.driver = None
        self.cookie_file = 'whatsapp_cookies.pkl'
        
    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1200,800')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://web.whatsapp.com')
        
        # 尝试加载保存的cookies
        if self.load_cookies():
            print("尝试使用保存的会话...")
            self.driver.refresh()
            time.sleep(3)
            
            # 如果cookies有效则跳过登录
            if self.is_logged_in():
                print("使用保存的会话成功")
                return
                
        print("请扫描WhatsApp Web二维码进行登录...")
        # Wait for login with timeout
        start_time = time.time()
        while not self.is_logged_in():
            if time.time() - start_time > 120:  # 2分钟超时
                raise Exception("登录超时，请重试")
            time.sleep(5)
            
        # 登录成功后保存cookies
        self.save_cookies()
        
    def is_logged_in(self):
        try:
            # 检查多个登录状态元素
            chat_list = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="chat-list"]')
            qr_code = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-ref]')
            
            # 如果有聊天列表且没有二维码，说明已登录
            if chat_list and not qr_code:
                print("已成功登录WhatsApp Web")
                return True
                
            # 如果发现二维码，说明未登录
            if qr_code:
                print("请扫描二维码登录")
                return False
                
            return False
        except Exception as e:
            print(f"登录状态检查错误: {str(e)}")
            return False
            
    def send_message(self, contact, message):
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="chat-list-search"]')
        search_box.click()
        search_box.send_keys(contact)
        time.sleep(2)
        
        chat = self.driver.find_element(By.CSS_SELECTOR, f'span[title="{contact}"]')
        chat.click()
        time.sleep(1)
        
        input_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="conversation-compose-box-input"]')
        input_box.send_keys(message + Keys.ENTER)
        time.sleep(1)
        
    def save_cookies(self):
        import pickle
        with open(self.cookie_file, 'wb') as f:
            pickle.dump(self.driver.get_cookies(), f)
        print("Cookies保存成功")

    def load_cookies(self):
        import os
        import pickle
        if not os.path.exists(self.cookie_file):
            return False
            
        try:
            with open(self.cookie_file, 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            return True
        except Exception as e:
            print(f"加载cookies失败: {str(e)}")
            return False

    def close(self):
        if self.driver:
            try:
                self.save_cookies()
            except Exception as e:
                print(f"保存cookies失败: {str(e)}")
            self.driver.quit()
