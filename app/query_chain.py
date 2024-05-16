from langchain_aws import ChatBedrock
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings_model_id = "amazon.titan-text-express-v1"
region_name = "us-west-2"

bedrock_embedding = BedrockEmbeddings(
    region_name=region_name,
    model_id=embeddings_model_id
)

anthropic_claude_llm = ChatBedrock(
    region_name=region_name,
    model_id="anthropic.claude-3-haiku-20240307-v1:0"
)

TEMPLATE = """Given an input, create syntactically correct PHP code. Don't provide any explanation with the code. Use the following format:

Question: "Question here"
Answer: "Answer here"

Answer the question based only on the following context:
{context}

Question: Write Drupal functional test for the following
{question}"""

custom_prompt_template = PromptTemplate(
    input_variables=["context", "question"], template=TEMPLATE
)

# Load the data and split it into chunks
loader = DirectoryLoader('./ragdata')
documents = loader.load()

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
)
docs = text_splitter.split_documents(documents)

# Load the embeddings into Chroma in-memory vector store
vectorstore = Chroma.from_documents(docs, embedding=bedrock_embedding)
vectorstore_retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

model = anthropic_claude_llm
prompt = ChatPromptTemplate.from_template(TEMPLATE)
chain = (
    {
        "context": vectorstore_retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)


def question_chain(question):
    chain = (
        {
            "context": vectorstore_retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(question)
