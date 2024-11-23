import requests
import re

# Function to fetch webpage content with a referer header
def fetch_webpage_content(url, referer):
    headers = {"Referer": referer}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None

# Function to extract token from the video URL
def extract_token(url):
    match = re.search(r'token=([\w-]+)', url)
    return match.group(1) if match else None

# Main function
def generate_playlist():
    base_url = "https://hotflixbd.com/token.php?stream=T-Sports"
    referer = "https://hotflixbd.com/"
    
    # Fetch page content
    page_content = fetch_webpage_content(base_url, referer)
    if not page_content:
        print("Failed to fetch page content.")
        return

    # Extract video URL from the page content
    match = re.search(r'(https?://[^\s]+\.m3u8[^\s]*)', page_content)
    video_url = match.group(1) if match else None

    # Extract token from the video URL
    token = extract_token(video_url) if video_url else None
    if not token:
        print("Failed to extract token.")
        return

    # Create M3U playlist structure
    m3u_playlist = "#EXTM3U\n"
    m3u_playlist += "#EXTINF:-1 tvg-logo=\"https://i.postimg.cc/mDyqDJKG/landscape-original-poster-021730001725875728.png\" group-title=\"MOVIES\", TOFFEE MOVIES\n"
    m3u_playlist += f"https://musajeeb.com/Gazi/video.m3u8?token={token}\n"
    m3u_playlist += "#EXTINF:-1 tvg-logo=\"https://i.postimg.cc/66d2FDMW/image.jpg\" group-title=\"Live Sports\", T-Sports\n"
    m3u_playlist += f"https://musajeeb.com/T-Sports/video.m3u8?token={token}\n"

    # Save the playlist to a file
    with open("playlist.m3u", "w") as file:
        file.write(m3u_playlist)

    print("Playlist updated successfully.")

if __name__ == "__main__":
    generate_playlist()
