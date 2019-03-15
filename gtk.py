import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import re
import os

sell_action = False
gold_action = False
pause_bot = False
headless_mode = False
sleep_mode = True

class Alert(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Alert")
        self.box = Gtk.Box(spacing=0)
        self.add(self.box)

        self.label = Gtk.Label()
        self.label.set_text("                       Bot is busy.. \nPlease wait untill first task ends..")
        self.box.pack_start(self.label, True, True, 50)

        self.set_size_request(200,0)
        self.set_resizable(False)

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gladiatus Bot")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.gold_action = gold_action
        self.sell_action = sell_action
        self.pause_bot = pause_bot
        self.headless_mode = headless_mode
        self.sleep_mode = sleep_mode

        self.sell = Gtk.Button(label="Sell Items = False")
        self.gold = Gtk.Button(label="Take Out Gold = False")
        self.pause = Gtk.Button(label="Pause Bot = False")
        self.headless = Gtk.Button(label="Headless Mode = False")
        self.sleep = Gtk.Button(label="Sleep Mode = True")
        self.settings = Gtk.Button(label="Open Settings")
        self.status = Gtk.Button(label="Show Current Info")
        
        self.sell.connect("clicked",self.on_sell_clicked)
        self.gold.connect("clicked",self.on_gold_clicked)
        self.pause.connect("clicked",self.on_pause_clicked)
        self.headless.connect("clicked",self.on_headless_clicked)
        self.sleep.connect("clicked",self.on_sleep_clicked)
        self.settings.connect("clicked",self.on_settings_clicked)
        self.status.connect("clicked",self.on_status_clicked)

        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.gold, False, False, 0)
        self.box.pack_start(self.pause, False, False, 0)
        self.box.pack_start(self.headless, False, False, 0)
        self.box.pack_start(self.sleep, False, False, 0)
        self.box.pack_start(self.settings, False, False, 0)
        self.box.pack_start(self.status, False, False, 0)

        self.connect('delete-event',Gtk.main_quit)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def on_sell_clicked(self, widget):
        if self.gold_action:
            Alert().show_all()
        else:
            self.sell_action = True
            self.sell.set_label("Sell Items = True")

    def on_gold_clicked(self, widget):
        if self.sell_action:
            Alert().show_all()
        else:
            self.gold_action = True
            self.gold.set_label("Take Out Gold = True")

    def on_pause_clicked(self, widget):
        if self.pause_bot:
            self.pause_bot = False
            self.pause.set_label("Pause Bot = False")
        else:
            self.pause_bot = True
            self.pause.set_label("Pause Bot = True")

    def on_headless_clicked(self, widget):
        if self.headless_mode:
            self.headless_mode = False
            self.headless.set_label("Headless Mode = False")
        else:
            self.headless_mode = True
            self.headless.set_label("Headless Mode = True")

    def on_sleep_clicked(self, widget):
        if self.sleep_mode:
            self.sleep_mode = False
            self.sleep.set_label("Sleep Mode = False")
        else:
            self.sleep_mode = True
            self.sleep.set_label("Sleep Mode = True")
        
    def on_status_clicked(self, widget):
        return

    def on_settings_clicked(self, widget):
        SettingsWindow().show_all()

class SettingsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gladiatus Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)
        
        self.login = Gtk.Button(label="Login")
        self.general = Gtk.Button(label="General")
        self.sell = Gtk.Button(label="Sell")
        self.buy = Gtk.Button(label="Buy")
        self.extract = Gtk.Button(label="Extract")

        self.login.connect("clicked",self.on_clicked_login)

        self.box.pack_start(self.login, False, False, 0)
        self.box.pack_start(self.general, False, False, 0)
        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.buy, False, False, 0)
        self.box.pack_start(self.extract, False, False, 0)
        
        self.set_size_request(200,0)
        self.set_resizable(False)

    def on_clicked_login(self, widget):
        SettingsLogin().show_all()

class SettingsLogin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Login Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.username, self.password, self.server_option = self.read_user_settings()

        self.txt = Gtk.Entry()
        self.txt.set_placeholder_text("nickname")
        if self.username is not "":
            self.txt.set_text(self.username)

        self.txt2 = Gtk.Entry()
        self.txt2.set_placeholder_text("password")
        self.txt2.set_invisible_char("*")
        self.txt2.set_visibility(False)
        if self.password is not "":
            self.txt2.set_text(self.password)

        self.server = Gtk.ComboBoxText()
        self.server.set_entry_text_column(0)
        self.server.append_text("Server 1")
        self.server.append_text("Server 25")
        self.server.append_text("Server 34")
        self.server.append_text("Server 35")
        self.server.append_text("Server 36")
        self.server.append_text("Server 37")
        self.server.append_text("Server 38")
        self.server.append_text("Server 39")
        self.server.append_text("Server 40")
        if int(self.server_option) >= 0 and int(self.server_option) <= 8:
            self.server.set_active(int(self.server_option))

        self.box.pack_start(self.txt, False, False, 0)
        self.box.pack_start(self.txt2, False, False, 0)
        self.box.pack_start(self.server, False, False, 0)

        self.connect('delete-event',self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def read_user_settings(self):
        lines = [line.rstrip('\n') for line in open('user_settings')]
        username = ""
        password = ""
        server = ""
        for line in lines:
            if 'Login' in line:
                username = re.findall("\'(.*?)\'", line)[0]
            elif 'Password' in line:
                password = re.findall("\'(.*?)\'", line)[0]
            elif 'Server' in line:
                server = re.findall("\'(.*?)\'", line)[0]
        return username, password, server

    def save_settings(self, widget, data):
        username = self.txt.get_text()
        password = self.txt2.get_text()
        server = self.server.get_active()
        if os.path.exists("user_settings"):
            os.remove("user_settings")
        with open("user_settings", 'w+') as f:
            f.write("Login='" + username + "'\n")
            f.write("Password='" + password + "'\n")
            f.write("Server='" + str(server) + "'")
        
mWindow = MainWindow()
mWindow.show_all()

Gtk.main()
