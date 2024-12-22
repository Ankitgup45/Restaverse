from flask import Flask, redirect, url_for, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = '##'  # Replace with a strong secret key in production

# Enable CORS for the application
CORS(app)

# Configure Google OAuth
google_bp = make_google_blueprint(
   client_id='###',  # Replace with your Google Client ID
    client_secret='###',  # Replace with your Google Client Secret
    redirect_to='google_login'
)

# Register the Google blueprint with the application
app.register_blueprint(google_bp, url_prefix='/google_login')

## Dummy data for Google reviews
dummy_reviews = [
    {
        "id": 1,
        "author": "John Doe",
        "rating": 5,
        "text": "Great service and friendly staff!",
        "date": "2023-01-01",
        "responses": []
    },
    {
        "id": 2,
        "author": "Jane Smith",
        "rating": 4,
        "text": "Very good experience, will come again.",
        "date": "2023-01-02",
        "responses": []
    },
    {
        "id": 3,
        "author": "Alice Johnson",
        "rating": 3,
        "text": "Average experience, could be better.",
        "date": "2023-01-03",
        "responses": []
    },
    {
        "id": 4,
        "author": "Bob Brown",
        "rating": 5,
        "text": "Excellent service, highly recommend!",
        "date": "2023-01-04",
        "responses": []
    },
    {
        "id": 5,
        "author": "Tom Harris",
        "rating": 2,
        "text": "Not great, had to wait too long.",
        "date": "2023-01-05",
        "responses": []
    },
    {
        "id": 6,
        "author": "Emily Davis",
        "rating": 4,
        "text": "Good experience overall, but room for improvement.",
        "date": "2023-01-06",
        "responses": []
    },
    {
        "id": 7,
        "author": "Michael Lee",
        "rating": 3,
        "text": "It was okay, not as expected.",
        "date": "2023-01-07",
        "responses": []
    },
    {
        "id": 8,
        "author": "Sarah Wilson",
        "rating": 5,
        "text": "Absolutely fantastic! Will definitely return.",
        "date": "2023-01-08",
        "responses": []
    },
    {
        "id": 9,
        "author": "David Green",
        "rating": 4,
        "text": "Great food, nice ambiance, but a little pricey.",
        "date": "2023-01-09",
        "responses": []
    },
    {
        "id": 10,
        "author": "Laura King",
        "rating": 2,
        "text": "Not satisfied, had a bad experience with the staff.",
        "date": "2023-01-10",
        "responses": []
    },
    {
        "id": 11,
        "author": "Chris White",
        "rating": 4,
        "text": "Good place, but could use more variety in the menu.",
        "date": "2023-01-11",
        "responses": []
    },
    {
        "id": 12,
        "author": "Patricia Scott",
        "rating": 5,
        "text": "Amazing food and excellent service. Highly recommended!",
        "date": "2023-01-12",
        "responses": []
    },
    {
        "id": 13,
        "author": "Steven Hall",
        "rating": 3,
        "text": "Okay experience, expected more based on reviews.",
        "date": "2023-01-13",
        "responses": []
    },
    {
        "id": 14,
        "author": "Nancy Adams",
        "rating": 4,
        "text": "Good overall, would love to see more options for vegetarians.",
        "date": "2023-01-14",
        "responses": []
    },
    {
        "id": 15,
        "author": "John Miller",
        "rating": 5,
        "text": "Loved it! The ambiance was perfect, and the food was delicious.",
        "date": "2023-01-15",
        "responses": []
    },
    {
        "id": 16,
        "author": "Karen Perez",
        "rating": 3,
        "text": "The food was decent, but the wait time was long.",
        "date": "2023-01-16",
        "responses": []
    },
    {
        "id": 17,
        "author": "George Martinez",
        "rating": 4,
        "text": "Service was great, food was good, but the seating area was a bit noisy.",
        "date": "2023-01-17",
        "responses": []
    },
    {
        "id": 18,
        "author": "Rebecca Lopez",
        "rating": 5,
        "text": "One of the best dining experiences I've had. Will be back soon!",
        "date": "2023-01-18",
        "responses": []
    }
]

# Define the index route
@app.route('/')
def index():
    return "Welcome to the Google Integration Portal!"

# Define the Google login route
@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))  # Redirect to Google login
    resp = google.get('/plus/v1/people/me')  # Fetch user information from Google
    assert resp.ok, resp.text  # Ensure the request was successful
    user_info = resp.json()
    return jsonify(user_info)  # Return user info as JSON

# Define a route to get dummy reviews
@app.route('/reviews')
def get_reviews():
    return jsonify(dummy_reviews)  # Return the dummy reviews as JSON

# Define a route to respond to a review
@app.route('/reviews/<int:review_id>/respond', methods=['POST'])
def respond_to_review(review_id):
    response_data = request.json
    response_text = response_data.get('response')

    # Find the review by ID and add the response
    for review in dummy_reviews:
        if review['id'] == review_id:
            review['responses'].append(response_text)
            return jsonify({"message": "Response added successfully!"}), 200

    return jsonify({"error": "Review not found!"}), 404

# Logout route
@app.route('/logout')
def logout():
    google.logout()  # Clears the user's session
    return redirect(url_for('index'))  # Redirect to the home page after logout

# Run the application
if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application in debug mode
