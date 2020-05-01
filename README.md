# Selenium Chrome WebDriver With Proxy Authorization

## Project Details

Proxy authentication on 'headless' Selenium Chrome browser.

Private proxies with username:password:ip:port

Since extensions on Selenium Chrome WebDriver are not working with its headless mode, the alternative is to take advantage of a virtual display when running the browser.  

NordVPN HTTP/HTTPS proxies have worked successfully using this script.  

## How-to

Add proxy credentials in `settings.py`.  

(Debian or Debian-based OS)  
Open the terminal, and run the command below.

```shell
sudo apt install -y xvfb
```

Clone this project.

```shell
git clone https://github.com/0xboz/selenium_chrome_proxy_authorization.git
cd selenium_chrome_proxy_authorization
```

Create an virtual environment for this project.

```shell
python3 -m venv venv
```

Activate venv and install all required packages.

```shell
source venv/bin/activate
(venv) pip install -r requirements.txt
```

Run the script.

```shell
(venv) python main.py
```
