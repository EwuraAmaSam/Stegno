import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from moviepy.editor import AudioFileClip
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
import os
from scipy.io.wavfile import write as write_wav
import scipy.io.wavfile
import shutil


# Initialize pygame
pygame.mixer.init()

# Create the main application window
root = tk.Tk()
root.title("Audio Encryption Project")

# Dropdown menu for encryption methods
encryption_methods = ["Reverse", "Subtraction"]
selected_method = tk.StringVar()
selected_method.set(encryption_methods[0])

# Define file_path and converted_file_path 
file_path = None
converted_file_path = None

def open_file():
    global file_path, converted_file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        # Update the label text with the selected file's name
        text_label.config(text=os.path.basename(file_path))
        # Convert the audio file to .wav format
        converted_file_path = os.path.splitext(file_path)[0] + ".wav"
        if not os.path.exists(converted_file_path):
            clip = AudioFileClip(file_path)
            clip.write_audiofile(converted_file_path)
        # Plot the audio signal
        plot_audio(converted_file_path)
        # Play the audio
        play_audio(converted_file_path)

def plot_audio(file_path):
    try:
        # Load audio data using moviepy
        clip = AudioFileClip(file_path)
        frames = np.array(list(clip.iter_frames()))
        framerate = clip.fps

        # Plot the audio signal
        fig = plt.figure(figsize=(3, 2))  # Set a smaller figure size
        plt.plot(frames)
        plt.title("Audio Signal")
        plt.xlabel("Time (samples)")
        plt.ylabel("Amplitude")
        plt.grid(True)

        # Embed the Matplotlib figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open {file_path}: {e}")

def play_audio(file_path):
    try:
        # Load and play the converted audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to play {file_path}: {e}")

def reverse_audio(file_path):
    try:
        # Load audio data using moviepy
        clip = AudioFileClip(file_path)
        frames = np.array(list(clip.iter_frames()))

        # Reverse the audio frames
        reversed_frames = np.flip(frames, axis=0)

        # Return the reversed frames
        return reversed_frames

    except Exception as e:
        messagebox.showerror("Error", f"Failed to reverse audio: {e}")
        return None


def play_reversed_audio(reversed_frames, framerate):
    try:
        # Save the reversed audio
        temp_file_path = "reversed_audio.wav"
        # Write the reversed frames to the temporary WAV file
        scipy.io.wavfile.write(temp_file_path, framerate, reversed_frames)

        # Load and play the reversed audio using pygame
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to play reversed audio: {e}")

def add_noise(file_path):
    try:
        # Load audio data using moviepy
        clip = AudioFileClip(file_path)
        # Clip the audio unto frames so it can be manipulated.
        frames = np.array(list(clip.iter_frames()))
        
        # Generate noisy audio by adding random noise to the frames
        noisy_frames = frames - 0.2 * np.random.normal(0, 1, frames.shape)

        return noisy_frames

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add noise to audio: {e}")
        return None

def play_noisy_audio(noisy_frames, framerate):
    try:
        # Create a temporary WAV file to save the noisy audio
        temp_file_path = "noisy_audio.wav"
        # Write the noisy frames to the temporary WAV file
        scipy.io.wavfile.write(temp_file_path, framerate, noisy_frames)

        # Load and play the noisy audio using pygame
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to play noisy audio: {e}")


