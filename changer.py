#!/usr/bin/python3
import requests
import subprocess
import time

def state_from_time(a_time, sunset, sunrise):
    if (a_time[0] < sunrise[0]):
        state = "Night.jpg"
    elif (a_time[0] < 11):
        state = "Dawn.jpg"
    elif (a_time[0] < sunset[0] - 1):
        state = "Day.jpg"
    elif (a_time[0] < sunset[0]):
        state = "Dusk.jpg"
    else:
        state = "Night.jpg"
    return state  

def fetch_state():
    print("Fetching state...")
    current_time = time.localtime()
    current_hours_mins = [int(current_time[3]), int(current_time[4])]
    site = 'https://www.gaisma.com/en/location/san-luis-obispo-california.html'
    if (needs_update(current_time)):
        print("Updating...")
        response = requests.get(site)
        content = response.content.decode(response.encoding)
        first_relevant_section = content.find("Today")
        relevant = content[first_relevant_section:first_relevant_section + 99]
        relevant = relevant.split("</td>")[1:]
        sunrise = relevant[0][-5:].split(":")
        sunrise = [int(sunrise[0]), int(sunrise[1])]
        sunset = relevant[1][-5:].split(":")
        sunset = [int(sunset[0]), int(sunset[1])]
        save_file_state(sunrise, sunset, current_time)
        return state_from_time(current_hours_mins, sunset, sunrise)
    else:
        print("No update required...")
        f = open("last_updated.txt", "r")
        times = f.read().split("\n")
        sunrise = times[1].split(":")
        sunrise = [int(sunrise[0]), int(sunrise[1])]
        sunset = times[2].split(":")
        sunset = [int(sunset[0]), int(sunset[1])]
        return state_from_time(current_hours_mins, sunset, sunrise)


def save_file_state(sunrise, sunset, current_time):
    f = open("last_updated.txt", "w")
    f.write("{0} {1}\n{2}:{3}\n{4}:{5}\n".format(current_time[1], current_time[2], sunrise[0], sunrise[1], sunset[0], sunset[1]))

def needs_update(current_time):
    f = open("last_updated.txt", "r")
    last_updated = f.read().split("\n")[0].split(" ")
    if (int(last_updated[0]) == current_time[1]):
        if (int(last_updated[1]) == current_time[2]):
            return False
    return True
def main():
    state = fetch_state()
    print(state)
    fname   = "'file:///home/clipping/Pictures/firewatch-time/" + state + "'"
    set_cmd = ["gsettings","set","org.gnome.desktop.background",
               "picture-uri", fname]
    get_cmd = "gsettings get org.gnome.desktop.background picture-uri"

    current = subprocess.run(get_cmd.split(" "),
              stdout=subprocess.PIPE).stdout.decode(
              "utf-8").strip()

    if (current != fname):
        subprocess.run(set_cmd)

main()
