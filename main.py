import time
from threading import Thread
from tkinter import Label

import kivy
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
#import boolean property
from kivy.properties import BooleanProperty


Window.size = (200, 150)
Window.minimum_width, Window.minimum_height = Window.size
prev = curr = Window.size


class LabeledRadioButton(GridLayout):
    text = StringProperty()
    active = BooleanProperty()

    def changeTime(self, country):
        global adder
        adder = conts[country]


adder = 1
conts = {'New York': -4, 'Los Angeles': -7, 'London': 1, 'Rome': 2,
         'Paris': 2, 'Sydney': 10, 'Tokyo': 9, 'United Arab\nEmirates': 4}


class MainWindow(Screen):
    
    def updateTime(self):
        
        while True:
            timeString = time.gmtime()
            timeString = f"{(timeString.tm_hour+adder)%24:02d}:{timeString.tm_min:02d}:{timeString.tm_sec:02d}"
            self.ids.time_label.text = timeString
            time.sleep(.1)
    
    @mainthread
    def changeWindowCondition(self, *args):
        global adder, prev, curr
        prev, curr = curr, Window.size
        if prev != curr:
            if curr[0] < 755 or curr[1] < 312:
                    if self.ids.countries.children:
                        self.ids.countries.clear_widgets()
            else:
                    if len(self.ids.countries.children) == 0:
                        self.on_enter()

    def hide_widget(self, wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

    def r(self):
        timeThread = Thread(target=self.updateTime)
        timeThread.daemon = True
        timeThread.start()

    radioButs = {}

    def on_enter(self, **kwargs):
        global adder
        self.ids.countries.clear_widgets()
        self.r()
        for country in self.manager.get_screen('setts').ids.countries.children:
            if country.state == 'down':
                temp = LabeledRadioButton(
                    text=country.text, on_active=lambda temp: self.changeTime(temp.text))
                #temp.bind(on_release=lambda x:eval(f"self.changeTime('{country.text}')"))

                self.ids.countries.add_widget(temp)
                self.radioButs[country.text] = temp
        adder = 1

    def changeWindowSize(self):
        if Window.size[0] < 700 or Window.size[1] < 500:
            Window.size = (700, 500)
        Window.minimum_width, Window.minimum_height = (700, 500)


class SecondWindow(Screen):

    def changeWindowSize(self):
        if Window.size[0] < 200 or Window.size[1] < 150:
            Window.size = (200, 150)
        Window.minimum_width, Window.minimum_height = (200, 150)


class StartUp(Screen):
    pass


class W(ScreenManager):
    pass


f = Builder.load_file(filename=r"./style.kv")


class MainApp(App):
    def build(self):
        self.f = f
        return self.f


if __name__ == '__main__':
    MainApp().run()
