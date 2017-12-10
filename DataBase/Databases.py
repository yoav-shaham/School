__author__ = "Yoav Shaham"

import pickle
import threading
import os
from random import *


#---------------variable-------------------
data = {}
lock = False
#------------------------------------------
#read up to 10
#write one
class database(object):
    def __init__(self, filename):
        self._file_name = filename

    def get_data(self):
        if not os.path.exists(self._file_name):
            return {}
        pickle_file = open(self._file_name, "r")
        data_dict = pickle.load(pickle_file)
        pickle_file.close()
        return data_dict

    def get_value(self, key):
        """
        return None if key doesn't exist
        """
        return self.get_data().get(key)

    def set_value(self, key, value):
        data = self.get_data()
        data[key] = value
        pickle_file = open(self._file_name, "w")
        data_dict = pickle.dump(data, pickle_file)
        pickle_file.close()


class database_usr(database):
    def __init__(self, filename):
        super(database_usr, self).__init__(filename)
        self.lock = threading.Lock()

    def get_database(self):
        with self.lock:
            return super(database_usr, self).get_data()

    def set_value(self, key, value):
        with self.lock:
            return super(database_usr, self).set_value(key, value)

    def get_value(self, key):
        with self.lock:
            return super(database_usr, self).get_value(key)


def writing(thread_num, database):
    """
    :param thread_num: the thread name/number
    :type thread_num: str
    :param database: the accecing database class
    :type database: database_usr
    """
    for i in range(20):
        rand_num = randint(0, 20)
        database.set_value(thread_num, rand_num)
        print"THREAD " + str(thread_num) + " READS:" + str((database.get_database()))
    return True


def main():
    num_of_threads = 5
    filename = r"file.txt"
    database = database_usr(filename)
    for thread in range(num_of_threads):
        thread = threading.Thread(target=writing, args=(thread, database))
        thread.start()


if __name__ == "__main__":
    main()

