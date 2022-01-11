import pickle
from os.path import dirname, exists
from typing import Any

# from google.colab import drive

g_drive_storage_location = "/content/gdrive/"
g_drive_location = g_drive_storage_location + "My Drive/data/"


class GDrive:
    @staticmethod
    def mount():
        drive.mount(g_drive_storage_location)

    @staticmethod
    def write(data: Any, file_name: str):
        filehandler = open(GDrive.file_name(file_name), "wb")
        pickle.dump(data, filehandler)
        filehandler.close()

    @staticmethod
    def read(file_name: str, safe: bool = True):
        exists = GDrive.exists(file_name) if safe else True
        if exists == False:
            return None
        file = open(GDrive.file_name(file_name), "rb")
        object_file = pickle.load(file)
        file.close()
        return object_file

    @staticmethod
    def exists(file_name: str):
        return exists(GDrive.file_name(file_name))

    @staticmethod
    def file_name(file_name: str):
        return g_drive_location + file_name
