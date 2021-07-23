import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

indeed_result = requests.get(url)
indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")
table = indeed_soup.find("div", {"class": "flat-services"})

element = table.find_all("tr")
elem_size = len(element)

country = []
currency = []
code = []
for i in range(elem_size - 1):
  country.append(element[i+1].find_all("td")[0].string)
  currency.append(element[i+1].find_all("td")[1].string)
  code.append(element[i+1].find_all("td")[2].string)

for i in range(elem_size-1):
  if currency[i] == "No universal currency":
    del country[i]
    del code[i]

print("Hello! Please select a country by number:")
for idx, val in enumerate(country):
    print('#', idx, val)

def select():
  print("#: ", end = '')
  number = input()

  try:
      country_num = int(number)
      if country_num > 264:
        print("Choose a number from the list")
        select()
      else:
        print(f"You chose {country[country_num]}")
        print(f"The currency code is {code[country_num]}")
  except ValueError:
      print("That wasnt't a number.")
      select()

select()