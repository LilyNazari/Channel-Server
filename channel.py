#__________________________________________IMPORTS
from flask import Flask, request, jsonify
import json
import requests
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from textblob import TextBlob
from better_profanity import profanity
from flask_cors import CORS

#__________________________________________Create and configure Flask app
profanity.load_censor_words() # Loading profanity filter
class ConfigClass(object): # Class-based application configuration
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!' # change to something random, no matter what
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  
app.app_context().push() # create an app context before initializing db

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
})

#__________________________________________Channel and Hub Configuration
HUB_URL = 'http://localhost:5555'
HUB_AUTHKEY = '1234567890'
CHANNEL_AUTHKEY = '1234567890'
CHANNEL_NAME = "Art History Chat"
CHANNEL_ENDPOINT = "http://localhost:5001"
CHANNEL_FILE = 'messages.json'
CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'  
headers = {"Authorization": "authkey 1234567890"}
#__________________________________________Register Channel with Hub
@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT
    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', 
                             headers=headers,
                             data=json.dumps({
                                "name": CHANNEL_NAME,
                                "endpoint": CHANNEL_ENDPOINT,
                                "authkey": CHANNEL_AUTHKEY,
                                "type_of_service": CHANNEL_TYPE_OF_SERVICE,
                             }))
    
    if response.status_code != 200:
        print("Error creating channel: "+str(response.status_code))
        print(response.text)
        return
    
    channel_info = {
        "name": CHANNEL_NAME,
        "endpoint": CHANNEL_ENDPOINT,
        "authkey": CHANNEL_AUTHKEY,
        "type_of_service": CHANNEL_TYPE_OF_SERVICE
    }
    with open("channel_info.json", "w") as f:
        json.dump(channel_info, f, indent=4)
        
    print(f"Channel {CHANNEL_NAME} registered successfully.")

#_________________________________________Request Authorization Check
def check_authorization(request):
    #global CHANNEL_AUTHKEY
    #print("Authorization Header:", request.headers.get('Authorization'))  # Log the header for debugging
    #if 'Authorization' not in request.headers:
        #return False
    #if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        #return False
    return True

#_________________________________________Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    if not check_authorization(request):
        return "Invalid authorization1", 400
    return jsonify({'name': CHANNEL_NAME}),  200

#_________________________________________Get Messages: Returns A list of messages
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization2", 400
    return jsonify(read_messages())

#_________________________________________Off-Topic Detection using Naive Bayes
# Sample training data for off-topic detection
relevant_sentences = [
    "Let's talk about Renaissance art.",
    "Who is your favorite Impressionist painter?",
    "I love Vincent van Gogh's Starry Night!",
    "Can we discuss the Baroque period?",
    "What do you think about Picasso's influence on modern art?",
    "[nop]_word_[/nop]",
    "[nop]*word*[/nop]",
    "Yes",
    "No",
    "What techniques did Leonardo da Vinci use in his paintings?",
    "Tell me about the influence of Romanticism on landscape art.",
    "How did the Dada movement challenge traditional art?",
    "Which artists were prominent during the Rococo period?",
    "What role did fresco painting play in the Italian Renaissance?",
    "Can you explain Cubism and its key characteristics?",
    "How did Surrealism change the way we perceive reality in art?",
    "What makes Michelangelo's sculptures so significant?",
    "Who were the major contributors to Abstract Expressionism?",
    "Tell me about Frida Kahlo’s self-portraits and their meaning.",
    "What is the significance of ukiyo-e in Japanese art history?",
    "How did the invention of photography impact painting?",
    "What is the connection between Bauhaus and modern design?",
    "Can you explain the symbolism in Hieronymus Bosch’s work?",
    "How did the Harlem Renaissance influence African American art?",
    "Tell me about the differences between Gothic and Romanesque art.",
    "What are the characteristics of Fauvism?",
    "Who were the key figures in the Pre-Raphaelite Brotherhood?",
    "What is the historical importance of the Sistine Chapel ceiling?",
    "How did Neoclassicism respond to the Rococo style?"
]

irrelevant_sentences = [
    "I love watching football on weekends.",
    "What's your favorite movie?",
    "Let's talk about cooking recipes.",
    "I need help with my math homework.",
    "Who is the best pop singer today?",
    "I need recommendations for a good sci-fi novel.",
    "Let's plan a vacation to the beach.",
    "What’s the latest update on the stock market?",
    "Do you prefer cats or dogs as pets?",
    "Can you help me fix my computer?",
    "I love playing video games in my free time.",
    "Which city has the best street food?",
    "Tell me about the latest fashion trends.",
    "What’s your go-to workout routine?",
    "Who won the last Formula 1 race?",
    "I’m learning to play the guitar—any tips?",
    "What's the best way to grow tomatoes at home?",
    "What’s your favorite type of sushi?",
    "I can’t decide which phone to buy next.",
    "Let’s talk about conspiracy theories!",
    "Can you suggest a good romantic comedy?",
    "What’s the best way to train a puppy?",
    "How do I improve my chess strategy?",
    "Let’s discuss the latest smartphone features.",
    "What's your favorite type of coffee?"
]

# Labels: 1 for relevant, 0 for irrelevant
training_sentences = relevant_sentences + irrelevant_sentences
labels = [1] * len(relevant_sentences) + [0] * len(irrelevant_sentences)

