#!/usr/bin/python3           # This is database.py file
import sqlite3 as db


class ChatDB:

    def __init__(self):
        self.con = db.connect('data.db', check_same_thread=False)
        self.cursor = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `user`(
        `id` VARCHAR(10) PRIMARY KEY NOT NULL,
        `name` VARCHAR(100) NOT NULL,
        `password` VARCHAR(100) NOT NULL);'''
                            )
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `group`(
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` VARCHAR(100) NOT NULL DEFAULT 'chat group',
        `admin` VARCHAR(10) NOT NULL REFERENCES `user`(`id`)); '''
                            )
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `membership`(
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `user` VARCHAR(10) NOT NULL REFERENCES `user`(`id`),
        `group` INT NOT NULL REFERENCES `group`(`id`));'''
                            )
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `message`(
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `membership` INT NOT NULL REFERENCES `membership`(`id`),
        `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `text`varchar(1000));'''
                            )
        self.cursor.execute('''CREATE TRIGGER IF NOT EXISTS `register_admin` AFTER INSERT ON `group`
        BEGIN
        INSERT INTO `membership`(`user`,`group`) VALUES(new.`admin`,new.`id`);
        END;'''
                            )

    def insert_user(self, id, name, password):
        self.cursor.execute(f'''INSERT INTO `user`(`id`,`name`,`password`) values ('{id}', '{name}', '{password}');''')

    def insert_group(self, name, admin):
        self.cursor.execute(f'''INSERT INTO `group`(`name`,`admin`) values ('{name}', '{admin}');''')

    def insert_membership(self, user, group):
        self.cursor.execute(f'''INSERT INTO `membership`(`user`,`group`) values ('{user}', '{group}');''')

    def insert_message(self, user, group, text):
        self.cursor.execute(f'''SELECT `id` FROM `membership` WHERE `user`='{user}' AND `group`='{group}';''')
        membership = self.cursor.fetchone()[0]
        self.cursor.execute(f'''INSERT INTO `message`(`membership`,`text`) values ('{membership}', '{text}');''')

    def get_user(self, user_id, user_password):
        self.cursor.execute(f'''SELECT `name` FROM `user` WHERE `id`='{user_id}' AND `password`='{user_password}';''')
        name = self.cursor.fetchone()[0]
        return name

    def get_groups(self, user):
        self.cursor.execute(
            f'''SELECT `id`, `name`, `admin` from `group` WHERE `id` IN (SELECT `group` FROM `membership` WHERE 
            `user`='{user}');''')
        groups = self.cursor.fetchall()
        return groups

    def get_messages(self, group):
        self.cursor.execute(f'''SELECT `text`, `name` FROM 
        `message` 
        INNER JOIN `membership` 
        on message.membership = membership.id
        INNER JOIN `user`
        on membership.user = user.id
        WHERE `group` = {group}
        ORDER BY `time` DESC;'''
                            )
        data = self.cursor.fetchall()
        return data

    def get_members(self, group_id):
        self.cursor.execute(
            f'''SELECT `id`, `name` from `user` WHERE `id` IN (SELECT `user` FROM `membership` WHERE 
            `group`={group_id});''')
        data = self.cursor.fetchall()
        return data

    def delete_member(self,user_id,group_id):
        self.cursor.execute(
            f'''DELETE FROM `membership` WHERE `user`='{user_id}' and group = {group_id};''')

chat_db = ChatDB()
