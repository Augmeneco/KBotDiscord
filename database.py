import sqlite3
import json

db = sqlite3.connect('data/db.db', check_same_thread=False)
db_cur = db.cursor()

db_cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, data TEXT)')
db_cur.execute('CREATE TABLE IF NOT EXISTS registry (name TEXT, data TEXT)')

class User:
    id: int
    perm: int
    level: int
    data: dict
    counter: int

    def update(self):
        users.update(self)

class Users:
    users = {}

    def __init__(self):
        users = db_cur.execute('SELECT * FROM users').fetchall()
        for user in users:
            id = user[0]
            data = json.loads(user[1])

            self.users[id] = {
                'data': data
            }

    def get(self, id):
        if id not in self.users:
            self.add(id)

        user = User()
        user.id = id
        user.data = self.users[id]['data']
        user.perm = self.users[id]['data']['perm']
        user.counter = self.users[id]['data']['counter']
        user.level = self.users[id]['data']['level']

        return user

    def add(self, id):
        self.users[id] = {
            'data': {'perm':1, 'level':1, 'counter':1}
        }

        db_cur.execute('INSERT INTO users VALUES (?, ?)', (id, json.dumps(self.users[id]['data']) ))
        db.commit()

        return self.get(id)
    
    def update(self, user: User):
        user.data['perm'] = user.perm
        user.data['level'] = user.level
        user.data['counter'] = user.counter
        self.users[user.id]['data'] = user.data

        data = json.dumps(user.data)
        id = user.id

        db_cur.execute('UPDATE users SET data = ? WHERE id = ?', (data, id))
        db.commit()

    def exists(self, id):
        if id in self.users: return True
        else: False
        
users = Users()