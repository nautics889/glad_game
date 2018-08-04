import sqlite3

class DataBase:
    '''Interface to database'''
    def __init__(self):
        '''Make connection and create table of it doesn't exist'''
        self.con = sqlite3.connect('scores.db')
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Scores(Id INTEGER PRIMARY KEY AUTOINCREMENT, Score INT)')

    def add_score(self, score):
        '''Add new score to a table'''
        with self.con:
            self.cur.execute('INSERT INTO Scores (Score) VALUES (?)', (score,))

    def get_highest_score(self):
        '''Get the highest score form table'''
        with self.con:
            self.cur.execute('SELECT MAX(Score) FROM Scores')
            try:
                score = self.cur.fetchone()[0]
            except TypeError:
                score = '0'
            finally:
                return score

    def close(self):
        self.con.close()