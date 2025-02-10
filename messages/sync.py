import asyncio
from .selenium_driver import WhatsAppDriver
from database import db
import time

class MessageSync:
    async def __aenter__(self):
        self.driver = WhatsAppDriver()
        await self.driver.start_driver()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.driver.close()

    async def sync_messages(self):
        try:
            if not await self.driver.is_logged_in():
                raise Exception("请先扫描二维码登录WhatsApp Web")

            print("验证登录状态成功，开始同步消息...")

            chats = await self.driver.get_all_chats()
            if not chats:
                print("没有找到任何聊天")
            return []

            new_messages = []
            for chat in chats:
                messages = await self.driver.get_chat_messages(chat)
                if messages:
                    for msg in messages:
                        if not db.message_exists(msg['id']):
                            new_messages.append(msg)

            if new_messages:
                print(f"发现 {len(new_messages)} 条新消息")
                db.store_messages(new_messages)
                return new_messages

            print("没有发现新消息")
            return False

        except Exception as e:
            print(f"同步错误: {str(e)}")
            raise

    async def send_message(self, contact, message):
        await self.driver.send_message(contact, message)
