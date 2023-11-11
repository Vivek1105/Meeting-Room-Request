import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Vishu@123",
            database="meeting_scheduler"
        )
        self.cursor = self.connection.cursor()

    def create_tables(self):
        create_meetings_table = """
        CREATE TABLE IF NOT EXISTS meetings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            start_time INT NOT NULL,
            end_time INT NOT NULL
        )
        """
        self.cursor.execute(create_meetings_table)
        self.connection.commit()

    def check_schedule_conflict(self, date, start_time, end_time):
        check_query = """
        SELECT id FROM meetings
        WHERE date = %s
        AND (
            (start_time >= %s AND start_time < %s)
            OR
            (end_time > %s AND end_time <= %s)
        )
        """
        self.cursor.execute(check_query, (date, start_time, end_time, start_time, end_time))
        return self.cursor.fetchone() is not None

    def add_meeting(self, date, start_time, end_time):
        add_meeting_query = """
        INSERT INTO meetings (date, start_time, end_time)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(add_meeting_query, (date, start_time, end_time))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()





