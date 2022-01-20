from tali.models.systems import CrossModalMatchingNetwork, ModusPrime

from .auto_builder.transformers import (
    AutoAverager,
    AutoCLIPResNet,
    AutoCLIPTextTransformer,
    AutoCLIPVisionTransformer,
)

model_hub = {
    "CrossModalisPrime": ModusPrime,
}