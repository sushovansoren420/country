from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify certain origins if needed)
    allow_credentials=True,
    allow_methods=["GET"],  # Allow GET requests (adjust as needed)
    allow_headers=["*"],    # Allow all headers
)

# Your existing code to fetch headings
def get_markdown_headings_only(country_name: str):
    formatted_name = country_name.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{formatted_name}"

    try:
        response = httpx.get(url, timeout=10, follow_redirects=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        output = ""
        for tag in headings:
            level = int(tag.name[1])
            text = tag.get_text(strip=True)
            if text:
                output += f"{'#' * level} {text}\n"
        return output.strip()

    except Exception as e:
        return f"Error: {e}"

@app.get("/wiki-headings")
def wiki_headings(country: str):
    return get_markdown_headings_only(country)
