import keyboard
import time
import sys
import os
import requests as request
from bs4 import BeautifulSoup
base = "http://127.0.0.1:5000/"
lin = "http://127.0.0.1:5000/roleplay_selection/Beginning%20Test%20RPs"
link= "http://127.0.0.1:5000/role_selection/Beginning%20Test%20RPs/The%20Negotiation%20Challenge"

r = request.get(base)
soup = BeautifulSoup(r.content, 'html.parser')
# print(soup.prettify())
# print(soup.find_all('a'))
r = request.get(lin)
soup1 = BeautifulSoup(r.content, 'html.parser')
# print(soup1.prettify())
# print(soup1.find_all('a'))
r = request.get(link)
soup2 = BeautifulSoup(r.content, 'html.parser')
# print(soup2.prettify())
# print(soup2.find_all('a'))
# print(soup2.find_all('input'))
# print(soup2.find_all('button'))
# print(soup2.find_all('textarea'))
# print(soup2.find_all('div'))
# print(soup2.find_all('p'))
# print(soup2.find_all('h1'))
print(soup2)
# select a role from the dropdown menu
p = soup2.find_all('select')[0]
# select option 1 and press selct
print(p[0]['value'])


print(p)



# use the keyboard module to select the role


# use the inp variable to select the input box
# t = soup.find_all('input')[0].txt = "hello, and welcome to my world."
# print(t)
# t.clear()
# txt = t.get_text()
# print(txt)

# x = txt.capitalize()

# print (x)

# use the keyboard module to type the message
# use the keyboard module to press enter to send the message


def main():
    # select the window to use
    keyboard.press_and_release("alt+tab") 
    time.sleep(1)
    # select the text input box
    keyboard.press_and_release("tab")
    time.sleep(1)
    # type the message
    keyboard.write("hello")
    # press enter to send
    keyboard.press_and_release("enter")
    time.sleep(1)
    
    
    
    print("starting please click the window for the chat")
    i = 0
    while time.sleep(5):
        print(i)
        i = i + 1
        if i == 5:
            break
    print("started")
    # press tab to gain control of the typing box and wait
    keyboard.press_and_release("tab")
    time.sleep(1)
    # type the message
    keyboard.write("hello")
    # press enter to send
    keyboard.press_and_release("enter")
    time.sleep(1)
    
    print("started")
    
