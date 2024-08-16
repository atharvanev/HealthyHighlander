from bs4 import BeautifulSoup
from typing import List
import requests
from datetime import datetime

def get_items() -> List[List[str]]:
  current_date = datetime.now().strftime("%m/%d/%Y")
  formatted_date = current_date.replace("/", "%2F")
  #print(current_date)
  glasgowUrl = f"https://foodpro.ucr.edu/foodpro/shortmenu.asp?sName=University+of+California%2C+Riverside+Dining+Services&locationNum=03&locationName=Glasgow&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate={formatted_date}"

  glasgowPage = requests.get(glasgowUrl)

  glasgow = BeautifulSoup(glasgowPage.text,features='html.parser')

  foods = glasgow.find_all('table', {
      'border': '0',
      'width': '100%',
      'cellpadding': '0',
      'cellspacing': '0',
      'bordercolorlight': 'black',
      'bordercolordark': 'black'
  })

  fooditems = []

  for food in foods:
    for item in food.find_all('div', class_ = ['shortmenumeals','shortmenurecipes']):
      # Extract text and remove extra whitespace
      text = item.get_text(strip=True, separator=' ')
      fooditems.append(text)


  Breakfast = []
  Lunch = []
  Dinner = []
  # print(fooditems)
  fooditems = fooditems[1:]
  # print(fooditems)


  for i, value in enumerate(fooditems):
      if value == "Lunch":
        fooditems = fooditems[i+1:]
        break
      else:
        Breakfast.append(value)

  for i, value in enumerate(fooditems):
      if value == "Dinner":
        fooditems = fooditems[i+1:]
        break
      else:
        Lunch.append(value)

  Dinner = fooditems

  # print("Breakfast Items",Breakfast,"\n")
  # print("Lunch Items",Lunch,"\n")
  # print("Dinner Items",Dinner,"\n")

  return [[current_date],Breakfast,Lunch,Dinner]

get_items()