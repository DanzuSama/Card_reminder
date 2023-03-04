from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

import data_manager
import reminder

Builder.load_file('View/Screen3/check_view_screen.kv')



class CheckViewScreen(Screen):
    db_name = 'reminder.db'
    current_id_tag = StringProperty()



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data_manager.ReminderDB.check_db(self)


    def __enter__(self):
        self.update_widget()

    def on_tap_back_button(self):
        self.manager.current = 'first'

    def on_current_id_tag(self, instance, value) -> None:
        data_for_cards = data_manager.ReminderDB.clean_data_from_db_use_id(self, int(self.current_id_tag))
        self.ids.name_form.text = data_for_cards[1]
        self.ids.message_form.text = data_for_cards[2]
        self.ids.period_form.text = data_for_cards[3]
        self.ids.time_form.text = data_for_cards[4]
        self.ids.how_time_form.text = data_for_cards[5]
        self.ids.long_form.text = data_for_cards[8]


    def on_tap_delete_button(self):
        data_manager.ReminderDB.delete_reminder(self, int(self.current_id_tag))
        self.manager.current = 'first'



    def update_reminder(self) -> None:
        self.screen_manager = self.manager
        self.screen_manager.get_screen('update_screen').current_id_tag = self.current_id_tag
        self.screen_manager.current = 'update_screen'



