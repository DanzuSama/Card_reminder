from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from datetime import datetime
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
import data_manager
from View.Screen_1.main_screen import MyFirstLayout

Builder.load_file('View/Screen_2/second_screen.kv')

global data_list
global long_course_days

data_list = []


class MySecondLayout(Screen):
    dialog = None
    db_name = 'reminder.db'


    def __init__(self, **kwargs):
        super(MySecondLayout, self).__init__(**kwargs)
        data_manager.ReminderDB.check_db(self)

# Method for button saver and go to first screen
    def create_new_task(self):
        if self.save_reminder(self):
            screen_manager = self.manager
            screen_manager.current = 'first'
            MyFirstLayout().clear_widgets()
        else:
            pass
#### Method for button saver and go to first screen

# Method for back button
    def go_to_first_screen(self):
        MyFirstLayout().clear_widgets()
        screen_manager = self.manager
        screen_manager.current = 'first'

### Method for back button

# Button for date picker and time picker
    def on_active(self,segmented_control: MDSegmentedControl,segmented_item: MDSegmentedControlItem,) -> None:
        '''Called when the segment is activated.'''
        if segmented_item.text == 'Date':
            self.show_date_picker()
        elif segmented_item.text == 'Time':
            self.add_remainder()
### Button for date picker and time picker

#saving data and upload to database
    def save_reminder(self, instance):
        task_name = self.ids.text_name_of_remainder.text
        message = self.ids.message_of_remainder.text
        period_time = self.ids.btn_date_picker.text
        start_time = self.ids.btn_add_remainder.text
        how_many_times_in_day = self.ids.reminder_view.text
        is_active = 'True'
        date_range = str(data_list)
        if task_name == '' or period_time == 'Pick a date' or start_time == 'Cancelled time' or period_time == 'Cancelled':
            self.show_alert_dialog()
            return False
        else:
            long_course = self.long_course_days
            data_manager.ReminderDB.add_reminder(self, task_name, message, period_time, start_time, how_many_times_in_day, is_active, date_range, long_course)
            self.ids.text_name_of_remainder.text = ''
            self.ids.message_of_remainder.text = ''
            self.ids.btn_date_picker.text = ''
            self.ids.btn_add_remainder.text = ''
            self.ids.reminder_view.text = ''
            self.ids.long_course.title = ''
            data_list.clear()
            return True
###End of method saving data


#Alert dialog
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Missing date, name or time",
                buttons=[
                    MDFlatButton(
                        text='I understand',
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()
### END Alert dialog

    def close_dialog(self, obj):
        self.dialog.dismiss()

#Create method for date_picker
    def on_save(self, instance, value, date_range):
        # self.ids.btn_date_picker.text = str(value)
        if (len(date_range) == 0):
            self.ids.btn_date_picker.text = 'Pick a date'
        else:
            #            self.update_layout('Date')
            self.ids.btn_date_picker.text = str(f'{date_range[0]} - {date_range[-1]}')
            data_list.append(date_range)
        self.long_course_days = len(date_range)
        self.ids.long_course.title = f'{len(date_range)} days long'

    def on_cancel(self, instance, value):
        self.ids.btn_date_picker.text = 'Cancelled'

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
###End of method for date_picker

#Create method for time_picker
    def get_date(self, date):
        print(date)

    def on_save_time(self, instance, value):
        self.ids.btn_add_remainder.text = str(value)
        time_saver = value

    def on_cancel_time(self, instance, value):
        self.ids.btn_add_remainder.text = 'Cancelled time'

    def add_remainder(self):
        # Define time
        default_time = datetime.strptime(datetime.now().strftime('%H:%M'), '%H:%M')
        time_dialog = MDTimePicker()
        # Set default time
        time_dialog.set_time(default_time)
        time_dialog.bind(on_save=self.on_save_time, on_cancel=self.on_cancel_time)
        time_dialog.open()
### End of method for time_picker
