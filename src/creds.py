from jproperties import Properties

configs = Properties()
with open('../config/app-config.properties', 'rb') as config_file:
    configs.load(config_file)

# ais.usvisa-info.com credentials

username = configs.get('username').data
password = configs.get('password').data

# Number id in the url (e.g.: https://ais.usvisa-info.com/en-ca/niv/schedule/41231513)
url_id = configs.get('url_id').data

# Country code in the url
country_code = configs.get('country_code').data

facility_name = configs.get('facility_name').data

latest_notification_date = configs.get('latest_notification_date').data

seconds_between_checks = int(configs.get('seconds_between_checks').data)

# Telegram bot token and chat
telegram_bot_token = configs.get('telegram_bot_token').data
telegram_chat_id = configs.get('telegram_chat_id').data
