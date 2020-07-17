import time

from roslibpy import Topic
from compas_fab.backends import RosClient

with RosClient('localhost') as client:
    talker = Topic(client, '/messages', 'std_msgs/String')
    talker.advertise()

    while client.is_connected:
        print('Sending...')
        talker.publish({'data': 'Hello'})
        time.sleep(1)

    talker.unadvertise()
