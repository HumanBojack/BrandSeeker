import numpy as np
from itertools import chain


def filter_output(output, fps, time, seconds_threshold=1, score_threshold=0.1, alpha=0.7):

    total_predicted_frames = len(set(chain(*[content['frame'] for content in output.values()])))
    timeMin = time/60

    if alpha is None:
        alpha = max(0.4, min(0.85, (timeMin*0.025) + 0.2))
        print('Calculated alpha is: ', alpha)
    else:
        alpha = max(0, min(1, alpha))

    alphaFrame = 1 - alpha
    alphaConf = alpha

    # Remove the brands that appears less than the threshold authorizes
    frames_threshold = seconds_threshold * fps
    output = {brand: content for brand, content in output.items() if len(content['frame']) > frames_threshold}

    output_dict = {}
    for brand, content in output.items():

        regularized_frame = (len(content['frame']) / total_predicted_frames)
        regularized_conf = (np.median(content['confidence']))
        score = 2 / (1/(regularized_frame * alphaFrame) + 1/(regularized_conf * alphaConf))
        print(score, brand)
        max_conf = content['confidence'].index(max(content['confidence']))

        if score > score_threshold:
            output_dict[brand] = [score, (np.median(content['confidence'])), content['frame'][max_conf], content['bbox'][max_conf]]

    # if output_dict:
    #     maxscore = max(content[0] for content in output_dict.values())
    #     output = {brand: content for brand, content in output_dict.items() if content[0] > (maxscore - 0.1)}
    #     return output

    return output_dict