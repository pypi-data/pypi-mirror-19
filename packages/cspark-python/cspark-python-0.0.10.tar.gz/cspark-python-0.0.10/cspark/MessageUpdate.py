import requests

from cspark.Update import Update


class MessageUpdate(Update):

    def __init__(self, message, room, headers):
        self.__message = message
        self.__room = room
        self.__headers = headers

    def get_plain_text(self):
        if 'text' in self.__message:
            return self.__message['text']

    def get_room(self):
        return self.__room

    def get_files_list(self):
        return self.__message['files']

    def download_file(self, number):
        file = self.__message['files'][number]
        response = requests.get(file, headers=self.__headers)

        if response.status_code == 200:
            with open('buffer.file', 'wb') as buffer:
                buffer.write(response.content)
