from bs4 import BeautifulSoup

import requests
url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find_all('table')[1]
titles = table.find_all('th')
clean_titles =[title.text.strip() for title in titles]

import pandas as pd
column_data = table.find_all('tr')
df = pd.DataFrame(columns = clean_titles)   
for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    length = len(df)
    df.loc[length] = individual_row_data
df.to_csv(r'/Users/brsbold/Documents/And Global Intern/Companies.csv', index=False)



