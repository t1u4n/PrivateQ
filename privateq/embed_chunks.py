from typing import Dict, Any
from privateq.data_process import get_embedding_model

class EmbedChunks:
    def __init__(self, model_name: str) -> None:
        self.embedding_model = get_embedding_model(
            embedding_model_name=model_name,
            model_kwargs={"device": "cuda"},
            encode_kwargs={"device": "cuda", "batch_size": 100})
    
    def __call__(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        """Embed a batch of text.

        Args:
            batch: A batch of text.
        Returns:
            A batch of text with embeddings.
        """
        embeddings = self.embedding_model.embed_documents(batch["text"])
        return {"text": batch["text"], "source": batch["source"], "embeddings": embeddings}