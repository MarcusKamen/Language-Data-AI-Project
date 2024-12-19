let year_predicted = -1;
let year_written = -1;
let title = "";
let author = "";


function getAISentence(){
    document.getElementById('sentence-section').style.display = "block";
    document.getElementById('get-sentence').style.display = "none";
    document.getElementById('user-sentence-input').style.display = "block";
    
    

    // Send the API request using fetch
    fetch('http://127.0.0.1:5000/random_sentence', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        // Check if there's an error
        if (result.error) {
            document.getElementById('sentence').innerText = 'Error: ' + result.error;
        } else {
            // Update the "year-found" element with the prediction result
            document.getElementById('sentence').innerText = result.random_sentence

            year_predicted = result.prediction;
            year_written = result.actual;
            title = result.title;
            author = result.author;
        }
    })
    .catch(error => {
        // Display any network errors
        document.getElementById('sentence').innerText = 'Error: ' + error.message;
    });
    
}
function yearEntered(){
    document.getElementById('guess-response').style.display = "block";
    document.getElementById('user-sentence-input').style.display = "none";
    document.getElementById('user-guess-container').style.display = "block";
    document.getElementById('user-guess').innerText = "User Guess: " + document.getElementById('sentence-input').value;
    document.getElementById('computer-guess-output').innerText = year_predicted;
    document.getElementById('year-output').innerText = year_written;
    document.getElementById('title-and-author').innerText = title + " by " + author;
}

document.getElementById("sentence-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevents the newline in the textarea
        yearEntered();
    }
});