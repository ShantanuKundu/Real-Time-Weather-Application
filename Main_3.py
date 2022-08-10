#--DESCRIPTION OF THE PROGRAM--

from tkinter import *
import requests
from PIL import Image, ImageTk
from datetime import datetime
import API_info as cw
import Ccode as cc
from prettytable import PrettyTable

root = Tk()
root.title("Weather-GUI Application ")

def format_response(weather):
    global name, temp, temp_max, temp_min, prs, humid, wind_sp, sun_r, sun_s, desc
    if weather['cod'] != "404":
        name = weather['name']
        temp = round((weather['main']['temp'] - 273),2)
        temp_max = round((weather['main']['temp_max'] -273),2)
        temp_min = round((weather['main']['temp_min'] - 273),2)
        prs = (weather['main']['pressure'])/1000
        humid = weather['main']['humidity']
        wind_sp = round((weather['wind']['speed']*18/5),2)
        sun_r = datetime.fromtimestamp(weather['sys']['sunrise'])
        sun_s = datetime.fromtimestamp(weather['sys']['sunset'])
        desc = weather['weather'][0]['description']
        
        report =  'City: %s \nTemperature: %s°C \nMaximum Temperature: %s°C \nMinimum Temperature: %s°C \nPressure: %sbar \nHumidity: %s \nWind Speed: %skm/h \nSunrise: %s \nSunset: %s \nDescription: %s' % (name, temp, temp_max, temp_min,  prs,  humid,  wind_sp, sun_r, sun_s, desc)
        print("The Weather Details of ",name, " has been reported." )
    
        list1=["Name",'Country','Temp','Tempmax', 'Tempmax', 'Pressure','Humidity','Wind Speed','Sunrise,','Sunset','Description']
        list2=[name, country, temp, temp_max, temp_min, prs, humid, wind_sp, sun_r, sun_s, desc]
        table = PrettyTable(["list1","list2"])
        for x in range(0,11):
            table.add_row([list1[x],list2[x]])
        print(table)
    else:
        report = "Invalid Data"
        print("Invalid Data")
    return report    

    
def weather(city):
    global api_key
    global base_url
    global country
    city_name = entry.get()
    if city_name == "":
        print("No City Entered.")
    else:    
        api_key = cw.api_key
        base_url = cw.base_url

        country=input("Enter Country: ")
        if country == "":
            print("No Country Entered.")
        else:
            for i in cc.l:
                if i["name"]==country:
                    code = i["code"]
                    break
                
                            
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "," + code
    response = requests.get(complete_url)
    weather = response.json()

    results['text'] = format_response(weather)

    icon_name = weather['weather'][0]['icon']
    open_image(icon_name)

def open_image(icon):
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw', image=img)
    weather_icon.image = img

canvas = Canvas(root, height=600, width=800)
canvas.pack()

background_image = PhotoImage(file="H:\\REAL TIME WEATHER APP\\background.png")
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

label1 = Label(root, text = "REAL-TIME WEATHER GUI APPLICATION")
label1.config(font = ('algerian', 18))
canvas.create_window(400, 25, window=label1)

frame = Frame(root, bg='sky blue', bd=7)
frame.place(relx = 0.5, rely =0.1, relwidth=0.9, relheight=0.1, anchor = 'n')

entry = Entry(frame, font=40)
entry.place(relwidth=0.5, relheight=1)

def clear():
    entry.delete(0, END)
    print("Cleared")
    country_code=0
    
button1 = Button(frame, text = "GET WEATHER", command=lambda: weather(entry.get()), bg='brown', fg='white', font=('garamond', 15, 'bold'))
button1.place(relx=0.51, relwidth=0.28, relheight=1)

button2 = Button(frame, text = "CLEAR", command=clear, bg='brown', fg='white', font=('garamond', 15, 'bold'))
button2.place(relx=0.8, relwidth=0.2, relheight=1)

lower_frame = Frame(root, bg='sky blue', bd=12)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')

results = Label(lower_frame, anchor='nw', justify='left', bd=4)
results.config(font=40, bg='white')
results.place(relwidth=1, relheight=1)

weather_icon = Canvas(results, bg='white', bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

root.mainloop()
