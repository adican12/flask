
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="<api-key>")

# OR initialize with proxies

proxy_dict = {
          "http"  : "http://127.0.0.1",

        }
push_service = FCMNotification(api_key="AAAABw6N4YM:APA91bGdb1U8UlPAdGJh8fuetr0znEDDdCWIaE0xu7_GBRcg2nFJCW8xtr_-H2mcqPYPCal60wQszlJk_bepAiu1DBCdnQ3NzLGUPk4SPq11fizESsTQbMplpKrAd7aQERdnAf2Bhnf0", proxy_dict=proxy_dict)

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "<device registration_id>"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

# Send to multiple devices by passing a list of ids.

registration_ids = ["AAAABw6N4YM:APA91bGdb1U8UlPAdGJh8fuetr0znEDDdCWIaE0xu7_GBRcg2nFJCW8xtr_-H2mcqPYPCal60wQszlJk_bepAiu1DBCdnQ3NzLGUPk4SPq11fizESsTQbMplpKrAd7aQERdnAf2Bhnf0"]
message_title = "Cantor the cat"
message_body = "Hope you're remmber to go out with ligal tonight"
result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

print(result)
