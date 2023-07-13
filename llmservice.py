import os ,re 
import requests

# BAM Credentials
BAM_KEY = os.getenv("BAM_KEY", None)
BAM_API_ENDPOINT = os.getenv("BAM_API", None)
#Endpoint Url
ENDPOINT_URL = BAM_API_ENDPOINT + "generate"

# Authentication header
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+BAM_KEY
}

def generate_summary(input_text):
    #Set input text
    llmInput=input_text
    #
    intent=classification(llmInput)
    entities=entity_extraction(llmInput)
    #
    email = extract_email(entities)
    print(email)
    #Parameters
    parameters = {
                "decoding_method": "greedy",
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 50,
                "min_new_tokens": 50,
                "max_new_tokens": 200
                }
    #Template for Summarization
    template={
        "id": "prompt_builder",
        "data": {
            "instruction": "Write a short summary for the chat transcripts.",
            "input_prefix": "Input:",
            "output_prefix": "Output:",
             "examples": [
                            {
                            "input": "Virtual agent: Welcome! How can I assist you today?\n\nCaller: I want to apply for a credit card.\n\nVirtual agent: Fantastic! Do you have an existing account with us?\n\nCaller: Yes, I have a savings account.\n\nVirtual agent: Great! Let's get started. Could you please provide your email address?\n\nCaller: john.doe@email.com\n\nVirtual agent: Thank you. To proceed, we require your date of birth.\n\nCaller: 15-Apr-1990\n\nVirtual agent: Perfect. Let me check if you're eligible for a credit card.\n\nVirtual agent: Yes, you're eligible! What type of credit card are you interested in?\n\nCaller: I prefer a rewards credit card.\n\nVirtual agent: Excellent choice! Is there a specific credit limit you have in mind?\n\nCaller: $5,000 would be ideal.\n\nVirtual agent: Noted. Lastly, we'll need your consent to run a credit check. Shall we proceed?\n\nCaller: Yes, please go ahead.\n\nVirtual agent: Thank you for your cooperation. We'll review your application and get back to you within 2-3 business days.\n\nCaller: Thank you. That's all I needed.\n\nVirtual agent: You're welcome! If you have any further questions, feel free to ask. Have a great day!\n\n",
                            "output": "Caller wants to apply for a credit card. He has a savings account with the bank. He wants a rewards credit card with a $5,000 limit. He agrees to a credit check. The bank will review his application and get back to him within 2-3 business days."
                            },
                            {
                            "input": "Virtual agent: Hello! How can I assist you today?\n\nCaller: I need to book a flight.\n\nVirtual agent: Certainly! Could you please provide me with your departure and destination airports?\n\nCaller: I'll be departing from JFK and flying to LAX.\n\nVirtual agent: Great! When do you plan to travel?\n\nCaller: I want to leave on July 15th and return on July 20th.\n\nVirtual agent: Wonderful! Let me check the available flights for those dates.\n\nVirtual agent: I have found several options. Do you have a preferred airline?\n\nCaller: I prefer flying with Delta.\n\nVirtual agent: Understood. Here are the Delta flights available:\n\nFlight 1: Departure - 9:00 AM from JFK, Arrival - 12:00 PM at LAX\nFlight 2: Departure - 12:30 PM from JFK, Arrival - 3:30 PM at LAX\nFlight 3: Departure - 3:00 PM from JFK, Arrival - 6:00 PM at LAX\n\nCaller: I'll take the first flight, please.\n\nVirtual agent: Noted. Could you please provide your full name and contact number for the booking?\n\nCaller: My name is Sarah Thompson, and my contact number is +1 (555) 123-4567.\n\nVirtual agent: Thank you for the details. I will now proceed to book your flight. Please hold on for a moment.\n\nVirtual agent: Your flight has been successfully booked. You will receive a confirmation email shortly. Is there anything else I can assist you with?\n\nCaller: That's all. Thank you!\n\nVirtual agent: You're welcome! Have a safe and pleasant journey!\n\n",
                            "output": "Caller wants to book a flight from JFK to LAX. She wants to leave on July 15th and return on July 20th. She prefers Delta flights. She will take the first flight. The flight has been successfully booked."
                            }
                        ]
        }
        }
    llmPayload = {
                    "model_id": "google/flan-ul2", 
                    "inputs":[llmInput], 
                    "template":template,
                    "parameters": parameters
                }
    
    # print(llmPayload)
    print("Calling Summarization...")
    response = requests.post(ENDPOINT_URL, json=llmPayload, headers=headers)
    print(response.json())
    response=response.json()
    if "results" in response:
        generated_text=response['results'][0]['generated_text']
        generated_text=generated_text.replace('.','')
        print(generated_text)
        # intent=classification(llmInput)
        # entities=entity_extraction(llmInput)
        sentiment=sentiment_analysis(generated_text)
        # response_summary={"summary":generated_text,
        #                   ""}
        return generated_text,intent,sentiment,entities,email
    else:
        erro_message=response['message']
        return erro_message,"NA","NA"

