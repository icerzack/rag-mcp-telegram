# RAG basics

Retrieval-Augmented Generation (RAG) typically works like this:

1. Ingest documents (read from files, APIs, databases, etc.).
2. Split into chunks (fixed-size, semantic, or hierarchical chunking).
3. Embed chunks into vectors using an embedding model (e.g., sentence-transformers, OpenAI embeddings).
4. Store vectors in a vector DB (e.g., Chroma, Pinecone, Qdrant, Weaviate).
5. At query time, embed the user question using the same embedding model.
6. Retrieve the most similar chunks (cosine similarity, L2 distance, etc.).
7. Provide chunks as context to the LLM and generate an answer.

## Chunking strategies
- Fixed-size: simple, works for most cases (e.g., 1000 chars with 200 overlap).
- Semantic chunking: split at sentence/paragraph boundaries, preserve meaning.
- Hierarchical: chunk at multiple levels (document → section → paragraph).
- Overlap: important to preserve context across chunk boundaries.

## Embedding models
- General-purpose: `all-MiniLM-L6-v2`, `paraphrase-multilingual-MiniLM-L12-v2`.
- Domain-specific: fine-tuned models for specific domains (code, medical, legal).
- Multilingual: important for non-English content.
- Size vs quality tradeoff: larger models are better but slower.

## Vector stores
- Chroma: simple, embedded, good for prototyping.
- Pinecone: managed, scalable, pay-per-use.
- Qdrant: self-hosted, fast, good filtering.
- Weaviate: graph + vector, advanced features.
- FAISS: Facebook's library, in-memory, very fast.

## Retrieval strategies
- Top-k: return k most similar chunks (simple, fast).
- MMR (Maximal Marginal Relevance): balance similarity and diversity.
- Hybrid search: combine vector search with keyword/BM25.
- Re-ranking: use a cross-encoder to re-rank top-k results.

## Prompting best practices
- Good prompts explicitly constrain the model to use the provided context only.
- Include clear instructions: "Answer based only on the CONTEXT below. If the answer is not in the context, say so."
- Format context clearly: use markers like "SOURCE: <file>" to show provenance.
- Limit context size: most LLMs have token limits (e.g., 4k, 8k, 32k tokens).
- Include metadata: file names, timestamps, confidence scores help the model.

## Common issues
- Hallucination: model makes up facts not in context. Mitigate with strict prompts and source citations.
- Weak retrieval: wrong chunks retrieved. Try better embeddings, hybrid search, or re-ranking.
- Context overflow: too many chunks exceed token limit. Use better chunking or limit top-k.
- Stale data: documents updated but index not refreshed. Implement reindexing strategy.

## Evaluation
- Measure retrieval quality: precision@k, recall@k, MRR (Mean Reciprocal Rank).
- Measure answer quality: factual accuracy, relevance, completeness.
- A/B test different chunking/embedding strategies.
- Use human evaluation for subjective quality metrics.

