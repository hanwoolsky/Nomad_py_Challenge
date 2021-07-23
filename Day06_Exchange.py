import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

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

print("Welcome to CurrencyConvert PRO 2000\n")
for idx, val in enumerate(country):
    print('#', idx, val)

print("\nWhere are you from? Choose a country by a number.\n")

print("#: ", end = '')
fir_country = int(input())
print(country[fir_country])
print("\nNow choose another country.\n")
print("#: ", end = '')
sec_country = int(input())
print(country[sec_country])

def exchange(num):
  url2 = f"https://transferwise.com/gb/currency-converter/{code[fir_country].lower()}-to-{code[sec_country].lower()}-rate?amount={num}"
  currency_result = requests.get(url2)
  cur_soup = BeautifulSoup(currency_result.text, "html.parser")
  cur_rate = cur_soup.find("h3", {"class": "cc__source-to-target"})
  rate = float(cur_rate.find_all("span")[2].string)
  return rate

def convert():
  print(f"\nHow many {code[fir_country]} do you want to convert to {code[sec_country]}?")
  amount = input()
  try:
    num = float(amount)
    ex_rate = exchange(num)
    print(f"{format_currency(num, code[fir_country], locale = 'ko_KR')} is ", format_currency(num*ex_rate, code[sec_country], locale = "ko_KR"))
  except ValueError:
    print("That wasnt't a number.")
    convert()

convert()
