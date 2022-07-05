import numpy as np
from itertools import chain


def filter_output(output, fps, time, seconds_threshold=2, score_threshold=0.09, alpha=0.7):

    total_predicted_frames = len(set(chain(*[content['frame'] for content in output.values()])))
    timeMin = time/60

    if alpha is None:
        if timeMin > 30:
            alpha = 0.2
        elif timeMin < 10:
            alpha = 0.6
        else:
            alpha = timeMin * 0.2 / 10

    alphaFrame = 1 - alpha
    alphaConf = alpha

    # Remove the brands that appears less than the threshold authorizes
    frames_threshold = seconds_threshold * fps
    output = {brand: content for brand, content in output.items() if len(content['frame']) > frames_threshold}

    output_dict = {}
    for brand, content in output.items():

        regularized_frame = 1 / (len(content['frame']) / total_predicted_frames)
        regularized_conf = 1 / (np.median(content['confidence']))
        score = 2 / (regularized_frame * alphaFrame + regularized_conf * alphaConf)
        max_conf = content['confidence'].index(max(content['confidence']))

        if score > score_threshold:
            output_dict[brand] = [score, (np.median(content['confidence'])), content['frame'][max_conf], content['bbox'][max_conf]]


    maxscore = max(content[0] for content in output_dict.values())
    output = {brand: content for brand, content in output_dict.items() if content[0] > (maxscore - 0.1)}

    return output