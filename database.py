import sqlite3

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`) VALUES (?)", (chat_id,))

    def delete_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_id,))

    def get_chat(self):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue", ()).fetchmany(1)
            if(bool(len(chat))):
                for i in chat:
                    return i[1]
            else:
                return False

    def create_chat(self, chat_one, chat_two):
        pass