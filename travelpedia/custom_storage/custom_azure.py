from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'mayankmediastorage'
    account_key = 'juw/KmjlD9BKjH54LDWaHzvQN2DWjThD7IDZDCPL66uOufVKJICsNNX/Drj1t5Ea85zxnOvbOtX9DuQVxnITcQ=='
    azure_container = 'media'
    expiration_secs = None