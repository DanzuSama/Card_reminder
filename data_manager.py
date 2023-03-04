import sqlite3


class ReminderDB:
    def __init__(self, db_name='reminder.db'):
        self.db_name = db_name

    def check_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            message TEXT,
            period_time TEXT,
            start_time TEXT,
            how_many_times_in_day TEXT,
            is_active TEXT,
            date_range TEXT,
            long_course TEXT
        )""")
        conn.commit()
        conn.close()

    def add_reminder(self, task_name, message, period_time, start_time, how_many_times_in_day, is_active, date_range,
                     long_course):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO reminders (task_name, message, period_time, start_time, how_many_times_in_day, is_active, date_range, long_course) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (task_name, message, period_time, start_time, how_many_times_in_day, 'True', date_range, long_course))
        conn.commit()
        conn.close()

    def get_reminders(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reminders")
        rows = cursor.fetchall()

        conn.close()
        return rows

    def delete_reminder(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reminders WHERE id=?", (id,))
        conn.commit()

        conn.close()

    def update_reminder(self, id, task_name, message, period_time, start_time, how_many_times_in_day, is_active, date_range, long_course):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE reminders SET task_name=?, message=?, period_time=?, start_time=?, how_many_times_in_day=?, is_active=?, date_range=?, long_course=? WHERE id=?",
            (task_name, message, period_time, start_time, how_many_times_in_day,is_active, date_range, long_course, id))
        conn.commit()

        conn.close()

    def get_ids_from_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM reminders")
        rows = cursor.fetchall()

        conn.close()
        return rows


    def get_task_name_from_db(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT task_name FROM reminders WHERE id=?", (id,))
        rows = cursor.fetchall()

        conn.close()
        return rows

    def get_message_from_db(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT message FROM reminders WHERE id=?", (id,))
        rows = cursor.fetchall()

        conn.close()
        return rows

    def get_period_time_from_db(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT period_time FROM reminders WHERE id=?", (id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_data_from_db(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reminders WHERE id=?", (id,))
        rows = cursor.fetchall()

        conn.close()
        return rows

    def update_long_course(self, id, long_course):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET long_course=? WHERE id=?",
                       (long_course, id))
        conn.commit()

        conn.close()

    def update_long_course_and_date_range(self, id, long_course, date_range):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET long_course=?, date_range=? WHERE id=?",
                       (long_course, date_range, id))
        conn.commit()

        conn.close()

    def get_start_time_from_db(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT start_time FROM reminders WHERE id=?", (id,))
        return cursor.fetchall()


    def get_how_many_times_in_day_from_db(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT how_many_times_in_day FROM reminders WHERE id=?", (id,))
        conn.close()
        return cursor.fetchall()

    def change_is_active_to_false(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET is_active=? WHERE id=?",
                       ('False', id))
        conn.commit()

        conn.close()

    def change_is_active_to_true(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET is_active=? WHERE id=?",
                       ('True', id))
        conn.commit()
        conn.close()

    def update_date_range(self, id, date_range):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET date_range=? WHERE id=?",
                       (date_range, id))
        conn.commit()
        conn.close()

    def clean_data_from_db_use_id(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reminders WHERE id=?", (id,))
        rows = cursor.fetchall()

        conn.close()
        temp_data = rows
        temp_id = temp_data[0][0]
        temp_name = temp_data[0][1]
        temp_message = temp_data[0][2]
        temp_period_time = temp_data[0][3]
        temp_start_time = temp_data[0][4]
        temp_how_many_times_in_day = temp_data[0][5]
        temp_is_active = temp_data[0][6]
        temp_date_range = temp_data[0][7]
        temp_date_range = temp_date_range.replace('[', '')
        temp_date_range = temp_date_range.replace(']', '')
        temp_long_course = temp_data[0][8]
        return temp_id, temp_name, temp_message, temp_period_time, temp_start_time, temp_how_many_times_in_day, temp_is_active, temp_date_range, temp_long_course



