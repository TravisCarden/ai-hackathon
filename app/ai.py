from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import prompt_data

# Initialize the model with specified parameters
def initialize_model():
    return ChatBedrock(
        region_name="us-east-1",
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1}
    )

# Define the prompt template
def get_template():
    return """Hello AI,

Do not output anything apart from the test case PHP code. I have a Drupal module and I need comprehensive automated tests created for it. Based on this data, generate tests that cover the functionalities reflected in the code.

Use the following format:
Question: "routing file data here"
Answer: "PHP test cases here"

Consider the following testing aspects:

- Backend logic: Create PHPUnit tests for services, hooks, and other PHP-based logic.
- Frontend behavior: If the module includes frontend components, create JavaScript tests that validate the user interface and interactions.
- Other Drupal-specific functionality: Generate tests for configuration forms, permissions, user interactions, entity operations, and more.

Focus on implementing detailed tests with assertions and logic that thoroughly validate the module's correctness and robust functionalities.

Here are some examples of routing files and test cases which are in JSON format:
Question: """ + prompt_data.question + """
Answer: """ + prompt_data.answer + """

Question: {question}
"""

# Create a custom prompt template
def create_prompt_template():
    template = get_template()
    return PromptTemplate(
        input_variables=["question"],
        template=template
    )

# Create the chat prompt template from the template string
def create_chat_prompt_template(template):
    return ChatPromptTemplate.from_template(template)

# Create the chain to invoke the model with the provided data
def create_chain(model, prompt):
    return (
        {
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )

# Main function to set up and run the model invocation
def invoke(data):
    model = initialize_model()
    custom_prompt_template = create_prompt_template()
    prompt = create_chat_prompt_template(custom_prompt_template.template)
    chain = create_chain(model, prompt)
    return chain.invoke(data)
