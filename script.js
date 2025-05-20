document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Show loader
    document.getElementById("loader").style.display = "block";
    document.getElementById("result").innerHTML = "";

    const payload = {
        Age: parseInt(document.getElementById("age").value),
        Height_cm: parseFloat(document.getElementById("height").value),
        Weight_kg: parseFloat(document.getElementById("weight").value),
        BMI: parseFloat(document.getElementById("bmi").value),
        Gender: document.getElementById("gender").value,
        "Blood Type": document.getElementById("blood").value,
        Smoking: document.getElementById("smoking").value,
        "Alcohol Status": document.getElementById("alcohol").value,
        Symptom: document.getElementById("symptoms").value
            .split(",")
            .map((s) => s.trim())
    };

    try {
        const response = await fetch("http://127.0.0.1:5001/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById("result").innerHTML = `
                <p><strong>Prediction:</strong> ${result.prediction}</p>
                <p><strong>Suggested Food:</strong> ${result.suggested_food.join(", ")}</p>
                <p><strong>Suggested Yoga:</strong> ${result.suggested_yoga.join(", ")}</p>
            `;
        } else {
            document.getElementById("result").innerHTML = <span style="color: red;">Error: ${result.error || "Something went wrong"}</span>;
        }
    } catch (error) {
        document.getElementById("result").innerHTML = <span style="color: red;">An error occurred: Failed to fetch</span>;
    } finally {
        // Hide loader
        document.getElementById("loader").style.display = "none";
    }
});
