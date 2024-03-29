import sys
import requests
import imaplib
import email
from email.header import decode_header
import webbrowser
import threading
from os.path import expanduser
import concurrent.futures
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
import concurrent.futures
from datetime import datetime
import time,string,zipfile,os
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from threading import Thread
import threading
import base64
from PIL import Image
import cv2
import platform  # Imported platform module

def press_key(key, driver):
    actions = ActionChains(driver)
    actions.send_keys(key)
    actions.perform()

def randkeys(element, keys, driver):
    for myi in keys:
        element.send_keys(myi)
        time.sleep(random.uniform(0.05, 0.25))

def create_proxyauth_extension(proxy_host, proxy_port,proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    if plugin_path is None:
        file='./chrome_proxy_helper'
        if not os.path.exists(file):
            os.mkdir(file)
        plugin_path = file+'/%s_%s@%s_%s.zip'%(proxy_username,proxy_password,proxy_host,proxy_port)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def initdriver(proxy):
    proxy = "proxy"
    print(proxy)
    chrome_options = webdriver.ChromeOptions()

    therand = random.randint(0,3)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host=str(str(proxy.split(":")[0]).strip().replace("\n","").replace("\r","")),
    proxy_port=str(str(proxy.split(":")[1]).strip().replace("\n","").replace("\r","")),
    proxy_username=str('user'),
    proxy_password='passw',
    scheme='http'
    )
    chrome_options.add_extension(proxyauth_plugin_path)

    # Detect operating system and set chromedriver path accordingly
    operating_system = platform.system()
    if operating_system == "Linux":
        chromedriver_path = './chromedriver'
    else:
        chromedriver_path = 'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.delete_all_cookies()
    return driver

# The rest of the code remains unchanged...