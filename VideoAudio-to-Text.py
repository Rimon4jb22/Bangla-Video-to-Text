
'''
Before running the code, copy the pip command from below and run it in your console...
{

 pip install yt-dlp SpeechRecognition

}
'''



import os
import re
import subprocess
import shutil

import yt_dlp
import speech_recognition as sr


CHUNK_SECONDS = 30
SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit PCM


def safe_name(name, limit=150):
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    name = re.sub(r"\s+", " ", name).strip() or "output"

    result = ""

    for char in name:
        if len((result + char).encode("utf-8")) > limit:
            break
        result += char

    return result.rstrip()


def unique_path(directory, name, extension):
    path = os.path.join(directory, f"{name}{extension}")
    counter = 1

    while os.path.exists(path):
        path = os.path.join(
            directory,
            f"{name}_{counter}{extension}"
        )
        counter += 1

    return path


def select_language():
    languages = {
        "1": ("বাংলা", "bn-BD"),
        "2": ("English", "en-US"),
        "3": ("Hindi", "hi-IN"),
        "4": ("Urdu", "ur-PK"),
        "5": ("Chinese", "zh-CN"),
        "6": ("Arabic", "ar-SA"),
        "7": ("Japanese", "ja-JP"),
        "8": ("Korean", "ko-KR"),
    }

    print("\nভিডিও / অডিওর ভাষা নির্বাচন করুন:\n")

    for number, (name, _) in languages.items():
        print(f"{number}. {name}")

    print("9. Other / নিজের Language Code দিন")

    while True:
        choice = input("\nOption দিন: ").strip()

        if choice in languages:
            name, code = languages[choice]
            print(f"\nSelected Language: {name} ({code})")
            return code

        if choice == "9":
            code = input(
                "\nLanguage code দিন (উদাহরণ: fr-FR): "
            ).strip()

            if code:
                return code

            print("Language code দেওয়া হয়নি!")
            continue

        print("ভুল option! আবার চেষ্টা করুন।")


def get_local_file(file_type):
    while True:
        path = input(
            f"\n{file_type} file-এর সম্পূর্ণ path দিন:\n> "
        ).strip().strip('"')

        if os.path.isfile(path):
            return path

        print("\nফাইল পাওয়া যায়নি। Path আবার চেক করুন।")


def download_video(url):
    print("\nভিডিওর তথ্য নেওয়া হচ্ছে...")

    with yt_dlp.YoutubeDL({
        "quiet": True,
        "noplaylist": True
    }) as ydl:
        info = ydl.extract_info(url, download=False)

    title = safe_name(
        info.get("title", "downloaded_video")
    )

    print(f"\nভিডিওর নাম:\n{title}")
    print("\nভিডিও ডাউনলোড হচ্ছে...")

    options = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(
            os.getcwd(),
            title + ".%(ext)s"
        ),
        "noplaylist": True,
        "windowsfilenames": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            url,
            download=True
        )

        video_file = ydl.prepare_filename(info)

        if info.get("requested_downloads"):
            video_file = (
                info["requested_downloads"][0]
                .get("filepath", video_file)
            )

    if not os.path.exists(video_file):
        raise FileNotFoundError(
            "ডাউনলোড করা ভিডিও পাওয়া যায়নি।"
        )

    return video_file, title


def transcribe(input_file, language):
    recognizer = sr.Recognizer()

    bytes_per_second = (
        SAMPLE_RATE
        * CHANNELS
        * SAMPLE_WIDTH
    )

    chunk_size = (
        bytes_per_second
        * CHUNK_SECONDS
    )

    print("\nSpeech-to-Text শুরু হচ্ছে...")

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", input_file,
        "-vn",
        "-ac", str(CHANNELS),
        "-ar", str(SAMPLE_RATE),
        "-f", "s16le",
        "-"
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=chunk_size
    )

    texts = []
    index = 0

    try:
        while True:

            pcm_data = process.stdout.read(
                chunk_size
            )

            if not pcm_data:
                break

            index += 1

            print(
                f"\nProcessing chunk {index}..."
            )

            audio_data = sr.AudioData(
                pcm_data,
                SAMPLE_RATE,
                SAMPLE_WIDTH
            )

            try:
                text = recognizer.recognize_google(
                    audio_data,
                    language=language
                ).strip()

                if text:
                    texts.append(text)
                    print(f"\nপাওয়া গেছে:\n{text}")

            except sr.UnknownValueError:
                print("এই অংশের কথা বোঝা যায়নি।")

            except sr.RequestError as e:
                print(
                    f"Google Speech API সমস্যা: {e}"
                )

            finally:
                del audio_data
                del pcm_data

    finally:

        if process.stdout:
            process.stdout.close()

        if process.poll() is None:
            process.terminate()

        process.wait()

    if not texts:
        raise RuntimeError(
            "কোনো speech থেকে text পাওয়া যায়নি।"
        )

    return "\n\n".join(texts)


def delete_file(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
            print(
                f"Deleted: "
                f"{os.path.basename(path)}"
            )

    except OSError as e:
        print(f"Delete failed: {e}")


def main():

    if not shutil.which("ffmpeg"):
        print(
            "\nFFmpeg পাওয়া যায়নি!"
            "\nFFmpeg PATH-এ add করুন।"
        )
        return

    print("\n" + "=" * 60)
    print("Video / Audio to Text Converter")
    print("=" * 60)

    print("\nSource নির্বাচন করুন:\n")
    print("1. Online Video")
    print("2. Offline Video")
    print("3. Offline Audio")

    while True:

        choice = input(
            "\nOption দিন (1/2/3): "
        ).strip()

        if choice in ("1", "2", "3"):
            break

        print(
            "ভুল option! শুধু 1, 2 অথবা 3 দিন।"
        )

    if choice == "1":

        source = input(
            "\nভিডিও URL দিন:\n> "
        ).strip()

        if not source:
            print("\nভিডিও URL দেওয়া হয়নি!")
            return

    elif choice == "2":

        source = get_local_file("ভিডিও")

    else:

        source = get_local_file("অডিও")


    # Source নেওয়ার পর Language নির্বাচন
    language = select_language()

    downloaded_video = False
    video_file = None

    try:

        if choice == "1":

            video_file, title = download_video(source)

            downloaded_video = True
            input_file = video_file

        else:

            input_file = source

            title = safe_name(
                os.path.splitext(
                    os.path.basename(source)
                )[0]
            )


        # Streaming transcription
        final_text = transcribe(
            input_file,
            language
        )


        # TXT save
        output_file = unique_path(
            os.getcwd(),
            title,
            ".txt"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(final_text)


        print("\n" + "=" * 60)
        print("সফলভাবে কাজ সম্পন্ন হয়েছে!")
        print("=" * 60)

        print(
            f"\nTXT File:\n"
            f"{os.path.basename(output_file)}"
        )


        if downloaded_video:

            delete_choice = input(
                "\nDownloaded video ডিলিট করবেন? "
                "(y/n): "
            ).strip().lower()

            if delete_choice in ("y", "yes"):
                delete_file(video_file)


    except Exception as e:

        print("\n" + "=" * 60)
        print("একটি সমস্যা হয়েছে!")
        print(str(e))
        print("=" * 60)


if __name__ == "__main__":
    main()