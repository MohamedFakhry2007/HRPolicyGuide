"""
Retrieval-Augmented Generation implementation for the HR Policy Chatbot.

This module handles the retrieval of relevant documents and generation of responses.
"""

import os
import logging
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from hr_policy_chatbot.database import get_all_policy_documents, log_chat_interaction

# Set up logger
logger = logging.getLogger(__name__)

# Initialize Google Generative AI
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

# TF-IDF vectorizer for document retrieval
vectorizer = None
document_vectors = None
documents = None

# Initialize the retrieval system when the module is loaded
try:
    logger.info("Auto-initializing retrieval system on module load")
    if vectorizer is None or document_vectors is None or documents is None:
        # We'll initialize on first use
        pass
except Exception as e:
    logger.error(f"Error auto-initializing retrieval system: {str(e)}", exc_info=True)


def initialize_retrieval_system():
    """
    Initialize the document retrieval system.
    
    This function loads all policy documents from the database,
    tokenizes them, and computes TF-IDF vectors for efficient retrieval.
    """
    global vectorizer, document_vectors, documents
    
    logger.info("Initializing retrieval system")
    
    try:
        # Get all policy documents from the database
        documents = get_all_policy_documents()
        
        if not documents:
            logger.warning("No policy documents found in the database")
            return
        
        # Extract document contents
        doc_contents = [doc["content"] for doc in documents]
        
        # Initialize and fit the TF-IDF vectorizer
        vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
        document_vectors = vectorizer.fit_transform(doc_contents)
        
        logger.info(f"Retrieval system initialized with {len(documents)} documents")
    
    except Exception as e:
        logger.error(f"Error initializing retrieval system: {str(e)}", exc_info=True)
        raise


def preprocess_query(query):
    """
    Preprocess a user query for retrieval with Arabic support.
    
    Args:
        query: The user's query text.
        
    Returns:
        Preprocessed query text.
    """
    logger.debug(f"Preprocessing query: {query}")
    
    try:
        # Define Arabic stopwords
        arabic_stopwords = {
            'في', 'من', 'على', 'و', 'ال', 'الى', 'ما', 'هل', 'عن', 'مع',
            'هذا', 'هذه', 'هذان', 'هؤلاء', 'هناك', 'كيف', 'اين', 'متى'
        }
        
        # Convert to lowercase and split into words
        words = query.lower().split()
        
        # Remove stopwords and keep only Arabic text
        words = [w for w in words if w not in arabic_stopwords]
        
        # Join back into string
        preprocessed_query = " ".join(words)
        
        logger.debug(f"Preprocessed query: {preprocessed_query}")
        return preprocessed_query
    
    except Exception as e:
        logger.error(f"Error preprocessing query: {str(e)}", exc_info=True)
        return query


def retrieve_relevant_documents(query, top_n=3):
    """
    Retrieve the most relevant policy documents for a given query.
    
    Args:
        query: The user's query text.
        top_n: The number of top documents to retrieve.
        
    Returns:
        List of relevant documents with their relevance scores.
    """
    global vectorizer, document_vectors, documents
    
    logger.info(f"Retrieving relevant documents for query: {query}")
    
    try:
        # Initialize retrieval system if not already initialized
        if vectorizer is None or document_vectors is None or documents is None:
            initialize_retrieval_system()
        
        # If still no documents, return empty list
        if not documents:
            logger.warning("No policy documents available for retrieval")
            return []
        
        # Preprocess the query
        preprocessed_query = preprocess_query(query)
        
        # Transform the query to TF-IDF vector space
        query_vector = vectorizer.transform([preprocessed_query])
        
        # Calculate similarity scores between query and documents
        similarity_scores = cosine_similarity(query_vector, document_vectors).flatten()
        
        # Get indices of top N documents sorted by similarity score
        top_indices = similarity_scores.argsort()[-top_n:][::-1]
        
        # Filter out documents with very low relevance
        relevant_docs = []
        for idx in top_indices:
            score = similarity_scores[idx]
            if score > 0.1:  # Minimum relevance threshold
                doc = documents[idx]
                relevant_docs.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "content": doc["content"],
                    "relevance_score": float(score)
                })
        
        logger.info(f"Retrieved {len(relevant_docs)} relevant documents")
        logger.debug(f"Relevant document scores: {[doc['relevance_score'] for doc in relevant_docs]}")
        
        return relevant_docs
    
    except Exception as e:
        logger.error(f"Error retrieving relevant documents: {str(e)}", exc_info=True)
        return []


async def generate_response(query, relevant_docs):
    """
    Generate a response to the user's query using Gemini and retrieved documents.
    
    Args:
        query: The user's query text.
        relevant_docs: List of relevant documents to use as context.
        
    Returns:
        Generated response text.
    """
    logger.info("Generating response with Gemini")
    
    try:
        # Prepare context from relevant documents
        context = ""
        if relevant_docs:
            context = "معلومات السياسات المتعلقة:\n\n"
            for i, doc in enumerate(relevant_docs):
                context += f"وثيقة {i+1}: {doc['title']}\n{doc['content']}\n\n"
        
        # Prepare prompt for Gemini
        prompt = f"""
        أنت مساعد للموارد البشرية في مؤسسة مالية. مهمتك هي الإجابة على أسئلة الموظفين بخصوص سياسات الموارد البشرية.
        استخدم المعلومات المقدمة فقط للإجابة، وإذا لم تجد إجابة محددة، فقل ذلك بصراحة.
        قدم إجابات واضحة ومختصرة ومفيدة باللغة العربية، مع أن تكون ودودة ومهنية.
        
        معلومات السياسات:
        {context}
        
        سؤال الموظف: {query}
        """
        
        # Generate response using a supported Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = await model.generate_content_async(prompt)
        
        # Extract response text
        response_text = response.text
        
        # Log the interaction to the database
        log_chat_interaction(query, response_text)
        
        logger.info("Response generated successfully")
        logger.debug(f"Generated response: {response_text[:100]}...")
        
        return response_text
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}", exc_info=True)
        return "عذراً، حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة مرة أخرى لاحقاً."
