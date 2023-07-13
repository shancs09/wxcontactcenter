from flask import Flask, render_template, request, jsonify
import requests
import json
from llmservice import generate_summary
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the ticket text from the form
        text = request.form['text']

        # Call the API service to process the text and retrieve the ticket details
        title, description, label,entities,email = process_text(text)

        # Update ticket.json with the new entry
        update_ticket(title, description, label,entities,email)

        # Pass the submitted text back to the rendered template
        return render_template('index.html', tickets=get_tickets(), submitted_text=text)

    # Get the data from ticket.json
    tickets = get_tickets()

    return render_template('index.html', tickets=tickets)

# Function to process the text and retrieve ticket details from an API service
def process_text(text):

    # # Make a request to the API service
    description,intent,sentiment,entities,email=generate_summary(text)
    
    # Extract the ticket details
    title = intent
    description = description
    label = sentiment
    entities =entities
    email=email

    # Update ticket.json with the new entry
    update_ticket(title, description, label,entities,email)

    return title, description, label,entities,email

# Function to update ticket.json
def update_ticket(title, description, label,entities,email):
    
    # Load existing data from ticket.json
    with open('ticket.json', 'r') as file:
        data = json.load(file)

    # Generate a new ID
    new_id = len(data) + 1
    
    # Create a new entry
    new_entry = {'id': new_id, 'title': title, 'description': description, 'label': label,'entities':entities,'email':email}

    # Append the new entry to the existing data
    data.append(new_entry)

    # Write the updated data back to ticket.json
    with open('ticket.json', 'w') as file:
        json.dump(data, file)

# Function to get data from ticket.json
def get_tickets():
    with open('ticket.json', 'r') as file:
        data = json.load(file)
    return data

# New route for retrieving ticket history by email
@app.route('/gethistorybyemail', methods=['GET'])
def get_history_by_email():
    email = request.args.get('email')
    if email:
        tickets = get_tickets()
        filtered_tickets = [ticket for ticket in tickets if ticket['email'] == email]
        return jsonify(filtered_tickets)
    else:
        return "Email parameter is missing.", 400

# New route for classification for transcripts
@app.route('/processtext', methods=['POST'])
def process_text():
    # Get the text from the request
    text = request.json['text']

    # Process the text to extract information
    description, intent, sentiment, entities, email = generate_summary(text)

    # Update ticket.json with the new entry
    update_ticket(intent, description, sentiment, entities, email)

    # Create a dictionary with the extracted information
    extracted_info = {
        'title': intent,
        'description': description,
        'label': sentiment,
        'entities': entities,
        'email': email
    }

    # Return the extracted information as JSON
    return jsonify(extracted_info)

if __name__ == '__main__':
    app.run(debug=True)
