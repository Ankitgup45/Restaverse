import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Reviews() {
  const [reviews, setReviews] = useState([]);
  const [responseText, setResponseText] = useState('');
  const [selectedReviewId, setSelectedReviewId] = useState(null);

  useEffect(() => {
    // Fetch reviews from the Flask backend
    axios.get('http://localhost:5000/reviews')
      .then(response => {
        setReviews(response.data);
      })
      .catch(error => {
        console.error('Error fetching reviews:', error);
      });
  }, []);

  const handleResponseSubmit = (reviewId) => {
    axios.post(`http://localhost:5000/reviews/${reviewId}/respond`, { response: responseText })
      .then(response => {
        alert(response.data.message);
        setResponseText(''); // Clear the response text
        setSelectedReviewId(null); // Clear the selected review ID
        // Optionally, you can re-fetch reviews to update the UI
        return axios.get('http://localhost:5000/reviews');
      })
      .then(response => {
        setReviews(response.data);
      })
      .catch(error => {
        console.error('Error responding to review:', error);
      });
  };

  return (
    <div>
      <h2> GOOGLE REVIEWS </h2>
      <div>
        {reviews.map(review => (
          <div key={review.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
            <strong>{review.author}</strong> ({review.rating} stars) <br />
            {review.text} <br />
            <small>{review.date}</small>
            <div>
              <h4>Responses:</h4>
              {review.responses.length > 0 ? (
                review.responses.map((response, index) => (
                  <div key={index} style={{ marginLeft: '20px' }}>
                    <strong>Response:</strong> {response}
                  </div>
                ))
              ) : (
                <div>No responses yet.</div>
              )}
            </div>
            <button  className="button" onClick={() => setSelectedReviewId(review.id)}>Respond</button>
            {selectedReviewId === review.id && (
              <div>
                <textarea
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  placeholder="Write your response here..."
                  rows="3"
                  cols="30"
                />
                <button className="button" onClick={() => handleResponseSubmit(review.id)}>Submit Response</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reviews;
