import requests
import time
import pandas as pd
from datetime import datetime
from discord_webhook import DiscordWebhook
import base64
####################################################################
def format_number(value):
    if pd.notnull(value) and isinstance(value, (int, float)):
        return '{:,.0f}'.format(value)
    return str(value)
####################################################################
def line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer pT1euenXWTM7xS5Os2EqhnumXmYwtF1tpJHivQKGdzr'}
    payload = {'message': message}
    r = requests.post(url, headers=headers, data=payload)
    return message
####################################################################
def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string
####################################################################
def create_image(html, css):
    HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    HCTI_API_USER_ID = '447fd9a7-6d04-466f-b1ef-9278acfdbdae'
    HCTI_API_KEY = '0afdbc5f-29a4-4d76-bc35-832094fab555'

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
    webhook.add_file(file=image_data, filename='land_snapshot.png')

    response = webhook.execute()
####################################################################
def create_html_file(data, time, h2, h3, h4, timestamp):
    css = '''
        h1, p {
            margin: 5px 0px 10px 0px;
        }

        html {
            font-family: 'Roboto', sans-serif;
        }

        table {
        border: 1px dashed #f2f2f2;
        width: 1200px;
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
            width: 100px;
        }

        th img {
        width: 20px;
        height: 20px;
        object-fit: cover;
        }

        tr:nth-child(odd) {
            background-color: #fafafa;
        }

        td:nth-child(1){
            text-align: left;
            font-weight: bold;
        }
    '''
    html1 = '''
        <body>
        <h1><img src="https://vos.line-scdn.net/dosi-citizen-prod/citizen-web/assets/land.396cfbaec7b40fcff9c9.png"> DOSI Land Snapshot Round '''+land_round+'''</h1>
        <small>Data snapshot at '''+time+'''</small>
        <table id="dosi-land">
            <tr>
                <th><img src="data:image/png;base64,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"><br>Zone</th>
                <th><img src="https://vos.line-scdn.net/dosi-citizen-prod/citizen-web/assets/FNSA.bf79e8d72a9c5a7f082e.png"><br>FNSA<br>Reward</th>
                <th><img src="https://vos.line-scdn.net/dosi-citizen-prod/citizen-web/assets/don.85a68a002bba841d247f.png"><br>DON<br>Required</th>
                <th><img src="data:image/png;base64,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"><br>LUP<br>Required</th>
                <th><img src="data:image/png;base64,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"><br>Participants</th>
                <th><img src="https://vos.line-scdn.net/dosi-citizen-prod/citizen-web/assets/trophy.ef43898c0e91bac4f2bc.png"><br>Winners</th>
                <th><img src="data:image/png;base64,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"><br>Citizen NFTs</th>
                <th><img src="https://vos.line-scdn.net/dosi-citizen-prod/citizen-web/assets/ticket.a6bdfb53f139b7653076.png"><br>LUPs</th>
                <th><img src="data:image/png;base64,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"><br>NFT per<br>Participant</th>
                <th><img src="https://vos.line-scdn.net/dosi-citizen-prod/citizen-web/assets/ticket.a6bdfb53f139b7653076.png"><br>LUP per<br>Participant</th>
            </tr>
    '''
    
    html2=''
    for index, row in data.iterrows():
        html2 = html2+'''
            <tr>
                <td>'''+str(row['zones'])+'''</td>
                <td>'''+format_number(row['zoneRewards'])+'''</td>
                <td>'''+format_number(row['requiredDON'])+'''</td>
                <td>'''+format_number(row['requiredLUP'])+'''</td>
                <td>'''+format_number(row['participantCount'])+'''</td>
                <td>'''+format_number(row['winnerCount'])+'''</td>
                <td>'''+format_number(row['citizenNftCount'])+'''</td>
                <td>'''+format_number(row['levelUpPassCount'])+'''</td>
                <td>'''+str(round(row['nftPerParticipant'],2))+'''</td>
                <td>'''+str(round(row['lupPerParticipant'],2))+'''</td>
            </tr>
        '''
  
    html3 = '''</table>
    <p>Level 2 Participation: '''+format_number(data.loc[data['zones'].str.contains('Level 2'), 'participantCount'].sum())+'''/'''+format_number(h2)+''' ('''+str(round(data.loc[data['zones'].str.contains('Level 2'), 'participantCount'].sum()/h2*100,2))+'''%)<br>
    Level 3 Participation: '''+format_number(data.loc[data['zones'].str.contains('Level 3'), 'participantCount'].sum())+'''/'''+format_number(h3)+''' ('''+str(round(data.loc[data['zones'].str.contains('Level 3'), 'participantCount'].sum()/h3*100,2))+'''%)<br>
    Level 4 Participation: '''+format_number(data.loc[data['zones'].str.contains('Level 4'), 'participantCount'].sum())+'''/'''+format_number(h4)+''' ('''+str(round(data.loc[data['zones'].str.contains('Level 4'), 'participantCount'].sum()/h4*100,2))+'''%)
    </p>
    '''
    html4 = '''</body>
    '''
    discord_message = "## :cityscape: Land Snapshot Round "+land_round+" :cityscape:\n`Data as of `<t:"+str(int(timestamp))+":f>` (your local time.)`\n**This message is auto generated every 4hr during Land participation period.  \nIf you have any question please contact <@701502808079204375> for more details.*"
    send_discord(discord_message, create_image(html1+html2+html3+html4,css))
