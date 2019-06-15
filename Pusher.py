
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="<api-key>")

# OR initialize with proxies

proxy_dict = {
          "http"  : "http://127.0.0.1",

        }
push_service = FCMNotification(api_key="AAAAB5JEBKs:APA91bHjEWYSTDRBDkK4wO94bgidJWCfd-TTFEoLRpDfkxcWGkgOiRfuPVZdveYAexQCdxN04eYj1n-PXlmhCxKBchorN1wGIRHB6g4qUNENUPgVYbuvz-dfT8OnB0SXk6tZoljIBQr_", proxy_dict=proxy_dict)

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "<device registration_id>"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

# Send to multiple devices by passing a list of ids.
registration_ids = ["ePAszQiwjk8:APA91bEUea36aLpzMvxvZQXH_lDVMtTrkwzz-58if6-8gE2wmACqvNNyFNMt8OZ6rNBGZHSzFRbuN4Fj6wloXUIFpfv2OrV3LmehmcrZTBTr3y_A9vWsy_hjsnBxC6oCnMOjgw5wQaTN"]
message_title = "Cantor the cat"
message_body = "Hope you're remmber to go out with ligal tonight"
result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

print(result)
