# Domu

This is an AI-powered conversation simulator that generates realistic dialogues between debt collectors and debtors. The system uses GPT-4 to create natural-sounding conversations while following specific rules and guidelines.

## Prerequisites

- Python 3.x
- OpenAI API key
- Required Python packages:
  - openai
  - numpy

## Setup

1. Set up two python environments:
```
python -m venv conversation
source conversation/bin/activate
```

2. Install required packages:
```bash
pip install openai numpy
```

3. Set up your OpenAI API key:
   - Open `conversation.py` and `similarities.py`
   - Replace the empty `OPENAI_API_KEY` string with your API key


## Usage

### Generating Conversations

1. Run the conversation generator:
```bash
python conversation.py
```

This will:
- Start a simulated conversation between a collector and debtor
- Save the generated conversation in the `generated_conversations` directory
- Create a `generated_example.txt` file for similarity comparison

### Checking Similarities

To compare a generated conversation with an original example:
```bash
python similarities.py
```

This will:
- Calculate the cosine similarity between the generated and original conversations
- Output a similarity score between 0 and 1

### Alternative

Alternatively, you can run the file `command.py` which will execute both files (`conversation.py` and `similarities.py`) in sequence:
```bash
python command.py
```

## Configuration

You can modify the following parameters in `conversation.py`:
- `temperature`: Controls response randomness (default: 0.4 for external, 0.35 for internal)
- `max_retries`: Number of retry attempts for API calls (default: 3)
- Initial message: Change the starting message in the conversation
