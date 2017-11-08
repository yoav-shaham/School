__author__ = "Yoav Shaham"

import pickle
import threading
import os


#---------------variable-------------------
data={}
lock=False
#------------------------------------------
#read up to 10
#write one
class database(object):
    def __init__(self, filename):
        self._file_name=filename
    def get_datatbase(self):
        if not os.path.exists(self._file_name):
            return {}
        pickle_file = open(self._file_name, "r")
        data_dict = pickle.load(pickle_file)
        pickle_file.close()
        return data_dict
    def wirte_to_database(self, key):
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

def main():
    threading.Thread()

if __name__=="__main__":
    main()
