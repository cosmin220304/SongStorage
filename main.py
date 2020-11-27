import os
from uuid import uuid4

quit = False
accepted_types = ["PCM", "WAV", "AIFF", "MP3",
                  "AAC", "OGG", "WMA", "FLAC", "ALAC", "WMA"]


def quit_program():
    global quit
    print("Are you sure?[Y/N]")
    answer = input().lower()
    if answer == "y" or answer == "yes":
        quit = True


def add_song(file):
    type = file.split(".")[1]
    id = str(uuid4())
    copy_command = ""

    if type in accepted_types:
        print("File accepted!")

    if os.name == "posix":
        copy_command = "cp"
    else:
        copy_command = "copy"

    os.system(f"{copy_command} {file} Storage")
    os.rename(f"Storage/{file}", f"Storage/{id}.{type}")


def delete_song(id):
    type = "mp3"  # todo: get from database the type
    path = f"Storage/{id}.{type}"
    if os.path.exists(path):
        os.remove(path)
        print("Success!")
    else:
        print("Could not find file!")


def modify_data(id, *new_data):
    print(new_data)


def unkown_command():
    print(f"Command is unkown!")


command_to_function = {
    "quit": quit_program,
    "add_song": add_song,
    "delete_song": delete_song,
    "modify_data": modify_data,
}


def main():
    while quit == False:
        user_input = input().split(" ")
        command = user_input[0].lower()
        function = command_to_function.get(command, unkown_command)
        function(*user_input[1:])


main()
