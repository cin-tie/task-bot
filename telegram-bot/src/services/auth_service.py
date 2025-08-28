import aiohttp
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.base_url = os.getenv("AUTH_SERVICE_URL", "http://auth-service:3000")

    async def register_user(self, telegram_id: str, username: str, password: str, email: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/auth/register"
        payload = {
            "telegram_id": telegram_id,
            "username": username,
            "password": password,
            "email": email
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 201:
                        return await response.json()
                    else:
                        error_text = await response.json()
                        logger.error(f"Auth service error: {error_text}")
                        raise Exception(f"Auth service error: {error_text}")
                    
        except Exception as e:
            logger.error(f"Failed to register user: {e}")
            raise
    
    async def check_user_exists(self, telegram_id: str) -> bool:
        url = f"{self.base_url}/auth/check-user/{telegram_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
        except:
            return False
    
    async def login_user(self, telegram_id: str, password: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/auth/login"
        payload = {
            "telegramId": telegram_id,
            "password": password
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except:
            return None