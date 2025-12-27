const API_URL = "http://127.0.0.1:8000/search"; // FastAPI endpoint

async function searchVideos() {
    const queryInput = document.getElementById("query");
    const resultsDiv = document.getElementById("results");

    const query = queryInput.value.trim();

    if (!query) {
        alert("Please enter a search query");
        return;
    }

    // Clear old results
    resultsDiv.innerHTML = `
        <p style="text-align:center; color:#ccc;">Searching YouTube for "${query}"...</p>
    `;

    try {
        const response = await fetch(`${API_URL}?query=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error("Failed to fetch results");
        }

        const data = await response.json();

        if (!data.results || data.results.length === 0) {
            resultsDiv.innerHTML = `
                <p style="text-align:center; color:#ffaaaa;">
                    No results found
                </p>
            `;
            return;
        }

        displayResults(data.results);

    } catch (error) {
        console.error(error);
        resultsDiv.innerHTML = `
            <p style="text-align:center; color:red;">
                Error connecting to backend
            </p>
        `;
    }
}

function displayResults(videos) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    videos.forEach(video => {
        const card = document.createElement("div");
        card.className = "video-card";

        card.innerHTML = `
            <img src="${video.thumbnail}" alt="thumbnail">
            <div class="video-info">
                <h3>${video.title}</h3>
                <p>${video.description || "No description available"}</p>
                <a href="https://www.youtube.com/watch?v=${video.video_id}" target="_blank">
                    Watch on YouTube
                </a>
            </div>
        `;

        resultsDiv.appendChild(card);
    });
}
