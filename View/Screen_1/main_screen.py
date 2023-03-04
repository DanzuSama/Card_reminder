from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.material_resources import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

import data_manager
from View import notificationCard
from View.notificationCard.notification_card import NotificationCard

Builder.load_file('View/Screen_1/main_screen.kv')

global is_active


class MyFirstLayout(Screen):
    dialog = None
    manager = ObjectProperty()
    db_name = 'reminder.db'
    alert_dialog = ObjectProperty()

    def __init__(self, **kwargs):
        super(MyFirstLayout, self).__init__(**kwargs)
        self.screen_manager = None
        data_manager.ReminderDB.check_db(self)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Update",
                "height": dp(56),
                "on_release": lambda x=f"Update": self.update_callback(),
            },
            {
                "viewclass": "OneLineListItem",
                "text": f"Change theme",
                "height": dp(56),
                "on_release": lambda x='Change theme': self.change_theme_callback(),
            }
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

    def go_to_second_screen(self):
        screen_manager = self.manager
        screen_manager.current = 'second'

    def on_enter(self, *args):
        self.generate_cards()

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()

    def update_callback(self):
        self.menu.dismiss()
        self.update_cards()
        self.create_widget('Update cards')

    def change_theme_callback(self):
        print('change_theme_callback')
        self.menu.dismiss()

    ###Create widget for notification
    def create_widget(self, text_to_display):
        label = Label(text=text_to_display,
                      size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'y': 0},
                      size=(400, 50))
        # Add widget to display
        self.ids.MainBox.add_widget(label)
        # Delete widget after 10 seconds
        Clock.schedule_once(lambda dt: self.ids.MainBox.remove_widget(label), 10)

    ######button for end notification

    def update_cards(self):
        self.generate_cards()

    # Generate cards for main screen
    def generate_cards(self):
        # Update the list of cards
        self.ids.remainder_list.clear_widgets()
        if not self.ids.remainder_list.children:
            for temp_id in data_manager.ReminderDB.get_ids_from_db(self):
                data_for_cards = data_manager.ReminderDB.clean_data_from_db_use_id(self, int(temp_id[-1]))
                long_course = data_for_cards[8]
                long_day_text = 'days left'
                if long_course == 1 or long_course == 0 or long_course == '1' or long_course == '0':
                    long_day_text = 'day left'
                card = NotificationCard(
                    id_name=str(data_for_cards[0]),
                    task_name=str(data_for_cards[1]),
                    message=str(data_for_cards[2]),
                    period_time=str(data_for_cards[3]),
                    start_time=str(data_for_cards[4]),
                    how_many_times_in_day=str(data_for_cards[6]),
                    is_active=str(data_for_cards[6]),
                    date_range=str(data_for_cards[7]),
                    long_course=str(data_for_cards[8]),
                    long_day_text=long_day_text,
                )
                callback = self.on_tap_notification_plus_button
                card.bind(on_release=lambda x=card: callback(x))
                self.ids.remainder_list.add_widget(card)

    def on_tap_notification_plus_button(
            self, instance_card: notificationCard.notification_card
    ) -> None:
        self.screen_manager = self.manager
        task_id = instance_card.id_name

        self.screen_manager.get_screen('check_view').current_id_tag = task_id
        self.screen_manager.current = 'check_view'
