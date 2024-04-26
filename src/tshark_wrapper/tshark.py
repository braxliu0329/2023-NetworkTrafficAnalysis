import subprocess
import re

REQUEST_PATTERN = re.compile(r'^(GET|POST|PUT|DELETE|HEAD)\s\S+\s(HTTP\/1\.1|HTTP\/2)')
RESPONSE_PATTERN = re.compile(r'(HTTP\/1\.1|HTTP\/2)\s(\d{3})\s\S+')

# Call a tshark subprocess to follow a TCP stream
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

def split_stream(stream):
    lines = stream.split('\n')
    requests = []
    responses = []
    for i in range(len(lines)):
        if re.match(REQUEST_PATTERN, lines[i]):
            requests.append(i)
        if re.match(RESPONSE_PATTERN, lines[i]):
            responses.append(i)
    return ('\n'.join(requests), '\n'.join(responses))


# You can easily extend this to work for UDP, TLS, and HTTP/2 streams by
# changing it from "tcp" to "xyz" in the command payload



