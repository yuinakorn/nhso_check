import requests
from dotenv import dotenv_values

config_env = dotenv_values(".env")


def sent_notify_message(message):
    line_token = config_env["LINE_TOKEN"]
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {
        'Authorization': 'Bearer ' + line_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    return line_notify.status_code

