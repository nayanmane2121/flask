from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Shared options for all questions
shared_options = ["Red", "Blue", "Green"] # "Yellow", "Apple", "Banana", "Cherry", "Dog", "Cat", "Bird", "Fish"]

# Questions
questions = [
    {"id": 1, "question": "What is your favorite color?"},
    {"id": 2, "question": "What is your favorite fruit?"},
    {"id": 3, "question": "What is your favorite animal?"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['POST'])
def get_question():
    # Get the current question ID and selected options
    current_question_id = request.json.get("currentQuestionId", 0)
    selected_values = request.json.get("selectedValues", [])

    # Calculate available options
    available_options = [opt for opt in shared_options if opt not in selected_values]

    # Get the next question
    next_question = None
    for question in questions:
        if question["id"] == current_question_id + 1:
            next_question = {**question, "options": available_options}
            break

    return jsonify(next_question)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    form_data = data.get('formData', '')
    userName = data.get('userName', '')

    try:
        sender_email = 'rohit.kadam@tcognition.com'
        receiver_email = 'nayan.mane@tcognition.com'
        subject = f'Dynamic Form Submission From {userName}'

        # Create email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(form_data, 'plain'))

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, 'Roka@1902')
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        return jsonify({'message': 'Email sent successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)