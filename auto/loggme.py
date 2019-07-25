from telethon.sync import TelegramClient
from telethon import functions, types

# Remember to use your own values from my.telegram.org!
api_id = 875323
api_hash = 'af081d62587aed4d253ded7f1a27f623'
def getChannelMemberCount():
    with TelegramClient('my-sess', api_id, api_hash) as client:
        # Getting information about yourself
        try:
            entity = client.get_entity('ethpoliticstabor')
            result = client(functions.channels.GetFullChannelRequest(
                channel=entity
            ))
            
            return result.full_chat.participants_count
        except ValueError as e:
            return False
