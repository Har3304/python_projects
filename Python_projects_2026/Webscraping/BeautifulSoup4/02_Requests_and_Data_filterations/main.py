from bs4 import BeautifulSoup
import requests
import urllib3
import pandas as pd



#Find a job That includes python and css implementation
dictionary={'Job':[],
            'Owner(s)':[],
            'Location':[],
            'Posted On':[],
            'Compatible':[]}
df=pd.DataFrame(dictionary)
print(df)

urllib3.disable_warnings()

url = "https://realpython.github.io/fake-jobs/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

response = requests.get(url, headers=headers, verify=False)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "lxml")
cards=soup.find_all('div', class_='card')
ref=[]
counter=0
decision=''
for c in cards:
    if 'Python' in c.text:
        data=[]
        targets=(c.text.split('\n'))
        for el in targets:
            if el.strip():
                data.append(el.strip())
        links=c.find_all('a')
        print(links)
        for l in links:    
            if 'Apply' in str(l):  
                counter+=1                        
                r=requests.get((str(l).split(' ')[2])[6:-1])
                cont=BeautifulSoup((r).text, 'lxml').find('div', class_='content').text
                cont=str(cont)
                if 'css' in cont or 'CSS' in cont or 'Css' in cont:                
                    print(counter, "Yes")
                    decision='Yes'
                else:
                    print(counter,'No')
                    decision='No'
        df.loc[len(df)]=[data[0], data[1], data[2], data[3], decision]

print(df)





# role=[]
# counter=0
# for r in ref:
#     counter+=1
#     cont=BeautifulSoup(requests.get(r).text, 'lxml').find('div', class_='content').text
#     cont=str(cont)
#     if 'css' in cont or 'CSS' in cont or 'Css' in cont:
#         df.loc[ref.index(r), 'Compatible']='Yes'
#         print(counter, "Yes")
#     print(counter,'No')
