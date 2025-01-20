import datetime
import sys
import time
from platform import system

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from creds import username, password, facility_name, latest_notification_date, seconds_between_checks
from telegram import send_message, send_photo
from urls import BASE_URL, SIGN_IN_URL, SCHEDULE_URL, APPOINTMENTS_URL


def log_in(driver):
    if driver.current_url != SIGN_IN_URL:
        return

    print('Logging in.')

    # Clicking the OK button in the "You need to sign in or sign up before continuing" dialog
    ok_button = driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/button')
    if ok_button:
        ok_button.click()

    # Filling the user and password
    user_box = driver.find_element(By.NAME, 'user[email]')
    user_box.send_keys(username)
    password_box = driver.find_element(By.NAME, 'user[password]')
    password_box.send_keys(password)

    # Clicking the checkbox
    driver.find_element(By.XPATH, '//*[@id="sign_in_form"]/div[3]/label/div').click()

    # Clicking 'Sign in'
    driver.find_element(By.XPATH, '//*[@id="sign_in_form"]/p[1]/input').click()

    # Waiting for the page to load.
    time.sleep(2)
    print('Logged in.')


def is_worth_notifying(year, month, days):
    first_available_date_object = datetime.datetime.strptime(f'{year}-{month}-{days[0]}', "%Y-%B-%d")
    latest_notification_date_object = datetime.datetime.strptime(latest_notification_date, '%Y-%m-%d')

    return first_available_date_object <= latest_notification_date_object


def check_appointments(driver):
    driver.get(SCHEDULE_URL)
    log_in(driver)

    driver.get(APPOINTMENTS_URL)

    # Clicking the Continue button in case of rescheduling multiple people to include all
    continue_button = driver.find_element(By.CLASS_NAME, 'primary')
    if continue_button and continue_button.get_property('value') == 'Continue':
        continue_button.click()

    facility_select = Select(driver.find_element(By.ID, 'appointments_consulate_appointment_facility_id'))
    facility_select.select_by_visible_text(facility_name)
    time.sleep(1)

    if driver.find_element(By.ID, 'consulate_date_time_not_available').is_displayed():
        print("No dates available")
        return

    # Click on "Date of Appointment" to display calendar
    driver.find_element(By.ID, 'appointments_consulate_appointment_date').click()

    while True:
        for date_picker in driver.find_elements(By.CLASS_NAME, 'ui-datepicker-group'):
            day_elements = date_picker.find_elements(By.TAG_NAME, 'td')
            available_days = [day_element.find_element(By.TAG_NAME, 'a').get_attribute("textContent")
                              for day_element in day_elements if day_element.get_attribute("class") == ' undefined']
            if available_days:
                month = date_picker.find_element(By.CLASS_NAME, 'ui-datepicker-month').get_attribute("textContent")
                year = date_picker.find_element(By.CLASS_NAME, 'ui-datepicker-year').get_attribute("textContent")
                message = f'Available days found in {month} {year}: {", ".join(available_days)}. Link: {SIGN_IN_URL}'
                print(message)

                if not is_worth_notifying(year, month, available_days):
                    print("Not worth notifying.")
                    return

                send_message(message)
                send_photo(driver.get_screenshot_as_png())
                return

        # Skipping two months since we processed both already
        driver.find_element(By.CLASS_NAME, 'ui-datepicker-next').click()
        driver.find_element(By.CLASS_NAME, 'ui-datepicker-next').click()

# Nginx in front of the ais.usvisa-info is configured to block Selenium
# Setting headers to mimic "real" browser
def fix_headers(request):
    # delete the existing misconfigured default headers values
    del request.headers["User-Agent"]
    del request.headers["Sec-Ch-Ua"]
    del request.headers["Sec-Fetch-Site"]
    del request.headers["Accept-Encoding"]
    # replace the deleted headers with edited values
    request.headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    request.headers["Sec-Ch-Ua"] = "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\""
    request.headers["Sec-Fetch-Site"] = "cross-site"
    request.headers["Accept-Encoding"] = "gzip, deflate, br, zstd"
    # add the missing headers
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # add the interceptor
    driver.request_interceptor = fix_headers

    while True:
        current_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
        print(f'Starting a new check at {current_time}.')
        try:
            check_appointments(driver)
        except Exception as err:
            print(f'Exception: {err}')

        time.sleep(seconds_between_checks)


if __name__ == "__main__":
    main()
