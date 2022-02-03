import logging
import pathlib

import defusedxml.ElementTree as ET
import numpy as np

from tali.utils.storage import load_json

log = logging.getLogger(__name__)


def load_text_into_language_time_stamps(filepath):
    filepath = pathlib.Path(f"{filepath}".replace("\n", ""))
    caption_data_filepath = pathlib.Path(
        filepath.parent / "start_timestamp_to_caption_dict.yaml"
    )

    # if caption_data_filepath.exists():
    #     return load_yaml(caption_data_filepath)

    meta_data = load_json(filepath)

    captions = meta_data["captions"]

    captions_matched = {
        key: value for key, value in captions.items() if key in ["a.en", "en"]
    }

    if len(captions_matched) > 1:
        selected_key = "en"
    else:
        selected_key = list(captions_matched.keys())[0]

    selected_captions = captions_matched[selected_key]
    xml_tree = ET.fromstring(selected_captions)

    root = list(xml_tree.iter())
    timestamp_to_caption_dict = {}

    for item in root:
        if selected_key == "a.en":
            children_text = [
                child.text.replace("\n", " ")
                for child in item
                if child.text is not None
            ]
            if item.tag == "p" and children_text:
                timestamp_to_caption_dict[
                    float(item.attrib["t"]) / 1000
                ] = children_text

        elif selected_key == "en":
            if item.tag == "p" and len(item.items()) == 2:
                [(_, start), (_, dur)] = item.items()

                timestamp_to_caption_dict[float(start) / 1000] = (
                    item.text.replace("\n", " ") if item.text is not None else ""
                )

    # save_yaml(object_to_store=timestamp_to_caption_dict, filepath=caption_data_filepath)

    return timestamp_to_caption_dict


def get_text_tokens(meta_data_filepath, start_timestamp, end_timestamp):
    # logging.info(f'{start_timestamp} {end_timestamp}')
    timestamp_to_caption_dict = load_text_into_language_time_stamps(
        filepath=meta_data_filepath
    )
    start_timestamp = float(np.floor(start_timestamp))
    end_timestamp = float(np.floor(end_timestamp))

    temp_timestamp_to_caption_dict = {}

    for current_start_timestamp in sorted(timestamp_to_caption_dict.keys()):
        current_start_timestamp_float = float(current_start_timestamp)
        if start_timestamp <= current_start_timestamp_float <= end_timestamp:
            temp_timestamp_to_caption_dict[
                current_start_timestamp_float
            ] = timestamp_to_caption_dict[current_start_timestamp]

        if current_start_timestamp_float > end_timestamp:
            break

    return temp_timestamp_to_caption_dict