# Vectorization and Model Training
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_sentences)
model = MultinomialNB()
model.fit(X, labels)

def is_off_topic(content):
    X_new = vectorizer.transform([content])
    prediction = model.predict(X_new)
    return prediction[0] == 0  # Return True if off-topic

#_________________________________________Feedback Logic: Generates feedback based on the message content
def generate_feedback(message_content):
    feedback_messages = {
    "art": [
        "Art is not what you see, but what you make others see. – Edgar Degas",
        "The purpose of art is washing the dust of daily life off our souls. – Pablo Picasso",
        "Every artist dips his brush in his own soul and paints his own nature into his pictures. – Henry Ward Beecher",
        "Art enables us to find ourselves and lose ourselves at the same time. – Thomas Merton",
        "Impressionism was once criticized for looking unfinished, but it revolutionized modern painting.",
        "Ancient cave paintings, such as those in Lascaux, France, date back over 17,000 years!",
        "Dadaism emerged as an anti-art movement during World War I, challenging traditional artistic norms.",
        "The Surrealist movement, led by artists like Salvador Dalí, explored the unconscious mind through dreamlike imagery."
    ],
    "history": [
        "Did you know? Art history is often divided into periods such as Renaissance, Baroque, and Modernism.",
        "The Renaissance marked a rebirth of art inspired by ancient Greece and Rome.",
        "During the Baroque period, artists like Caravaggio and Rembrandt used dramatic lighting techniques known as chiaroscuro.",
        "The Impressionist movement began in the 19th century, with artists like Monet and Renoir focusing on light and movement.",
        "Cubism, pioneered by Picasso and Braque, broke objects into geometric shapes to depict multiple perspectives.",
        "The Harlem Renaissance in the 1920s celebrated African American culture through art, music, and literature.",
        "Fresco painting, used in Michelangelo's Sistine Chapel, involves applying pigment onto wet plaster for durability."
    ],
    "artist": [
        "Fun fact: Leonardo da Vinci was ambidextrous and could write with both hands!",
        "Pablo Picasso went through different artistic phases, including his Blue and Rose periods.",
        "Frida Kahlo often painted self-portraits, reflecting her struggles and resilience.",
        "Michelangelo considered himself a sculptor, even though he painted the Sistine Chapel ceiling.",
        "Vincent van Gogh created over 2,000 artworks but only sold one painting in his lifetime.",
        "Claude Monet's garden in Giverny inspired many of his famous paintings, including the Water Lilies series.",
        "Georgia O'Keeffe is known for her large-scale flower paintings and depictions of the American Southwest."
    ],
    "painting": [
        "The 'Mona Lisa' was once stolen from the Louvre in 1911 and recovered two years later.",
        "Van Gogh's 'Starry Night' was painted from his asylum room's window.",
        "Jackson Pollock pioneered action painting, a technique involving dripping paint onto canvas.",
        "Edvard Munch's 'The Scream' was stolen twice, once in 1994 and again in 2004!",
        "Diego Velázquez's 'Las Meninas' is considered a masterpiece of perspective and composition.",
        "Johannes Vermeer used a camera obscura, an early optical device, to create lifelike compositions.",
        "Gustav Klimt’s 'The Kiss' is covered in real gold leaf, emphasizing its opulence and sensuality."
    ]
}
    messages = read_messages()
    blob = TextBlob(message_content)
    nouns = [word.lower() for word, tag in blob.tags if tag in ('NN', 'NNS')]
    print("Extracted Nouns:", nouns)  # Debugging Line
    if True:  # Only provide feedback after every 3 user messages
        for topic in feedback_messages:
            if topic in nouns:
                return random.choice(feedback_messages[topic])
    return None

#_________________________________________Send Message: Handles sending and receiving messages
@app.route('/', methods=['POST'])
def send_message():
    if not check_authorization(request):
        return "Invalid authorization3", 400
    
    message = request.json
    if not message or 'content' not in message or 'sender' not in message or 'timestamp' not in message:
        return "Invalid message format", 400

    if profanity.contains_profanity(message['content']):
        return "Inappropriate content", 400

    if is_off_topic(message['content']):
        return "Off-topic content", 400
    
    #extra = message['extra'] if 'extra' in message else None
    extra = message.get('extra', None)
    # Generate feedback message
    feedback = generate_feedback(message['content'])
    print("Feedback Generated:", feedback)
    messages = read_messages()
    if feedback:
        messages.append({'content': feedback,
                        'sender': "ArtBot",
                        'timestamp': message['timestamp'],
                        'extra': None,
                        })
    
    # Save user message
    messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
    save_messages(messages)
    return "OK", 200

#_________________________________________Read and Save Messages (with a 20 messages limit)
def read_messages():
    global CHANNEL_FILE
    try:
        with open(CHANNEL_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def save_messages(messages):
    MAX_MESSAGES = 10
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)

#_________________________________________Welcome Message(if no messages are present)
def add_welcome_message():
    messages = read_messages()
    if not messages:  
        welcome_message = {
            'content': "Welcome to the Art History Chat! 🎨 Let's discuss paintings, famous artists, and art movements through the history!",
            'sender': " ",
            'timestamp': "0",
            'extra': None
        }
        messages.append(welcome_message)
        save_messages(messages)
add_welcome_message()

#_________________________________________Run Application
if __name__ == '__main__':
    app.run(port=5001, debug=True) 
    
    