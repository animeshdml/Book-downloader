'''
                                        This program scrapes 'Library Genesis website to fetch you books in just few clicks.
                                        Point to be noted:
                                            1. Only .pdf format is supported for now
                                            2. Number of links is not available for display at the moment.
                                            3. Titles are not completely strpped yet
                                        
'''



'''Importing libraries:
requests : Used for sending request to the server and getting the response
bs4 : Used for parsing data
urllib : Used for downloading the page data
csv : Used for writing scraped data into a csv file
pandas : Used for reading data stored in the csv file
'''
import requests,bs4,urllib,csv              
import pandas as pd
#Getting the name of the book to be searched
print('Enter book name: ',end='')
search = input()
#url of the age to be scraped
url = f'http://gen.lib.rus.ec/search.php?req={search}'

res = requests.get(url) #requests to the server and gets response
res.raise_for_status()  #raises error if request is rejected or due to any other reason

#res.text bieng passed to the BeautifulSoup function as only text object can be processed
#'html.parse' is given to provide a uniform parser even if it is used on another platform
soup = bs4.BeautifulSoup(res.text,'html.parser') 

table = soup.find('table',attrs = {"class":"c"}) #Finding the table with class='c'

results = table.findAll('tr') #Finding all the <tr> tag components

#Initialising all the variables to be stored in the csv file
author = []
title = []
publisher = []
year = []
pages = []
language = []
size = []
extension = []
link1 = []
link2 = []
link3 = []
link4 = []
link5 = []
# Items stored in results is in list form, thus looping over its items
for i in range(1,len(results)):
    author.append((results[i].select('td'))[1].getText())   #Selecting <td> tag text content
    title.append((results[i].select('td'))[2].getText())
    publisher.append((results[i].select('td'))[3].getText())
    year.append((results[i].select('td'))[4].getText())
    pages.append((results[i].select('td'))[5].getText())
    language.append((results[i].select('td'))[6].getText())
    size.append((results[i].select('td'))[7].getText())
    extension.append((results[i].select('td'))[8].getText())
    link1.append(results[i].select('td')[9].find('a').get('href'))  #Selecting <td> tag <a> content with value 'href'
    link2.append(results[i].select('td')[10].find('a').get('href'))
    link3.append(results[i].select('td')[11].find('a').get('href'))
    link4.append(results[i].select('td')[12].find('a').get('href'))
    link5.append(results[i].select('td')[13].find('a').get('href'))

columns = []
columns.append([author,title,publisher,year,pages,language,size,extension,link1,link2,link3,link4,link5])   #Writing everything in one list so as to write later in the csv file

# Converting above list into row form as only rows can be written in csv file
rows = list(zip(*columns[0]))

#Inserting headings of each column element
rows.insert(0,('Author','Title','Publisher',"Year","Pages","Language","Size","Type","Link 1","Link 2","Link 3","Link 4","Link 5"))
#Writing on the csv file strictly using 'utf-8' encoding
with open('Scrape.csv','w',newline = '',encoding = 'utf-8') as f:
    csv_output = csv.writer(f)
    csv_output.writerows(rows)

#Reading files using pandas library for more readability
file = pd.read_csv('Scrape.csv')
if file.size == 0:
    print("Book not found")
    quit()

#Printing only the desired content of the data
print(file.iloc[:,:8])

#Determining the index of the book to get
print("Enter index number of the book: ",end='')
book = int(input())

#Determining the link to be used as there are 5 links stored in the data
print("Enter the link you would like to use: ",end='')
link = int(input())

download_page_link = file.iloc[book,7+link] #Getting download link from the data 

#Scraping another page which was gained from link
download_page = requests.get(download_page_link)
download_page.raise_for_status()
page_soup = bs4.BeautifulSoup(download_page.text,'html.parser')

#Getting the download page's link
for i in range(len(page_soup.find_all('a'))):
    if (page_soup.find_all('a')[i].getText()) == 'GET':
        download_link = page_soup.find_all('a')[i]['href']

#Writing data on the csv file
def download_file(download_url):
    response = urllib.request.urlopen(download_url)
    print("Enter the name of book: ",end='')
    book_name = input()
    file = open('%s.pdf'%book_name, 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

download_file(download_link)
quit()
