document.getElementById('predictForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const form = this;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  data.Symptom = data.Symptom.split(',').map(s => s.trim());

  document.getElementById('loader').style.display = 'block';
  document.getElementById('result').style.display = 'none';

  fetch('http://127.0.0.1:5001/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    document.getElementById('loader').style.display = 'none';
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(result => {
    document.getElementById('result').innerHTML = `
      <h2>Prediction: ${result.prediction}</h2>
      <p><strong>Suggested Food:</strong> ${Array.isArray(result.suggested_food) ? result.suggested_food.join(', ') : result.suggested_food}</p>
      <p><strong>Suggested Yoga:</strong> ${Array.isArray(result.suggested_yoga) ? result.suggested_yoga.join(', ') : result.suggested_yoga}</p>
    `;
    document.getElementById('result').style.display = 'block';
  })
  .catch(error => {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('result').innerHTML = <p style="color:red;">An error occurred: ${error.message}</p>;
    document.getElementById('result').style.display = 'block';
  });
});
