from profanity_check import predict
import re


# checks msg for profanity using profanity_check. Returns 1 if found, 0 if not
def profanity_filter(msg):
    if predict(msg):
        return 1
    else:
        return 0


# checks msg for links in it. Returns 1 if found, 0 if not
def url_filter(msg: str):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, msg)
    if url:
        print([x[0] for x in url])
        return 1
    elif not url:
        return 0
