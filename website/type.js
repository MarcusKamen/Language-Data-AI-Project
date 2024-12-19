function getSentence() {
    // Hide the "type-sentence" element and show the "year-found" element
    document.getElementById('type-sentence').style.display = "none";
    document.getElementById('year-found').style.display = "block";
    
    // Get the text from the "type-sentence" element
    text = document.getElementById('sentence-input').value;
    console.log(text);


    // Prepare the data to be sent in the API call
    data = { text: text };

    // Send the API request using fetch
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Check if there's an error
        if (result.error) {
            document.getElementById('year-found').innerText = 'Error: ' + result.error;
        } else {
            // Update the "year-found" element with the prediction result
            document.getElementById('year-found').innerText = result.prediction;
        }
    })
    .catch(error => {
        // Display any network errors
        document.getElementById('year-found').innerText = 'Error: ' + error.message;
    });
}

document.getElementById("sentence-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevents the newline in the textarea
        getSentence();
    }
});