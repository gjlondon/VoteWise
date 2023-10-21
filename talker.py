from pathlib import Path
import uuid
import subprocess
import glob
import urllib.parse
import argparse
import os
import nltk
from nltk.tokenize import sent_tokenize
import time


from pydub import AudioSegment
import fakeyou

from environs import Env

env = Env()
# Read .env into os.environ
env.read_env()

FAKE_YOU_USER = env.str("FAKE_YOU_USER")
FAKE_YOU_PASSWORD = env.str("FAKE_YOU_USER")


def make_audio(msg, voice):
    fu = fakeyou.FakeYou()
    fu.login(FAKE_YOU_USER, FAKE_YOU_PASSWORD)

    result = fu.say(msg, voice)

    voice_name = uuid.uuid4()
    filename = Path(f'./audio/{voice_name}.wav')
    filename.write_bytes(result.content)
    return filename


def concatenate_wav_files(file_list, output_file, max_length=40 * 1000):  # max_length in milliseconds
    # Empty audio segment
    combined = AudioSegment.empty()

    # Loop through file names and concatenate
    for file_name in file_list:
        sound = AudioSegment.from_wav(file_name)
        combined += sound

        # Trim the audio if it's longer than max_length
        if len(combined) > max_length:
            combined = combined[:max_length]
            break  # Exit the loop as we've reached the max length

    # Export combined audio
    combined.export(output_file, format="wav")
    return output_file


def make_video(audio, image):
    print(audio)
    print(image)

    # Generate a UUID
    dir_name = str(uuid.uuid4())

    # Define the directory path. If you want it in a specific location, adjust the parent directory accordingly.
    dir_path = Path('.') / "video" / dir_name

    # Create the directory
    dir_path.mkdir(parents=True, exist_ok=True)

    current_directory = os.getcwd()

    command = [
        "docker", "run", "--gpus", "all", "--rm",
        "-v", f"{current_directory}:/host_dir", "wawa9000/sadtalker",
        "--driven_audio", f"/host_dir/{audio}",
        "--source_image", f"/host_dir/{image}",
        "--expression_scale", "1.0",
        "--still",
        "--result_dir", f"/host_dir/{dir_path}"
    ]

    print(command)

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Docker command executed successfully!")
        print(result.stdout)
    else:
        print("Docker command failed!")
        print(result.stderr)

    return glob.glob(f"{dir_path}/*/*.mp4")


def video_from_text(msg_list, image, voice):
    wav_paths = []

    for msg in msg_list:
        wav_paths.append(make_audio(msg, voice))
        time.sleep(1)

    voice_name = uuid.uuid4()
    filename = Path(f'./audio/{voice_name}.wav')
    output_wave = concatenate_wav_files(wav_paths, filename)

    video_path = make_video(output_wave, image)[0]

    return video_path


def get_full_url(relative_path):
    base_url = "http://votewise.radiantmachines.com:9000/"
    # Encode the path to make sure it's URL safe
    encoded_path = urllib.parse.quote(relative_path, safe='/:')
    return base_url + encoded_path



# arnold
"TM:gx7a6exf3bda"
# picard
"TM:zxfsed6gd89j"
# SJ
"TM:ky7m707xwp8y"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make Vid')
    msg  = "Hello There! I'm happy I could help you figure out who to vote for and which issues to support by understanding who you are and what matters most to you. Because you care about environmental protection and job creation, make sure to vote on November 5th. "
    msg = "Hi There, Don't forget to Vote for VoteWise - the world's first AI-powered personalized voter guide that is helping to ensure everyone votes and every vote counts. Help us use AI to deepen democracy and build a better world. Go here to vote for VoteWise. "
    talk = sent_tokenize(msg)
    video_from_text(talk, "static/votewise.jpg", "TM:ky7m707xwp8y")
    #make_audio(msg, "TM:ky7m707xwp8y" )
    #make_video("audio/d7de53ff-1837-4f7e-8855-0a9cc1685bc5.wav", "static/votewise.jpg")

