import tkinter as tk
from google.cloud import speech
import SpeechToText
import threading
import os
from google.cloud import translate_v2 as translate
import map_generation
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from map_generation import districts, provinces
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import sys

# Audio recording parameters
RATE = 44100
CHUNK = int(RATE / 10)  # 100ms
pauseSw = False
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "API.json"

class SpeechRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognition App")
        self.master.geometry("1000x800")  # Set width and height of the window
        self.stream = None  # Store the microphone stream object
        self.stream_thread = None  # Initialize the stream thread

        self.start_button = tk.Button(self.master, text="Start Microphone", command=self.start_listening, bg="lightblue", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self.master, text="Pause Microphone", command=self.pause_listening, state=tk.DISABLED, bg="lightblue", font=("Arial", 12, "bold"))
        self.pause_button.pack(pady=10)

        self.text_box = tk.Text(self.master, height=1, width=50, borderwidth=10, relief=tk.FLAT)
        self.text_box.pack(fill=tk.BOTH, expand=True)
        self.text_box.configure(height=3)
        self.text_box.insert("1.0", "Start typing...")
        self.text_box.bind("<FocusIn>", self.on_click)

        self.translate_button = tk.Button(self.master, text="Create", command=self.create, bg="lightblue", font=("Arial", 12, "bold"))
        self.translate_button.pack(pady=10)

        self.image_label = tk.Label(self.master)
        self.image_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)  # Bind window closing event

    def on_click(self, event):
        # Remove placeholder text when the text box is clicked
        if self.text_box.get("1.0", "end-1c") == "Start typing...":
            self.text_box.delete("1.0", "end-1c")

    def start_listening(self):
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stream_thread = threading.Thread(target=self.s2tfromthred)
        self.stream_thread.start()
    
    def pause_listening(self):
        global pauseSw
        pauseSw = True
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
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
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, transcript + "\r")
            else:
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, transcript + "\n")

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
        text_to_translate = self.text_box.get("1.0", tk.END).strip()
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
                ax = fig.gca()
                ax.text(0.5, 1, sentence, horizontalalignment='center', verticalalignment='top', transform=ax.transAxes, fontsize=10)
                fig.set_size_inches(12, 5)
                #plt.show()

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

def main():
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
