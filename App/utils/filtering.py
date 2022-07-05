import numpy as np
from itertools import chain

def filter_output(output, fps, seconds_threshold=2, confidence_threshold= 0.09, alpha = 0.7):

    alphaFrame = alpha
    alphaConf = 1 - alpha

    # Remove the brands that appears less than the threshold authorizes
    frames_threshold = seconds_threshold * fps
    output = {brand: content for brand, content in output.items() if len(content['frame']) > frames_threshold}

    # Remove the brands with a median confidence under our threshold
    total_predicted_frames = len(set(chain(*[content['frame'] for content in output.values()])))

    output_dict = {}
    
    for brand, content in output.items():

        regularized_frame = 1 / (len(content['frame']) / total_predicted_frames)
        regularized_conf = 1 / (np.median(content['confidence']))
        score = 2 / (regularized_frame * alphaFrame + regularized_conf * alphaConf)
        max_conf = content['confidence'].index(max(content['confidence']))

        if score > confidence_threshold:
            output_dict[brand] = [score, (np.median(content['confidence'])), content['frame'][max_conf], content['bbox'][max_conf]]

    return output_dict