from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

anthropic_claude_llm = ChatBedrock(
    region_name="us-east-1",
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1}
)

TEMPLATE = """Hello AI,

Do not output anything apart from the test case PHP code. I have a Drupal module and I need comprehensive automated tests created for it. Based on this data, generate tests that cover the functionalities reflected in the code.

Use the following format:
Question: "routing file data here"
Answer: "PHP test cases here"

Consider the following testing aspects:

- Backend logic: Create PHPUnit tests for services, hooks, and other PHP-based logic.
- Frontend behavior: If the module includes frontend components, create JavaScript tests that validate the user interface and interactions.
- Other Drupal-specific functionality: Generate tests for configuration forms, permissions, user interactions, entity operations, and more.

Focus on implementing detailed tests with assertions and logic that thoroughly validate the module's correctness and robust functionalities.

Question: {question}
"""

custom_prompt_template = PromptTemplate(
    input_variables=["question"], template=TEMPLATE
)

prompt = ChatPromptTemplate.from_template(TEMPLATE)
model = anthropic_claude_llm

chain = (
    {
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

def invoke(data):
    chain = (
        {
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(data)
