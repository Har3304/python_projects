import requests
import selenium
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd

dictionary={'image':[],
        'Company':[],
        'Model':[],
        'RAM':[],
        'ROM':[],
        'Expandable':[],
        'Display_cm':[],
        'Front_Camera_MP':[],
        'Rear_Camera_MP':[],
        'Battery_mAh':[],
        'Processor':[],
        'Warranty':[],
        'Rating':[],
        'Number_of_ratings':[],
        'Reviews':[],
        'Price_rs':[]}
df=pd.DataFrame(dictionary)

counter=0
for x in range(4, 10):    
    base_url=f"https://www.flipkart.com/search?q=phones+under+10000&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=phones+under+10000%7CMobiles&requestId=988f47e3-5495-42de-939b-18553347416a&as-searchtext=phones&page={x}"
    print(f"Page - {x}")
    response = requests.get(base_url)

    soup = BeautifulSoup(response.content, 'lxml').prettify()

    with open('example.html', 'w', encoding='utf-8') as f:
        f.write(soup)

    with open('example.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'lxml')

    cards=soup.find_all('div', class_='jIjQ8S')    
    card_no=1
    for c in cards:
        dictionary={'image':[0],
            'Company':[],
            'Model':[],
            'RAM':[],
            'ROM':[],
            'Expandable':[],
            'Display_cm':[],
            'Front_Camera_MP':[],
            'Rear_Camera_MP':[],
            'Battery_mAh':[],
            'Processor':[],
            'Warranty':[],
            'Rating':[],
            'Number_of_ratings':[],
            'Reviews':[],
            'Price_rs':[]}
        img_link = BeautifulSoup(c.prettify(), 'lxml').find('img', class_='UCc1lI')            
        content = requests.get(img_link['src'][:-5], stream=True)    
        with open(f'{counter}.jpg', 'wb') as f:        
            for chunk in content.iter_content(chunk_size=8192): # Iterate over chunks of data
                    f.write(chunk)    
        model=str(BeautifulSoup(c.prettify(), 'lxml').find('div', class_='RG5Slk').text).strip()    
        company=str(model).split(' ')[0]
        dictionary['Company'].append(company)
        dictionary['Model'].append(model)
        details=BeautifulSoup(c.prettify(), 'lxml').find('ul', class_='HwRTzP')

        lines = BeautifulSoup(details.prettify(), 'lxml').find_all('li', class_='DTBslk')
        
        for l in lines:                
            if 'Year' in str(l) or 'Month' in str(l):
                dictionary['Warranty'].append(l.get_text().strip())
            if 'rocessor'in str(l):        
                dictionary['Processor'].append(l.get_text().strip())
            if 'Battery' in str(l):
                dictionary['Battery_mAh'].append(int((l.get_text().strip().split(' '))[0]))
            if 'cm' in str(l):
                dictionary['Display_cm'].append(float(l.get_text().strip().split('cm')[0].strip()))
            if 'Camera' in str(l):
                if '|' in str(l):
                    dictionary['Rear_Camera_MP']=int(((str(l.get_text()).split('|')[0]).split('MP'))[0].strip())
                    dictionary['Front_Camera_MP']=int(((str(l.get_text()).split('|')[1]).split('MP'))[0].strip())
                else:
                    dictionary['Rear_Camera_MP'].append(str(l.get_text()).split('MP')[0].strip())
            if 'RAM' in str(l):
                dictionary["RAM"].append(int((((l.get_text().strip()).split(' | '))[0].split(" "))[0]))
                dictionary["ROM"].append(int((((l.get_text().strip()).split(' | '))[1].split(" "))[0]))
                if "Exp" in str(l):
                    dictionary["Expandable"].append(int((((l.get_text().strip()).split(' | '))[2].split(" "))[-2]))
        #Rating
        rate = BeautifulSoup(c.prettify(), 'lxml').find('div', class_='MKiFS6').text
        dictionary['Rating'].append(float(str(rate).strip()))
        rating_details = BeautifulSoup(c.prettify(), 'lxml').find_all('span', class_='PvbNMB')
        
        num_rat = rating_details[0].get_text().strip().split(' ')[0]
        num_rev = rating_details[0].get_text().strip().split(' ')[-2]
        if ',' in str(num_rat):
            dictionary['Number_of_ratings'].append(int(str(num_rat).replace(',', '')))
        else:
            dictionary['Number_of_ratings'].append(int(str(num_rat)))
        if ',' in str(num_rev):
            dictionary['Reviews'].append(int(str(num_rev).replace(',', ''))    )
        else:
            dictionary['Reviews'].append(int(str(num_rev)))

        #Price
        price = BeautifulSoup(c.prettify(), 'lxml').find('div', class_='hZ3P6w DeU9vF').get_text()
        dictionary['Price_rs'].append(int(str(price).split()[0][1:].replace(',', '')))
        for key in dictionary.keys():
            if not dictionary[f'{key}']:
                dictionary[key].append('_')        
        df=pd.concat([df, pd.DataFrame(dictionary)], ignore_index=True)
        counter+=1
        print("Card_no:", card_no)
        card_no+=1
        df.to_csv('example.csv')