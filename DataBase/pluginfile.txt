"""
This is an implementation of pickle based Database, with collision example.

The collision happens because when we open the pickle file with "w",
all of its content is deleted. If we will try to write / read in one
thread at the same time the other thread is writing - we may get an exception
(The first thread may try to do pickle.load from an empty file).
Note that the collision depends on which stage of value setting the writing
thread is at. If the write was finished (which statistically may happen) - no
collision will happen.

The example below uses two threads which do set & get in a loop.
You might need to run it a few times to get a collision!

Author: Tomer Galun
"""

import os
import pickle
import threading

DATABASE_FILE_NANE = "mydb.pkl"


class Database(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def _get_data(self):
        """
        returns the data dict from the storage
        """
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
        return self._get_data().get(key)

    def set_value(self, key, value):
        data = self._get_data()
        data[key] = value
        pickle_file = open(self._file_name, "w")
        data_dict = pickle.dump(data, pickle_file)
        pickle_file.close()


def thread_worker1(db):
    for i in xrange(10):
        db.set_value("cool", "is very cool")
        print db.get_value("cool")


def thread_worker2(db):
    for i in xrange(10):
        db.set_value("cool", "is not very cool")
        print db.get_value("cool")

if __name__ == "__main__":
    d = Database(DATABASE_FILE_NANE)

    # Simple set & get of values
    d.set_value("a", "Hello from the other side")
    d.set_value("b", "I must've called a thousand times")
    print d.get_value("a")
    print d.get_value("b")
    print d.get_value("d")  # returns None because the key doesn't exist

    # A collision example
    t = threading.Thread(target=thread_worker1, args=(d,))
    t2 = threading.Thread(target=thread_worker2, args=(d,))
    t.start()
    t2.start()
