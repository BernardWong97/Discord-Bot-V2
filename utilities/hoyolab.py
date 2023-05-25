import os, requests, json, time, random, string, hashlib
from typing import Union
from enums import RequestMethod
from colorama import init as colorama_init, Fore
from dotenv import load_dotenv
from database import retrieve_data

colorama_init()
load_dotenv()

class HoyolabException(Exception):
    pass

class GameClient(object):

    def __init__(self, cookie: str):
        self.request_url = None
        self.act_id = None
        self.lang = os.getenv("LANG_CODE")
        self.request_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh;q=0.6',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Origin': 'https://act.hoyolab.com',
            'Referer': 'https://act.hoyolab.com/',
            'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

    def claim_daily_reward(self) -> Union[dict, str, None]:
        url = f'{self.request_url}sign?lang={self.lang}'
        payload = {
            'act_id': self.act_id
        }
        
        try:
            response = self.send_request(url, payload)

            if response["data"] is not None:
                reward = self._retrieve_reward_info()
                return reward
            else:
                return response["message"]
        except Exception as e:
            print(f"{Fore.RED}Claim Daily Reward Error - {e}{Fore.RESET}")
        
        return None

    def send_request(self, url, payload = None):
        try:
            response = requests.request(method=RequestMethod.POST.name if payload is not None else RequestMethod.GET.name ,url=url, headers=self.request_headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}HTTP Request Error - {e}{Fore.RESET}")
            raise Exception("Error sending request")
        except json.decoder.JSONDecodeError as e:
            print(f"{Fore.RED}JSON Decoding Error - {e}{Fore.RESET}")
            raise Exception("Error decoding response")

    def _retrieve_reward_info(self):
        total_sign_day = self._retrieve_total_sign_day()
        monthly_rewards = self._retrieve_monthly_rewards()
        return monthly_rewards[total_sign_day - 1]

    def _retrieve_monthly_rewards(self):
        url = f'{self.request_url}home?lang={self.lang}&act_id={self.act_id}'
        response = self.send_request(url)
        return response["data"]["awards"]

    def _retrieve_total_sign_day(self):
        url = f'{self.request_url}info?lang={self.lang}&act_id={self.act_id}'
        response = self.send_request(url)
        return response["data"]["total_sign_day"]
    

class Genshin(GameClient):

    def __init__(self, cookie: str):
        super().__init__(cookie)

    def claim_daily_reward(self):
        self.request_url = os.getenv("GENSHIN_POST_URL")
        self.act_id = os.getenv("GENSHIN_ACT_ID")
        self.request_headers["Host"] = 'sg-hk4e-api.hoyolab.com'
        return super().claim_daily_reward()

    def get_user_note(self, uid: str):
        self.request_url = f'{os.getenv("GENSHIN_GET_URL")}dailyNote?server=os_asia&role_id={uid}'
        self.request_headers["Host"] = 'bbs-api-os.hoyolab.com'
        self.request_headers["Authority"] = 'bbs-api-os.hoyolab.com'
        self.request_headers["Ds"] = self._generate_ds()
        self.request_headers["X-Rpc-App_version"] = '1.5.0'
        self.request_headers["X-Rpc-Client_type"] = '5'
        self.request_headers["X-Rpc-Language"] = self.lang

        return self.send_request(self.request_url)

    def get_uid(self, uid):
        self.request_url = f'{os.getenv("GENSHIN_GET_URL_2")}getGameRecordCard?uid={uid}'
        self.request_headers["Host"] = 'bbs-api-os.hoyolab.com'
        self.request_headers["Authority"] = 'bbs-api-os.hoyolab.com'
        self.request_headers["Ds"] = self._generate_ds()
        self.request_headers["X-Rpc-App_version"] = '1.5.0'
        self.request_headers["X-Rpc-Client_type"] = '5'
        self.request_headers["X-Rpc-Language"] = self.lang

        response = self.send_request(self.request_url)

        try:
            return response["data"]["list"][0]["game_role_id"]
        except:
            print(f"{Fore.BLUE}{response}{Fore.RESET}")
            raise HoyolabException("Error getting genshin uid")


    def _generate_ds(self) -> str:
        t = int(time.time())
        r = "".join(random.choices(string.ascii_letters, k=6))
        h = hashlib.md5(f"salt={os.getenv('GENSHIN_SALT')}&t={t}&r={r}".encode()).hexdigest()

        return f"{t},{r},{h}"

class StarRail(GameClient):

    def __init__(self, cookie: str):
        super().__init__(cookie)

    def claim_daily_reward(self):
        self.request_url = os.getenv("STARRAIL_POST_URL")
        self.act_id = os.getenv("STARRAIL_ACT_ID")
        self.request_headers["Host"] = 'sg-public-api.hoyolab.com'
        return super().claim_daily_reward()
