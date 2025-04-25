
from transformers import AutoTokenizer, T5EncoderModel
from llama_index.core.embeddings import  BaseEmbedding
from pydantic import PrivateAttr
from typing import Any
import torch

class CodeT5Embedder(BaseEmbedding):
    _tokenizer: Any = PrivateAttr()
    _model: Any = PrivateAttr()

    def __init__(self, model_name="Salesforce/codet5-base"):
        super().__init__()
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = T5EncoderModel.from_pretrained(model_name)
        self._model.eval()

    def _get_text_embedding(self, text: str) -> list[float]:
        with torch.no_grad():
            inputs = self._tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = self._model(**inputs)
            last_hidden = outputs.last_hidden_state
            pooled = last_hidden.mean(dim=1).squeeze().numpy()
        return pooled.tolist()

    def _get_query_embedding(self, query: str) -> list[float]:
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)