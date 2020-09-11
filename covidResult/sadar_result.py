import requests
import json
import sys
import argparse
from bs4 import BeautifulSoup


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--srf", help="srf id of the patient", dest="srf_id", action="store", required=True)
    args = parser.parse_args()
    return args


args=getArguments()
srfNo=args.srf_id

#header string picked from chrome
headerString='''
{
"Host": "sadarhospital.com",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "none",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9",
"Cookie": "ci_session=f903a63eec9f517ac1c0a77232fbb3d695f83d57"
}
'''
request_header=json.loads(headerString)

#creating session
s = requests.Session()
url='https://sadarhospital.com/'
r=s.get(url, headers=request_header)


headerString='''
{
"Host": "sadarhospital.com",
"Connection": "keep-alive",
"Content-Length": "13",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"Origin": "https://sadarhospital.com",
"Content-Type": "application/x-www-form-urlencoded",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Referer": "https://sadarhospital.com/",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9"
}
'''
request_header=json.loads(headerString)

url='https://sadarhospital.com/Covid_Report/get_report'
payload={"srf_no":srfNo}
r=s.post(url, headers=request_header, data=payload)

soup = BeautifulSoup(r.text, 'html.parser')
finalPage=soup.find('div', id='accordionExample')

result=finalPage.find('h4')
if result != None:
    print(result.text)
else:
    resultDetails=finalPage.find_all('div', class_='card-body')
    resultDetails=finalPage.find_all('div', {'class': ['card-header', 'card-body']})
    if len(resultDetails) % 2 != 0:
        print("Something went wrong")
        sys.exit(1)
    for index in range(0, len(resultDetails), 2):
        header=resultDetails[index]
        body=resultDetails[index+1]
        print("{} : {}\n".format(header.find('h2').text.strip(), body.text.strip()))
