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


def get_welcome_channel_id(guild_id):
    try:
        for item in data:
            if item["server_id"] == guild_id:
                return item["welcome_channel_id"]
    except Exception as e:
        print(e)
    return None


def add_server(name, id):
    if get_server_index(id) >= 0:
        return "The server is already registered."
    data.append(
        {
            "name": name,
            "server_id": id,
            "active": True,
            "welcome_channel_id": None
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
