import openai
from datetime import datetime
from openai import OpenAI
from pathlib import Path
import json

model = "gpt-4o"

#examples of conversations
with open("C:\Projects\git\Domu\call_data.txt", 'r', encoding='utf-8') as file:
    conversation_examples = file.read()
#print (conversation_examples)

#rules of conversations from the side of agent
with open('C:\Projects\git\Domu\prompt.txt', 'r', encoding='utf-8') as file:
    rules = file.read()
#print (rules)

with open('C:\Projects\git\Domu\call_data_external.txt', 'r', encoding='utf-8') as file:
    conversation_examples_external = file.read()
    
with open('C:\Projects\git\Domu\call_data_internal.txt', 'r', encoding='utf-8') as file:
    conversation_examples_internal = file.read()


'''
#rules that collector should follow
with open('rules.json', 'r') as f:
    rules = json.loads(f, strict=False)
context = "\n".join([f"{key}: {value}" for key, value in rules.items()])
#print(context)
'''


#API keys
OPENAI_API_KEY = ""

client = OpenAI(api_key=OPENAI_API_KEY)
#tools for the agent to decide what to do next end the conversation or continue it
tools = [{
    "type": "function",
    "function": {
        "name": "answer",
        "description": "logically continue the given conversation",
        "parameters": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "The answer to the conversation"
                }
            },
            "required": [
                "answer"
            ],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "end_conversation",
        "description": "end the conversation",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}]


#function to generate the next phrase in the conversation between debtor and collector from the side of debtor
def external_speaks(conversation, temperature=0.4, end_soon=False, max_retries=3):
    example_input = "Imagine that you are a debtor (external) to whom the collector (internal) is calling. Create a logic short next phrase in this conversation, don't care much about politeness. At the moment the conversation go ro this point: " + conversation + "Make sure to provide only a short answer without any additional text (and without \"External:\" or \"Internal:\"). "
    if end_soon:
        example_input += "You are about to smoothly end the conversation. "
    example_input += "Make the style of speaking similar to the ones in this examples:" + conversation_examples + "where external uses this type of phrases:" + conversation_examples_external
    
    success = False
    retries = 0
    # while loop to retry to extract the message if there is an issue converting to JSON
    while not success:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": example_input}
                ],
                tools=tools,
                temperature=temperature,
                max_tokens=150
            )
            #if the message is not empty, it is a normal message
            if response.choices[0].message.content:
                message = response.choices[0].message.content
            else:
                #if the message is empty, it is a tool call
                message = response.choices[0].message.tool_calls[0].function.name 
                #if the tool call is to end the conversation, return an empty string
                if message == "end_conversation":
                    message =  ""
                else:
                    #if the tool call is not to end the conversation, extract the message from the tool call
                    message = response.choices[0].message.tool_calls[0].function.arguments # JSON string
                    message = json.loads(message) # Dictionary
                    message = message["answer"]
            success = True
        except Exception as e:
            print("Encountered error: " + str(e))
            success = False
            retries += 1
            if retries >= max_retries:
                raise Exception("Max retries reached")
    print ("\n External:" + message)
    return message

#function to generate the next phrase in the conversation between debtor and collector from the side of collector
def internal_speaks(conversation, temperature=0.35, end_soon=False, max_retries=3):
    example_input = "Imagine that you are a collector agent (internal) calling to a debtor. Create a logic next phrase in this conversation, that would be as much as possible similar to the ones in this examples: " + conversation_examples + ". At the moment the conversation go ro this point:  " + conversation + "Make sure to provide only answer without any additional text (and without \"internal:\" or \"external:\"). "
    if end_soon:
        example_input += "You are about to smoothly end the conversation. " #the condition id needed to control the length of the conversation
    #example_input += "Make the style of speaking similar to the ones in this examples:" + conversation_examples
    example_input += "Here is the rulles that you as a collector agent need to follow in the conversation:" + rules # + "And here is the information about the debtor:" + info_about_external
    example_input += "Make the style of speaking similar to the ones in this examples:" + conversation_examples + "where internal uses this type of phrases:" + conversation_examples_internal
    
    success = False
    retries = 0
    # while loop to retry to extract the message if there is an issue converting to JSON
    while not success:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": example_input}
                ],
                tools=tools,
                temperature=temperature,
                max_tokens=150
            )
            if response.choices[0].message.content:
                message = response.choices[0].message.content
            else:
                message = response.choices[0].message.tool_calls[0].function.name 
                if message == "end_conversation":
                    message =  ""
                else:
                    message = response.choices[0].message.tool_calls[0].function.arguments # JSON string
                    message = json.loads(message) # Dictionary
                    message = message["answer"]
            success = True
        except Exception as e:
            print("Encountered error: " + str(e), "\nMessage: " + message)
            success = False
            retries += 1
            if retries >= max_retries:
                raise Exception("Max retries reached")
    print ("\n Internal:" + message)
    return message

#beggin the conversation. The first message could be changed
message = "Thank you for calling. How can I help you today?"
conversation = "Internal:" + message
print (conversation)

message_i = 0 #the current message count
while True:
    end_soon = message_i > 30 #control the lenght of the conversation
    #end_soon = False
    # Step 1: Debtor speaks
    message = external_speaks(conversation, end_soon=end_soon)
    # You can uncode the next line if you want to talk to the agent directly
    #message = input("External tells: ")
    if message == "":
        break
    conversation =conversation + "\n External:" + message

    # Step 2: internal speaks
    message = internal_speaks(conversation, end_soon=end_soon)
    if message == "" or message in conversation:
        break
    conversation =conversation + "\n internal says:" + message

    #message_i += 1
    #print("Processed message " + str(message_i))

#save the conversation
date = datetime.now().strftime("%Y%m%d_%H%M%S") 
with open('C:\Projects\git\Domu\generated_conversations\debtor_agent_' + date + '.txt', 'w') as file:
    file.write(conversation)

#save the conversation as an example for the similarity check
with open('C:\Projects\git\Domu\generated_example.txt', 'w') as file:
    file.truncate(0)  
    file.write(conversation)




    



