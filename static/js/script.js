// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const predictionForm = document.getElementById('prediction-form');
    const predictButton = document.getElementById('predictButton');
    const predictionResultDiv = document.getElementById('prediction-result');
    const fileInput = document.getElementById('fileInput');
    const uploadedImageDisplay = document.getElementById('uploaded-image-display');

    // Initialize Chart.js
    const ctx = document.getElementById('probability-chart').getContext('2d');
    let probabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [...Array(10).keys()],
                datasets: [{
                label: 'Probability',
                data: Array(10).fill(0),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Probability'
                    }
                }
            }
        }
    });

    // Handle form submission
    predictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // Get input values
        const formData = new FormData(predictionForm);
        formData.append('action', 'upload');

        // Make prediction request
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.image_path){
                uploadedImageDisplay.innerHTML = `<img src="${data.image_path}" style="max-width: 100px;">`;
            }

            predictionResultDiv.innerHTML = 'Image Uploaded. Click Predict to see results.';
            predictionForm.dataset.imagePath = data.image_path;
        })
        .catch(error => {
            predictionResultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });

    predictButton.addEventListener('click', function(e) {
        e.preventDefault(); 

        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('action', 'predict');
        formData.append('file', file);
        
        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if(data.image_path){
                predictionResultDiv.innerHTML = `
                    <p>Prediction: ${data.prediction}</p>
                    <p>Uploaded Image: <img src="${data.image_path}" style="max-width: 100px;"></p>
                `;
            }
            updateProbabilityChart(data.probabilities);
        })
        .catch(error => {
            predictionResultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });

    // Function to update probability chart
    function updateProbabilityChart(probabilities) {      
        probabilityChart.data.datasets[0].data = Object.values(probabilities);
        probabilityChart.update();
    }

    document.querySelectorAll('.example-button').forEach(button => {
        button.addEventListener('click', function() {
            const exampleFile = this.dataset.example;
            const formData = new FormData();
            formData.append('action', 'example');
            formData.append('data-example', exampleFile);
    
            fetch('/predict', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.image_path){
                    predictionResultDiv.innerHTML = `
                        <p>Prediction: ${data.prediction}</p>
                        <p>Example Image: <img src="${data.image_path}" style="max-width: 100px;"></p>
                    `;
                }
                updateProbabilityChart(data.probabilities);
            })
            .catch(error => {
                predictionResultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            });
        });
    });
});