####################################################################
def fetch_holders():
    url_holders = "https://explorer.blockchain.line.me/v1/finschia-2/contracts/f68e7fd5/token-types?size=30&search_from=top"
    holders = requests.get(url_holders).json().get('token_types')
    lv2_holders = 0
    lv3_holders = 0
    lv4_holders = 0
    for holder in holders:
        if holder['token_type']=='10000003':
            lv2_holders = holder['holder_count']
        elif holder['token_type']=='10000004':
            lv3_holders = holder['holder_count']
        elif holder['token_type']=='10000005':
            lv4_holders = holder['holder_count']
    return lv2_holders, lv3_holders, lv4_holders
    
####################################################################
snapshot_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" (UTC+0)"
unix_timestamp = time.time()
land_round = '11'
land1_url = "https://citizen.dosi.world/api/citizen/v1/lands/31"
land2_url = "https://citizen.dosi.world/api/citizen/v1/lands/32"
land3_url = "https://citizen.dosi.world/api/citizen/v1/lands/33"
headers = ""

zones=[]
zoneRewards=[]
requiredDON=[]
requiredLUP=[]
participantCount=[]
participantRate=[]
winnerCount=[]
citizenNftCount=[]
levelUpPassCount=[]

holders_lv2, holders_lv3, holders_lv4 = fetch_holders()

land1 = requests.get(land1_url, headers=headers).json().get('zoneList')
for l in land1:
    zones.append("Level 2 Zone "+l['zoneType'][-1:])
    zoneRewards.append(int(l['rewardAmount']))
    requiredDON.append(int(l['requiredAsset']['amount']))
    requiredLUP.append(int(l['requiredLevelUpPassCount']))
    participantCount.append(int(l['participationStatus']['participantsCount']))
    participantRate.append(round(l['participationStatus']['participantsCount']/holders_lv2*100,2))
    winnerCount.append(int(l['participationStatus']['winnerCount']))
    citizenNftCount.append(int(l['participationStatus']['citizenNftCount']))
    levelUpPassCount.append(int(l['participationStatus']['levelUpPassCount']))

land2 = requests.get(land2_url, headers=headers).json().get('zoneList')
for l in land2:
    zones.append("Level 3 Zone "+l['zoneType'][-1:])
    zoneRewards.append(int(l['rewardAmount']))
    requiredDON.append(int(l['requiredAsset']['amount']))
    requiredLUP.append(int(l['requiredLevelUpPassCount']))
    participantCount.append(int(l['participationStatus']['participantsCount']))
    participantRate.append(round(l['participationStatus']['participantsCount']/holders_lv3*100,2))
    winnerCount.append(int(l['participationStatus']['winnerCount']))
    citizenNftCount.append(int(l['participationStatus']['citizenNftCount']))
    levelUpPassCount.append(int(l['participationStatus']['levelUpPassCount']))

