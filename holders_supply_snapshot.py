# DOSI Wallet Address - Finschia
# Stock ของที่มิ้นไว้แล้ว ยังไม่ได้แจกออก
# link1xsyfmnw8apwng5dsyuatqsr9kqpdgvcgah3gl9
# link1hlt7wpl4xut8zgds5chh9drgcmyyedkcxwlesy
# Burn กระเป๋าเก็บอ้วนที่เผาทิ้งแล้ว
# เดิม link1gzdpyyx854ftpg4h9fr36wsk8vvdqtvu5f7qvz
# ใหม่ link1hdujvs3hjfvtm0lujulrnrpaxcygut7lva2clf
# Citizen Friends Burn link1hvffqwtg82zru6fnz0kwclezz402480zkw0am5
# Marketplace อ้วนที่ตั้งขายอยู่
# link1e9r6el8f9um7xcldd6ne8hglavetuq6tgfgeym

import requests
import time
import pandas as pd
from datetime import datetime
from discord_webhook import DiscordWebhook

####################################################################
def format_number(value):
    if pd.notnull(value) and isinstance(value, (int, float)):
        return '{:,.0f}'.format(value)
    return str(value)
####################################################################
def create_image(html, css):
    HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    HCTI_API_USER_ID = '08d7cce6-946d-4cd3-8c9e-3a4c246d9df6'
    HCTI_API_KEY = '5a74a43e-ff97-479a-979c-a12abd75361b'

    data = { 'html': html,
            'css': css,
            'google_fonts': "Roboto" }

    image = requests.post(url = HCTI_API_ENDPOINT, data = data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))

    print("Your image URL is: %s"%image.json()['url'])
    image_url = image.json()['url']

    time.sleep(3)
    return image_url
####################################################################
def send_discord(message, image_url):
    # webhook_url = "https://discord.com/api/webhooks/1118077000846946326/S7erj7Nan8Zoe_ICGw8BuMcrA69vQnpoXciM_Tql8XKApQnZ494uLPr-A6mud2FCaDgI" # for testing
    webhook_url = "https://discord.com/api/webhooks/1115884800914509864/psxWHTjiuAxNRV_ByIeWyDIB3Xfhp5oLL6xuAa_JQXvIjD2xga2KFyNK2dGIh5ByUuml" # DOSI Insight
    webhook = DiscordWebhook(url=webhook_url)

    webhook.content = message
    image_data = requests.get(image_url).content
    webhook.add_file(file=image_data, filename='dosi_supply.png')

    response = webhook.execute()
####################################################################
def create_html_file(data, time):
    css = '''
        h1, p {
            margin: 5px 0px 10px 0px;
        }

        html {
            font-family: 'Roboto', sans-serif;
        }

        table {
        border: 1px dashed #f2f2f2;
        width: 800px;
        }

        th, td {
        padding: 2px;
        text-align: right;
        }

        th {
        background-color: #f2f2f2;
        font-size: 16px;
        text-align: center;
        vertical-align: top;
        padding: 5 0 5 0;
        }

        h1 img {
            width: 50px;
        }

        th img {
        width: 20px;
        height: 20px;
        object-fit: cover;
        }

        td img {
        border-radius: 50%;
        width: 30px;
        height: 30px;
        object-fit: cover;
        }

        tr:nth-child(odd) {
            background-color: #fafafa;
        }

        td:nth-child(1), td:nth-child(2){
            text-align: left;
            font-weight: bold;
        }
    '''

    html1 = '''
        <body>
        <h1><img src="https://vos.line-scdn.net/landpress-content-v2_1211/1665738596917.png"> DOSI Citizen Daily Holder & Supply Summary</h1>
        <small>Data snapshot at '''+time+'''</small>
        <table id="dosi">
            <tr>
                <th>Group</th>
                <th>Token</th>
                <th>Holders 👥</th>
                <th>Circulation 📦</th>
                <th>Burned 🔥</th>
            </tr>
    '''
    
    html2=''
    for index, row in data.iterrows():
        html2 = html2+'''
            <tr>
                <td>'''+row['Token Group']+'''</td>
                <td><img src="'''+row['Token Image']+'''"> '''+row['Token type']+'''</td>
                <td>'''+format_number(row['Holder'])+'''</td>
                <td>'''+format_number(row['circulation'])+'''</td>
                <td>'''+format_number(row['Burn'])+'''</td>
            </tr>
        '''
  
    html3 = '''</table></body></html>'''
    
    html = html1+html2+html3
    discord_message = "## DOSI Citizen Daily Holder & Supply Summary\n`Data as of "+time+"`\n**This message is auto generated from Finschia snapshot data.  If you have any question please contact <@701502808079204375> for more details.*"
    # send_discord(discord_message, create_image(html,css))

