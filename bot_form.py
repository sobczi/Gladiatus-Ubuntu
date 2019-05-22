#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
from gi.repository import Gdk
from configparser import SafeConfigParser
import re
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from multiprocessing import Process
from threading import Thread

from multiprocessing import Pool, Process, Pipe, Array
from bot_script import main_loop
from datetime import datetime

config = SafeConfigParser()
config.read('config35.ini')

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
    def __init__(self, _var):
        Gtk.Window.__init__(self, title="Gladiatus Bot")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)
        self.set_icon_from_file(self.get_resource_path("icon.ico"))

        self.sell = Gtk.Button(label="Sell Items = False")
        self.gold = Gtk.Button(label="Take Out Gold = False")
        self.packages_download = Gtk.Button(label="Download Packages = False")
        self.pause = Gtk.Button(label="Pause Bot = False")
        self.settings = Gtk.Button(label="Open Settings")
        self.status = Gtk.Button(label="Show Current Info")
        
        self.headless_c = Gtk.CheckButton()
        self.headless_c.set_active(return_bool("headless","headless"))
        self.headless_c.set_label("Headless Mode")
        
        self.sleep_c = Gtk.CheckButton()
        self.sleep_c.set_label("Sleep Mode")

        self.sell.connect("clicked",self.on_sell_clicked)
        self.gold.connect("clicked",self.on_gold_clicked)
        self.pause.connect("clicked",self.on_pause_clicked)
        self.settings.connect("clicked",self.on_settings_clicked)
        self.status.connect("clicked",self.on_status_clicked)
        self.headless_c.connect("clicked", self.on_clicked_headless_c)
        self.sleep_c.connect("clicked",self.on_clicked_sleep_c)
        self.packages_download.connect("clicked",self.on_clicked_packages)

        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.gold, False, False, 0)
        self.box.pack_start(self.packages_download, True, True, 0)
        self.box.pack_start(self.pause, False, False, 0)
        self.box.pack_start(self.settings, False, False, 0)
        self.box.pack_start(self.status, False, False, 0)
        self.box.pack_start(self.headless_c, False, False, 0)
        self.box.pack_start(self.sleep_c, False, False, 0)

        self.connect('delete-event',self.on_delete_event)
        self.set_size_request(200,0)
        self.set_resizable(False)
        self.var = _var

    def get_resource_path(self, rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def displayclock(self):
        tmp="Sell Items = "
        if self.var[0]:
            tmp+= "True"
        else:
            tmp+="False"
        self.sell.set_label(tmp)

        tmp="Take Out Gold = "
        if self.var[1]:
            tmp+="True"
        else:
            tmp+="False"
        self.gold.set_label(tmp)
        
        tmp="Download Packages = "
        if self.var[2]:
            tmp+= "True"
        else:
            tmp+= "False"
        self.packages_download.set_label(tmp)
        return True

    def watch_bot(self):
        if self.var[5]:
            Gtk.main_quit()

    def startclocktimer(self):
        GObject.timeout_add(1000, self.displayclock)
        GObject.timeout_add(1000, self.watch_bot)

    def on_clicked_packages(self, widget):
        if self.var[0] or self.var[1] or self.var[2]:
            Alert().show_all()
        else:
            self.var[2] = 1
            self.packages_download.set_label("Download Packages = True")
        
    def on_delete_event(self, widget, data):
        self.var[4]=1
        Gtk.main_quit()

    def on_clicked_headless_c(self, widget):
        if self.headless_c.get_active():
            self.headless_checked = "True"
        else:
            self.headless_checked = "False"
        config.set("headless","headless", self.headless_checked)
        config_save()

    def on_clicked_sleep_c(self, widget):
        #todo!
        return

    def on_sell_clicked(self, widget):
        if self.var[0] or self.var[1] or self.var[2]:
            Alert().show_all()
        else:
            self.var[0] = 1
            self.sell.set_label("Sell Items = True")

    def on_gold_clicked(self, widget):
        if self.var[0] or self.var[1] or self.var[2]:
            Alert().show_all()
        else:
            self.var[1] = 1
            self.gold.set_label("Take Out Gold = True")

    def on_pause_clicked(self, widget):
        if self.var[3]:
            self.var[3] = 0
            self.pause.set_label("Pause Bot = False")
        else:
            self.var[3] = 1
            self.pause.set_label("Pause Bot = True")

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
        self.farm = Gtk.Button(label="Farm")
        self.food = Gtk.Button(label="Food")
        self.gold = Gtk.Button(label="Gold")
        self.sell = Gtk.Button(label="Sell")
        self.buy = Gtk.Button(label="Buy")
        self.extract = Gtk.Button(label="Extract")

        self.login.connect("clicked",self.on_clicked_login)
        self.farm.connect("clicked",self.on_clicked_farm)
        self.food.connect("clicked", self.on_clicked_food)
        self.gold.connect("clicked", self.on_clicked_gold)
        self.sell.connect("clicked", self.on_clicked_sell)
        self.extract.connect("clicked",self.on_clicked_extract)
        self.buy.connect("clicked",self.on_clicked_buy)

        self.box.pack_start(self.login, False, False, 0)
        self.box.pack_start(self.farm, False, False, 0)
        self.box.pack_start(self.food, False, False, 0)
        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.gold, False, False, 0)
        self.box.pack_start(self.buy, False, False, 0)
        self.box.pack_start(self.extract, False, False, 0)
        
        self.set_size_request(200,0)
        self.set_resizable(False)

    def on_clicked_login(self, widget):
        SettingsLogin().show_all()
    def on_clicked_farm(self, widget):
        SettingsFarm().show_all()
    def on_clicked_food(self, widget):
        SettingsFood().show_all()
    def on_clicked_gold(self, widget):
        SettingsGold().show_all()
    def on_clicked_sell(self, widget):
        SettingsSell().show_all()
    def on_clicked_extract(self, widget):
        SettingsExtract().show_all()
    def on_clicked_buy(self, widget):
        SettingsBuy().show_all()

