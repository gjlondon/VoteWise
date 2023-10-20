from pathlib import Path
import uuid
import subprocess
import glob
import urllib.parse

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


def concatenate_wav_files(file_list, output_file, max_length=30 * 1000):  # max_length in milliseconds
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

    command = [
        "docker", "run", "--gpus", "all", "--rm",
        "-v", "/home/paperspace/code/sad:/host_dir", "wawa9000/sadtalker",
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


long = [
    "Ensign, On Stardate Saturday, you bypassed your training. "
    "Remember, stagnation halts our journey. Engage in daily exercises. Our ship's efficiency relies on your utmost fitness. ",
    "Pursue your fencing and sprints with diligence.",
    "This isn't just about the Federation, but transcending your own limits. On the holodeck, show that holographic iron your resolve. Every action defines your Starfleet legacy. Engage and persevere!",
    "Captain Picard."
]

# arnold
"TM:gx7a6exf3bda"
# picard
"TM:zxfsed6gd89j"
# SJ
"TM:ky7m707xwp8y"