####################################################################
# fetch holders & transactions data
def fetch_holders(url, headers=None, timestamp=None):
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        holders = json_data.get('token_types')

        cleaned_holders_data = {
            'Date': [timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp, timestamp],
            'Token Group': ['Citizen Lv1', 'Citizen Lv2', 'Citizen Lv3', 'Citizen Lv4', 'Friends Cat', 'Citizen Lv1', 'Citizen Lv1', 'Citizen Lv1', 'Citizen Lv1', 'Friends Dog', 'Friends Cat', 'Citizen Lv1', 'Citizen Lv1', 'Friends Goose', 'Citizen Lv1', 'Citizen Lv1', 'Friends Chameleon', 'Citizen Lv1', 'Friends Cat', 'Friends Dog', 'Friends Goose', 'Friends Chameleon', 'Friends RoboRex'],
            'Token type': ['Citizen Lv1', 'Citizen Lv2', 'Citizen Lv3', 'Citizen Lv4', 'Kitten', 'Barranquilla', 'Citizen Favor', 'Liner Citizen', 'Hellbound', 'Puppy', 'RoboCat', 'Meta Toy Dragonz', 'Game DOSI Citizen', 'Gosling', 'Citizen Heart', 'Citizen SNKRZ', 'Pygmy', 'Citizen Pala', 'Flying Kitty', 'Flying Doggie', 'Flying Goose', 'Flying Jacksons', 'RoboRex'],
            'Token Image': ['https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000100000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000300000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000400000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000500000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000600000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000700000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000800000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000200000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000a00000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000b00000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000c00000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000d00000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000e00000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000000f00000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001000000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001100000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001300000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001400000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001500000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001600000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001700000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001800000001', 'https://lbw-impro.line-apps.com/v1/daphne/token/f68e7fd5/1000001900000001'],
            'Total Supply': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            'Stock': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            'Burn': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            'Holder': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            '7Day Transaction': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        }

        for holder in holders:
            # Level 1
            if holder['token_type']=='10000001' or holder['token_type']=='10000009' or holder['token_type']=='10000012':
                cleaned_holders_data['Total Supply'][0]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][0]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][0]+=holder['num_txs_latest']
            # Level 2
            elif holder['token_type']=='10000003':
                cleaned_holders_data['Total Supply'][1]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][1]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][1]+=holder['num_txs_latest']
            # Level 3
            elif holder['token_type']=='10000004':
                cleaned_holders_data['Total Supply'][2]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][2]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][2]+=holder['num_txs_latest']
            # Level 4
            elif holder['token_type']=='10000005':
                cleaned_holders_data['Total Supply'][3]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][3]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][3]+=holder['num_txs_latest']
            # Cat
            elif holder['token_type']=='10000006':
                cleaned_holders_data['Total Supply'][4]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][4]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][4]+=holder['num_txs_latest']
            # Barranquilla
            elif holder['token_type']=='10000007':
                cleaned_holders_data['Total Supply'][5]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][5]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][5]+=holder['num_txs_latest']
            # Favor
            elif holder['token_type']=='10000008':
                cleaned_holders_data['Total Supply'][6]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][6]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][6]+=holder['num_txs_latest']
            # Liner
            elif holder['token_type']=='10000002':
                cleaned_holders_data['Total Supply'][7]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][7]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][7]+=holder['num_txs_latest']
            # Hellbound
            elif holder['token_type']=='1000000a':
                cleaned_holders_data['Total Supply'][8]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][8]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][8]+=holder['num_txs_latest']
            # Dog
            elif holder['token_type']=='1000000b':
                cleaned_holders_data['Total Supply'][9]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][9]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][9]+=holder['num_txs_latest']
            # RoboCat
            elif holder['token_type']=='1000000c':
                cleaned_holders_data['Total Supply'][10]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][10]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][10]+=holder['num_txs_latest']
            # Meta Toy Dragonz
            elif holder['token_type']=='1000000d':
                cleaned_holders_data['Total Supply'][11]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][11]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][11]+=holder['num_txs_latest']
            # Game DOSI Citizen
            elif holder['token_type']=='1000000e':
                cleaned_holders_data['Total Supply'][12]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][12]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][12]+=holder['num_txs_latest']
            # Goose
            elif holder['token_type']=='1000000f':
                cleaned_holders_data['Total Supply'][13]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][13]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][13]+=holder['num_txs_latest']
            # Heart
            elif holder['token_type']=='10000010':
                cleaned_holders_data['Total Supply'][14]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][14]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][14]+=holder['num_txs_latest']
            # SNKRZ
            elif holder['token_type']=='10000011':
                cleaned_holders_data['Total Supply'][15]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][15]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][15]+=holder['num_txs_latest']
            # Chameleon
            elif holder['token_type']=='10000013':
                cleaned_holders_data['Total Supply'][16]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][16]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][16]+=holder['num_txs_latest']
            # Pala
            elif holder['token_type']=='10000014':
                cleaned_holders_data['Total Supply'][17]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][17]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][17]+=holder['num_txs_latest']
            # Flying Cat
            elif holder['token_type']=='10000015':
                cleaned_holders_data['Total Supply'][18]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][18]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][18]+=holder['num_txs_latest']
            # Flying Dog
            elif holder['token_type']=='10000016':
                cleaned_holders_data['Total Supply'][19]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][19]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][19]+=holder['num_txs_latest']
            # Flying Goose
            elif holder['token_type']=='10000017':
                cleaned_holders_data['Total Supply'][20]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][20]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][20]+=holder['num_txs_latest']
            # Flying Chameleon
            elif holder['token_type']=='10000018':
                cleaned_holders_data['Total Supply'][21]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][21]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][21]+=holder['num_txs_latest']
            # RoboRex
            elif holder['token_type']=='10000019':
                cleaned_holders_data['Total Supply'][22]+=int(holder['total_supply']['value'])
                cleaned_holders_data['Holder'][22]+=holder['holder_count']
                cleaned_holders_data['7Day Transaction'][22]+=holder['num_txs_latest']
        
        return cleaned_holders_data
    else:
        print("Error:", response.status_code)
        return None

