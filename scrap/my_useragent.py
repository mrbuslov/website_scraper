# https://developers.whatismybrowser.com/useragents/explore/operating_system_name/
import random
from fake_useragent import UserAgent

def pc_agent():
    return UserAgent().random

def android_agent():
    agents = [
        'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.99 Mobile Safari/537.36',
        'Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/101.0',
        'Mozilla/5.0 (Android 12; Mobile; LG-M255; rv:101.0) Gecko/101.0 Firefox/101.0',
    ]

    return random.choice(agents)

def ios_agent():
    agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14A346 Safari/E7FBAF',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1',
    ]

    return random.choice(agents)