import time

from roslibpy import Topic
from compas_fab.backends import RosClient

def receive_message(message):
    print('Heard talking: ' + message['data'])

with RosClient('localhost') as client:
    listener = Topic(client, '/messages', 'std_msgs/String')
    listener.subscribe(receive_message)

    while client.is_connected:
        time.sleep(1)
