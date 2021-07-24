import tkinter as tk
import subprocess
import sys


class Overlay(object):
    def __init__(self, ip):
        self.ip_address = ip
        self.ping = 0
        self.min = 10000
        self.max = 0

        self.root = tk.Tk()
        self.root.geometry("250x25")
        self.root.config(bg="black")

        self.text = tk.StringVar()
        self.text_label = tk.Label(self.root, textvariable=self.text, font=('Consolas', '12'), fg='green', bg='black')
        self.text_label.pack()
        self.text_label.bind("<Button-1>", lambda _: sys.exit())

        self.root.overrideredirect(True)
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def update_label(self) -> None:
        self.ping = self.get_ping(self.ip_address)
        if self.ping > self.max:
            self.max = self.ping
        if self.ping < self.min:
            self.min = self.ping

        self.text.set("Ping: {}, Max: {}, Min: {}".format(self.ping, self.max, self.min))
        self.root.after(1000, self.update_label)

    def run(self) -> None:
        self.root.after(0, self.update_label)
        self.root.mainloop()

    @staticmethod
    def get_ping(ip) -> int:
        command = "ping -n 1 " + ip

        # run command in cmd without opening window and store the output
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        response = subprocess.check_output(command, startupinfo=startupinfo).split()

        # the ping value is the last in the list
        ping = str(response[-1])
        ping = ping[2:][:-3]
        return int(ping)


if __name__ == "__main__":
    config_file = open(r"config.txt")
    region = config_file.readline().split()[-1]

    ip_address = ""
    for line in config_file:
        text = line.split()
        if len(text) > 0:
            if region in text[0]:
                ip_address = text[1]

    overlay = Overlay(ip_address)
    overlay.run()
