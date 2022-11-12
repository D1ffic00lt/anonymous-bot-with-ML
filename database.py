import sqlite3

from templates import ignore_exceptions


class Database:
    @ignore_exceptions
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL,
            chat_id VARCHAR (255) NOT NULL,
            gender VARCHAR (60),
            rating INTEGER DEFAULT 1000,
            spam INTEGER DEFAULT 0,
            deceit INTEGER DEFAULT 0,
            sale INTEGER DEFAULT 0,
            NSFW INTEGER DEFAULT 0,
            PRIMARY KEY (id)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS queue (
            id INTEGER,
            chat_id VARCHAR (255) NOT NULL,
            gender VARCHAR (60),
            PRIMARY KEY (id)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
            id INTEGER,
            chat_one VARCHAR (255) NOT NULL,
            chat_two VARCHAR (255) NOT NULL
        )""")
        self.connection.commit()

    @ignore_exceptions
    def add_queue(self, chat_id, gender):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`, `gender`) VALUES (?, ?)", (chat_id, gender))

    @ignore_exceptions
    def delete_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_id,))

    @ignore_exceptions
    def delete_chat(self, id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE `id` = ?", (id_chat,))

    @ignore_exceptions
    def set_gender(self, chat_id, gender):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
            if bool(len(user)) is False:
                self.cursor.execute("INSERT INTO `users` (`chat_id`, `gender`) VALUES (?,?)", (chat_id, gender))
                return True
            else:
                return False

    @ignore_exceptions
    def get_gender_chat(self, gender):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE `gender` = ?", (gender,)).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    user_info = [row[1], row[2]]
                    return user_info
            else:
                return [0]

    @ignore_exceptions
    def get_gender(self, chat_id, text: bool = False):
        if text:
            with self.connection:
                user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
                if bool(len(user)):
                    for row in user:
                        return "Мужской" if row[2] == "male" else "Женский"
                else:
                    return "---"
        else:
            with self.connection:
                user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
                if bool(len(user)):
                    for row in user:
                        return row[2]
                else:
                    return False

    @ignore_exceptions
    def get_chat(self):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    user_info = [row[1], row[2]]
                    return user_info
            else:
                return [0]

    @ignore_exceptions
    def create_chat(self, chat_one, chat_two):
        with self.connection:
            if chat_two != 0:
                self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_two,))
                self.cursor.execute("INSERT INTO `chats` (`chat_one`, `chat_two`) VALUES (?, ?)", (chat_one, chat_two,))
                return True
            else:
                return False

    @ignore_exceptions
    def get_active_chat(self, chat_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_one` = ?", (chat_id,))
            id_chat = 0
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[2]]
            if id_chat == 0:
                chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_two` = ?", (chat_id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[1]]
                if id_chat == 0:
                    return False
                else:
                    return chat_info
            else:
                return chat_info

    @ignore_exceptions
    def change_rating(self, chat_id, rating):
        with self.connection:
            if self.cursor.execute("SELECT `rating` FROM `users` WHERE chat_id = ?", (chat_id,)).fetchall():
                return self.cursor.execute(
                    "UPDATE `users` SET `rating` = `rating` + ? WHERE `chat_id` = ?",
                    (rating, chat_id)
                )

    @ignore_exceptions
    def is_register(self, chat_id):
        with self.connection:
            if not self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany():
                return False
            return True

    @ignore_exceptions
    def restart(self):
        with self.connection:
            self.cursor.execute("DELETE FROM `queue`")
            self.cursor.execute("DELETE FROM `chats`")

    @ignore_exceptions
    def get_rating(self, chat_id):
        with self.connection:
            if self.cursor.execute(
                    "SELECT `rating` FROM `users` WHERE `chat_id` = ?",
                    (chat_id,)
            ).fetchmany():
                return self.cursor.execute(
                    "SELECT `rating` FROM `users` WHERE `chat_id` = ?",
                    (chat_id,)
                ).fetchmany()[0]
            return "---"

    @ignore_exceptions
    def add_rating(self):
        for i in self.cursor.execute("SELECT `chat_id` FROM `users` WHERE `rating` < 500").fetchall():
            with self.connection:
                self.cursor.execute(
                    "UPDATE `users` SET `rating` = `rating` + 200 WHERE `chat_id` = ?",
                    (i[0],)
                )

    @ignore_exceptions
    def add_report(self, report_type, chat_id):
        with self.connection:
            return self.cursor.execute(
                f"UPDATE `users` SET `{report_type}` = `{report_type}` + 1 WHERE chat_id = ?",
                (chat_id,)
            )

    @ignore_exceptions
    def set_rating(self, chat_id, rating):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `rating` = ? WHERE chat_id = ?",
                (rating, chat_id)
            )
