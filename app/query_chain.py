from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import BedrockEmbeddings
#from langchain_aws import BedrockLLM
#from langchain_community.chat_models import BedrockChat
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

embeddings_model_id = "amazon.titan-embed-text-v1"
region_name = "us-west-2"

bedrock_embedding = BedrockEmbeddings(
    region_name=region_name,
    model_id=embeddings_model_id
)

anthropic_claude_llm = ChatBedrock(
    region_name=region_name,
    model_id="anthropic.claude-3-haiku-20240307-v1:0"
)

TEMPLATE = """Use the following format:

Question: "Question here"
Answer: "Answer here"

Answer the question based only on the following context:

Question: What is my name?
Answer: Mriyam

Question: What is my age?
Answer: 28

Question: {question}"""

custom_prompt_template = PromptTemplate(
    input_variables=["context", "question"], template=TEMPLATE
)

model = anthropic_claude_llm
prompt = ChatPromptTemplate.from_template(TEMPLATE)
chain = (
    {
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)


def question_chain(question):
    chain = (
        {
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(question)
