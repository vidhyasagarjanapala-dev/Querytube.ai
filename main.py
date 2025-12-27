from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

app = FastAPI()

# CORS setup (works for your local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "AIzaSyDuxU60mIcNHnQdYwtugdAexWzn37TahUM"
youtube = build("youtube", "v3", developerKey=API_KEY)

# Load embedding model (optional for future semantic ranking)
model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_youtube_videos(search_query, max_results):
    """
    Basic YouTube search returning video metadata.
    """
    response = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        
        thumbnail_url = ""
        if "thumbnails" in item["snippet"]:
            thumbnail_url = item["snippet"]["thumbnails"].get("medium", {}).get("url", "")

        videos.append({
            "video_id": video_id,
            "title": title,
            "description": description,
            "thumbnail": thumbnail_url,
            "video_url": f"https://www.youtube.com/watch?v={video_id}"
        })

    return videos


@app.get("/search")
def search_videos(
    query: str = Query(...),
    max_results: int = 10
):
    """
    Search YouTube and return video metadata.
    """

    # 1. Fetch videos from YouTube
    videos = fetch_youtube_videos(query, max_results)

    return {"results": videos}
