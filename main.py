import os
from telethon import TelegramClient, events
import json
import requests

# Get the API keys and tokens from environment variables
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
imgbb_api_key = os.environ.get('API_KEY')

# Create a new TelegramClient
client = TelegramClient(bot_token, api_id, api_hash)


@client.on(events.NewMessage(pattern='/start'))
async def handle_start_command(event):
    # Send a message to the user who sent the start command
    await event.respond("(c) @HYBRID_Bots")
   
   
# Handle the event when a user sends a photo
@client.on(events.NewMessage(pattern='photo'))
async def handle_photo(event):
    # Get the photo file
    photo = await event.get_photo()
    # Open the photo file
    with open(photo, 'rb') as image_file:
        # Prepare the data for the Imgbb API call
        data = {
            'key': imgbb_api_key,
            'image': image_file
        }
        # Make the API call to upload the image
        response = requests.post('https://api.imgbb.com/1/upload', data=data)
        # Parse the response as JSON
        json_response = json.loads(response.text)
        # Check if the request was successful
        if json_response['success']:
            # Get the direct link for the image
            direct_link = json_response['data']['url']
            # Send the direct link to the user
            await event.reply(direct_link)
            # delete the file from the storage
            os.remove(photo)
        else:
            # Send an error message if the request was not successful
            await event.reply('An error occurred while uploading the image')
            # delete the file from the storage
            os.remove(photo)

# Start the bot
client.start()
client.run_until_disconnected()
