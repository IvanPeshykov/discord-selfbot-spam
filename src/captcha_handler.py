from typing import Dict, Any, Optional
import aiohttp
import discord
from aiohttp import BasicAuth
import asyncio
from data.config import captcha_api_key

class CaptchaHandler(discord.CaptchaHandler):
    async def fetch_token(
        self,
        data: Dict[str, Any],
        proxy: Optional[str],
        proxy_auth: Optional[BasicAuth],
        /,
    ) -> str:

        # First request to in.php
        url_in = "https://24captcha.online/in.php"
        payload_in = {
            "key": captcha_api_key,
            "sitekey": data['captcha_sitekey'],
            "pageurl": "https://discord.com/channels/@me",
            "json": 1,
            "rqdata": data['captcha_rqdata']
        }
        headers_in = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br"
        }

        async with aiohttp.ClientSession(headers=headers_in) as session:
            try:
                # Send initial request to in.php
                async with session.post(url_in, json=payload_in) as res_in:
                    res_in.raise_for_status()  # Raise an exception for HTTP errors
                    response_data_in = await res_in.json()
                    request_id = response_data_in.get('request')
                    if not request_id:
                        # print(f"Error in in.php request: {response_data_in}")
                        return ""
                    # print(f"Received request ID from in.php: {request_id}")

                    # Second request to res.php with retry logic for 'CAPCHA_NOT_READY'
                    url_res = "https://24captcha.online/res.php"
                    payload_res = {
                        "key": captcha_api_key,
                        "id": request_id,
                        "action": "get",
                        "json": 1
                    }

                    # Retry logic
                    while True:
                        async with session.post(url_res, json=payload_res) as res_res:
                            res_res.raise_for_status()
                            response_data_res = await res_res.json()
                            status = response_data_res.get('status')
                            if status == 1:  # Captcha solved
                                # print(f"Captcha solved successfully: {response_data_res['request']}")
                                return response_data_res['request']
                            elif status == 0 and response_data_res.get('request') == 'CAPCHA_NOT_READY':
                               #  print("Captcha not ready, retrying in 5 seconds...")
                                await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                            else:
                                # print(f"Error in res.php request: {response_data_res}")
                                return ""
            except Exception as e:
                print(f"Error: {e}")
                return ""
