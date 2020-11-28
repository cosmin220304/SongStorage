import os
from zipfile import ZipFile
from shutil import copy as file_copy
from uuid import uuid4
from tinydb import TinyDB, Query
from playsound import playsound

quit = False
accepted_types = ["pcm", "wav", "aiff", "mp3",
                  "aac", "ogg", "wma", "flac", "alac", "wma"]
db = TinyDB('db.json')
process = None


def quit_program():
    global quit
    # print("Are you sure?[Y/N]")
    # answer = input().lower()
    # if answer in ["", "y", "yes"]:
    quit = True
    return ""

# todo add date


def add_song(file, artist, song_name, date, *tags):
    try:
        fileArray = file.split(".")
        file_name = fileArray[0]
        type = fileArray[1].lower()
        id = str(uuid4())

        if type not in accepted_types:
            raise "Unregonized file format!"

        file_copy(file, "Storage")
        os.rename(f"Storage/{file}", f"Storage/{id}.{type}")

        data = {
            "ID": id,
            "file name": file_name,
            "type": type,
            "artist": artist,
            "song name": song_name,
            "date": date,
            "tags": tags
        }
        db.insert(data)

        return f"Success! Song id: {id}"

    except Exception as error:
        return f"Failure! {error}"


def delete_song(id, *_):
    try:
        query = Query()
        data = db.search(query["ID"] == id)[0]
        type = data["type"]
        path = f"Storage/{id}.{type}"

        if os.path.exists(path):
            os.remove(path)
        else:
            print("ERROR: Could not find file!")

        db.remove(query['ID'] == id)

        return "Success!"

    except IndexError:
        return "Failure! Data not found!"

    except Exception as error:
        return f"Failure! {error}"


def update_data_from_input(data):
    print("Update or leave empty where you do not want to modify the data")
    for key in data.keys():
        if key in ["ID", "type"]:
            continue

        # display old value for the current field
        print(f"{key}: \"{data[key]}\" -> ", end="")

        # update value if not empty
        new_value = input().strip()
        if new_value:
            if key == "tags":
                data[key] = new_value.split(" ")
            else:
                data[key] = new_value
    return data


def modify_data(id, *_):
    try:
        query = Query()
        data = db.search(query["ID"] == id)[0]

        new_data = update_data_from_input(data)
        db.update(new_data, query["ID"] == id)

        return f"Success! Updated: {new_data}"

    except IndexError:
        return "Failure! Data not found!"

    except Exception as error:
        return f"Failure! {error}"


def search(*kvp_list):
    query = Query()
    complexQuery = query["ID"] != None  # initalization

    for kvp in kvp_list:
        key, value = kvp.split("=")
        complexQuery &= (query[key] == value)

    data = db.search(complexQuery)
    return data


def create_save_list(archive_path, *kvp_list):
    try:
        save_list_path = f"{archive_path}/save_lists.zip"
        results = search(*kvp_list)

        with ZipFile(save_list_path, "w") as save_list:
            for data in results:
                file_name = data["ID"]
                file_type = data["type"]
                file_path = f"Storage/{file_name}.{file_type}"
                real_file_name = data["file name"]
                save_list.write(file_path, f"{real_file_name}.{file_type}")

        return "Success"

    except Exception as error:
        return f"Failure! {error}"

# Define a function for the thread


def play(id, *_):
    global process
    try:
        query = Query()
        data = db.search(query["ID"] == id)[0]
        type = data["type"]
        song_path = f'Storage/{id}.{type}'

       playsound(song_path, True)

        song_name = data["song name"]
        artist = data["artist"]
        return f"Playing {song_name} by {artist}"
        x.join()

    except IndexError:
        return "Failure! Data not found!"

    except Exception as error:
        return f"Failure! {error}"


def stop(*_):
    process.terminate()
    return ""


def unkown_command(_=""):
    return "Command is unkown!"


command_to_function = {
    "quit": quit_program,
    "add_song": add_song,
    "delete_song": delete_song,
    "modify_data": modify_data,
    "search": search,
    "create_save_list": create_save_list,
    "play": play,
    "stop": stop,
}


def main():
    while not quit:
        try:
            user_input = input().split(" ")
            command = user_input[0].lower()
            function = command_to_function.get(command, unkown_command)
            result = function(*user_input[1:])
            print(result)
        except Exception as error:
            print(error)


main()
