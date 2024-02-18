import os
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time



class App:

    def __init__(self, window, window_title, video_sources=[]):
        self.window = window
        self.window.title(window_title)
        self.video_sources = video_sources
        self.video_source = video_sources
        self.vids = [MyVideoCapture(video_source) for video_source in self.video_sources]
        self.curr_vid_idx = 0

        # open video source (by default this will try to open the computer webcam)
        self.vid = self.vids[self.curr_vid_idx]


        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def load_new_video(self):
        # Increment the current video index
        self.curr_vid_idx = (self.curr_vid_idx + 1) % len(self.vids)

        if self.curr_vid_idx == 0:
            # All videos have been shown, so close the window
            self.window.quit()
            return

        # Destroy the old video source
        del self.vid

        # Create a new video source
        self.vid = self.vids[self.curr_vid_idx]

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            # Add text overlay to the frame
            frame = self.add_text_overlay(frame, self.video_sources[self.curr_vid_idx])
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        else:
            print("Video finished")
            self.load_new_video()

        self.window.after(self.delay, self.update)

    def add_text_overlay(self, frame, text):
        # Define the font and text size
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2

        # Get the text size
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

        # Calculate the position for the text overlay
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = frame.shape[0] - 10

        # Add the text overlay to the frame
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)

        return frame


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        # else:
        #     return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()




# def start_app():
video_sources = [os.path.join("generated_video", filename) for filename in os.listdir("generated_video") if
                     filename.endswith(".mp4")]
    # Create a window and pass it to the Application object
    # print(video_sources)

App(tkinter.Tk(), "Tkinter and OpenCV", video_sources)
