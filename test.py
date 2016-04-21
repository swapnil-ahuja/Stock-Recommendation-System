import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import re
path="/home/swapnil/Desktop/intraQuarter"
f=['hum', 'adt', 'nflx', 'exc', 'big', 'gme', 'spls', 'cah', 'abt', 'nile', 'cog', 'bxp', 'clx', 'gm', 'adsk', 'mpc']
for each in f[1:]:
    full_file_path=path+"/forward/"+str(each)+".html"
    source=open(full_file_path,"r").read()
    #print(each)
    each="("+str(each)+")"
    each=each.upper()
    #print(each)
    value=source.split(each+"</h2>")[0]
    value2=value.split('<div class="title"><h2>')[1]
    print(value2+"\n")