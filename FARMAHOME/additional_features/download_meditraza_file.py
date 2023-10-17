###################
#     IMPORTS     #
###################
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import listdir, getlogin, path, makedirs, getenv
from datetime import datetime
from time import sleep
from shutil import move

from dotenv import load_dotenv

load_dotenv('../.env')

###################
#    FUNCTIONS    #
###################

class Browser:
    def __init__(self) -> None:
        '''Constructor of the Browser class.'''

        self.url = getenv('meditraza_url')
        self.today = datetime.now()
        self.downloads_folder = path.join(path.expanduser("~"), 'Downloads')
        self.destination_folder = f'C:\\Users\\{getlogin()}\\Downloads\\borrar'
        self.file_name = f'MEDITRAZA_{self.today.year}_{self.today.month}_{self.today.day}.xls'

    def initialize_driver(self) -> None:
        '''Initialize the webdriver.'''

        # With Google Chrome (it is necessary to have installed in the same folder the chromedriver.exe).
        # If chromedriver.exe is in a different folder, it is necessary to specify the path.
        self.driver = webdriver.Chrome()

    def go_to_url(self) -> None:
        '''Go to the URL.'''

        self.driver.get(self.url)

    def user_is_not_logged(self) -> bool:
        '''Check if the user is logged.'''

        try:
            self.driver.find_element(By.ID, "id_username")
            return True
        except:
            return False

    def login(self) -> None:
        '''Login with the user and password.'''

        # Fill user and password
        self.driver.find_element(By.ID, "id_username").send_keys(getenv('meditraza_user'))
        self.driver.find_element(By.ID, "id_password").send_keys(getenv('meditraza_password'))

        # Click login button
        self.driver.find_element('xpath', '//button[text()="Login"]').click()

    def check_if_the_file_has_not_been_downloaded(self) -> bool:
        '''Check if the file has already been downloaded.'''

        if self.file_name in listdir(self.downloads_folder):
            self.close_driver()
            raise FileExistsError(f'The file {self.file_name} has already been downloaded and exists in the directory.')
        else:
            return True

    def download_excel(self, export_url:str='exportar_excel') -> None:
        '''Click on the button to export the excel.'''

        self.driver.get(f'{self.url}{export_url}/{self.today.day}-{self.today.month}-{self.today.year}')
        browser.close_driver()

    def wait(self, total_seconds_to_wait:int=20) -> None:
        seconds = 0
        continue_waiting = True
        while continue_waiting and seconds < total_seconds_to_wait:
            sleep(1)
            if self.file_name in listdir(self.downloads_folder): continue_waiting = False
            seconds += 1

        if seconds == total_seconds_to_wait:
            raise TimeoutError('The file has not been downloaded.')

    def close_driver(self) -> None:
        '''Close the webdriver.'''

        self.wait()
        self.driver.quit()

###################
#       MAIN      #
###################

if __name__ == '__main__':
    browser = Browser() # Create the browser object.

    browser.initialize_driver() # Initialize the webdriver.

    browser.go_to_url() # Open the URL.

    if browser.user_is_not_logged(): # Check if the user is logged.
        browser.login()

    if browser.check_if_the_file_has_not_been_downloaded():
        browser.download_excel() # Download the excel file.

    if not path.exists(browser.destination_folder): # Check if the destination folder exists.
        makedirs(browser.destination_folder) # If not, create it.
        
    move(src=path.join(browser.downloads_folder, browser.file_name),
         dst=path.join(browser.destination_folder, browser.file_name)) # Move the file to the destination folder.