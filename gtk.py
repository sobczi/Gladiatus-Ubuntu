import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from configparser import SafeConfigParser
import re
import os

config = SafeConfigParser()
config.read('config.ini')

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

        self.sell = Gtk.Button(label="Sell Items = False")
        self.gold = Gtk.Button(label="Take Out Gold = False")
        self.pause = Gtk.Button(label="Pause Bot = False")
        self.headless = Gtk.Button(label="Headless Mode = False")
        self.sleep = Gtk.Button(label="Sleep Mode = False")
        self.settings = Gtk.Button(label="Open Settings")
        self.status = Gtk.Button(label="Show Current Info")
        
        self.headless_checked = False
        if config.get('top', 'headless') == "True":
            self.headless_checked = True
        self.headless_c = Gtk.CheckButton()
        self.headless_c.set_active(self.headless_checked)
        self.headless_c.set_label("Headless Mode")

        self.sleep_checked = False
        if config.get('top','sleep') == "True":
            self.sleep_checked = True
        self.sleep_c = Gtk.CheckButton()
        self.sleep_c.set_active(self.sleep_checked)
        self.sleep_c.set_label("Sleep Mode")

        self.sell.connect("clicked",self.on_sell_clicked)
        self.gold.connect("clicked",self.on_gold_clicked)
        self.pause.connect("clicked",self.on_pause_clicked)
        self.headless.connect("clicked",self.on_headless_clicked)
        self.sleep.connect("clicked",self.on_sleep_clicked)
        self.settings.connect("clicked",self.on_settings_clicked)
        self.status.connect("clicked",self.on_status_clicked)
        self.headless_c.connect("clicked", self.on_clicked_headless_c)
        self.sleep_c.connect("clicked",self.on_clicked_sleep_c)

        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.gold, False, False, 0)
        self.box.pack_start(self.pause, False, False, 0)
        self.box.pack_start(self.headless, False, False, 0)
        self.box.pack_start(self.sleep, False, False, 0)
        self.box.pack_start(self.settings, False, False, 0)
        self.box.pack_start(self.status, False, False, 0)
        self.box.pack_start(self.headless_c, False, False, 0)
        self.box.pack_start(self.sleep_c, False, False, 0)

        self.connect('delete-event',self.on_delete_event)
        self.set_size_request(200,0)
        self.set_resizable(False)


    def on_delete_event(self, widget, data):
        s = 'top'
        config.set(s,'force_headless','False')
        config.set(s,'force_sleep','False')
        config.set(s,'force_sell','False')
        config.set(s,'force_gold','False')
        config_save()
        Gtk.main_quit()

    def on_clicked_headless_c(self, widget):
        section = "top"
        if self.headless_c.get_active():
            self.headless_checked = "True"
        else:
            self.headless_checked = "False"
        config.set(section,"headless", self.headless_checked)
        config_save()

    def on_clicked_sleep_c(self, widget):
        section = "top"
        if self.sleep_c.get_active():
            self.sleep_checked = "True"
        else:
            self.sleep_checked = "False"
        config.set(section, "sleep", self.sleep_checked)
        config_save()

    def on_sell_clicked(self, widget):
        if config.get('top','force_gold') == "True" or config.get('top','force_sell') == "True":
            Alert().show_all()
        else:
            config.set('top','force_sell','True')
            self.sell.set_label("Sell Items = True")
        config_save()

    def on_gold_clicked(self, widget):
        if config.get('top','force_sell') == "True" or config.get('top','force_gold') == "True":
            Alert().show_all()
        else:
            config.set('top','force_gold','True')
            self.gold.set_label("Take Out Gold = True")
        config_save()

    def on_pause_clicked(self, widget):
        if config.get('top','pause') == "True":
            config.set('top','pause','False')
            self.pause.set_label("Pause Bot = False")
        else:
            config.set('top','pause','True')
            self.pause.set_label("Pause Bot = True")
        config_save()

    def on_headless_clicked(self, widget):
        if config.get('top','force_headless') == "True":
            config.set('top','force_headless','False')
            self.headless.set_label("Headless Mode = False")
        else:
            config.set('top','force_headless','True')
            self.headless.set_label("Headless Mode = True")
        config_save()

    def on_sleep_clicked(self, widget):
        if config.get('top','force_sleep') == "True":
            config.set('top','force_sleep','False')
            self.sleep.set_label("Sleep Mode = False")
        else:
            config.set('top','force_sleep','True')
            self.sleep.set_label("Sleep Mode = True")
        config_save()
        
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

        self.txt = Gtk.Entry()
        self.txt.set_placeholder_text("nickname")
        self.txt.set_text(config.get('login','nickname'))

        self.txt2 = Gtk.Entry()
        self.txt2.set_placeholder_text("password")
        self.txt2.set_invisible_char("*")
        self.txt2.set_visibility(False)
        self.txt2.set_text(config.get('login','password'))

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
        self.server.set_active(int(config.get('login','server')))

        self.box.pack_start(self.txt, False, False, 0)
        self.box.pack_start(self.txt2, False, False, 0)
        self.box.pack_start(self.server, False, False, 0)

        self.connect('delete-event',self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        section = "login"
        config.set(section, "nickname",self.txt.get_text())
        config.set(section, "password", self.txt2.get_text())
        config.set(section, "server", str(self.server.get_active()))
        config_save()
        return

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
        self.expedition_option.set_active(int(config.get('farm','expedition_option')))

        self.dungeon = Gtk.CheckButton()
        self.dungeon.set_active(return_bool("farm","dungeon"))
        self.dungeon.set_label("Dungeons")

        self.dungeon_option = Gtk.ComboBoxText()
        self.dungeon_option.set_entry_text_column(0)
        self.dungeon_option.append_text("1. Normal")
        self.dungeon_option.append_text("2. Advenced")
        self.dungeon_option.set_active(int(config.get('farm','dungeon_option')))

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
        config.set(section, "expedition_opton", str(self.expedition_option.get_active()))
        config.set(section, "dungeon", str(self.dungeon.get_active()))
        config.set(section, "dungeon_option", str(self.dungeon_option.get_active()))
        return

class SettingsFood(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Food Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.heal = Gtk.CheckButton()
        self.heal.set_active(return_bool("food","heal"))
        self.heal.set_label("Healing Bot")

        self.health_level = Gtk.Entry()
        self.health_level.set_placeholder_text("health level")
        self.health_level.set_text(config.get('food','heal_level'))

        self.food = Gtk.CheckButton()
        self.food.set_active(return_bool("food","food"))
        self.food.set_label("Refill Food [Backpack]")

        self.food_option = Gtk.ComboBoxText()
        self.food_option.set_entry_text_column(0)
        self.food_option.append_text("I")
        self.food_option.append_text("II")
        self.food_option.append_text("III")
        self.food_option.append_text("IV")
        self.food_option.append_text("V")
        self.food_option.set_active(int(config.get('food','food_option')))

        self.box.pack_start(self.heal, False, False, 0)
        self.box.pack_start(self.health_level, False, False, 0)
        self.box.pack_start(self.food, False, False, 0)
        self.box.pack_start(self.food_option, False, False, 0)

        self.connect('delete-event',self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)


    def save_settings(self, widget, data):
        section = "food"
        config.set(section, "food", str(self.food.get_active()))
        config.set(section, "food_option", str(self.food_option.get_active()))
        config_save()
        return

class SettingsGold(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gold Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.pack = Gtk.CheckButton()
        self.pack.set_active(return_bool("gold","pack"))
        self.pack.set_label("Pack Gold")

        self.pack_level = Gtk.Entry()
        self.pack_level.set_placeholder_text("minimum gold level")
        self.pack_level.set_text(config.get('gold','pack_level'))

        self.gold_limit = Gtk.CheckButton()
        self.gold_limit.set_active(return_bool("gold","gold_limit"))
        self.gold_limit.set_label("Max Gold To Take Out")

        self.gold_limit_level = Gtk.Entry()
        self.gold_limit_level.set_placeholder_text("gold limit")
        self.gold_limit_level.set_text(config.get('gold','gold_limit_level'))

        self.box.pack_start(self.pack, False, False, 0)
        self.box.pack_start(self.pack_level, False, False, 0)
        self.box.pack_start(self.gold_limit, False, False, 0)
        self.box.pack_start(self.gold_limit_level, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)
    
    def save_settings(self, widget, data):
        section = "gold"
        config.set(section,'pack',str(self.pack.get_active()))
        config.set(section,'pack_level',self.pack_level.get_text())
        config.set(section,'gold_limit',str(self.gold_limit.get_active()))
        config.set(section,'gold_limit_level',self.gold_limit_level.get_text())
        config_save()

class SettingsSell(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Sell Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.sell = Gtk.CheckButton()
        self.sell.set_active(return_bool("sell","sell"))
        self.sell.set_label("Sell Items")

        self.weapons = Gtk.CheckButton()
        self.weapons.set_active(return_bool("sell","weapons"))
        self.weapons.set_label("weapons")

        self.shields = Gtk.CheckButton()
        self.shields.set_active(return_bool("sell","shields"))
        self.shields.set_label("shields")

        self.plates = Gtk.CheckButton()
        self.plates.set_active(return_bool("sell","plates"))
        self.plates.set_label("plates")

        self.helmets = Gtk.CheckButton()
        self.helmets.set_active(return_bool("sell","helmets"))
        self.helmets.set_label("helmets")

        self.hands = Gtk.CheckButton()
        self.hands.set_active(return_bool("sell","hands"))
        self.hands.set_label("hands")

        self.boots = Gtk.CheckButton()
        self.boots.set_active(return_bool("sell","boots"))
        self.boots.set_label("boots")

        self.rings = Gtk.CheckButton()
        self.rings.set_active(return_bool("sell","rings"))
        self.rings.set_label("rings")

        self.amulets = Gtk.CheckButton()
        self.amulets.set_active(return_bool("sell","amulets"))
        self.amulets.set_label("amulets")

        self.boosters = Gtk.CheckButton()
        self.boosters.set_active(return_bool("sell","boosters"))
        self.boosters.set_label("boosters")

        self.bonuses = Gtk.CheckButton()
        self.bonuses.set_active(return_bool("sell","bonuses"))
        self.bonuses.set_label("bonuses")

        self.blessings = Gtk.CheckButton()
        self.blessings.set_active(return_bool("sell","blessings"))
        self.blessings.set_label("blessings")

        self.scrolls = Gtk.CheckButton()
        self.scrolls.set_active(return_bool("sell","scrolls"))
        self.scrolls.set_label("scrolls")

        self.sell_option = Gtk.ComboBoxText()
        self.sell_option.set_entry_text_column(0)
        self.sell_option.append_text("I")
        self.sell_option.append_text("II")
        self.sell_option.append_text("III")
        self.sell_option.append_text("IV")
        self.sell_option.append_text("V")
        self.sell_option.set_active(int(config.get('sell','sell_option')))

        self.box.pack_start(self.sell, False, False, 0)
        self.box.pack_start(self.sell_option, False, False, 0)
        self.box.pack_start(self.weapons, False, False, 0)
        self.box.pack_start(self.shields, False, False, 0)
        self.box.pack_start(self.plates, False, False, 0)
        self.box.pack_start(self.helmets, False, False, 0)
        self.box.pack_start(self.hands, False, False, 0)
        self.box.pack_start(self.boots, False, False, 0)
        self.box.pack_start(self.rings, False, False, 0)
        self.box.pack_start(self.amulets, False, False, 0)
        self.box.pack_start(self.boosters, False, False, 0)
        self.box.pack_start(self.bonuses, False, False, 0)
        self.box.pack_start(self.blessings, False, False, 0)
        self.box.pack_start(self.scrolls, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)


    def return_bool(self, string):
        if config.get('sell',string) == "True":
            return True
        else:
            return False

    def save_settings(self, widget, data):
        section = "sell"
        config.set(section,'sell', str(self.sell.get_active()))
        config.set(section,'sell_option',str(self.sell_option.get_active()))
        config.set(section,'weapons',str(self.weapons.get_active()))
        config.set(section,'shields',str(self.shields.get_active()))
        config.set(section,'plates',str(self.plates.get_active()))
        config.set(section,'helmets',str(self.helmets.get_active()))
        config.set(section,'hands',str(self.hands.get_active()))
        config.set(section,'boots',str(self.boots.get_active()))
        config.set(section,'rings',str(self.rings.get_active()))
        config.set(section,'amulets',str(self.amulets.get_active()))
        config.set(section,'boosters',str(self.boosters.get_active()))
        config.set(section,'bonuses',str(self.bonuses.get_active()))
        config.set(section,'blessings',str(self.blessings.get_active()))
        config.set(section,'scrolls',str(self.scrolls.get_active()))
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
        self.extract_option.set_active(int(config.get('extract','extract_option')))

        self.components = Gtk.CheckButton()
        self.components.set_active(return_bool("extract","send_components"))
        self.components.set_label("Send Components")

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
        self.box.pack_start(self.components, False, False, 0)
        self.box.pack_start(self.purple, False, False, 0)
        self.box.pack_start(self.orange, False, False, 0)
        self.box.pack_start(self.red, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        section = "extract"
        config.set(section,'extract',str(self.extract.get_active()))
        config.set(section,'extract_option',str(self.extract_option.get_active()))
        config.set(section,'components',str(self.components.get_active()))
        config.set(section,'purple',str(self.purple.get_active()))
        config.set(section,'orange',str(self.orange.get_active()))
        config.set(section,'red',str(self.red.get_active()))
        config_save()

class SettingsBuy(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Buy Settings")
        self.box = Gtk.VBox(spacing=5)
        self.add(self.box)

        self.pages = Gtk.Entry()
        self.pages.set_placeholder_text("pages of food")
        self.pages.set_text(config.get('buy','food_pages'))

        self.boosters_txt = Gtk.Entry()
        self.boosters_txt.set_placeholder_text("boosters of one type")
        self.boosters_txt.set_text(config.get('buy','boosters_type'))

        self.diff = Gtk.Entry()
        self.diff.set_placeholder_text("difference between value and price")
        self.diff.set_text(config.get('buy','difference'))

        self.rings = Gtk.CheckButton()
        self.rings.set_active(return_bool('buy','rings'))
        self.rings.set_label("Rings")

        self.amulets = Gtk.CheckButton()
        self.amulets.set_active(return_bool('buy','amulets'))
        self.amulets.set_label("Amulets")

        self.boosters = Gtk.CheckButton()
        self.boosters.set_active(return_bool('buy','boosters'))
        self.boosters.set_label("Boosters")

        self.food = Gtk.CheckButton()
        self.food.set_active(return_bool('buy','food'))
        self.food.set_label("Food")

        self.box.pack_start(self.pages, False, False, 0)
        self.box.pack_start(self.boosters_txt, False, False, 0)
        self.box.pack_start(self.diff, False, False, 0)
        self.box.pack_start(self.rings, False, False, 0)
        self.box.pack_start(self.amulets, False, False, 0)
        self.box.pack_start(self.boosters, False, False, 0)
        self.box.pack_start(self.food, False, False, 0)

        self.connect('delete-event', self.save_settings)
        self.set_size_request(200,0)
        self.set_resizable(False)

    def save_settings(self, widget, data):
        section = "buy"
        config.set(section,"food_pages",self.pages.get_text())
        config.set(section,"boosters_type",self.boosters_txt.get_text())
        config.set(section,"difference",self.diff.get_text())
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

def config_save():
    with open('config.ini','w') as file:
        config.write(file)
    return
mWindow = MainWindow()
mWindow.show_all()

Gtk.main()