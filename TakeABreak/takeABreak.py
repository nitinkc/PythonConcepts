import webbrowser
import time

duration = 2*60*60
#Testing
#duration = 2

n_times = 6
while(n_times > 1 ):        
    time.sleep(duration)
    webbrowser.open("https://www.youtube.com/watch?v=-qlJiGGvPUI")
    n_times = n_times-1