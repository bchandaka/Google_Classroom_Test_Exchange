
from google.cloud import pubsub_v1
import time



def pull(project="nv-scioly-manager", subscription_name="receiver"):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        print(message.data.decode("utf-8"))
        message.ack()
    future = subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))

    try:
        # When timeout is unspecified, the result method waits indefinitely.
        future.result(timeout=30)
    except Exception as e:
        print(
          'Listening for messages on {} threw an Exception: {}.'.format(
              subscription_name, e))


pull()