def encrypt_audio():
    global file_path, converted_file_path
    if selected_method.get() == "Reverse":
        if file_path and converted_file_path:
            reversed_frames = reverse_audio(converted_file_path)
            if reversed_frames is not None:
                # Plot the reversed audio signal
                fig = plt.figure(figsize=(3, 2))
                plt.plot(reversed_frames)
                plt.title("Reversed Audio Signal")
                plt.xlabel("Time (samples)")
                plt.ylabel("Amplitude")
                plt.grid(True)

                # Embed the Matplotlib figure in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().pack()

                # Get the framerate separately
                clip = AudioFileClip(converted_file_path)
                framerate = clip.fps

                # Play the reversed audio
                play_reversed_audio(reversed_frames, framerate)

        else:
            messagebox.showerror("Error", "Please select an audio file first.")
    elif selected_method.get() == "Addition":
        if file_path and converted_file_path:
            noisy_frames = add_noise(converted_file_path)
            if noisy_frames is not None:
                # Plot the noisy audio signal
                fig = plt.figure(figsize=(3, 2))
                plt.plot(noisy_frames)
                plt.title("Noisy Audio Signal")
                plt.xlabel("Time (samples)")
                plt.ylabel("Amplitude")
                plt.grid(True)

                # Embed the Matplotlib figure in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().pack()

                # Get the framerate separately
                clip = AudioFileClip(converted_file_path)
                framerate = clip.fps

                # Play the noisy audio
                play_noisy_audio(noisy_frames, framerate)

        else:
            messagebox.showerror("Error", "Please select an audio file first.")

# Create the Download button
def download_encrypted_audio():
    global converted_file_path
    if selected_method.get() == "Reverse":
        audio_path = "reversed_audio.wav"
    elif selected_method.get() == "Addition":
        audio_path = "noisy_audio.wav"
    else:
        messagebox.showerror("Error", "No encrypted audio available.")
        return
    
    if os.path.exists(audio_path):
        # Prompt the user to choose the download location
        download_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if download_path:
            # Copy the encrypted audio file to the chosen location
            shutil.copyfile(audio_path, download_path)
            messagebox.showinfo("Success", "Encrypted audio file downloaded successfully.")
    else:
        messagebox.showerror("Error", "No encrypted audio available.")


# Set the fixed size of the window
window_width = 400
window_height = 800
root.geometry(f"{window_width}x{window_height}")

# Disable window resizing
root.resizable(False, False)

# Create a Frame for the header
header_frame = tk.Frame(root, bg="yellow")
header_frame.pack(fill=tk.X)

# Put the program name in the header
header_text = tk.Label(header_frame, text="STEGNO", font=("Helvetica", 17, "bold"), bg="yellow", fg="black", pady=15)
header_text.pack(side=tk.RIGHT, padx=10, pady=10)

# Put the program tagline in the header.
left_text = tk.Label(header_frame, text="Share secure information...", font=("Helvetica", 10), bg="yellow", fg="black", pady=15)
left_text.pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame for uploading the audio
upload_audio_frame = tk.Frame(root, bg="black")  # Set the background color to yellow
upload_audio_frame.pack(fill=tk.X, padx=10, pady=20, ipadx=10)  # Adjust padding and add internal padding

# Text showing file name
text_label = tk.Label(upload_audio_frame, text="File name", bg="black", fg="white")
text_label.pack(side=tk.LEFT, padx=(30, 20))  # Add padding on the right side

# Create a Button to upload the audio
button = tk.Button(upload_audio_frame, text="Upload Audio", command=open_file, bg = "yellow", fg = "black", borderwidth=1, highlightthickness=0)
button.pack(side=tk.RIGHT, padx=(20, 30))  # Add padding on the left side

# Create the dropdown menu for encryption methods
dropdown = tk.OptionMenu(root, selected_method, *encryption_methods)
dropdown.pack()


# Create a Frame for the buttons - encrypt and download
button_frame = tk.Frame(root, bg="black")
button_frame.pack(fill=tk.X, padx=10, pady=10)

# Create the Encrypt button
encrypt_button = tk.Button(button_frame, text="Encrypt Audio", command=encrypt_audio, bg = "yellow", fg = "black", borderwidth=1, highlightthickness=0)
encrypt_button.pack(side=tk.LEFT, padx=10)

# Create the Download button
download_button = tk.Button(button_frame, text="Download", command=download_encrypted_audio, bg = "yellow", fg = "black", borderwidth=1, highlightthickness=0)
download_button.pack(side=tk.LEFT, padx=(180, 10))

# Run the Tkinter event loop
root.mainloop()