def classification(input_text):
    #Set input text
    llmInput=input_text
    #
    template = {
                "id": "prompt_builder",
                "data": {
                "instruction": "The following paragraph is a conversational summary on banking support system. The Conversation is about one of these options: \nTransfer funds, Check Account Balance, Create Account,Apply for Credit Card,Fraudulent Transaction.Read the following paragraph and determine which option the conversation is about.",
                "input_prefix": "Input:",
                "output_prefix": "Output:",
                "examples": []
                }
            }
    #Parameters
    parameters = {
                "decoding_method": "greedy",
                "min_new_tokens": 1,
                "max_new_tokens": 5,
                "beam_width": 1
            }
    # #Instruction for classification
    # instruction="The following paragraph is a conversational summary on Support system. The Ticket is about one of these options: Seeking Support, Requesting Information,Reporting a Problem,Requesting Assistance with a Transaction or Expressing Satisfaction or Gratitude. Read the following paragraph and determine which option the complaint is about."
    
    #Payload
    llmPayload = {
                "model_id": "google/flan-ul2", 
                "inputs":[llmInput], 
                "template":template,
                "parameters": parameters
            }

    # print(llmPayload)
    print("Calling Indent Identification...")
    response = requests.post(ENDPOINT_URL, json=llmPayload, headers=headers)
    print(response.json())
    response=response.json()
    if "results" in response:
        generated_text=response['results'][0]['generated_text']
        generated_text=generated_text.replace('.','')
        print(generated_text)
        return generated_text
    else:
        erro_message=response['message']
        return erro_message


def sentiment_analysis(input_text):
    #Set input text
    llmInput=input_text
    #Parameters
    parameters = {
                "decoding_method": "greedy",
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 50,
                "min_new_tokens": 1,
                "max_new_tokens": 1
                }
    #Template for Summarization
    template={
        "id": "prompt_builder",
        "data": {
            "instruction": "Classify below statement as positive or negative",
            "input_prefix": "Input:",
            "output_prefix": "Output:",
            "examples": []
        }
        }
    llmPayload = {
                    "model_id": "google/flan-ul2", 
                    "inputs":[llmInput], 
                    "template":template,
                    "parameters": parameters
                }
    # print(llmPayload)
    print("Calling Sentiment Classification...")
    response = requests.post(ENDPOINT_URL, json=llmPayload, headers=headers)
    print(response.json())
    response=response.json()
    if "results" in response:
        generated_text=response['results'][0]['generated_text']
        generated_text=generated_text.replace('.','')
        print(generated_text)
        return generated_text
    else:
        erro_message=response['message']
        return erro_message


