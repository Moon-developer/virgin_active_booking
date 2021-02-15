from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class VirginActive:
    def __init__(self):
        # get login
        self.id = getenv('CRED')

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--incognito")
        # self.chrome = webdriver.Chrome(chrome_options=chrome_options)
        self.chrome = webdriver.Chrome()

        # set days to book for:
        self.days = ['MON', 'WED', 'FRI', 'SUN']
        # time to book at:
        self.time = '08:05'
        # class to book for:
        self.name = 'shape'
        # booking url
        self.url = 'https://my.virginactive.co.za/bookings/'

    def login(self):
        if login_input := self.chrome.find_element_by_id('input_id'):
            login_input.send_keys(self.id + Keys.RETURN)

    def goto_make_a_booking(self) -> None:
        try:
            sleep(3)
            self.chrome.execute_script("goClubs('1')")
        except Exception as error:
            print(error)
            self.goto_make_a_booking()

    def get_date_of_picker(self, picker: int) -> dict:
        sleep(1)
        if date := self.chrome.find_element_by_xpath(f"//a[@id='picker_{picker}']").text:
            date = date.split('\n')
            result = {'day': date[0], 'date': date[1], 'month': date[2]}
            return result
        else:
            self.get_date_of_picker(picker=picker)

    def has_available_booking(self):
        slots = self.chrome.find_elements_by_class_name('slot')
        for slot in slots:
            button = slot.find_elements_by_class_name('timeelement')[-1]
            time = slot.find_elements_by_class_name('timeelement')[0].text.split(' ')[0]
            name = slot.find_elements_by_class_name('timeelement')[1].text.lower()
            if name == self.name and time == self.time and button.text.strip().lower() == 'book now':
                return button

    def book_for_class(self, booking_btn):
        href = booking_btn.find_element_by_tag_name('a').get_attribute('href')
        href = href.split(':')[-1]
        self.chrome.execute_script(href)
        self.chrome.implicitly_wait(10)
        self.chrome.execute_script('confirmBooking()')
        self.chrome.implicitly_wait(10)
        self.chrome.execute_script('getBookings(2)')
        self.chrome.implicitly_wait(10)

    def find_available_bookings(self):
        for i in range(0, 8):
            self.chrome.execute_script(f"selectDate({i})")
            date = self.get_date_of_picker(i)
            if date['day'] in self.days:
                if self.has_available_booking():
                    if booking_btn := self.has_available_booking():
                        self.book_for_class(booking_btn=booking_btn)

    def process_booking(self):
        self.chrome.get(self.url)
        self.login()
        self.goto_make_a_booking()
        self.find_available_bookings()
        self.chrome.quit()


if __name__ == '__main__':
    va = VirginActive()
    va.process_booking()
