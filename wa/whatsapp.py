# SWAMI KARUPPASWAMI THUNNAI

# ============================================================
# Simple yet Hackable! WhatsApp API [UNOFFICIAL] for Python3
# Note: The author gives permission to use it under Apache 2.0
# Special Thanks To: alecxe, For reviewing my code!
# ============================================================

import time
import os
import datetime as dt
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Beautiful Soup Library is reqired to make this library work(For getting participants list for the specified group).\npip3 install beautifulsoup4")


class WhatsApp:
    """
    This class is used to interact with your whatsapp [UNOFFICIAL API]
    """
    timeout = 10  # The timeout is set for about ten seconds

    def __init__(self, wait, pathToDriver, screenshot=None, session=None):
        chrome_options = Options()
        if session:
            chrome_options.add_argument("--user-data-dir={}".format(session))
            self.browser = webdriver.Chrome(pathToDriver, options=chrome_options)  # we are using chrome as our webbrowser
        else:
            self.browser = webdriver.Chrome(pathToDriver)

        self.browser.get("https://web.whatsapp.com/")
        self.browser.get("https://web.whatsapp.com/")

        time.sleep(wait)

        # element locators
        self.search_selector = '#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text'
        self.SendBox_XPATH = "/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div/div[2]"
        self.ParticipantCount_SELECTOR = "#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._3bvta > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(5) > div._10vh8 > div > div > div._25m4C._3weqn > span"
        self.Chat_Info_SELECTOR = "#main > header > div._2YnE3"
        self.Scrollbar_SELECTOR = "#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._3bvta > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div"
        self.Msg_SELECTOR = "span.i0jNr.selectable-text.copyable-text"
        self.MsgInfoOuterDiv_CLASS = "_22Msk"
        self.UserMsgInfo_CLASS = "_2jGOb"

    def isWindowOpen(self):
        """
        Check if the selenium window is open
        """
        try:
            _ = self.browser.window_handles
            return True
        except:
            return False



    # This method is used to send the message to the individual person or a group
    # will return true if the message has been sent, false else
    def send_message(self, name, message):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, self.SendBox_XPATH)))
            messages = message.split("\n")
            for msg in messages:
                send_msg.send_keys(msg)
                send_msg.send_keys(Keys.SHIFT+Keys.ENTER)
            time.sleep(0.3)
            send_msg.send_keys(Keys.ENTER)
            return True
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException:
            return False
        except Exception:
            return False

    # This method will count the no of participants for the group name provided
    def get_participants_count(self, group_name):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(group_name+Keys.ENTER)

        # we will send the name to the input key box
        # some say this two try catch below can be grouped into one
        # but I have some version specific issues with chrome [Other element would receive a click]
        # in older versions. So I have handled it spereately since it clicks and throws the exception
        # it is handled safely
        try:
            click_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.Chat_Info_SELECTOR)))
            click_menu.click()
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException as e:
            return "None"
        except Exception as e:
            return "None"

        current_time = dt.datetime.now()
        
        while True:
            try:
                participants_count = self.browser.find_element_by_css_selector(self.ParticipantCount_SELECTOR).text
                if "participants" in participants_count:
                    participants_count = int(participants_count.replace(' participants', ''))
                    ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                    return participants_count
            except Exception as e:
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

            elapsed_time = (dt.datetime.now() - current_time).seconds
            if elapsed_time > self.timeout:
                return "NONE"

    # This method is used to get all the participants
    def get_group_participants(self, group_name):
        count = self.get_participants_count(group_name)
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(group_name+Keys.ENTER)
        # we will send the name to the input key box
        # some say this two try catch below can be grouped into one
        # but I have some version specific issues with chrome [Other element would receive a click]
        # in older versions. So I have handled it spereately since it clicks and throws the exception
        # it is handled safely
        try:
            click_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.Chat_Info_SELECTOR)))
            click_menu.click()
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException as e:
            return "None"
        except Exception as e:
            return "None"

        participants = []
        scrollbar = self.browser.find_element_by_css_selector(self.Scrollbar_SELECTOR)
        for v in range(1, 3):
            self.browser.execute_script('arguments[0].scrollTop = ' + str(v*400), scrollbar)
            time.sleep(0.10)
            elements = self.browser.find_elements_by_tag_name("span")
            for element in elements:
                try:
                    html = element.get_attribute('innerHTML')
                    soup = BeautifulSoup(html, "html.parser")
                    for i in soup.find_all("span", class_="FqYAR"):
                        if len(participants) != int(count):
                            if i.text not in participants and i.text != 'You':
                                participants.append(i.text)
                        else:
                            return participants

                except Exception as e:
                    pass


    # This method does not care about anything, it sends message to the currently active chat
    # you can use this method to recursively send the messages to the same person
    def send_blind_message(self, message):
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, self.SendBox_XPATH)))
            messages = message.split("\n")
            for msg in messages:
                send_msg.send_keys(msg)
                send_msg.send_keys(Keys.SHIFT+Keys.ENTER)
            send_msg.send_keys(Keys.ENTER)
            return True
        except NoSuchElementException:
            return "Unable to Locate the element"
        except Exception as e:
            print(e)
            return False

    # This method will send you the picture
    def send_picture(self, name, picture_location, caption=None):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        try:
            attach_xpath = '//*[@id="main"]/header/div[3]/div/div[2]/div'
            send_file_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span'
            attach_type_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input'
            # open attach menu
            attach_btn = self.browser.find_element_by_xpath(attach_xpath)
            attach_btn.click()

            # Find attach file btn and send screenshot path to input
            time.sleep(1)
            attach_img_btn = self.browser.find_element_by_xpath(attach_type_xpath)

            # TODO - might need to click on transportation mode if url doesn't work
            attach_img_btn.send_keys(picture_location)           # get current script path + img_path
            time.sleep(1)
            if caption:
                caption_xpath = "/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/span/div/div[2]/div/div[3]/div[1]/div[2]"
                send_caption = self.browser.find_element_by_xpath(caption_xpath)
                send_caption.send_keys(caption)
            send_btn = self.browser.find_element_by_xpath(send_file_xpath)
            send_btn.click()

        except (NoSuchElementException, ElementNotVisibleException) as e:
            print(str(e))

    # For sending documents
    def send_document(self, name, document_location):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(name+Keys.ENTER)  # we will send the name to the input key box
        try:
            attach_xpath = '//*[@id="main"]/header/div[3]/div/div[2]/div'
            send_file_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span'
            attach_type_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input'
            # open attach menu
            attach_btn = self.browser.find_element_by_xpath(attach_xpath)
            attach_btn.click()

            # Find attach file btn and send screenshot path to input
            time.sleep(1)
            attach_img_btn = self.browser.find_element_by_xpath(attach_type_xpath)

            # TODO - might need to click on transportation mode if url doesn't work
            attach_img_btn.send_keys(document_location)           # get current script path + img_path
            time.sleep(1)
            send_btn = self.browser.find_element_by_xpath(send_file_xpath)
            send_btn.click()

        except (NoSuchElementException, ElementNotVisibleException) as e:
            print(str(e))


    # Clear the chat
    def clear_chat(self, name):
        self.browser.find_element_by_css_selector("._3FRCZ").send_keys(name+Keys.ENTER)
        menu_xpath = "/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[3]/div/span"
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, menu_xpath)))
        menu = self.browser.find_element_by_xpath(menu_xpath)
        menu.click()
        chains = ActionChains(self.browser)
        for i in range(4):
            chains.send_keys(Keys.ARROW_DOWN)
        chains.send_keys(Keys.ENTER)
        chains.perform()
        clear_xpath = '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div[2]'
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, clear_xpath)))
        self.browser.find_element_by_xpath(clear_xpath).click()


    # This method is used to get an invite link for a particular group
    def get_invite_link_for_group(self, groupname):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(groupname+Keys.ENTER)
        self.browser.find_element_by_css_selector("#main > header > div._5SiUq > div._16vzP > div > span").click()
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div > div > div:nth-child(5) > div:nth-child(3) > div._3j7s9 > div > div")))
            invite_link = self.browser.find_element_by_css_selector("#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div > div > div:nth-child(5) > div:nth-child(3) > div._3j7s9 > div > div")
            invite_link.click()
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                    (By.ID, "group-invite-link-anchor")))
            link = self.browser.find_element_by_id("group-invite-link-anchor")
            return link.text
        except:
            print("Cannot get the link")


    # This method is used to exit a group
    def exit_group(self, group_name):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(group_name+Keys.ENTER)
        self.browser.find_element_by_css_selector("._2zCDG > span:nth-child(1)").click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1CRb5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")))
        time.sleep(3)
        _exit = self.browser.find_element_by_css_selector("div._1CRb5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")
        _exit.click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1WZqU:nth-child(2)")))
        confirm_exit = self.browser.find_element_by_css_selector("div._1WZqU:nth-child(2)")
        confirm_exit.click()

    # Get the driver object
    def get_driver(self):
        return self.browser

    # Get last messages
    def get_last_message_for(self, name):
        messages = list()
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(name+Keys.ENTER)
        time.sleep(3)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-in"):
            message = i.find("span", class_="selectable-text")
            if message:
                message2 = message.find("span")
                if message2:
                  messages.append(message2.text)
        messages = list(filter(None, messages))
        return messages

    def get_all_message_blind(self):
        try:
            msgs = self.browser.find_elements_by_css_selector(self.Msg_SELECTOR)
            msgs_info = self.browser.find_elements_by_class_name(self.MsgInfoOuterDiv_CLASS)
            for idx, div in enumerate(msgs_info.copy()):
                try:
                    info = div.find_element_by_class_name(self.UserMsgInfo_CLASS).get_attribute('data-pre-plain-text')  # get div with msg info if the msg is sent by someone other than the bot
                except NoSuchElementException:
                    info = div.find_element_by_tag_name('div').get_attribute('data-pre-plain-text')

                info = info.encode('utf-8').decode('ascii', errors='ignore') # remove unwanted unicode characters that cant be 
                                                                             # converted to ascii 
                contact_name = info.split(']')[1][1:-2] # get contact name from msg info
                msgs_info[idx] = contact_name

            msg = [message.text for message in msgs]

            return msg, msgs_info

        except:
            return None, None

    def goto_contact(self, contact):
        search = self.browser.find_element_by_css_selector(self.search_selector)
        search.send_keys(contact+Keys.ENTER)
        time.sleep(2)

    # This method is used to quit the browser
    def quit_browser(self):
        self.browser.quit()

