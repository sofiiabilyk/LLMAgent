import subprocess

"""
This is the main file to execute the commands.
It does both generates the new conversation between the debtor and agent and 
calculates the similarity between the generated conversation and the ones conducted by humans.
Before running this file, make sure that the conversation.py and similarities.py 
are in the same directory as indicateed in this file, and environments are created.

"""

# Run conversation.py with env - conversation
subprocess.run(["c:/Projects/Domu/conversation/Scripts/python.exe", "C:\Projects\Domu\conversation.py"])

# Run similarities.py with env - conversation
subprocess.run(["c:/Projects/Domu/conversation/Scripts/python.exe", "C:\Projects\Domu\similarities.py"])
