from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


import data_manager
from reminder import Reminder

Builder.load_file('View/notificationCard/notification_card.kv')

class NotificationCard(MDBoxLayout):
    id_name = StringProperty()
    task_name = StringProperty()
    message = StringProperty()
    period_time = StringProperty()
    start_time = StringProperty()
    how_many_times_in_day = StringProperty()
    is_active = StringProperty()
    date_range = StringProperty()
    long_course = StringProperty()
    long_day_text = StringProperty()
    db_name = 'reminder.db'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data_manager.ReminderDB.check_db(self)
        self.register_event_type("on_release")
        self.my_reminder = None
        self.on_off_notification(self, self.is_active)


    def on_off_notification(self, instance, is_active):
        is_active = str(is_active)
        if is_active == 'True':
            self.is_active = 'True'
            data_manager.ReminderDB.change_is_active_to_true(self, self.id_name)
            self.ids.on_off_switch_notification.active = True
            if self.my_reminder is None:
                self.my_reminder = Reminder(self, self.id_name)
            self.my_reminder.start()
        if is_active == 'False':
            if self.my_reminder is not None:
                self.my_reminder.stop()
                self.my_reminder = None
            self.is_active = 'False'
            data_manager.ReminderDB.change_is_active_to_false(self, self.id_name)
            self.ids.on_off_switch_notification.active = False


    def set_long_day(self, long_day):
        data_manager.ReminderDB.update_long_course(self, self.id_name, long_day)

    def set_date_range(self, date_range):
        data_manager.ReminderDB.update_date_range(self, self.id_name, date_range)

    def off_button_switch(self, instance):
        self.ids.on_off_switch_notification.active = False

    def on_release(self):
        pass