class SettingsLogin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Login Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.txt_label = Gtk.Label(label="Nickname")
        self.txt = Gtk.Entry()
        self.txt.set_placeholder_text("nickname")
        self.txt.set_text(config.get('login','login'))

        self.psswd_label = Gtk.Label(label="Password")
        self.txt2 = Gtk.Entry()
        self.txt2.set_placeholder_text("password")
        self.txt2.set_invisible_char("*")
        self.txt2.set_visibility(False)
        self.txt2.set_text(config.get('login','password'))

        self.server_label = Gtk.Label(label="Server")
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
        self.server.set_active(self.server_option_load())

        self.box.pack_start(self.txt_label,False,False,0)
        self.box.pack_start(self.txt, False, False, 0)
        self.box.pack_start(self.psswd_label,False,False,0)
        self.box.pack_start(self.txt2, False, False, 0)
        self.box.pack_start(self.server_label,False,False,0)
        self.box.pack_start(self.server, False, False, 0)

        self.connect('delete-event',self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        section = "login"
        config.set(section, "nickname",self.txt.get_text())
        config.set(section, "password", self.txt2.get_text())
        config.set(section, "server", self.server_option_save())
        config_save()

    def server_option_load(self):
        temporary = int(config.get("login","server"))
        if temporary == 1:
            return 0
        elif temporary == 25:
            return 1
        elif temporary == 34:
            return 2
        elif temporary == 35:
            return 3
        elif temporary == 36:
            return 4
        elif temporary == 37:
            return 5
        elif temporary == 38:
            return 6
        elif temporary == 39:
            return 7
        elif temporary == 40:
            return 8

    def server_option_save(self):
        temporary = self.server.get_active()
        if temporary == 0:
            return "1"
        elif temporary == 1:
            return "25"
        elif temporary == 2:
            return "34"
        elif temporary == 3:
            return "35"
        elif temporary == 4:
            return "36"
        elif temporary == 5:
            return "37"
        elif temporary == 6:
            return "38"
        elif temporary == 7:
            return "39"
        elif temporary == 8:
            return "40"

class SettingsFarm(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Farm Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.expedition = Gtk.CheckButton()
        self.expedition.set_active(return_bool("farm","expedition"))
        self.expedition.set_label("Expeditions")

        self.expedition_option = Gtk.ComboBoxText()
        self.expedition_option.set_entry_text_column(0)
        self.expedition_option.append_text("1. First")
        self.expedition_option.append_text("2. Second")
        self.expedition_option.append_text("3. Third")
        self.expedition_option.append_text("4. Fourth")
        self.expedition_option.set_active(int(config.get('farm','expedition_option'))-1)

        self.dungeon = Gtk.CheckButton()
        self.dungeon.set_active(return_bool("farm","dungeon"))
        self.dungeon.set_label("Dungeons")

        self.dungeon_option = Gtk.ComboBoxText()
        self.dungeon_option.set_entry_text_column(0)
        self.dungeon_option.append_text("1. Normal")
        self.dungeon_option.append_text("2. Advenced")
        if not return_bool("farm","dungeon_advenced"):
            self.dungeon_option.set_active(0)
        else:
            self.dungeon_option.set_active(1)

        self.event = Gtk.CheckButton()
        self.event.set_active(return_bool("farm","event"))
        self.event.set_label("Event Wars")

        self.box.pack_start(self.expedition, False, False, 0)
        self.box.pack_start(self.expedition_option, False, False, 0)
        self.box.pack_start(self.dungeon, False, False, 0)
        self.box.pack_start(self.dungeon_option, False, False, 0)
        self.box.pack_start(self.event, False, False, 0)

        self.connect('delete-event',self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        section = "farm"
        config.set(section, "expedition",str(self.expedition.get_active()))
        config.set(section, "expedition_option", str(self.expedition_option.get_active()+1))
        if self.dungeon_option.get_active() == 0:
            config.set(section,"dungeon_advenced","False")
        else:
            config.set(section,"dungeon_advenced","True")
        config.set(section, "dungeon", str(self.dungeon.get_active()))
        config_save()

class SettingsFood(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Food Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.health_label = Gtk.Label(label="Health level")
        self.health_level = Gtk.Entry()
        self.health_level.set_placeholder_text("health level")
        self.health_level.set_text(config.get('heal','health_level'))

        self.food_label = Gtk.Label(label="Food Backpack")
        self.food_option = Gtk.ComboBoxText()
        self.food_option.set_entry_text_column(0)
        self.food_option.append_text("I")
        self.food_option.append_text("II")
        self.food_option.append_text("III")
        self.food_option.append_text("IV")
        self.food_option.append_text("V")
        self.food_option.set_active(read_backpack("backpacks","health_backpack"))

        self.box.pack_start(self.health_label,False,False,0)
        self.box.pack_start(self.health_level, False, False, 0)
        self.box.pack_start(self.food_label, False,False,0)
        self.box.pack_start(self.food_option, False, False, 0)

        self.connect('delete-event',self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        config.set("backpacks", "health_backpack", save_backpack(self.food_option.get_active()))
        config_save()

class SettingsGold(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gold Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.pack = Gtk.CheckButton()
        self.pack.set_active(return_bool("pack_gold","pack_gold"))
        self.pack.set_label("Pack Gold")

        self.pack_level = Gtk.Entry()
        self.pack_level.set_placeholder_text("minimum gold level")
        self.pack_level.set_text(config.get('pack_gold','pack_level'))

        self.gold_limit = Gtk.CheckButton()
        self.gold_limit.set_active(return_bool("take_gold","take_gold"))
        self.gold_limit.set_label("Max Gold To Take Out")

        self.gold_limit_level = Gtk.Entry()
        self.gold_limit_level.set_placeholder_text("gold limit")
        self.gold_limit_level.set_text(config.get('take_gold','take_gold_limit'))

        self.box.pack_start(self.pack, False, False, 0)
        self.box.pack_start(self.pack_level, False, False, 0)
        self.box.pack_start(self.gold_limit, False, False, 0)
        self.box.pack_start(self.gold_limit_level, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)
    
    def save_settings(self, widget, data):
        config.set('pack_gold','pack_gold',str(self.pack.get_active()))
        config.set('pack_gold','pack_level',self.pack_level.get_text())
        config.set('take_gold','take_gold',str(self.gold_limit.get_active()))
        config.set('take_gold','take_gold_limit',self.gold_limit_level.get_text())
        config_save()

class SettingsSell(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Sell Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.sell = Gtk.CheckButton()
        self.sell.set_active(return_bool("sell_items","sell_items"))
        self.sell.set_label("Sell Items")

        self.sell_option = Gtk.ComboBoxText()
        self.sell_option.set_entry_text_column(0)
        self.sell_option.append_text("I")
        self.sell_option.append_text("II")
        self.sell_option.append_text("III")
        self.sell_option.append_text("IV")
        self.sell_option.append_text("V")
        self.sell_option.set_active(read_backpack('backpacks','free_backpack'))

        self.red = Gtk.CheckButton()
        self.red.set_label("Red")
        self.red.set_active(return_bool("sell_items","red"))

        self.orange = Gtk.CheckButton()
        self.orange.set_label("Orange")
        self.orange.set_active(return_bool("sell_items","orange"))

        self.purple = Gtk.CheckButton()
        self.purple.set_label("Purple")
        self.purple.set_active(return_bool("sell_items","purple"))

        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.sell_option, False, False, 0)
        self.box.pack_start(self.purple, False, False, 0)
        self.box.pack_start(self.orange, False, False, 0)
        self.box.pack_start(self.red, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def return_bool(self, string):
        if config.get('sell',string) == "True":
            return True
        else:
            return False

    def save_settings(self, widget, data):
        config.set("sell_items","sell_items", str(self.sell.get_active()))
        config.set("sell_items","purple",str(self.purple.get_active()))
        config.set("sell_items","orange",str(self.orange.get_active()))
        config.set("sell_items","red",str(self.red.get_active()))
        config.set("backpacks","free_backpack",save_backpack(self.sell_option.get_active()))
        config_save()

class SettingsExtract(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Extract Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.extract = Gtk.CheckButton()
        self.extract.set_active(return_bool("extract","extract"))
        self.extract.set_label("Extract Items")

        self.extract_option = Gtk.ComboBoxText()
        self.extract_option.set_entry_text_column(0)
        self.extract_option.append_text("I")
        self.extract_option.append_text("II")
        self.extract_option.append_text("III")
        self.extract_option.append_text("IV")
        self.extract_option.append_text("V")
        self.extract_option.set_active(read_backpack('backpacks','extract_backpack'))

        self.purple = Gtk.CheckButton()
        self.purple.set_active(return_bool("extract","purple"))
        self.purple.set_label("Purple")

        self.orange = Gtk.CheckButton()
        self.orange.set_active(return_bool("extract","orange"))
        self.orange.set_label("Orange")

        self.red = Gtk.CheckButton()
        self.red.set_active(return_bool("extract","red"))
        self.red.set_label("Red")

        self.box.pack_start(self.extract, False, False, 0)
        self.box.pack_start(self.extract_option, False, False, 0)
        self.box.pack_start(self.purple, False, False, 0)
        self.box.pack_start(self.orange, False, False, 0)
        self.box.pack_start(self.red, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        config.set("extract",'extract',str(self.extract.get_active()))
        config.set("backpacks",'extract_backpack',save_backpack(self.extract_option.get_active()))
        config.set("extract",'purple',str(self.purple.get_active()))
        config.set("extract",'orange',str(self.orange.get_active()))
        config.set("extract",'red',str(self.red.get_active()))
        config_save()

class SettingsBuy(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Buy Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.pages_label = Gtk.Label(label="Pages of food")
        self.pages = Gtk.Entry()
        self.pages.set_placeholder_text("pages of food")
        self.pages.set_text(config.get('auction_house','food_pages'))

        self.boost_label = Gtk.Label(label="Boosters per type")
        self.boosters_txt = Gtk.Entry()
        self.boosters_txt.set_placeholder_text("boosters of one type")
        self.boosters_txt.set_text(config.get('auction_house','boosters_per_type'))

        self.diff_label = Gtk.Label(label="Maximum difference")
        self.diff = Gtk.Entry()
        self.diff.set_placeholder_text("difference between value and price")
        self.diff.set_text(config.get('auction_house','highest_difference'))

        self.rings = Gtk.CheckButton()
        self.rings.set_active(return_bool('auction_house','rings'))
        self.rings.set_label("Rings")

        self.amulets = Gtk.CheckButton()
        self.amulets.set_active(return_bool('auction_house','amulets'))
        self.amulets.set_label("Amulets")

        self.boosters = Gtk.CheckButton()
        self.boosters.set_active(return_bool('auction_house','boosters'))
        self.boosters.set_label("Boosters")

        self.food = Gtk.CheckButton()
        self.food.set_active(return_bool('auction_house','food'))
        self.food.set_label("Food")

        self.box.pack_start(self.pages_label,False,False,0)
        self.box.pack_start(self.pages, False, False, 0)
        self.box.pack_start(self.boost_label,False,False,0)
        self.box.pack_start(self.boosters_txt, False, False, 0)
        self.box.pack_start(self.diff_label,False,False,0)
        self.box.pack_start(self.diff, False, False, 0)
        self.box.pack_start(self.rings, False, False, 0)
        self.box.pack_start(self.amulets, False, False, 0)
        self.box.pack_start(self.boosters, False, False, 0)
        self.box.pack_start(self.food, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        section = "auction_house"
        config.set(section,"food_pages",self.pages.get_text())
        config.set(section,"boosters_per_type",self.boosters_txt.get_text())
        config.set(section,"highest_difference",self.diff.get_text())
        config.set(section,"rings",str(self.rings.get_active()))
        config.set(section,"amulets",str(self.amulets.get_active()))
        config.set(section,"boosters",str(self.boosters.get_active()))
        config.set(section,"food",str(self.food.get_active()))
        config_save()

def return_bool(section, string):
    if config.get(section, string) == "True":
        return True
    else:
        return False

def save_backpack(option):
    if option == 0:
        return "512"
    elif option == 1:
        return "513"
    elif option == 2:
        return "514"
    elif option == 3:
        return "515"
    elif option == 4:
        return "516"

def read_backpack(section, variable):
    backpack = config.get(section, variable)
    if backpack == "512":
        return 0
    elif backpack == "513":
        return 1
    elif backpack == "514":
        return 2
    elif backpack == "515":
        return 3
    elif backpack == "516":
        return 4

def config_save():
    with open('config35.ini','w') as file:
        config.write(file)

variables = Array('i',range(6))
for i in range(6):
    variables[i] = 0

p2 = Process(target=main_loop, args=(variables,))
p2.start()

mWindow = MainWindow(variables)
mWindow.show_all()
mWindow.startclocktimer()
Gtk.main()