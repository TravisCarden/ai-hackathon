from langchain_community.embeddings import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

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

TEMPLATE = """Given an input, create syntactically correct PHP code. Don't provide any explanation with the code.

Use the following format:

Question: "Question here"
Answer: "Answer here"

Question: Write a Drupal functional test PHP function for the following
{question}"""

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