land3 = requests.get(land3_url, headers=headers).json().get('zoneList')
for l in land3:
    zones.append("Level 4 Zone "+l['zoneType'][-1:])
    zoneRewards.append(int(l['rewardAmount']))
    requiredDON.append(int(l['requiredAsset']['amount']))
    requiredLUP.append(int(l['requiredLevelUpPassCount']))
    participantCount.append(int(l['participationStatus']['participantsCount']))
    participantRate.append(round(l['participationStatus']['participantsCount']/holders_lv4*100,2))
    winnerCount.append(int(l['participationStatus']['winnerCount']))
    citizenNftCount.append(int(l['participationStatus']['citizenNftCount']))
    levelUpPassCount.append(int(l['participationStatus']['levelUpPassCount']))

lands = pd.DataFrame({
    'zones': zones,
    'zoneRewards': zoneRewards,
    'requiredDON': requiredDON,
    'requiredLUP': requiredLUP,
    'participantCount': participantCount,
    'participantRate': participantRate,
    'winnerCount': winnerCount,
    'citizenNftCount': citizenNftCount,
    'levelUpPassCount': levelUpPassCount
})

lands['nftPerParticipant'] = round(lands['citizenNftCount']/lands['participantCount'],2)
lands['lupPerParticipant'] = round(lands['levelUpPassCount']/lands['participantCount'],2)

print(lands)

shows_lv2 = lands.loc[lands['zones'].str.contains('Level 2'), 'participantCount'].sum()
shows_lv3 = lands.loc[lands['zones'].str.contains('Level 3'), 'participantCount'].sum()
shows_lv4 = lands.loc[lands['zones'].str.contains('Level 4'), 'participantCount'].sum()

line_message = "DOSI Land Snapshot "+snapshot_time+"\n\n"
line_message += "Show up rates:\n"
line_message += "Level 2: "+str(shows_lv2)+"/"+str(holders_lv2)+" ("+str(round(shows_lv2/holders_lv2*100,2))+"%)\n"
line_message += "Level 3: "+str(shows_lv3)+"/"+str(holders_lv3)+" ("+str(round(shows_lv3/holders_lv3*100,2))+"%)\n"
line_message += "Level 4: "+str(shows_lv4)+"/"+str(holders_lv4)+" ("+str(round(shows_lv4/holders_lv4*100,2))+"%)\n"
for index, row in lands[['zones', 'participantRate']].iterrows():
    line_message += row['zones']+": "+str(row['participantRate'])+"%\n"
line_message += "\nEstimated rewards per NFT (after tax)\n"
for index, row in lands[['zones', 'zoneRewards', 'winnerCount', 'citizenNftCount', 'levelUpPassCount', 'nftPerParticipant', 'lupPerParticipant']].iterrows():
    if (row['winnerCount']*row['nftPerParticipant'])>0:
        reward = row['zoneRewards']*0.7/(row['winnerCount']*row['nftPerParticipant'])*0.7
        line_message += row['zones']+": "+str(round(reward*0.9,4))+" - "+str(round(reward*1.1,4))+"\n"
print(line_notify(line_message))
line_message = "\nEstimated rewards per LUP (after tax)\n"
for index, row in lands[['zones', 'zoneRewards', 'winnerCount', 'citizenNftCount', 'levelUpPassCount', 'nftPerParticipant', 'lupPerParticipant']].iterrows():
    if (row['winnerCount']*row['lupPerParticipant'])>0:
        reward = row['zoneRewards']*0.3/(row['winnerCount']*row['lupPerParticipant'])*0.7
        line_message += row['zones']+": "+str(round(reward*0.9,4))+" - "+str(round(reward*1.1,4))+"\n"
line_message += "\nEstimated rewards per NFT per 21,900DON (after tax):\n"
for index, row in lands[['zones', 'zoneRewards', 'requiredDON', 'winnerCount', 'citizenNftCount', 'nftPerParticipant']].iterrows():
    if (row['winnerCount']*row['nftPerParticipant'])/row['requiredDON']*21900*0.7>0:
        line_message += row['zones']+": "+str(round(row['zoneRewards']*0.7/(row['winnerCount']*row['nftPerParticipant'])/row['requiredDON']*21900*0.7,2))+"\n"
print(line_notify(line_message))
create_html_file(lands, snapshot_time, holders_lv2, holders_lv3, holders_lv4, unix_timestamp)
