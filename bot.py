import discord
import asyncio

TOKEN = "token"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

users_food_lists = {}
users_food_lists_messages = {}

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("/food"):
        command = message.content[len("/food"):].strip()
        user_id = str(message.author.id)

        if not command:
            return
        
        if command == "clear":
            uber_link = "https://www.ubereats.com/orders/"
            channel = message.channel

            async for old_message in channel.history(limit=None):
                if old_message.content.startswith(uber_link):
                    await old_message.delete()
                    await asyncio.sleep(0.5)
        
        if command.startswith("add"):
            await add_food(command, user_id, message)
        
        if command.startswith("remove"):
            await remove_food(command, user_id, message)
        
        await message.delete()

# Add Food
async def add_food(command, user_id, message):
    if user_id not in users_food_lists:
        users_food_lists[user_id] = []

    food_item = ""
    for char in command[len("add"):].strip():
        if char in [",", ".", "\n"]:
            if food_item.strip():
                users_food_lists[user_id].append(food_item)
            food_item = ""
        else:
            food_item += char
    
    if food_item.strip():
        users_food_lists[user_id].append(food_item)
    await print_list(user_id, message)

# Remove Food
async def remove_food(command, user_id, message):
    if user_id not in users_food_lists:
        return
    else:
        if command == "remove all":
            await remove_all_food(user_id, message)
        else:
            try:
                item_number = int(command[len("remove"):].strip())
            except ValueError:
                item_number = -1
            if item_number <= 0 or item_number > len(users_food_lists[user_id]):
                return
            if len(users_food_lists[user_id]) == 1:
                await remove_all_food(user_id, message)
            else:
                users_food_lists[user_id].pop(item_number - 1)
                await print_list(user_id, message)

# Remove all helper
async def remove_all_food(user_id, message):
    if user_id in users_food_lists_messages:
        prev_message_id = users_food_lists_messages[user_id]
        prev_message = await message.channel.fetch_message(prev_message_id)
        if prev_message:
            await prev_message.delete()
    del users_food_lists[user_id]
    del users_food_lists_messages[user_id]

# Sneaky link
async def link_food(command, user_id, message):
    return 

# For printing the list
async def print_list(user_id, message):
    response = f"{message.author.mention} list: \n"
    for index, item in enumerate(users_food_lists[user_id], start=1):
        response += f"{index}. {item}\n"
    if user_id in users_food_lists_messages:
        prev_message_id = users_food_lists_messages[user_id]
        prev_message = await message.channel.fetch_message(prev_message_id)
        if prev_message:
            await prev_message.delete()
    new_message = await message.channel.send(response)
    users_food_lists_messages[user_id] = new_message.id   
                    

client.run(TOKEN)