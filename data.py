import json


DATA_FILE = "data.json"
data = None


def load():
    with open(DATA_FILE) as file:
        global data
        data = json.load(file)


def save():
    with open(DATA_FILE, "w") as file:
        file.write(json.dumps(data, indent=4))


load()


def get_subscriptions():
    servers = {}
    for item in data:
        servers[item["server_id"]] = item["active"]
    return servers


def get_server_index(guild_id):
    index = 0
    while index < len(data):
        if data[index]["server_id"] == guild_id:
            return index
        index = index + 1
    return -1


def add_server(name, id):
    if get_server_index(id) >= 0:
        return "The server is already registered."
    data.append(
        {
            "name": name,
            "server_id": id,
            "active": True,
        }
    )
    save()
    return id


def edit_server(id, active):
    index = get_server_index(id)
    if index == -1:
        return "No server found with this id."
    data[index]["active"] = active
    save()
    return id


def remove_server(id):
    index = get_server_index(id)
    if index == -1:
        return "No server found with this id."
    data.pop(index)
    save()
    return id


def set_welcome_channel_id(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        data[index]["welcome_channel_id"] = channel_id
        save()
        return channel_id
    except Exception as e:
        print(e)
        return f"Error happened: {str(e)}"


def get_welcome_channel_id(guild_id):
    try:
        for item in data:
            if item["server_id"] == guild_id:
                return item["welcome_channel_id"]
    except Exception as e:
        return None


def set_free_games_channel_id(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        data[index]["free_games_channel_id"] = channel_id
        save()
        return channel_id
    except Exception as e:
        print(e)
        return f"Error happened: {str(e)}"


def get_free_games_channel_id(guild_id):
    try:
        for item in data:
            if item["server_id"] == guild_id:
                return item["free_games_channel_id"]
    except Exception as e:
        return None


def set_epic_games_names(guild_id, games):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        data[index]["epic_games"] = games
        save()
        return games
    except Exception as e:
        print(e)
        return f"Error happened: {str(e)}"


def get_epic_games_names(guild_id):
    try:
        for item in data:
            if item["server_id"] == guild_id:
                return item["epic_games"]
    except Exception as e:
        return []


def set_klei_links(guild_id, links):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        data[index]["klei_links"] = links
        save()
        return links
    except Exception as e:
        print(e)
        return f"Error happened: {str(e)}"


def get_klei_links(guild_id):
    try:
        for item in data:
            if item["server_id"] == guild_id:
                return item["klei_links"]
    except Exception as e:
        return []


def set_member_count_channel_id(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        data[index]["member_count_channel_id"] = channel_id
        save()
        return channel_id
    except Exception as e:
        print(e)
        return f"Error happened: {str(e)}"


def get_member_count_channel_id(guild_id):
    try:
        for item in data:
            if item["server_id"] == guild_id:
                return item["member_count_channel_id"]
    except Exception as e:
        return None


def set_role_message_id(guild_id, message_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        data[index]["set_role_message_id"] = message_id
        save()
        return message_id
    except Exception as e:
        print(e)
        return f"Error happened: {str(e)}"
