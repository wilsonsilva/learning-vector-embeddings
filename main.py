from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from datasets import load_dataset
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores.cassandra import Cassandra

import os

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_DB_CLIENT_ID = os.getenv('ASTRA_DB_CLIENT_ID')
ASTRA_DB_CLIENT_SECRET = os.getenv('ASTRA_DB_CLIENT_SECRET')
ASTRA_DB_KEYSPACE = os.getenv('ASTRA_DB_KEYSPACE')
ASTRA_DB_SECURE_BUNDLE_PATH = os.getenv('ASTRA_DB_SECURE_BUNDLE_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

cloud_config = {'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH}

auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astra_session = cluster.connect()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
my_embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

my_cassandra_vector_store = Cassandra(
  embedding=my_embedding,
  session=astra_session,
  keyspace=ASTRA_DB_KEYSPACE,
  table_name="qa_mini_demo",
)

# Dataset multiple Onion News (fake/parody) articles
print("Loading data from huggingface")
my_dataset = load_dataset("Biddls/Onion_News", split="train")
headlines = my_dataset["text"][:50]

print("\nGenerating embeddings and storing in AstraDB")
my_cassandra_vector_store.add_texts(headlines)

print("Inserted %i headlines.\n" % len(headlines))

vector_index = VectorStoreIndexWrapper(vectorstore=my_cassandra_vector_store)
first_question = True

while True:
  if first_question:
    query_text = input("\nEnter your question (or type 'quit' to exit): ")
    first_question = False
  else:
    query_text = input("\nWhat's your next question (or type 'quit' to exit): ")

  if query_text == "quit":
    break

  print("QUESTION: \"%s\"" % query_text)
  answer = vector_index.query(query_text, llm=llm).strip()
  print("ANSWER: \"%s\"\n" % answer)

  print("DOCUMENTS BY RELEVANCE")

  for doc, score in my_cassandra_vector_store.similarity_search_with_score(query_text, k=4):
    print(" %0.4f \"%s ...\"" % (score, doc.page_content[:60]))
