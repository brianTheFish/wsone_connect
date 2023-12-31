import ipaddress
import subprocess
import socket
import time
import os

from dns import reversename, resolver
import keyboard
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox

from subprocess import Popen, PIPE

from dns.exception import DNSException

start = 'SA;'
ssh = 'ssh'
root = 'root@'
network = "192.168.0.122"
date = "date"
cat = 'cat'  # file commands
echo = 'echo'  # do commands
grep = 'grep'
serial = 'serial'
command = '/mnt/wsone/config/monitor/mc_mon.cfg'  # use with cat to show system ID
gui_settings = "/mnt/wsone/config/system/current/gui_settings.cfg"
system_memory = "/sys/dev/block/8:0/"
connect = "/dev/ttyACM0"
# backlight_off = 'SC,1 echo 1 > /sys/class/backlight/backlght/brightness'
backlight_off = 'echo 1 > /sys/class/backlight/backlight/brightness'
backlight_on = 'echo 6 > /sys/class/backlight/backlight/brightness'
cmd_body = 'RxTowN=1'
to_device = '> /dev/ttyACM0'
tail = 'tail'
flow_right = "SA; echo 1 > /sys/class/flow/RxTowN"
flow_left = "SA; echo 0 > /sys/class/flow/RxTowN"
socket.setdefaulttimeout(0.75)


def search_network():
    name_out = ""
    dot_count = ""
    devices = os.popen('arp -a').readlines()
    for device in devices:
        ip = device.split()
        if len(ip) > 0:
            device_ip = ip[0]
            ip_split = device_ip.split('.')

            if ip_split[0] == '192':
                if int(ip_split[3]) > 110:
                    try:
                        name = socket.gethostbyaddr(device_ip)
                        print(name)
                        name_out = name[0]
                        device_ip = name[2][0]
                        if "wsone" in name_out:
                            print("got it")
                            result2 = subprocess.getoutput(ssh + " " + root + device_ip + " " + cat + " " + command)
                            serial_split = result2.split()[7:9]
                            print(serial_split)
                    except socket.herror:
                        pass

            dot_count += "."

        print(dot_count)


location = os.path.join("C:\\Users", os.getenv('username'), ".ssh", "")
path = os.path.join(location, "known_host")


# result = subprocess.Popen([start, cmd, ssh, root + network, '/k', 'echo', command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
# print(result)
# output = [os.system(ssh + " " + root + network + " " + date)]
# print(output)

# s = pxssh.pxssh()
# s.sendline ('ssh root@')
# result = subprocess.getoutput(ssh + " " + root + network)
# print(result)
# os.system("yes")


