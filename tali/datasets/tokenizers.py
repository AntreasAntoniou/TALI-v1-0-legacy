import os

import torch
from torch import nn
from transformers import CLIPTokenizerFast

from tali.datasets.utils.simple_tokenizer import SimpleTokenizer
from tali.datasets.utils.tokenizers import tokenize
from base import utils

log = utils.get_logger(__name__)

class BPETokenizer(nn.Module):
    def __init__(self, context_length):
        super(BPETokenizer, self).__init__()
        self.tokenizer = SimpleTokenizer()
        self.context_length = context_length

    def forward(self, x):
        return tokenize(x, tokenizer=self.tokenizer, context_length=self.context_length)


class HuggingFaceBPETokenizer(nn.Module):
    def __init__(self, context_length):
        super(HuggingFaceBPETokenizer, self).__init__()
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.tokenizer = CLIPTokenizerFast.from_pretrained(
            "openai/clip-vit-base-patch16"
        )
        self.context_length = context_length

    def forward(self, x):
        tokenized_words = self.tokenizer(x[: self.context_length])["input_ids"]

        tokenized_tensor = torch.Tensor(tokenized_words)
        preshape = tokenized_tensor.shape
        if len(tokenized_tensor.shape) == 2:
            tokenized_tensor = tokenized_tensor.view(-1)
        postshape = tokenized_tensor.shape

        if len(tokenized_tensor) > self.context_length:
            return tokenized_tensor[: self.context_length]

        diff_length = self.context_length - len(tokenized_tensor)
        try:
            padding_tensor = torch.zeros(diff_length)
            return torch.cat([tokenized_tensor, padding_tensor], dim=0)
        except Exception:
            log.error(f'Error bro {preshape} {postshape}.')
        # logging.info(f'{x} {tokenized_words} {torch.Tensor(tokenized_words).shape} {padding_tensor}')

    def batch_decode(self, x):
        return self.tokenizer.batch_decode(x)

    def decode(self, x):
        return self.tokenizer.decode(x)
