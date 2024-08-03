"""
this module manage small actions over an sqlite database
"""
import sqlite3
from pathlib import Path
from os import getcwd
import os
import time

SYSTEM = os.name

def get_local_time():
    t = time.gmtime()
    hour = t.tm_hour
    day = t.tm_mday
    sec = str(t.tm_sec)
    minu = str(t.tm_min)
    
    if SYSTEM == 'posix':
        hour -= 4
        if hour < 0:
            hour += 12
            day -= 1
            pass
        pass
    hour = str(hour)
    day = str(day)
    mounth = str(t.tm_mon)
    if len(day) == 1:
        day = f'0{day}'
        pass
    if len(mounth) == 1:
        mounth = f'0{mounth}'
        pass
    if len(hour) == 1:
        hour = f'0{hour}'
        pass
    if len(minu) == 1:
        minu = f'0{minu}'
        pass
    if len(sec) == 1:
        sec = f'0{sec}'
        pass
    return f'{day}    {hour}:{minu}:{sec}'

class StatisticDataBaseRow:
    
    """
    the representation of one row in the global log in the database of the predicter
    """
    
    def __init__(self,val,count=0,dates=[]):
        self._value = val
        self._count = count
        self._dates = dates
        pass
    
    @property
    def Value(self):
        return self._value
        
    @property
    def Count(self):
        return self._count
    
    @property
    def Dates(self):
        for date in self._dates:
            yield date
            pass
        pass
    
    def __str__(self):
        return f'Value: {self._value}, Count: {self._count}'
    
    def __repr__(self):
        return str(self)
    
    pass

class PredicterDataBaseRow:
    
    """
    the representation of one row in the database of the predicter
    """
    
    def __init__(self,val,count=0,date=None):
        if not date:
            date = get_local_time()
            pass
        self._value = val
        self._count = count
        self._date = date
        pass
    
    @property
    def Value(self):
        return self._value
    
    @property
    def Count(self):
        return self._count
    
    @property
    def Date(self):
        return self._date
    
    def __str__(self):
        representation = f'Value: {self._value}, Count: {self._count}, Date: {self._date}'
        return '{' + representation + '}'
    
    def __repr__(self):
        return str(self)
    
    pass

