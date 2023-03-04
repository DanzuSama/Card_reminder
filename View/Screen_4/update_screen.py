from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from datetime import datetime
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
import data_manager
from View.Screen_1.main_screen import MyFirstLayout

Builder.load_file('View/Screen_4/update_screen.kv')

global data_list
global long_course_days

data_list = []

class UpdateScreen(Screen):
    dialog = None
    db_name = 'reminder.db'
    current_id_tag = StringProperty()
    current_name_tag = StringProperty()
    current_message_tag = StringProperty()
    current_period_time_tag = StringProperty()
    current_start_time_tag = StringProperty()
    current_how_many_times_in_day_tag = StringProperty()



    def __init__(self, **kwargs):
        super(UpdateScreen, self).__init__(**kwargs)
        data_manager.ReminderDB.check_db(self)

    def on_current_id_tag(self, instance, value) -> None:
        temp_id = self.current_id_tag
        temp_data = data_manager.ReminderDB.clean_data_from_db_use_id(self, int(temp_id))
        self.ids.upload_name_of_remainder.text = temp_data[1]
        self.ids.upload_message_of_remainder.text = temp_data[2]
        self.ids.btn_date_picker.text = temp_data[3]
        self.ids.btn_add_remainder.text = temp_data[4]
        self.ids.upload_reminder_view.text = temp_data[5]
        if len(temp_data[8]) == 0 or len(temp_data[8]) == 1 or len(temp_data[8]) == '0' or len(temp_data[8]) == '1':
            self.ids.long_course.title = str(temp_data[8]) + ' day'
        else:
            self.ids.long_course.title = str(temp_data[8]) + ' days'
        self.long_course_days = temp_data[8]




    def update_task(self):
        if self.save_reminder(self):
            screen_manager = self.manager
            screen_manager.current = 'first'
            MyFirstLayout().clear_widgets()
        else:
            pass

    def go_to_check_view_screen(self):
        MyFirstLayout().clear_widgets()
        screen_manager = self.manager
        screen_manager.current = 'check_view'

        ### Method for back button

    # Button for date picker and time picker
    def on_active(self, segmented_control: MDSegmentedControl, segmented_item: MDSegmentedControlItem, ) -> None:
        '''Called when the segment is activated.'''
        if segmented_item.text == 'Date':
            self.show_date_picker()
        elif segmented_item.text == 'Time':
            self.add_remainder()

    ### Button for date picker and time picker

    # saving data and upload to database
    def save_reminder(self, instance):
        task_name = self.ids.upload_name_of_remainder.text
        message = self.ids.upload_message_of_remainder.text
        period_time = self.ids.btn_date_picker.text
        start_time = self.ids.btn_add_remainder.text
        how_many_times_in_day = self.ids.upload_reminder_view.text
        date_range = str(data_list)
        if task_name == '' or period_time == 'Pick a date' or start_time == 'Cancelled time' or period_time == 'Cancelled':
            self.show_alert_dialog()
            return False
        else:
            is_active = 'True'
            long_course = self.long_course_days
            print(long_course)
            data_manager.ReminderDB.update_reminder(self, self.current_id_tag, task_name, message, period_time, start_time,
                                                    how_many_times_in_day, is_active, date_range, long_course)
            data_list.clear()
            return True

    ###End of method saving data

    # Alert dialog
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

    # Create method for date_picker
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

    # Create method for time_picker
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