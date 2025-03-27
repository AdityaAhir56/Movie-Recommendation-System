function getRecommendations() {
    var movieInput = document.getElementById("movieInput").value.trim();
    if (!movieInput) {
        alert("Please enter a movie title.");
        return;
    }
    // Simulate fetching recommendations (replace with your Python code)
    var recommendations = ["Movie 1", "Movie 2", "Movie 3"];
    var recommendationsList = document.getElementById("recommendations");
    recommendationsList.innerHTML = "";
    recommendations.forEach(function(recommendation) {
        var li = document.createElement("li");
        li.textContent = recommendation;
        recommendationsList.appendChild(li);
    });
}

document.getElementById("recommendBtn").addEventListener("click", getRecommendations);