class PredicterDB:
    
    """
    an abstraction of an sqlite3 database
    """
    
    def __init__(self,name,path=None):
        if path:
            if not type(path) == str:
                raise Exception('path most be of type str')
            _path = Path(path)
            if not _path.exists or _path.is_file():
                raise Exception('invalid path')
            self._path = _path
            pass
        else:
            self._path = Path(getcwd())
            pass
        self._root_path = self._path.joinpath(f'{name}.db')
        self._name = name
        self._connection = None
        self._cursor = None
        if not self.exists:
            self._init()
            pass
        pass
    
    @property
    def top(self):
        return 6500
    
    @property
    def x100classes(self):
        return self.top // 100
    
    @property
    def x10classes(self):
        return 10
    
    @property
    def aclasses(self):
        return 10
    
    @property
    def dclasses(self):
        return 100
    
    @property
    def name(self):
        return self._name
    
    @property
    def fullpath(self):
        return str(self._root_path.resolve())
    
    @property
    def exists(self):
        if not self.fullpath in [str(f) for f in self._path.iterdir()]:
            return False
        return True
    
    @property
    def history(self):
        self.open()
        self._cursor.execute('SELECT * FROM values_readed')
        temp = self._cursor.fetchall()
        result = []
        for r in temp:
            value_id = r[0]*100 + r[1]*10 + r[2] + r[3]
            self._cursor.execute(f'SELECT date_id FROM values_dates WHERE value_id = {value_id}')
            date_ids = self._cursor.fetchall()
            date_id = date_ids[len(date_ids) - 1][0]
            result.append(PredicterDataBaseRow(value_id,r[4],date_id))
            pass
        self.close()
        return result
        
    def open(self):
        self._connection = sqlite3.connect(self.fullpath)
        self._cursor = self._connection.cursor()
        pass
    
    def close(self):
        self._connection.commit()
        self._cursor.close()
        self._connection.close()
        self._cursor = None
        self._connection = None
        pass

    def _init_values_dates_table(self):
        self._cursor.execute('''CREATE TABLE values_dates (
            value_id REAL,
            date_id TEXT,
            value_date_count INTEGER,
            PRIMARY KEY (value_id,date_id),
            FOREIGN KEY (date_id) REFERENCES dates(date_id))
        ''')
        pass
    
    def _init_dates_table(self):
        self._cursor.execute('''CREATE TABLE dates (
            date_id TEXT PRIMARY KEY
        )
        ''')
        pass
    
    def _init_values_readed_table(self):
        self._cursor.execute('''CREATE TABLE values_readed (
            x100_interval_id INTEGER,
            x10_interval_id INTEGER,
            atomic_interval_id INTEGER,
            value_id INTEGER,
            value_count INTEGER,
            PRIMARY KEY (x100_interval_id,x10_interval_id,atomic_interval_id,value_id),
            FOREIGN KEY (x100_interval_id) REFERENCES x100_intervals_count(interval_id),
            FOREIGN KEY (x10_interval_id) REFERENCES x10_intervals_counts(x10_interval_id),
            FOREIGN KEY (atomic_interval_id) REFERENCES atomic_intervals_count(atomic_interval_id))
        ''')
        pass
    
    def _init_atomic_intervals_counts_table(self):
        self._cursor.execute('''CREATE TABLE atomic_intervals_counts (
            x100_interval_id INTEGER,
            x10_interval_id INTEGER,
            atomic_interval_id INTEGER,
            interval_count INTEGER,
            PRIMARY KEY (x100_interval_id,x10_interval_id,atomic_interval_id),
            FOREIGN KEY (x10_interval_id) REFERENCES x10_intervals_counts(x10_interval_id)
            FOREIGN KEY (x100_interval_id) REFERENCES x100_intervals_count(interval_id))
        ''')
        pass
    
    def _init_x10_intervals_counts_table(self):
        self._cursor.execute('''CREATE TABLE x10_intervals_counts (
            x100_interval_id INTEGER,
            x10_interval_id INTEGER,
            interval_count INTEGER,
            PRIMARY KEY (x100_interval_id,x10_interval_id),
            FOREIGN KEY (x100_interval_id) REFERENCES x100_intervals_count(interval_id))
        ''')
        pass

    def _init_x100_intervals_counts_table(self):
        self._cursor.execute('''CREATE TABLE x100_intervals_counts (
            interval_id INTEGER PRIMARY KEY,
            interval_count INTEGER)
         ''')
        pass
    
    def _init(self):
        self.open()
        self._init_x100_intervals_counts_table()
        self._init_x10_intervals_counts_table()
        self._init_atomic_intervals_counts_table()
        self._init_values_readed_table()
        self._init_dates_table()
        self._init_values_dates_table()
        self.close()
        pass
    
    def _get_x100_and_x10_and_atomic_intervals(self,value):
        i = 1
        while value > i*100 and i < 66:
            i += 1
            pass
        j = 1
        while value > i*100 + j*10 and j < 11:
            j += 1
            pass
        return {'x100': i - 1, 'x10': j - 1,'atomic': int(value - (i - 1)*100 - (j - 1)*10)}
    
    def _get_x100count(self,interval_id):
        self._cursor.execute(f'SELECT interval_count FROM x100_intervals_counts WHERE interval_id = {interval_id}')
        c = self._cursor.fetchall()
        if len(c) == 0: return 0
        return c[0][0]
    
    def _get_x10count(self,x100_id,interval_id):
        self._cursor.execute(f'SELECT interval_count FROM x10_intervals_counts WHERE x100_interval_id = {x100_id} AND x10_interval_id = {interval_id}')
        c = self._cursor.fetchall()
        if len(c) == 0: return 0
        return c[0][0]
    
    def _get_atomic_count(self,x100_id,x10_id,at_id):
        self._cursor.execute(f'SELECT interval_count FROM atomic_intervals_counts WHERE x100_interval_id = {x100_id} AND x10_interval_id = {x10_id} AND atomic_interval_id = {at_id}')
        c = self._cursor.fetchall()
        if len(c) == 0: return 0
        return c[0][0]
    
    def _get_value_count(self,x100_id,x10_id,at_id,v_id):
        self._cursor.execute(f'SELECT value_count FROM values_readed WHERE x100_interval_id = {x100_id} AND x10_interval_id = {x10_id} AND atomic_interval_id = {at_id} AND value_id = {v_id}')
        c = self._cursor.fetchall()
        if len(c) == 0: return 0
        return c[0][0]
    
    def _get_values_dates_count(self,value,date):
        self._cursor.execute(f'SELECT value_date_count FROM values_dates WHERE value_id = {value} AND date_id = \"{date}\"')
        c = self._cursor.fetchall()
        if len(c) == 0: return 0
        return c[0][0]
    
    def _update_x100table(self,x100_id):
        id_count = self._get_x100count(x100_id)
        if id_count == 0:
            self._cursor.execute(f'INSERT INTO x100_intervals_counts VALUES ({x100_id},1)')
            pass
        else:
            self._cursor.execute(f'UPDATE x100_intervals_counts SET interval_count = {id_count + 1} WHERE interval_id = {x100_id}')
            pass
        pass
    
    def _update_x10table(self,x100_id,x10_id):
        self._update_x100table(x100_id)
        id_count = self._get_x10count(x100_id,x10_id)
        if id_count == 0:
            self._cursor.execute(f'INSERT INTO x10_intervals_counts VALUES ({x100_id},{x10_id},1)')
            pass
        else:
            self._cursor.execute(f'UPDATE x10_intervals_counts SET interval_count = {id_count + 1} WHERE x100_interval_id = {x100_id} AND x10_interval_id = {x10_id}')
            pass
        pass
    
    def _update_atomic_table(self,x100_id,x10_id,at_id):
        self._update_x10table(x100_id,x10_id)
        id_count = self._get_atomic_count(x100_id,x10_id,at_id)
        if id_count == 0:
            self._cursor.execute(f'INSERT INTO atomic_intervals_counts VALUES ({x100_id},{x10_id},{at_id},1)')
            pass
        else:
            self._cursor.execute(f'UPDATE atomic_intervals_counts SET interval_count = {id_count + 1} WHERE x100_interval_id = {x100_id} AND x10_interval_id = {x10_id} AND atomic_interval_id = {at_id}')
            pass
        pass
    
    def _update_values_table(self,x100_id,x10_id,at_id,value):
        self._update_atomic_table(x100_id,x10_id,at_id)
        v_id = value - x100_id*100 - x10_id*10 - at_id
        value_count = self._get_value_count(x100_id,x10_id,at_id,v_id)
        if value_count == 0:
            self._cursor.execute(f'INSERT INTO values_readed VALUES ({x100_id},{x10_id},{at_id},{v_id},1)')
            pass
        else:
            self._cursor.execute(f'UPDATE values_readed SET value_count = {value_count + 1} WHERE x100_interval_id = {x100_id} AND x10_interval_id = {x10_id} AND atomic_interval_id = {at_id} AND value_id = {v_id}')
            pass
        pass
    
    def _update_dates(self,date):
        self._cursor.execute(f'SELECT * FROM dates WHERE date_id = \"{date}\"')
        c = self._cursor.fetchall()
        if len(c) == 0:
            self._cursor.execute(f'INSERT INTO dates VALUES (\"{date}\")')
            pass
        pass
    
    def _update_values_dates_table(self,value,date):
        v_d_count = self._get_values_dates_count(value,date)
        if v_d_count == 0:
            self._cursor.execute(f'INSERT INTO values_dates VALUES ({value},\"{date}\",1)')
            pass
        else:
            self._cursor.execute(f'UPDATE values_dates SET value_date_count = {v_d_count + 1} WHERE value_id = {value} AND date_id = \"{date}\"')
            pass
        pass
    
    def _process_data_interval(self,values,interval_size=None):
        history = {}
        if interval_size:
            for v in values:
                if not v // interval_size in history.keys():
                    history[v // interval_size] = 1
                    pass
                else:
                    history[v // interval_size] += 1
                    pass
            return f'Intervals class {interval_size}',history
        for v in values:
            v_id = (v * 100 - int(v) * 100) / 100
            if not v_id in history.keys():
                history[v_id] = 1
                pass
            else:
                history[v_id] += 1
                pass
            pass
        return 'Intervals class decimal',history
    
    def update(self,value,date=None):
        if not date:
            date = get_local_time()
            pass
        self.open()
        data = self._get_x100_and_x10_and_atomic_intervals(value)
        x100_interval,x10_interval,atomic_interval = data['x100'],data['x10'],data['atomic']
        self._update_values_table(x100_interval,x10_interval,atomic_interval,value)
        self._update_dates(date)
        self._update_values_dates_table(value,date)
        self.close()
        pass
    
    def History(self,**kwargs):
        order = 'ASC'
        limit = None
        
        if 'order' in kwargs.keys():
            order = kwargs['order']
            pass
        if 'limit' in kwargs.keys():
            limit = kwargs['limit']
            pass
        
        if not order in ['ASC','DESC']:
            raise Exception('order most be one of \"ASC\" or \"DESC\"')
        if not limit == None and not type(limit) == int:
            raise Exception('limit most be None or an integer')
        
        self.open()
        command = f'SELECT * FROM values_dates ORDER BY date_id {order}'
        if limit:
            command += f' LIMIT {limit}'
            pass
        
        self._cursor.execute(command)
        result = [PredicterDataBaseRow(r[0],r[2],r[1]) for r in self._cursor.fetchall()]
        self.close()
        return result
        
    def intervals_history(self,bottom=0,top=6500,**kwargs):
        limit = None
        order = 'DESC'
        interval = None
        
        if 'limit' in kwargs.keys():
            limit = kwargs['limit']
            pass
        if 'order' in kwargs.keys():
            order = kwargs['order']
            pass
        if 'interval' in kwargs.keys():
            interval = kwargs['interval']
            pass
        
        if not order in ['ASC','DESC']:
            raise Exception('the value of "order" most be either of "ASC" or "DESC"')
        if not type(limit) == int and not limit == None:
            raise Exception('the value of "limit" most be integer')
        if not type(bottom) in [int,float] or not type(top) in [int,float]:
            raise Exception('top and bottom most be of type "integer or float"')
        if not interval in [100,10,1,None]:
            raise Exception('interval value most be either of 100,10,1 or None')
        
        script = f'SELECT value_id FROM values_dates WHERE value_id >= {bottom} and value_id <= {top} ORDER BY date_id {order}'
        if limit:
            script += f' LIMIT {limit}'
            pass
        
        self.open()
        self._cursor.execute(script)
        result = [r[0] for r in self._cursor.fetchall()]
        self.close()
        return self._process_data_interval(result,interval)
    
    pass