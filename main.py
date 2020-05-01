from settings import USERNAME, PASSWORD, CHROME_WEBDRIVER

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import logging


def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """
    Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension       

    return str -> plugin_path
    """
    import string
    import zipfile

    if plugin_path is None:
        plugin_path = '/tmp/chrome_proxyauth_plugin.zip'

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


if __name__ == "__main__":

    display = Display(visible=0, size=(1920, 1080))
    display.start()

    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host="us3651.nordvpn.com",
        proxy_port=80,
        proxy_username=USERNAME,
        proxy_password=PASSWORD
    )

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_extension(proxyauth_plugin_path)
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=CHROME_WEBDRIVER)

    try:
        driver.get("http://ifconfig.me/ip")
        ip_address = driver.find_element(By.XPATH, '//html/body/pre').text
        print(ip_address)
    except NoSuchElementException as e:
        logging.error(e.__repr__())

    if display:
        display.stop()

    if driver:
        driver.quit()
