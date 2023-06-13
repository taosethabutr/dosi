import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed

# Set the dimensions of the screenshot
width = 1250
height = 350

# Set the URL of the website you want to capture
url = "https://stack3reth.github.io/dosi-land/"

# Set the Discord webhook URL
# webhook_url = "https://discord.com/api/webhooks/1118077000846946326/S7erj7Nan8Zoe_ICGw8BuMcrA69vQnpoXciM_Tql8XKApQnZ494uLPr-A6mud2FCaDgI" # for testing

webhook_url = "https://discord.com/api/webhooks/1115884800914509864/psxWHTjiuAxNRV_ByIeWyDIB3Xfhp5oLL6xuAa_JQXvIjD2xga2KFyNK2dGIh5ByUuml"

# Configure Chrome options for the webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without a GUI)

# Initialize the webdriver
driver = webdriver.Chrome(options=chrome_options)

# Set the window size to the desired dimensions
driver.set_window_size(width, height)

# Navigate to the URL
driver.get(url)
driver.execute_script("document.body.style.overflow = 'hidden';")

# Wait for the page to load (increase the sleep time if needed)
time.sleep(5)

# Capture the screenshot
screenshot_path = "screenshot.png"
driver.save_screenshot(screenshot_path)

# Quit the webdriver
driver.quit()

# Send the screenshot to the Discord webhook
webhook = DiscordWebhook(url=webhook_url)

snapshot_time = (datetime.now()-timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')+" (UTC+0)"

webhook.content = "## :cityscape: Land Snapshot :cityscape:\n`Data as of "+snapshot_time+"`\n**This message is auto generated every 4hr on Monday during Land participation period.  If you have any question please contact <@701502808079204375> for more details.*"

with open(screenshot_path, "rb") as file:
    webhook.add_file(file.read(), filename='screenshot.png')

response = webhook.execute()

os.remove(screenshot_path)