from threading import Thread

from webcam.data.file import File
from webcam.jobs.converting_job import ConvertingJob
from webcam.services.opencv import OpenCV


class Camera:
    def __init__(self):
        self.cv = OpenCV()
        self.capture = self.cv.get_capture()

        self.file = File()
        self.converting_job = ConvertingJob()

        self.is_recording = False
        self.is_camera_open = False

    def is_open(self):
        return self.is_camera_open

    def access(self):
        self.is_camera_open = True
        Thread(target=self.__start_reading_frames).start()

    def release(self):
        self.is_camera_open = False
        self.cv.release()

    def start_recording(self):
        if self.is_open():
            self.is_recording = True

    def stop_recording(self):
        self.is_recording = False
        self.file.release()
        last_file = self.file.last()
        self.converting_job.convert(last_file)

    def create_file(self, name):
        self.file.create(name)

    def __start_reading_frames(self):
        while self.capture.isOpened() and self.is_open():
            ret, frame = self.capture.read()
            if ret and self.is_recording:
                self.file.write(frame)
