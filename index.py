from datetime import datetime
import requests
import pandas as pd

url = "https://osome-public.p.rapidapi.com/counts"

query = input("Enter hashtags to search, separated by commas (include the #)\n")
startdate = input("Enter date to search from (YYYY-MM-DD)\n")
enddate = input("Enter date to search until (YYYY-MM-DD)\n")
print("Loading...")

querystring = {"start":f"{startdate} 00:00:00","end":f"{enddate} 00:00:00","q": query}

headers = {
	"X-RapidAPI-Key": "4aa4b81ef0msh203c4fb3acdd875p1bc1e0jsn8f3f35ab1633",
	"X-RapidAPI-Host": "osome-public.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

result_url = response.json()['result_url']

response2 = requests.request("GET", result_url)

list = response2.text.splitlines()

df = pd.DataFrame(columns=['hashtag', 'count'])

dataindex = 0

for i in list:
	tag = i.split('\t')[0]
	count = i.split('\t')[1]

	df2 = pd.DataFrame([[tag, count]], columns=['hashtag', 'count'], index=[dataindex])
	dataindex = dataindex + 1
	df = pd.concat([df, df2])

today = datetime.today().replace(microsecond=0)
filename = f"{today.strftime('%Y-%m-%d %H-%M-%S')} range {startdate} to {enddate}.xlsx"
df.to_excel(f"excel files\{filename}")
print("Written to excel file")
