from flask import Flask, render_template, url_for
import socket
from subprocess import check_output
import re
import numpy as np
import time
from datetime import datetime
from random import seed, randint
from cpu_statistics import cpu_stats_json, cpu_percent_json, cpu_freq_json, show_processes_cpu_sorted

app = Flask(__name__)

@app.route("/")
def api_root():
    return "Connection Successful"

@app.route("/home")
def home():
    show_ip()
    return render_template("index.html")

@app.route('/background_process_test')
def background_process_test():
    print(socket.gethostname())
    return ("nothing")

@app.route('/background_process_ip')
def background_process_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0]) # gets IP
    return ("nothing")


@app.route('/background_process_timed_cpu')
def refresh():
    cpu_stats_json()
    cpu_percent_json()
    cpu_freq_json()
    show_processes_cpu_sorted()
    return("nothing")


@app.route('/background_cpu_table')
def refreshCPUtable():
    return render_template("table.html")



@app.route('/interface')
# def test():
#     return render_template("ip_interface.html")

def show_ip():
    # Prints interfaces to console
    path = r"\templates\ip_interface.html"

    with open(r'templates\show_ip_interface_brief.txt') as fh:
        fstring = fh.readlines() # array of lines
        line_1 = str(fstring[1])
        headings = line_1.split()
        headings = np.array(headings)
        headings = np.append(headings, "ID")
        headings =  tuple(headings) # turns array into tuple
        data = []
        for line in fstring:
            pattern = re.findall( r'\b(GigabitEthernet0/0/0|GigabitEthernet0/0/1|GigabitEthernet0|VirtualPortGroup0|VirtualPortGroup1)\b', line ) # array
            if pattern:
                temp = line.split()
                for i in pattern:
                    time.sleep(1)
                    seed(datetime.now())
                    r_int = randint(0, 100000)
                    # url = "<a href=\"/" + str(r_int) + "\">"+ str(pattern[0]) +"</a>"
                    # temp[0] = i.replace(str(pattern[0]),url) # replace interface with hyperlink
                    temp.append(str(r_int))
                    data.append(temp)
        data = np.array(data, dtype=list)   
        data =  tuple([tuple(e) for e in data])
        print(headings)
        print(data)
    return render_template("interface_table.html", headings=headings, data=data) #, url=url

@app.route('/interface/<rand_num_str>') # dynamic app route for ip interfaces
def view(rand_num_str):
    with open(r'templates\show_interface_gigabitethernet0.txt') as file:
        fstring = file.read()

        pattern = r"(?<=address is )(.+?)(?=, DLY 10 usec,)"
        found = re.findall(pattern, fstring, re.DOTALL)
        joined_string = ' '.join(str(e) for e in found)
        print(joined_string)

        pattern2 = r"(?<=5 minute)(.+?)(?=0 underruns)"
        found2 = re.findall(pattern2, fstring, re.DOTALL)
        joined_string2 = ' '.join(str(e) for e in found2)
        app_string = "5 minute" + joined_string2 + " 0 underruns"
        print(app_string)
        list2  = tuple(map(str, app_string.split(', ')))
        # print(list2)
        
    return render_template("view_interface.html", p1=joined_string, p2=app_string, list2=list2)


if __name__ == "__main__":
    app.run(host="0.0.0.0") 
    # accessible by any computer 
    # on the network
