from utils import preprocess_text, load_embedding_model, embed_text
from qdrant_client import QdrantClient, models
import config

class EmbeddingVectorDBManager:
    def __init__(self):
        
        # self.embedding_model =  embedding_model
        
        self.client = QdrantClient(url="http://localhost:6333")
        
        # self.persist_directory = persist_directory
        # self.vector_store = None
        
    # tiền xử lý
    def preprocess(self, chunk):       
        text = preprocess_text(chunk["user"])
        return text
    

    #TẠO COLLECTION
    def create(self, collection_name = config.VECTOR_STORE['collection_name']):
        
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

    def add(self, chunks, collection_name = config.VECTOR_STORE['collection_name']):
        
        tokenizer, model = load_embedding_model()

        if self.client.collection_exists(collection_name=collection_name):
            print(collection_name," exists")
        else :
            print(collection_name," doesn't exist. Start create...")
            self.create(collection_name)

        self.client.upload_points(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=id,
                    vector=embed_text(self.preprocess(chunk), tokenizer, model),
                    payload=chunk,
                )for id, chunk in enumerate(chunks) #if doc['KeyPK'] > 80000
            ],
            batch_size=256
        )
    # delete
    def delete(self, collection_name = config.VECTOR_STORE['collection_name']):
        
        self.client.delete_collection(collection_name=collection_name)
        print(f"Deleted {collection_name}.")

    # get collections
    def get_list(self):
        list = self.client.get_collections()
        print(list)

###################################

import json

data_json = config.DATA
with open(data_json, 'r', encoding='utf-8') as file:
    dataset = json.load(file)


embed_manager = EmbeddingVectorDBManager()

# embed_manager.add(dataset)

# embed_manager.delete()
embed_manager.get_list()