import logging

import cv2
import torch

log = logging.getLogger(__name__)


def load_frames(
    selected_frame_list,
    image_height,
    image_width,
    image_channels,
):
    image_tensor = torch.zeros(
        (len(selected_frame_list), image_channels, image_height, image_width)
    )

    for idx, frame_filepath in enumerate(selected_frame_list):

        image = cv2.imread(frame_filepath)
        image = (
            cv2.resize(
                image, (image_width, image_height), interpolation=cv2.INTER_CUBIC
            )
            / 255.0
        )
        image = torch.Tensor(image).permute([2, 0, 1])
        image_tensor[idx] = image

    return image_tensor