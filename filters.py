from profanity_check import predict


def profanity_filter(msg):
    if predict(msg):
        return True
    else:
        return False
