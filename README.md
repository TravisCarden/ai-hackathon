# Acquia 48Create 2024 AI Hackathon Project

## Run locally

- Open the repo in VSCode DevContainer. You should notice a message when you open the repo, you can click the button "Reopen in Container". Or you could press `Cmd+Shift+P`, then type "Reopen in Container" and press Return/Enter.
- In the VSCode DevContainer/VSCode window, open a terminal.
- Run `source assume-role.sh`, then enter your MFA when asked. This assumes you have `CloudServicesDev` and `AWS-Users` AWS accounts set up for AWS CLI locally.
- Run `streamlit run app/main.py` from the same terminal.
- Open the `Network URL` displayed in your browser. (eg. http://172.17.0.2:8501)

## Helpful commands

```
$ aws bedrock list-foundation-models --region=us-west-2 --by-provider anthropic --query "modelSummaries[*].modelId"
$ aws bedrock list-foundation-models --region=us-west-2 --by-provider amazon --query "modelSummaries[*].modelId"
```

## Further experiments

- [Test generation using only prompt engineering](https://github.com/TravisCarden/ai-hackathon/blob/tedbow-prompt-eng)
