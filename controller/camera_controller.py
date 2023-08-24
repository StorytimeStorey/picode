import picamera as cam
import datetime
import os

class Camera:
    def __init__(self):
        self.camera = cam.PiCamera()
        self.save_directory = "../images"
        self.dir_today = None
        self.current_picture = None

    def check_dir(self):
        today = datetime.datetime.now()
        dir_path = os.path.join(self.save_directory, f"{today.year}/{today.month}/{today.day}")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            self.dir_today = dir_path

        
    def capture_image(self):
        self.check_dir()
        now = datetime.datetime.now()
        self.current_picture = os.path.join(self.dir_today, f"image_{now.hour:02d}{now.minute:02d}.jpg")
        self.camera.capture(self.current_picture)
