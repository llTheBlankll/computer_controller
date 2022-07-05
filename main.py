import os
import socket
import json
import subprocess

from time import sleep as delay
from Crypto.Cipher import AES


def decrypt_text(text: bytes):
    aes: AES = AES.new("zAG5bUGU5rHQh5zP", AES.MODE_CFB, "KDfpDKv7AYHtYnew")
    message: bytes = aes.decrypt(text)
    return message.decode("utf-8")


def encrypt_text(text: bytes):
    aes: AES = AES.new("zAG5bUGU5rHQh5zP", AES.MODE_CFB, "KDfpDKv7AYHtYnew")
    message: bytes = aes.encrypt(text)
    return message


class Server:
    def __init__(self) -> None:
        # Server connection configuration
        self.host: str = "192.168.1.21"
        self.port: int = 4444
        self.pair_config_dir: str = "/tmp"

        # Commands file.
        self.command_file: str = "./commands.json"

        self.commands = json.load(open(self.command_file, "r"))
        """
        List of commands
        Keys:
        name: str
        executable: str
        arguments: list
        """

    def pair_device(self, device_name) -> None:
        f = open(self.pair_config_dir + "/remote_control.conf", "a+")
        f.write(device_name.endswith(""))
        f.close()
        print(f"Device {device_name} is paired successfully!")
        delay(2)
        return

    def get_paired_device(self) -> str:
        f = open(self.pair_config_dir + "/remote_control.conf", "r")
        device: str = f.readline()
        f.close()
        return device

    def execute_command(self, name: str) -> bool:
        for command in self.commands:
            # Hinting
            command_name: str = command["name"]
            command_exec: str = command["executable"]
            command_args: list = command["arguments"]
            # Insert the executable file to the first index.
            command_args.insert(0, command_exec)

            if name == command_name:
                subprocess.Popen(command_args)
                return True

        return False

    def list_commands(self) -> None:
        for command in self.commands:
            print(f"Command Name: {command['name']}")
            print(f"Executable  : {command['executable']}")
            print(f"Arguments   : {command['arguments']}")

    def add_command(self, args: list):
        with open("./commands.json", "w+") as f:
            new_command: dict = {
                "name": args[0],
                "executable": args[1],
                "arguments": args[2:]
            }
            self.commands.append(new_command)
            json.dump(self.commands, f)

    def listen_for_command(self) -> None:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver.bind(
            (
                self.host,
                self.port
            )
        )
        # Listen for connection
        print("Listen for connection...")
        while True:
            receiver.listen()
            (connection, address) = receiver.accept()
            with connection:
                print(f"Connection found from {address[0]} at {address[1]}")
                data: bytes = connection.recv(1024)
                message = decrypt_text(data)
                args = message.split(" ")
                if len(args) < 0:
                    return
                # * Device pairing
                if args[0] == "pair" and len(args) > 1:
                    print("Device pairing initialized.")
                    # Check if the computer is already paired to a device.
                    if os.path.exists(self.pair_config_dir + "/remote_control.conf"):
                        print(f"Computer was already paired to device '{self.get_paired_device()}'")
                        return
                    answer = input(f"Would you like to accept the device {args[1]}? Y/N: ")
                    if answer.lower() == "y":
                        self.pair_device(device_name=args[1])
                    # Execution will not continue.
                    return
                # Execute command
                if args[0] == "execute" and args[1] == self.execute_command(args[1]):
                    pass
                # Add Command
                if args[0] == "add" and args[1] == "command":
                    # Check if it has necessary arguments.
                    if len(args[2:]) < 0:
                        return
                    self.add_command(args[2:])
            # Close Section
            connection.close()
            receiver.close()


if __name__ == "__main__":
    server = Server()
    server.listen_for_command()
