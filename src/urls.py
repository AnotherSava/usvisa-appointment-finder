from creds import url_id, country_code

BASE_URL = f'https://ais.usvisa-info.com/en-{country_code}/niv'
SIGN_IN_URL = f'{BASE_URL}/users/sign_in'
SCHEDULE_URL = f'{BASE_URL}/schedule/{url_id}'
APPOINTMENTS_URL = f'{SCHEDULE_URL}/appointment'
SCHEDULE_APPOINTMENT_URL = f'{SCHEDULE_URL}/continue'
SCHEDULE_CONTINUE_URL = f'{SCHEDULE_URL}/continue_actions'
