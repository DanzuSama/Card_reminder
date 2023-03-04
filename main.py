from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDFadeSlideTransition
from View.Screen3 import check_view_screen
from View.Screen_1 import main_screen
from View.Screen_2 import second_screen
from View.Screen_4 import update_screen


Window.size = (500, 800)



class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        self.manager_screen = MDScreenManager(transition=MDFadeSlideTransition())
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(main_screen.MyFirstLayout(name='first'))
        self.add_widget(second_screen.MySecondLayout(name='second'))
        self.add_widget(check_view_screen.CheckViewScreen(name='check_view'))
        self.add_widget(update_screen.UpdateScreen(name='update_screen'))



class MyApp(MDApp):
    theme_cls = ThemeManager()

    def __init__(self):
        super().__init__()
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '800'
        self.title = 'Reminder App'
        self.manager_screen = MyScreenManager()



    def build(self) -> MDScreenManager:
        return self.manager_screen


if __name__ == '__main__':

    MyApp().run()

print('hello')
def switch_theme_style():
    return None