def entity_extraction(input_text):
    #Set input text
    llmInput=input_text
    #Parameters
    parameters =  {
                "decoding_method": "greedy",
                "min_new_tokens": 1,
                "max_new_tokens": 50,
                "beam_width": 1
                }
    #Template for Summarization
    template={
                "id": "prompt_builder",
                "data": {
                "instruction": "Extract PII entities from the text given",
                "input_prefix": "Input:",
                "output_prefix": "Output:",
                "examples": [
                    {
                    "input": "Virtual agent: Welcome, how can I assist you?\n\nCaller: transfer funds\n\nVirtual agent: Before we can transfer any funds, please confirm where you'd like to transfer funds from.\n\nChecking accountSavings account\nCaller: Checking account\n\nVirtual agent: Okay! How much would you like to transfer?\n\nCaller: what is my account balance\n\nVirtual agent: To check your account balance, please provide your email address\n\nCaller: test@ibm.com\n\nVirtual agent: Great. What is your data of birth?\n\nCaller: 24-Nov-1983\n\nVirtual agent: One moment while I retrieve your records.\n\nVirtual agent: Your current balance is one hundred dollars\n\nVirtual agent: Okay! How much would you like to transfer?\n\nCaller: 50$\n\nVirtual agent: Alright. When would you like to make the transfer?\n\nCaller: today\n\nVirtual agent: Thanks. Please enter your four-digit authentication or PIN code\n\nCaller: 1234\n\nVirtual agent: Great, I found you in our system! Provide the last four digits of your account to transfer to.\n\nCaller: 5678\n\nVirtual agent: Sounds good. Just to confirm - you'd like to transfer 50.00 dollars from your checking account into account ending with5678 on Jun 28, 2023.\n\nIs that correct?\n\nCaller: yes\n\nVirtual agent: Great! Let me process this for you.\n\nVirtual agent: You will receive a confirmation email in the next 2-3 minutes once the transfer is complete.\n\nIs there anything else that I can help you with?\n\nCaller: no thanks\n\nVirtual agent: Have a good day!",
                    "output": "1. email: test@ibm.com \n 2. dob: 24-Nov-1983 \n"
                    }
                ]
                }
            }
    llmPayload = {
                    "model_id": "google/flan-ul2", 
                    "inputs":[llmInput], 
                    "template":template,
                    "parameters": parameters
                }
    # print(llmPayload)
    print("Calling Entity Extraction...")
    response = requests.post(ENDPOINT_URL, json=llmPayload, headers=headers)
    print(response.json())
    response=response.json()
    if "results" in response:
        generated_text=response['results'][0]['generated_text']
        print(generated_text)
        modified_generated_text = re.sub(r'(\d\.\s)', r'\n\1', generated_text)
        return modified_generated_text
    else:
        erro_message=response['message']
        return erro_message

def extract_email(text):
    # Regular expression pattern for matching email addresses
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Search for the email pattern in the given text
    match = re.search(pattern, text)
    print(match)
    if match:
        # If a match is found, return the email address
        return match.group(0)
    else:
        # If no match is found, return None or handle it accordingly
        return None
    
