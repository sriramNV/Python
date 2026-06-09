#   Program to convert given seconds to min, hr and days 

secs = int(input("Enter the seconds: ")) # 14423

mins = secs // 60   #   mins = 240 min
sec = secs % 60     #   sec = 23 14423%60 = 23

hrs = mins // 60    #   hrs = 4 hrs 240 / 60 = 4
min = mins % 60     #   min = 0     240 % 60 = 0

day = hrs // 24
hr = hrs %  24


print(f"{day}:{hr}:{min}:{sec}")