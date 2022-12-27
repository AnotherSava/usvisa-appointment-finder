# US Visa appointment finder 😎

😎 Parser of US visa appointment slots on [ais.usvisa-info.com](www.ais.usvisa-info.com)

Script will notify you via telegram if any slots available under your conditions.

## Installation

The recommended way to install ```
usvisa-appointment-finder```
 uses pip and add configuration to get started:

```bash
pip install -r requirements.txt
```

After creating telegram bot via `@botfather` and creating group, just add your bot to this group. To find `telegram_chat_id` parameter just add `@getidsbot` to your group.

## Configuration

Rename default config file `app-config-sample.properties` to `app-config.properties`

Here's a quick example:

```properties
username=name@email.com
password=qwerty
url_id=12345
country_code=ca
facility_name=Vancouver
latest_notification_date=2023-10-01
seconds_between_checks=180
telegram_bot_token=12345:some_token
telegram_chat_id=12345
```

## License

[MIT](./LICENSE)