# Drupal Module Test Generator - an Acquia 48Create 2024 AI Hackathon Project

The Drupal Module Test Generator is a Python application designed to automate the creation of comprehensive test cases for Drupal modules based on their routing files. It utilizes the [Bedrock service](https://aws.amazon.com/bedrock) from AWS for the [Claude Sonnet model](https://aws.amazon.com/bedrock/claude/), [Streamlit](https://streamlit.io/) for the user interface, and [LangChain](https://www.langchain.com/) for natural language processing.

## Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/TravisCarden/ai-hackathon.git
    ```

2. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Run `source assume-role.sh`, then enter your MFA when asked. This assumes you have `CloudServicesDev` and `AWS-Users` AWS accounts set up for AWS CLI locally.

3. Run the Streamlit app:

    ```bash
    streamlit run app/main.py
    ```

4. Access the Streamlit app in your browser and provide the routing file data as input. The app will generate PHP test cases based on the provided data.


## Development

Once you've followed the steps to run the application, you'll be ready to start developing it further. Additionally, for those already utilizing Docker and Visual Studio Code, we've set up a [`devcontainer`]([devcontainer](https://code.visualstudio.com/docs/devcontainers/containers)) to streamline the setup process. Simply ensure you have the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed. Then, open your `ai-hackathon` directory in VSCode, and it should prompt you to use the development container automatically.

## Helpful commands

```bash
aws bedrock list-foundation-models --region=us-west-2 --by-provider anthropic --query "modelSummaries[*].modelId"
aws bedrock list-foundation-models --region=us-west-2 --by-provider amazon --query "modelSummaries[*].modelId"
```

## Further experiments

- [Test generation using only prompt engineering](https://github.com/TravisCarden/ai-hackathon/blob/tedbow-prompt-eng)
