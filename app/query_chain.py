from langchain_aws import ChatBedrock
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter

#embeddings_model_id = "amazon.titan-embed-text-v2:0"
region_name = "us-east-1"

#bedrock_embedding = BedrockEmbeddings(
#    region_name=region_name,
#    model_id=embeddings_model_id
#)

anthropic_claude_llm = ChatBedrock(
    region_name=region_name,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0"
)

TEMPLATE = """Hello AI,

I have a Drupal module and I need comprehensive automated tests created for it. I'm providing you with JSON data that represents the structure and contents of the module's files. Based on this data, generate tests that cover the functionalities reflected in the code.

Consider the following testing aspects:

Backend logic: Create PHPUnit tests for services, hooks, and other PHP-based logic.
Frontend behavior: If the module includes frontend components, create JavaScript tests that validate the user interface and interactions.
Other Drupal-specific functionality: Generate tests for configuration forms, permissions, user interactions, entity operations, and more.
Focus on implementing detailed tests with assertions and logic that thoroughly validate the module's correctness and robust functionalities. Here's the JSON data representing the module:

Input: {input}

Once the tests are written, output them in a JSON format that can be consumed by the create_files.php script for creating test files in the Drupal module directory."""

custom_prompt_template = PromptTemplate(
    #input_variables=["context", "input"], template=TEMPLATE
    input_variables=["input"], template=TEMPLATE
)

## Load the data and split it into chunks
#loader = DirectoryLoader('./ragdata')
#documents = loader.load()

## Split document into chunks
#text_splitter = RecursiveCharacterTextSplitter(
#    chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
#)
#docs = text_splitter.split_documents(documents)

## Load the embeddings into Chroma in-memory vector store
#vectorstore = Chroma.from_documents(docs, embedding=bedrock_embedding)
#vectorstore_retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

model = anthropic_claude_llm
prompt = ChatPromptTemplate.from_template(TEMPLATE)
chain = (
    {
        #"context": vectorstore_retriever,
        "input": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)


def input_chain(question):
    chain = (
        {
            #"context": vectorstore_retriever,
            "input": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(question)
