'''
Before running the code, copy the pip command from below and run it in your console...
{

 pip install moviepy pydub SpeechRecognition google-cloud-speech

}
'''



import os
import tempfile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr

# Step 1: Extract audio from video and store in the temporary directory
def extract_audio(video_file, temp_dir):
    audio_file = os.path.join(temp_dir, "extracted_audio.wav")
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)
    print(f"Audio extracted to {audio_file}")
    return audio_file

# Step 2: Split the audio into chunks and store in the temporary directory
def split_audio(input_file, temp_dir, chunk_length_ms=60000):
    audio = AudioSegment.from_file(input_file)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    chunk_files = []
    
    for i, chunk in enumerate(chunks):
        chunk_filename = os.path.join(temp_dir, f"chunk_{i}.wav")
        chunk.export(chunk_filename, format="wav")
        chunk_files.append(chunk_filename)
        print(f"Exported {chunk_filename}")
    
    return chunk_files

# Step 3: Convert audio to text using Google Speech-to-Text (Bangla)
def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)
    
    with audio_data as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="bn-BD")
        print(f"Converted Text from {audio_file}: {text}")
        return text
    except sr.UnknownValueError:
        print(f"Could not understand audio from {audio_file}")
        return ""
    except sr.RequestError as e:
        print(f"Request failed for {audio_file}: {e}")
        return ""

# Step 4: Combine all text chunks into one transcript
def combine_text_chunks(text_chunks):
    return " ".join(text_chunks)

# Main function to run the video-to-text conversion and save output
def video_to_text():
    # Ask user for video file path and output text file name
    video_file = input("Enter the path to the video file: ")
    output_text_file = input("Enter the name for the output text file (e.g., output.txt): ")
    
    # Step 1: Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory created at: {temp_dir}")
        
        # Step 2: Extract audio and store in the temporary directory
        audio_file = extract_audio(video_file, temp_dir)
        
        # Step 3: Split audio into chunks in the temporary directory
        audio_chunks = split_audio(audio_file, temp_dir)
        
        # Step 4: Convert each audio chunk to text
        all_text_chunks = []
        for chunk in audio_chunks:
            text_chunk = convert_audio_to_text(chunk)
            all_text_chunks.append(text_chunk)
        
        # Step 5: Combine all text chunks into a single transcript
        final_transcript = combine_text_chunks(all_text_chunks)
        
        # Step 6: Save final transcript to a text file
        with open(output_text_file, "w", encoding="utf-8") as f:
            f.write(final_transcript)
        
        print("\nFinal Transcribed Text saved to:", output_text_file)
        
        # Temporary directory and all files within it will be deleted automatically here

# Example usage in Google Colab
if __name__ == "__main__":
    video_to_text()
