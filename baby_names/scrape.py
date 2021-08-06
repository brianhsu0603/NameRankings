import requests
from bs4 import BeautifulSoup
import csv

def scrape_names(year):

    # open the file in the write mode
    f = open('data/baby-'+str(year)+".txt", 'w')

    # create the csv writer
    f.writelines(str(year) + "\n")
    
    headers = {"referer":"https://www.google.com",
               "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    URL = "https://www.ssa.gov/oact/babynames/decades/names"+str(year)+"s.html"
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")
    nameList = soup.select('table[class="t-stripe"] tbody tr')

    for element in range(len(nameList)-1):
        res = nameList[element].text
        res = res.split("\n")
        rank = res[0]
        names = res[1]
        names = names.split(" ")
        boy_name = names[0]
        girl_name = names[2]

        data = [rank, boy_name, girl_name]
        data = ",".join(data) + "\n"

        f.writelines(data)
    
    f.close()

    return ('data/baby-'+str(year)+".txt")
