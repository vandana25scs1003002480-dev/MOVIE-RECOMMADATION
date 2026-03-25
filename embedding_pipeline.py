# embedding_pipeline.py

import time
import pandas as pd
from tqdm import tqdm
from chroma_utils import get_or_create_collection, add_documents

def store_tmdb_dataframe(df: pd.DataFrame):
    db = get_or_create_collection("movie_vectors")

    texts = df["overview"].tolist()
    ids = df["tmdb_id"].astype(str).tolist()
    metas = df.to_dict("records")

    batch_size = 100

    for i in tqdm(range(0, len(df), batch_size)):
        batch_docs = texts[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        batch_meta = metas[i:i + batch_size]

        add_documents(db, batch_docs, batch_ids, batch_meta)
        time.sleep(60)  # Gemini rate limit

    print("Vector DB built successfully!")
