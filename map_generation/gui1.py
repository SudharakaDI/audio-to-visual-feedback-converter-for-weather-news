
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from google.cloud import speech
import SpeechToText
import threading
import os
from google.cloud import translate_v2 as translate
import map_generation
from PIL import Image, ImageTk
from map_generation import districts, provinces
from main import run_video_generation_process
import io
import sys

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\op\build\assets\frame0")

RATE = 44100
CHUNK = int(RATE / 10)  # 100ms
pauseSw = False
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "API.json"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1000x800")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1000,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    # relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    350.0,
    30.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#7382D2",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=0.0,
    y=0.0,
    width=1000.0,
    height=58.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    175.0,
    326.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    513.0,
    326.0,
    image=image_image_2
)

canvas.create_rectangle(
    155.0,
    88.0,
    565.0,
    153.0,
    fill="#D9D9D9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: start_listening(),
    relief="flat"
)
button_1.place(
    x=31.0,
    y=88.0,
    width=100.0,
    height=30.0
)

canvas.create_text(
    49.0,
    94.0,
    anchor="nw",
    text="Record",
    fill="#000000",
    font=("Inter", 14 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=31.0,
    y=128.0,
    width=100.0,
    height=30.0
)

canvas.create_text(
    45.0,
    135.0,
    anchor="nw",
    text="Pause",
    fill="#000000",
    font=("Inter", 14 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
)
button_3.place(
    x=588.0,
    y=86.0,
    width=65.0,
    height=65.0
)

canvas.create_text(
    700.0,
    105.0,
    anchor="nw",
    text="Generate",
    fill="#000000",
    font=("Inter", 14 * -1)
)
window.resizable(False, False)
window.mainloop()


def on_click(self, event):
    # Remove placeholder text when the text box is clicked
    if self.text_box.get("1.0", "end-1c") == "Start typing...":
        self.text_box.delete("1.0", "end-1c")


def start_listening(self):
    self.start_button.config(state=Tk.DISABLED)
    self.pause_button.config(state=Tk.NORMAL)
    self.stream_thread = threading.Thread(target=self.s2tfromthred)
    self.stream_thread.start()


def pause_listening(self):
    global pauseSw
    pauseSw = True
    self.start_button.config(state=Tk.NORMAL)
    self.pause_button.config(state=Tk.DISABLED)
    if self.stream_thread and self.stream_thread.is_alive():
        self.stream_thread.join(timeout=1)  # Wait for the streaming thread to finish
    if self.stream:
        self.stream.stop()  # Stop the microphone stream


def on_closing(self):
    global pauseSw
    pauseSw = True  # Set the flag to stop microphone stream
    if self.stream_thread and self.stream_thread.is_alive():
        self.stream_thread.join(timeout=1)  # Wait for the streaming thread to finish, with a timeout of 1 second
    if self.stream:
        self.stream.stop()  # Stop the microphone stream
    self.master.destroy()  # Close the window
    sys.exit()  # Exit the program


def listen_print_loop(self, responses):
    global pauseSw
    for response in responses:
        if pauseSw:  # Check if the microphone should be stopped
            break
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if not result.is_final:
            self.text_box.delete("1.0", Tk.END)
            self.text_box.insert(Tk.END, transcript + "\r")
        else:
            self.text_box.delete("1.0", Tk.END)
            self.text_box.insert(Tk.END, transcript + "\n")


def s2tfromthred(self):
    global pauseSw
    pauseSw = False
    language_code = "si-LK"

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with SpeechToText.MicrophoneStream(RATE, CHUNK) as self.stream:
        audio_generator = self.stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        self.listen_print_loop(responses)


def create(self):
    translate_client = translate.Client()
    text_to_translate = self.text_box.get("1.0", Tk.END).strip()
    if text_to_translate:
        translation = translate_client.translate(text_to_translate, target_language='en')
        print("Translated text:", translation['translatedText'])
        self.create_image_display(translation['translatedText'])


def create_image_display(self, paragraph):
    sentences = map_generation.sentence_split_from_paragraph(paragraph)
    for sentence in sentences:
        try:
            entities = map_generation.extract_all_entities(sentence, districts, provinces)
            dictionary = map_generation.create_dictionary(entities)
            map_generation.print_weather_mapping_dictionary(dictionary)
            fig = map_generation.display_map(dictionary)
            run_video_generation_process(dictionary)
            ax = fig.gca()
            ax.text(0.5, 1, sentence, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes,
                    fontsize=10)
            fig.set_size_inches(12, 5)
            # plt.show()

            # Convert matplotlib figure to a PNG image
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            img = Image.open(buffer)

            # Convert PIL Image to Tkinter PhotoImage
            photo = ImageTk.PhotoImage(img)

            # Update the label with the new image
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep reference to the image to prevent garbage collection

            # This line will pause execution until the user closes the current image
            self.master.update()

        except Exception as e:
            print(f"Error generating or displaying figure: {e}")