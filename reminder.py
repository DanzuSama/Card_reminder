import threading
import time
import datetime
import re
import data_manager
from kivy.clock import Clock
from plyer import notification
from View.DialogScreen.dialog_screen import MyDialog


global id_list
id_list = []


class Reminder(threading.Thread):
    db_name = 'reminder.db'

### Get the data from the notification card
    def __init__(self, notification_card_instance, id):
        threading.Thread.__init__(self)
        self.long_course = None
        self.task_start_time = None
        self.message = None
        self.task_name = None
        self.dates_list = None
        self.thread = None
        self.notification_card_instance = notification_card_instance
        self.id = id
        self._stop_event = threading.Event()

    def __enter__(self):
        self.create_notification_from_db()


    def create_notification_from_db(self):
        temp_data = data_manager.ReminderDB.clean_data_from_db_use_id(self, self.id)
        task_id = temp_data[0]
        self.task_name = temp_data[1]
        self.message = temp_data[2]
        task_period_time = temp_data[3]
        self.task_start_time = temp_data[4]
        task_how_many_times_in_day = temp_data[5]
        is_active = temp_data[6]
        date_range = temp_data[7]
        self.long_course = int(temp_data[8])
        self.dates_list = [datetime.datetime.strptime(d.strip(), "datetime.date(%Y, %m, %d)").date() for d in
                           re.findall(r'datetime\.date\(\d{4},\s\d{1,2},\s\d{1,2}\)', date_range)]
        
        self.send_notification()


    ### Create notification need to fix data range working
    def send_notification(self):
        while not self._stop_event.is_set():
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            today = datetime.date.today()
            time.sleep(.1)
            for date in self.dates_list:
                time.sleep(.1)
                if date == today:
                    time.sleep(.1)
                    if current_time == self.task_start_time:
                        notification.notify(
                            title=self.task_name,
                            message=self.message,
                            app_name='Reminder',
                            app_icon='image/remi.ico',
                            timeout=50,
                        )
                        self.dates_list.remove(date)
                        data_manager.ReminderDB.update_date_range(self, self.id, str(self.dates_list))
                        self.long_course -= 1
                        if self.long_course == 0 or self.dates_list == []:
                            self.stop()
                            self.change_long_course()
                            self.show_dialog()
                        else:
                            str(self.long_course)
                            self.change_long_course()
                            self.show_dialog()
                            time.sleep(.5)

    ### Start the thread and add the id to the global list
    def start(self):
        if self.id in id_list:
            print('Already running: ', self.id)
        else:
            self.thread = threading.Thread(target=self.create_notification_from_db)
            self.thread.start()
            id_list.append(self.id)

    ### Stop the thread and remove the id from the global list
    def stop(self):
        if self.id in id_list:
            self._stop_event.set()
            print('stop notification: ', self.id)
            id_list.remove(self.id)
            self.notification_card_instance.ids.on_off_switch_notification.active = False

    def show_day_too_low_dialog(self):
        Clock.schedule_once(lambda dt: MyDialog().show('Day is too low', 'Change the day'), 0)

    def show_dialog(self):
        Clock.schedule_once(lambda dt: MyDialog().show(self.task_name, self.message), 0)


    def change_long_course(self):
        self.notification_card_instance.set_long_day(self.long_course)



