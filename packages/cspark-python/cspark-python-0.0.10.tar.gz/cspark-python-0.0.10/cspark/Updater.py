import requests
import time

from cspark.MessageUpdate import MessageUpdate
from cspark.MessageResponse import MessageResponse


class Updater(object):

    MODE_INSANE_REQUESTS, MODE_WEBHOOK = range(2)

    API_URL = "https://api.ciscospark.com/v1/"

    def __init__(
            self,
            access_token,
            mode=MODE_INSANE_REQUESTS,
            context_engine_class=None,
    ):
        self.__access_token = access_token
        self.__mode = mode
        self.__context_engine = context_engine_class()

        self.__headers = {'Authorization': 'Bearer ' + self.__access_token}
        self.__self_data = None
        self.__id = None
        self.__rooms = None

        self.__routers = []
        self.___new_message_callbacks = []

    def idle(self):

        # Getting data about bot itself
        response = requests.get(Updater.API_URL + 'people/me', headers=self.__headers)
        self.__self_data = response.json()
        self.__id = self.__self_data['id']

        while True:
            try:
                time.sleep(0.5)

                # Getting list of rooms
                response = requests.get(Updater.API_URL + 'rooms', headers=self.__headers)
                self.__rooms = response.json()['items']

                for room in self.__rooms:

                    # Looking if room last activity been processed
                    last_room_activity_record = self.__context_engine.get_data(
                        _key={
                            'type': 'last_room_activity_record',
                            'room_id': room['id'],
                            'last_activity': room['lastActivity']
                        }
                    )

                    # If not, process room's messages
                    if last_room_activity_record is None:
                        self.__context_engine.put_data(
                            _key={
                                'type': 'last_room_activity_record',
                                'room_id': room['id'],
                                'last_activity': room['lastActivity']
                            }
                        )

                        mention_me = ''
                        if room['type'] == 'group':
                            mention_me = '&mentionedPeople=me'

                        # Get last messages
                        messages_response = requests.get(
                            Updater.API_URL + '/messages?max=100&roomId=' + room['id'] + mention_me,
                            headers=self.__headers
                        )
                        messages = messages_response.json()['items']

                        for message in messages:
                            # Looking if message has been processed
                            message_record = self.__context_engine.get_data(
                                _key={
                                    'type': 'message_record',
                                    'message_id': message['id'],
                                }
                            )

                            # If not, process
                            if message_record is None and not message['personId'] == self.__id:
                                self.__context_engine.put_data(
                                    _key={
                                        'type': 'message_record',
                                        'message_id': message['id'],
                                    }
                                )
                                update = MessageUpdate(message, room, self.__headers)
                                self.__handle_update(update)
            except Exception as e:
                print(e)

    def add_router(self, class_name):
        pass

    def __get_context(self, update):
        return None

    def __handle_update(self, update):
        if type(update) is MessageUpdate:
            for new_message_callback in self.___new_message_callbacks:
                new_message_callback(update, self.__get_context(update))

    def send_response(self, room, response):
        if type(response) is MessageResponse:
            requests.post(
                Updater.API_URL + 'messages',
                headers=self.__headers,
                data={
                    'roomId': room['id'],
                    'markdown': response.get_plain_text()
                }
            )

    def add_new_message_listener(self, callback):
        self.___new_message_callbacks.append(callback)