# usound = subprocess.getoutput(ssh + " " + root + network + " " + backlight_off)
# print(usound)
#
# time.sleep(2)
#
# usound = subprocess.getoutput(ssh + " " + root + network + " " + backlight_on)
# print(usound)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("1000x900")
        self.title("WSOne External control")
        self.monitor = StringVar()
        self.ip_address = StringVar()
        self.date = StringVar()
        self.canvas_back = None
        self.serial_number = StringVar()
        self.display()

    def display(self):
        self.canvas_back = CTkCanvas(self, bg='#9BCDD2', width=1260, height=860)
        self.canvas_back.pack(fill="both")

        title = CTkLabel(self.canvas_back, text="WSOne External Test Control", font=('Courier', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=40)
        comp_name = CTkCanvas(self.canvas_back, width=15, height=20, bg='#9BCDD2')
        comp_name.grid(row=0, column=2, pady=20)
        comp_name1 = CTkLabel(comp_name, text="Deltex", text_color="#003865", font=('Helvetica', 28, 'bold'), width=12)
        comp_name1.pack()
        comp_name2 = CTkLabel(comp_name, text="medical", text_color="#A2B5BB", font=('Helvetica', 18))
        comp_name2.pack()
        self.monitor_canvas = CTkCanvas(self.canvas_back, bg='#FAF0E4', width=1100, height=130)
        self.monitor_canvas.grid(row=1, column=0, padx=40, columnspan=2, sticky="nsew")

        button_canvas = CTkCanvas(self.canvas_back, bg='#FAF0E4', width=550, height=630)
        button_canvas.grid(row=2, column=0, pady=20, padx=30, sticky="nsew")
        self.screen_canvas = CTkCanvas(self.canvas_back, bg='#FAF0E4', width=420, height=630)
        self.screen_canvas.grid(row=2, column=1, pady=20, padx=10, sticky="nsew")
        monitor_id = CTkLabel(self.monitor_canvas, text="Monitor serial number")
        monitor_id.pack(pady=10, padx=20, side=LEFT)
        self.monitor_entry = CTkEntry(self.monitor_canvas, font=("Courier", 14, "bold"), width=140)
        self.monitor_entry.pack(side=LEFT, padx=10)
        Ip_label = CTkLabel(self.monitor_canvas, text="Monitor IP Address")
        Ip_label.pack(side=LEFT, pady=5, padx=20)
        self.Ip_entry = CTkEntry(self.monitor_canvas, font=("Courier", 14, "bold"), width=160)
        self.Ip_entry.pack(side=LEFT, pady=10)
        connect = CTkButton(self.monitor_canvas, text="Connect", font=("Courier", 14, "bold"), command=self.set_monitor)
        connect.pack(side=RIGHT, padx=20, pady=20)
        CTkLabel(button_canvas, text="Data Section", font=("courier", 12, "bold")).grid(row=0, column=1)
        CTkLabel(button_canvas, text=".................", font=("courier", 12, "bold")).grid(row=0, column=2)
        CTkLabel(button_canvas, text=".................", font=("courier", 12, "bold")).grid(row=0, column=0)
        CTkButton(button_canvas, text="Monitor Date", command=self.get_date).grid(row=1, column=0, pady=10, padx=15)
        CTkButton(button_canvas, text="Monitor Details", command=self.get_details).grid(row=2, column=0, pady=10,
                                                                                        padx=15)
        self.probe_coennected = self.screen_canvas.create_text(100, 15, text=" *** ", font=("Courier", 12))
        lab2 = CTkLabel(self.screen_canvas, text="Output from Buttons", font=("courier", 12, "bold"))
        lab2.grid(row=0, column=1)
        CTkLabel(self.screen_canvas, text="Date", font=("Courier", 14)).grid(row=1, column=0, pady=10, padx=15)
        self.date_text = self.screen_canvas.create_text(280, 50, text=" ", font=("Courier", 12))

        CTkLabel(self.screen_canvas, text="Monitor Details", font=("Courier", 14)).grid(row=2, column=0, pady=10,
                                                                                        padx=15)
        self.box = CTkTextbox(self.screen_canvas, width=250, height=80)
        self.box.grid(row=2, column=1, padx=10)
        CTkButton(self.canvas_back, text="Search network", font=("Courier", 18), command=self.search_network).grid(
            row=10, column=0, pady=10)
        self.network_box = CTkTextbox(self.canvas_back, font=("Courier", 14), width=350, height=120)
        self.network_box.grid(row=10, column=1, pady=15)
        CTkButton(self.canvas_back, text="Exit", font=("Courier", 18), command=self.exit).grid(row=10, column=2,
                                                                                               padx=20, pady=10)
        self.screen_canvas.itemconfig(self.date_text, text="----")
        CTkLabel(button_canvas, text="Screen Output", font=("courier", 12, "bold")).grid(row=3, column=1)
        CTkButton(button_canvas, text="Screen Off", command=self.screen_off).grid(row=4, column=0, pady=10, padx=15)
        CTkButton(button_canvas, text="Screen On", command=self.screen_on).grid(row=4, column=1, pady=10, padx=15)
        CTkLabel(button_canvas, text="Range Scale", font=("Courier", 14)).grid(row=5, column=0, pady=10, padx=15)
        CTkButton(button_canvas, text="25%", command=lambda: self.range_scale("25"), width=30).grid(row=5, column=1,
                                                                                                    padx=15,
                                                                                                    sticky="W")
        CTkButton(button_canvas, text="50%", command=lambda: self.range_scale("50"), width=30).grid(row=5, column=1,
                                                                                                    padx=15)
        CTkButton(button_canvas, text="75%", command=lambda: self.range_scale("75"), width=30).grid(row=5, column=1,
                                                                                                    padx=15,
                                                                                                    sticky="E")
        CTkLabel(button_canvas, text="Ultrasound Gain", font=("Courier", 14)).grid(row=6, column=0, pady=10, padx=15)
        CTkButton(button_canvas, text="^", command=self.gain_up, width=30).grid(row=6, column=1, padx=15, sticky="W")
        CTkButton(button_canvas, text="v", command=self.gain_down, width=30).grid(row=6, column=1, padx=15)
        CTkLabel(button_canvas, text="Flow Direction", font=("Courier", 14)).grid(row=7, column=0, pady=10, padx=15)
        CTkButton(button_canvas, text="<", command=self.flow_left, width=30).grid(row=7, column=1, padx=15, sticky="W")
        CTkButton(button_canvas, text=">", command=self.flow_right, width=30).grid(row=7, column=1, padx=15)
        CTkLabel(self.screen_canvas, text=" > ", font=("Courier", 14)).grid(row=3, column=0, pady=10,
                                                                            padx=15, sticky="W")
        CTkLabel(self.screen_canvas, text="Range Scale response > ", font=("Courier", 14)).grid(row=4, column=0,
                                                                                                pady=10,
                                                                                                padx=15)
        CTkLabel(self.screen_canvas, text="Gain response > ", font=("Courier", 14)).grid(row=5, column=0, pady=10,
                                                                                         padx=15, sticky="W")
        CTkLabel(self.screen_canvas, text="Flow response > ", font=("Courier", 14)).grid(row=6, column=0, pady=10,
                                                                                         padx=15, sticky="W")
        CTkLabel(button_canvas, text="Scale Range", font=("Courier", 14)).grid(row=8, column=0, pady=10, padx=15)
        CTkButton(button_canvas, text="50", command=lambda: self.scale("50"), width=30).grid(row=8, column=1,
                                                                                             padx=15, sticky="W")
        CTkButton(button_canvas, text="100", command=lambda: self.scale("100"), width=30).grid(row=8, column=1,
                                                                                               padx=15)
        CTkButton(button_canvas, text="150", command=lambda: self.scale("150"), width=30).grid(row=8, column=1,
                                                                                               padx=15, sticky="E")
        CTkButton(button_canvas, text="200", command=lambda: self.scale("200"), width=30).grid(row=8, column=2,
                                                                                               padx=15, sticky="W")
        CTkButton(button_canvas, text="250", command=lambda: self.scale("250"), width=30).grid(row=8, column=2,
                                                                                               padx=15, sticky="E")
        CTkLabel(self.screen_canvas, text=">").grid(row=7, column=0, padx=10, sticky="W")
        CTkButton(button_canvas, text="System details.", command=self.system_details).grid(row=9, column=0,
                                                                                           pady=10, padx=15)
        CTkLabel(self.screen_canvas, text="System Details", font=("Courier", 14)).grid(row=8, column=0, pady=10,
                                                                                       padx=15)
        self.system_box = CTkTextbox(self.screen_canvas, width=280, height=150)
        self.system_box.grid(row=8, column=1, padx=10, pady=10)
        CTkLabel(button_canvas, text="_").grid(row=10, column=0, pady=30)
        CTkButton(button_canvas, text="System SD card memory status", command=self.system_memory).grid(row=11, column=0, padx=15, pady=30, sticky="S")
        CTkLabel(self.screen_canvas, text="Memory Status...", font=("Curier", 14)).grid(row=9, column=0, padx=10, sticky="W")
        CTkLabel(self.screen_canvas, text="Total", font=("Courier", 14)).grid(row=9, column=0, padx=20, sticky="E")
        CTkLabel(self.screen_canvas, text="Partition", font=("Courier", 14)).grid(row=9, column=1, padx=20, sticky="W")
        CTkLabel(self.screen_canvas, text="Size", font=("Courier", 14)).grid(row=9, column=1, padx=100, sticky="E")
        self.sd_text = self.screen_canvas.create_text(180, 590, text=" *** ", font=("Courier", 12))
        self.sd_part = self.screen_canvas.create_text(270, 590, text=" *** ", font=("Courier", 12))
        self.sd_size = self.screen_canvas.create_text(400, 590, text=" *** ", font=("Courier", 12))
        self.Ip_entry.insert(0, "192.168.0.122")
        self.monitor_entry.insert(0, "111")

    def set_monitor(self):
        #################################################
        #
        if not self.monitor_entry.get():
            CTkMessagebox(message="Which monitor serial number", icon="warning", option_1="Thanks")
        else:
            self.serial_number.set(self.monitor_entry.get())
            l1 = f"{self.monitor_entry.get()}-set"
            self.monitor_entry.delete(0, END)
            self.monitor_entry.insert(0, l1)

        if not self.Ip_entry.get():
            CTkMessagebox(message="Which IP Address?", icon="warning", option_1="Thanks")
        else:
            subprocess.Popen(f"start cmd /k ssh root@{self.Ip_entry.get()} ", shell=True)
            os.system("taskkill /im cmd.exe /f")
            self.ip_address.set(self.Ip_entry.get())
            l2 = f"{self.Ip_entry.get()}-set"
            self.Ip_entry.delete(0, END)
            self.Ip_entry.insert(0, l2)
        connected = subprocess.getoutput(
            ssh + " " + root + self.ip_address.get() + " " + cat + " " + connect)
        print(connected)
        if "file" in connected:
            pass
        else:
            self.screen_canvas.itemconfig(self.probe_coennected, text="Dopp-link Connected")

    def get_date(self):
        date_out = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + date)
        if len(date_out) < 30:
            self.screen_canvas.itemconfig(self.date_text, text=date_out)

        else:
            CTkMessagebox(message="Date Error", icon="warning", option_1="Thanks")

    def search_network(self):
        self.network_box.delete("0.0", "end")
        dot_count = ""
        devices = os.popen('arp -a').readlines()
        for device in devices:
            ip = device.split()
            if len(ip) > 0:
                device_ip = ip[0]
                ip_split = device_ip.split('.')
                if ip_split[0] == '192':
                    if int(ip_split[3]) > 110:
                        try:
                            name = socket.gethostbyaddr(device_ip)
                            self.update_network_box(f"\n{name[0]} {name[2]}")
                            name_out = name[0]
                            device_ip = name[2][0]
                            if "wsone" in name_out:
                                result2 = subprocess.getoutput(ssh + " " + root + device_ip + " " + cat + " " + command)
                                serial_split = result2.split()[7:9]
                                self.update_network_box(f"\n{serial_split}")
                        except socket.herror:
                            pass
                dot_count = "."
                if keyboard.is_pressed("ESC"):
                    print("*****")
            self.update_network_box(dot_count)
        self.update_network_box("Finish")

    def get_details(self):
        result2 = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + cat + " " + command)
        results = result2.split()
        version1 = results[2] + " " + results[3] + "\n" + results[4] + " " + results[5] + "\n" + results[7] + "\t" + \
                   results[8] + "\n"
        model = results[14] + results[15] + results[16] + "  " + results[11] + results[12]
        self.box.insert("1.0", version1)
        self.box.insert("5.0", model)
        self.box.update()
        serial_split = result2.split()[7:9]
        if self.serial_number.get() == serial_split[1][1:-1]:
            l1 = f"{self.monitor_entry.get()} Match"
            self.monitor_entry.delete(0, END)
            self.monitor_entry.insert(0, l1)
        else:
            l1 = f"{self.monitor_entry.get()} -----"
            self.monitor_entry.delete(0, END)
            self.monitor_entry.insert(0, l1)

    def update_network_box(self, data):
        self.network_box.insert("0.0", data)
        self.network_box.update()

    def screen_off(self):
        subprocess.Popen(f"ssh root@{self.ip_address.get()} {backlight_off}", stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
        CTkLabel(self.screen_canvas, text="Off").grid(row=3, column=0, sticky="E")

    def screen_on(self):
        subprocess.Popen(f"ssh root@{self.ip_address.get()} {backlight_on}", stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
        CTkLabel(self.screen_canvas, text="On").grid(row=3, column=1)

    def velocity(self):
        print("Velocity")

    def gain_up(self):
        print("Gain up")

    def gain_down(self):
        print("Gain down")

    def flow_left(self):
        print("Flow Left")
        output = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + flow_left)
        print(output)

    def flow_right(self):
        print("Flow Right")
        output = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + flow_right)
        print(output)

    def range_scale(self, scale):
        print(f"Range Scale - {scale}")

    def scale(self, scale):
        print(f"Scale = {scale}")

    def system_details(self):
        result = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + cat + " " + gui_settings)
        output = result.split()
        version = output[2] + output[3] + "\n" + output[5] + " - " + output[6] + "\n" + output[7] + " - " + output[8] + \
                  " " + output[9] + "\n" + output[10] + " - " + output[11] + "\n" + output[12] + " - " + output[13] + " " +\
                  output[14] + ", " + output[15] + ", " + output[16] + "\n" + "Format  - " + output[17][:7] + " " + output[18] + " - " \
                  + output[19] + output[20] + "\n\t" + output[21] + " " + output[22] + "\n\t" + output[23] + " " + output[24]
        self.system_box.insert("0.0", version)

    def system_memory(self):
        size1 = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + cat + " " + system_memory + "size")
        size1f = round(((int(size1) / 1000000) * 512) / 1000, 2)
        self.screen_canvas.itemconfig(self.sd_text, text=f"{size1f}Gb")
        partition = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + cat + " " + system_memory + "sda1/partition")
        self.screen_canvas.itemconfig(self.sd_part, text=partition)
        size2 = subprocess.getoutput(ssh + " " + root + self.ip_address.get() + " " + cat + " " + system_memory + "sda1/size")
        size2f = round(((int(size2) / 1000000) * 512) / 1000, 2)
        self.screen_canvas.itemconfig(self.sd_size, text=f"{size2f}Gb")

    def exit(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
