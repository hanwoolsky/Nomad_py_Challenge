import os
import requests

site = []
list_input = []
answer = 'Y'

while(answer == 'Y'):
  print("Welcome to IsItDown.py!")
  print("Please write a URL or URLs you want to check(seperated by comma)")

  list_input = input().replace(',', '').split()
  size = len(list_input)

  for i in range(size):
    if ".com" in list_input[i]:
      site += [list_input[i].replace('http://','').replace('https://','').replace('.com', '')]
    else:
      print(f"{list_input[i]} is not a valid URL.")

  new_size = len(site)

  for i in range(new_size):
    try:
      indeed_result = requests.get("http://" + site[i] + ".com")
      if indeed_result.status_code == 200:
        print("http://" + site[i] + ".com is up!")
      else:
        print("http://" + site[i] + ".com is down!")
    except:
      print("http://" + site[i] + ".com is down!")
  
  temp = 'G'
  while(temp == 'G'):
    temp = input("Do you want to start over? (y/n)")
    if (temp == 'Y' or temp == 'y'):
      temp = 'B'
      answer = 'Y'
      os.system('clear')
    elif (temp == 'N' or temp == 'n'):
      print("Ok, bye!")
      temp = 'B'
      answer = 'N'
    else:
      print("That's not a valid answer.")
      temp = 'G'
  list_input = []
  site = []