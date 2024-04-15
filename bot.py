import json
import dateutil.parser
from dotenv import load_dotenv
import discord

load_dotenv()
client = discord.Client()

def list_json_files():
    return [f for f in os.listdir('embeds/') if f.endswith('.json')]

@client.event
async def on_ready():
    print('Bot is ready. (type exit to exit.)')
    while True:  # Loop to prompt for another embed
        print('Available JSON files:', list_json_files())
        file_name = input('Enter the name of the JSON file (or "exit" to exit): ')
        if file_name.lower() == 'exit':
            break
        try:
            with open(f'embeds/{file_name}', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            continue
        channel_id_input = input('Enter the channel ID: ')
        if channel_id_input.lower() == 'exit':
            break
        channel_id = int(channel_id_input)
        channel = client.get_channel(channel_id)
        if channel is None:
            print(f"Channel with ID '{channel_id}' not found.")
            continue
        for embed_dict in data['embeds']:
            timestamp_str = embed_dict.pop('timestamp', None)
            embed = discord.Embed.from_dict(embed_dict)
            if timestamp_str:
                embed.timestamp = dateutil.parser.parse(timestamp_str)
            try:
                await channel.send(embed=embed)
                print(f"Embed sent to channel '{channel_id}'.")  # Success feedback
            except discord.HTTPException as e:
                print(f"Failed to send embed: {e}")  # Error handling

client.run(os.getenv('DISCORD_BOT_TOKEN'))