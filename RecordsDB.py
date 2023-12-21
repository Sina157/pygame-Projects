import sqlite3


def CreateTable(DataBaseName="DataBase"):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute('''
          CREATE TABLE IF NOT EXISTS Records
          ([ID] INTEGER PRIMARY KEY, [Record] INTEGER, [Name] TEXT)
          ''')


def AddToRecords(Name, Record, DataBaseName="DataBase"):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute(f'''
           INSERT INTO Records (Record , Name)
                 VALUES
                 ("{Name}","{Record}")
           ''')
    conn.commit()


def GetAllRecords(DataBaseName="DataBase"):
    Result = []
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute('''
          SELECT * FROM Records
          ''')
    for item in query.fetchall():
        Result.append({"ID": item[0], "Record": item[1], "Name": item[2]})
    return Result


def DeleteRecordById(RecordId, DataBaseName="DataBase"):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute(f'''
          DELETE FROM Records WHERE ID={RecordId}
          ''')
    conn.commit()


def DeleteAllRecords(DataBaseName="DataBase"):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute(f'''
          DELETE FROM Records
          ''')
    conn.commit()