if __name__ == '__main__':
    # #Input text
    # input_text="00:00   [ali]   The goal today is to agree on a design solution.\\\\n00:12   [alex]  I think we should consider choice 1.\\\\n00:25   [ali]   I agree\\\\n00:40   [erin]  Choice 2 has the advantage that it will take less time.\\\\n01:03   [alex]  Actually, that\\'s a good point.\\\\n01:30   [ali]   So, what should we do?\\\\n01:55   [alex]  I\\'m good with choice 2.\\\\n02:20   [erin]  Me too.\\\\n02:45   [ali]   Done!"
    # input_text="Virtual agent: Hello! How may I assist you today?\n\nCaller: I want to make a hotel reservation.\n\nVirtual agent: Absolutely! Could you please provide me with the city and dates of your stay?\n\nCaller: I'll be visiting Chicago from August 5th to August 10th.\n\nVirtual agent: Perfect! How many guests will be staying?\n\nCaller: It's just me, so one guest.\n\nVirtual agent: Great! Let me find the available hotels for your dates.\n\nVirtual agent: Here are a few options: Hotel A, Hotel B, and Hotel C. Which one would you like to book?\n\nCaller: Hotel B sounds good.\n\nVirtual agent: Excellent choice! To proceed with the reservation, I'll need your full name and contact information.\n\nCaller: My name is Emily Johnson, and you can reach me at +1 (555) 987-6543.\n\nVirtual agent: Thank you for the details. I will now process your reservation. Please hold on for a moment.\n\nVirtual agent: Your reservation at Hotel B from August 5th to August 10th has been confirmed. You will receive a confirmation email shortly.\n\nCaller: Thank you so much!\n\nVirtual agent: You're welcome! If there's anything else I can assist you with, feel free to ask. Have a wonderful stay in Chicago!\n\n"
    # input_text="Virtual agent: Hello! How may I assist you today?\n\nCaller: I want to make a hotel reservation.\n\nVirtual agent: Absolutely! Could you please provide me with the city and dates of your stay?\n\nCaller: I'll be visiting Chicago from August 5th to August 10th.\n\nVirtual agent: Perfect! How many guests will be staying?\n\nCaller: It's just me, so one guest.\n\nVirtual agent: Great! Let me find the available hotels for your dates.\n\nVirtual agent: Here are a few options: Hotel A, Hotel B, and Hotel C. Which one would you like to book?\n\nCaller: Hotel B sounds good.\n\nVirtual agent: Excellent choice! To proceed with the reservation, I'll need your full name and contact information.\n\nCaller: My name is Emily Johnson, and you can reach me at +1 (555) 987-6543.\n\nVirtual agent: Thank you for the details. I will now process your reservation. Please hold on for a moment.\n\nVirtual agent: Your reservation at Hotel B from August 5th to August 10th has been confirmed. You will receive a confirmation email shortly.\n\nCaller: Thank you so much!\n\nVirtual agent: You're welcome! If there's anything else I can assist you with, feel free to ask. Have a wonderful stay in Chicago!\n\n"
    input_text="Virtual agent: Welcome! How can I assist you today?\nCaller: I would like to check my account balance.\nVirtual agent: Sure! To retrieve your account balance, I'll need some information. Please provide me with your email address.\nCaller: sarah.smith@email.com\nVirtual agent: Thank you. In order to verify your identity, could you also provide your date of birth?\nCaller: 10-Mar-1980\nVirtual agent: Great. Give me a moment to retrieve your account details.\nVirtual agent: Your current account balance is $2,500.32. Is there anything else I can assist you with?\nCaller: No, thank you. That's all I needed to know.\nVirtual agent: You're welcome! If you have any further questions, feel free to reach out. Have a wonderful day!"
    # summary=generate_summary(input_text)
    # print(summary)
    summary,intent,sentiment,entity_extraction=generate_summary(input_text)
    print(summary,intent,sentiment,entity_extraction)
    
    # #Classification text
    # classify_intent=classification("sam is having trouble accessing his account. erin will investigate and get back to him with a solution. sam's username is \"user123\"")
    # print(classify_intent)

    # #Sentiment text
    # sentiment=sentiment("sam is having trouble accessing his account. erin will investigate and get back to him with a solution. sam's username is \"user123\"")
    # print(sentiment)

    # input_text="Virtual agent: Welcome! How can I assist you today?\nCaller: I would like to check my account balance.\nVirtual agent: Sure! To retrieve your account balance, I'll need some information. Please provide me with your email address.\nCaller: sarah.smith@email.com\nVirtual agent: Thank you. In order to verify your identity, could you also provide your date of birth?\nCaller: 10-Mar-1980\nVirtual agent: Great. Give me a moment to retrieve your account details.\nVirtual agent: Your current account balance is $2,500.32. Is there anything else I can assist you with?\nCaller: No, thank you. That's all I needed to know.\nVirtual agent: You're welcome! If you have any further questions, feel free to reach out. Have a wonderful day!"
    # entities=entity_extraction(input_text)
    # print(entities)

