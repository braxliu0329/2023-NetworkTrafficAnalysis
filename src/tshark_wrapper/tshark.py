import subprocess
import re

def tcp_stream(capture, format, stream):
    command = [
        'tshark',
        '-r',
        capture,
        '-qz',
        f'follow,tcp,{format},{stream}'
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    return None