####################################################################
# fetch stock
def fetch_stock(url, headers=None):
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        stock = json_data.get('holders')[0].get('amount')

        return stock
    else:
        print("Error:", response.status_code)
        return None

####################################################################
def main():
    # timestamp = time.time()
    # timestamp = datetime.now().strftime('%Y%m%d')
    timestamp = datetime.now().toordinal()-693594
    snapshot_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" (UTC+0)"

    ###########################
    url_holders = "https://explorer.blockchain.line.me/v1/finschia-2/contracts/f68e7fd5/token-types?size=30&search_from=top"

    url_stock_lv1_01 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000001/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAxIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_lv1_02 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000009/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA5In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_lv1_03 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000012/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDEyIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_lv2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000003/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAzIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_lv3 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000004/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA0In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_lv4 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000005/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA1In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_cat_01 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000006/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA2In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGx0N3dwbDR4dXQ4emdkczVjaGg5ZHJnY215eWVka2N4d2xlc3oifQ=="

    url_stock_cat_02 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000006/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA2In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_barranquilla = "" # it's 0 now
    
    url_stock_favor = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000006/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA4In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="
    
    url_stock_liner = "" # it's 0 now

    url_stock_hellbound = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000a/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBhIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_dog = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000b/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBiIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGx0N3dwbDR4dXQ4emdkczVjaGg5ZHJnY215eWVka2N4d2xlc3oifQ=="

    url_stock_robocat = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000c/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBjIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGx0N3dwbDR4dXQ4emdkczVjaGg5ZHJnY215eWVka2N4d2xlc3oifQ=="

    url_stock_mtdz = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000d/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBkIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_game = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000e/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBlIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_goose = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000f/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBmIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGx0N3dwbDR4dXQ4emdkczVjaGg5ZHJnY215eWVka2N4d2xlc3oifQ=="

    url_stock_heart = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000010/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDEwIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_snkrz = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000011/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDExIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_chameleon = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000013/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDEzIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGx0N3dwbDR4dXQ4emdkczVjaGg5ZHJnY215eWVka2N4d2xlc3oifQ=="

    url_stock_pala = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000014/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE0In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_fcat = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000015/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE1In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_fdog = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000016/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE2In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_fgoose = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000017/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE3In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_fchameleon = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000018/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE4In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxeHN5Zm1udzhhcHduZzVkc3l1YXRxc3I5a3FwZGd2Y2dhaDNnbTkifQ=="

    url_stock_roborex = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000019/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE5In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGx0N3dwbDR4dXQ4emdkczVjaGg5ZHJnY215eWVka2N4d2xlc3oifQ=="

    #######################################################################################################################################
    url_burn_lv1_01 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000001/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAxIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_lv1_01_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000001/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAxIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_lv1_02 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000009/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA5In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_lv1_02_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000009/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA5In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_lv1_03 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000012/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDEyIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_lv2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000003/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAzIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_lv2_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000003/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAzIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_lv3 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000004/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA0In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_lv3_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000004/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA0In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_lv4 = "" # there's no lv4 burn

    url_burn_cat = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000006/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA2In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaHZmZnF3dGc4MnpydTZmbnowa3djbGV6ejQwMjQ4MHprdzBhbTYifQ=="

    url_burn_barranquilla = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000007/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA3In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_barranquilla_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000007/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA3In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_favor = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000008/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA4In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_favor_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000008/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDA4In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_liner = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000002/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAyIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_liner_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000002/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDAyIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_hellbound = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000a/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBhIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_hellbound_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000a/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBhIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_dog = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000b/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBiIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaHZmZnF3dGc4MnpydTZmbnowa3djbGV6ejQwMjQ4MHprdzBhbTYifQ=="

    # url_burn_robocat = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000c/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBjIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_mtdz = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000d/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBkIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxZ3pkcHl5eDg1NGZ0cGc0aDlmcjM2d3NrOHZ2ZHF0dnU1Zjdxd2EifQ=="

    url_burn_mtdz_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000d/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBkIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_game = "" # does not exist

    url_burn_game_2 = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000e/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBlIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_goose = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/1000000f/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDBmIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaHZmZnF3dGc4MnpydTZmbnowa3djbGV6ejQwMjQ4MHprdzBhbTYifQ=="

    url_burn_heart = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000010/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDEwIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_snkrz = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000011/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDExIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    url_burn_chameleon = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000013/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDEzIn0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaHZmZnF3dGc4MnpydTZmbnowa3djbGV6ejQwMjQ4MHprdzBhbTYifQ=="

    url_burn_pala = "https://explorer.blockchain.line.me/v1/finschia-2/item-token-types/f68e7fd5/10000014/holders?size=1&upper_than=eyJ0b2tlblR5cGVJZGVudGlmaWVyVG9rZW5UeXBlSG9sZGVyRmlsdGVyIjp7ImNvbnRyYWN0SWQiOiJmNjhlN2ZkNSIsInRva2VuVHlwZSI6IjEwMDAwMDE0In0sIm9yZGVyQnkiOiJBRERSRVNTX0RFU0MiLCJhZnRlciI6ImxpbmsxaGR1anZzM2hqZnZ0bTBsdWp1bHJucnBheGN5Z3V0N2x2YTJjbGcifQ=="

    headers = {}

    print("Update started")
    holders = fetch_holders(url_holders,headers, timestamp)
    print("Holders & Total Supply Updated")

    # Update stock supply
    holders['Stock'][0]+=fetch_stock(url_stock_lv1_01,headers)+fetch_stock(url_stock_lv1_02,headers) #+fetch_stock(url_stock_lv1_03,headers)
    holders['Stock'][1]+=fetch_stock(url_stock_lv2,headers)
    holders['Stock'][2]+=fetch_stock(url_stock_lv3,headers)
    holders['Stock'][3]+=fetch_stock(url_stock_lv4,headers)
    holders['Stock'][4]+=fetch_stock(url_stock_cat_01,headers)+fetch_stock(url_stock_cat_02,headers)
    # holders['Stock'][5]+=fetch_stock(url_stock_barranquilla,headers)
    holders['Stock'][6]+=fetch_stock(url_stock_favor,headers)
    # holders['Stock'][7]+=fetch_stock(url_stock_liner,headers)
    holders['Stock'][8]+=fetch_stock(url_stock_hellbound,headers)
    holders['Stock'][9]+=fetch_stock(url_stock_dog,headers)
    holders['Stock'][10]+=fetch_stock(url_stock_robocat,headers)
    holders['Stock'][11]+=fetch_stock(url_stock_mtdz,headers)
    holders['Stock'][12]+=fetch_stock(url_stock_game,headers)
    holders['Stock'][13]+=fetch_stock(url_stock_goose,headers)
    holders['Stock'][14]+=fetch_stock(url_stock_heart,headers)
    holders['Stock'][15]+=fetch_stock(url_stock_snkrz,headers)
    holders['Stock'][16]+=fetch_stock(url_stock_chameleon,headers)
    holders['Stock'][17]+=fetch_stock(url_stock_pala,headers)
    holders['Stock'][18]+=fetch_stock(url_stock_fcat,headers)
    holders['Stock'][19]+=fetch_stock(url_stock_fdog,headers)
    holders['Stock'][20]+=fetch_stock(url_stock_fgoose,headers)
    holders['Stock'][21]+=fetch_stock(url_stock_fchameleon,headers)
    holders['Stock'][22]+=fetch_stock(url_stock_roborex,headers)
    print("Stock Supply Updated")

    # Update burn supply
    holders['Burn'][0]+=fetch_stock(url_burn_lv1_01,headers)+fetch_stock(url_burn_lv1_02,headers)+fetch_stock(url_burn_lv1_01_2,headers)+fetch_stock(url_burn_lv1_02_2,headers) #+fetch_stock(url_burn_lv1_03,headers)
    holders['Burn'][1]+=fetch_stock(url_burn_lv2,headers)+fetch_stock(url_burn_lv2_2,headers)
    holders['Burn'][2]+=fetch_stock(url_burn_lv3,headers)+fetch_stock(url_burn_lv3_2,headers)
    # holders['Burn'][3]+=fetch_stock(url_burn_lv4,headers)
    holders['Burn'][4]+=fetch_stock(url_burn_cat,headers)
    holders['Burn'][5]+=fetch_stock(url_burn_barranquilla,headers)+fetch_stock(url_burn_barranquilla_2,headers)
    holders['Burn'][6]+=fetch_stock(url_burn_favor,headers)+fetch_stock(url_burn_favor_2,headers)
    holders['Burn'][7]+=fetch_stock(url_burn_liner,headers)+fetch_stock(url_burn_liner_2,headers)
    holders['Burn'][8]+=fetch_stock(url_burn_hellbound,headers)+fetch_stock(url_burn_hellbound_2,headers)
    holders['Burn'][9]+=fetch_stock(url_burn_dog,headers)
    # holders['Burn'][10]+=fetch_stock(url_burn_robocat,headers)
    holders['Burn'][11]+=fetch_stock(url_burn_mtdz,headers)+fetch_stock(url_burn_mtdz_2,headers)
    holders['Burn'][12]+=fetch_stock(url_burn_game_2,headers)
    holders['Burn'][13]+=fetch_stock(url_burn_goose,headers)
    holders['Burn'][14]+=fetch_stock(url_burn_heart,headers)
    holders['Burn'][15]+=fetch_stock(url_burn_snkrz,headers)
    holders['Burn'][16]+=fetch_stock(url_burn_chameleon,headers)
    holders['Burn'][17]+=fetch_stock(url_burn_pala,headers)
    # holders['Burn'][18]+=fetch_stock(url_burn_fcat,headers)
    # holders['Burn'][19]+=fetch_stock(url_burn_fdog,headers)
    # holders['Burn'][20]+=fetch_stock(url_burn_fgoose,headers)
    # holders['Burn'][21]+=fetch_stock(url_burn_fchameleon,headers)
    print("Burn Supply Updated")

    
    dosi = pd.DataFrame(holders)
    dosi['circulation'] = dosi['Total Supply']-dosi['Stock']-dosi['Burn']
    dosi = dosi.sort_values(by=['Token Group', 'circulation'], ascending=[True, False]).reset_index(drop=True)
    
    print("Data update completed")
    print(dosi)
    create_html_file(dosi, snapshot_time)

    # filename = "dosi pnl.xlsx"
    # filepath = r"D:\\OneDrive\\Crypto\\DOSI\\"
    # filepath = ""
    # sheetname = 'Supply'

    # with pd.ExcelWriter(filepath+filename, mode='a', if_sheet_exists='overlay') as writer:
    #     dosi.to_excel(writer, sheet_name=sheetname, index=False, startrow=writer.sheets[sheetname].max_row, header=None)
    #     print("Saved to file to ", filepath, filename)

####################################################################
if __name__ == "__main__":
    main()
