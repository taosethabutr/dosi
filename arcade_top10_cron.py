import requests
import pandas as pd
from datetime import datetime
from github import Github

####################################################################
def github_write(repo_name, file_path, file_content, access_token):
    # Connect to the GitHub repository using an access token
    g = Github(access_token)
    repo = g.get_user().get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        sha = file.sha

        # Update the file in the repository
        repo.update_file(file_path, "Updating HTML file", file_content, sha, branch="main")
        print("HTML file created/updated successfully in the GitHub repository.")
    except Exception as e:
        print(f"Error occurred while creating/updating the HTML file: {str(e)}")
####################################################################
def create_html_file(data, time):
    html1 = '''
    <!DOCTYPE html>
<html>
<head>
  <title>DOSI Arcade Top 10</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;900&display=swap" rel="stylesheet">
  <style>
    h1, p {
        margin: 5px 0px 10px 0px;
    }

    html {
        font-family: 'Roboto', sans-serif;
    }

    table {
      border-collapse: collapse;
      width: 1000px;
    }

    th, td {
      padding: 2px;
      text-align: left;
    }

    th {
      background-color: #f2f2f2;
      font-size: 24px;
      text-align: center;
      padding: 5 0 5 0;
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

    td:nth-child(5), td:nth-child(9), td:nth-child(13) {
            text-align: right;
    }

    td:nth-child(1){
            border-left: 1px dashed #f2f2f2;
    }

    td:nth-child(1), td:nth-child(6), td:nth-child(10), td:nth-child(14) {
            border-right: 1px dashed #f2f2f2;
    }

    td:nth-child(1){
            text-align: center;
    }
  </style>
</head>
<body>
<h1>DOSI Arcade Top 10</h1>
<p>Data snapshot at '''+time+'''</p>
  <table id="dosi-top10">
    <tr>
        <th rowspan="1">Rank</th>
        <th colspan="1"></th>
        <th colspan="3">Rainbow Blast</th>
        <th colspan="1"></th>
        <th colspan="3">Penguin Dash</th>
        <th colspan="1"></th>
        <th colspan="3">Hexa Cube</th>
        <th colspan="1"></th>
      </tr>
      '''
    
    html2=''
    for index, row in data.iterrows():
        html2 = html2+'''
            <tr>
                <td>'''+str(row['rank'])+'''</td>
                <td>&nbsp;&nbsp;</td>
                <td><img src="'''+row['p1']+'''"></td>
                <td>'''+row['n1']+'''</td>
                <td>'''+format_number(row['s1'])+'''</td>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                <td><img src="'''+row['p2']+'''"></td>
                <td>'''+row['n2']+'''</td>
                <td>'''+format_number(row['s2'])+'''</td>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                <td><img src="'''+row['p3']+'''"></td>
                <td>'''+row['n3']+'''</td>
                <td>'''+format_number(row['s3'])+'''</td>
                <td>&nbsp;&nbsp;</td>
            </tr>
        '''
  
    html3 = '''</table>
    </body>
    </html>
    '''
    repository_name = 'dosi-arcade'
    file_path = 'index.html'
    file_content = html1+html2+html3
    github_access_token = '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'
    github_write(repository_name, file_path, file_content, github_access_token)

####################################################################
def fetch_data(url, headers=None, timestamp=None):
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Error:", response.status_code)
        return None

def format_number(value):
    if pd.notnull(value) and isinstance(value, (int, float)):
        return '{:,.0f}'.format(value)
    return value

def line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer pT1euenXWTM7xS5Os2EqhnumXmYwtF1tpJHivQKGdzr'}
    payload = {'message': message}
    r = requests.post(url, headers=headers, data=payload)
    return message

####################################################################
def main():
    snapshot_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" (UTC+7)"
    url_rainbow = "https://citizen.dosi.world/api/citizen/v1/arcade/rainbowblast/ranking"
    url_penguin = "https://citizen.dosi.world/api/citizen/v1/arcade/penguindash/ranking"
    url_hexa = "https://citizen.dosi.world/api/citizen/v1/arcade/hexacube/ranking"

    result = fetch_data(url_rainbow).get('rankList')
    selected_columns = ['rank', 'pictureUrl', 'displayName', 'score']
    rainbow = [{col: row[col] for col in selected_columns} for row in result]
    rainbow = pd.DataFrame(rainbow)

    result = fetch_data(url_penguin).get('rankList')
    selected_columns = ['pictureUrl', 'displayName', 'score']
    penguin = [{col: row[col] for col in selected_columns} for row in result]
    penguin = pd.DataFrame(penguin)

    result = fetch_data(url_hexa).get('rankList')
    selected_columns = ['pictureUrl', 'displayName', 'score']
    hexa = [{col: row[col] for col in selected_columns} for row in result]
    hexa = pd.DataFrame(hexa)

    message = "Top 10 Arcade Snapshot\n 🕖"+ snapshot_time

    message = message+"\n\n🌈 Rainbow Blast\n"
    for i, r in rainbow.iterrows():
        m = r['displayName']+" ("+str(format_number(r['score']))+")\n"
        message = message+m
    
    message = message+"\n🐧 Penguin Dash\n"
    for i, r in penguin.iterrows():
        m = r['displayName']+" ("+str(format_number(r['score']))+")\n"
        message = message+m
        
    message = message+"\n💎 Hexa Cube\n"
    for i, r in hexa.iterrows():
        m = r['displayName']+" ("+str(format_number(r['score']))+")\n"
        message = message+m
        
    message = message+"\n https://stack3reth.github.io/dosi-arcade/"
    print(line_notify(message))

    
    new_column_names = {'pictureUrl': 'p1', 'displayName': 'n1', 'score': 's1'}
    rainbow = rainbow.rename(columns=new_column_names)
    new_column_names = {'pictureUrl': 'p2', 'displayName': 'n2', 'score': 's2'}
    penguin = penguin.rename(columns=new_column_names)
    new_column_names = {'pictureUrl': 'p3', 'displayName': 'n3', 'score': 's3'}
    hexa = hexa.rename(columns=new_column_names)

    combined_df = pd.concat([rainbow, penguin, hexa], axis=1).fillna("")
    
    create_html_file(combined_df, snapshot_time)

####################################################################
if __name__ == "__main__":
    main()