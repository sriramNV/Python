#   Program to convert given seconds to min, hr and days 

secs = int(input("Enter the seconds: ")) # 14423

mins = secs // 60   

sec = secs % 60     

hrs = mins // 60    

min = mins % 60    

day = hrs // 24

hr = hrs %  24


print(f"{day}:{hr}:{min}:{sec} in day:hour:min:sec")