# YouTube Channel Scraper 📺📊
This Python project scrapes video details from a specified YouTube channel using Selenium WebDriver. It extracts data such as video title, duration, views, upload date, likes, tags, and comments, then saves it into an Excel file for further analysis.
## Features

- **Channel Scrolling and Video Loading:**

  - The scraper automatically scrolls down on a YouTube channel’s video page to load and capture information from all listed videos.
  - This feature simulates user scroll actions to bypass lazy-loading, ensuring that all available videos on a channel are scraped.
    
- **Video Information Extraction:**

  - Title: Fetches the title of each video.
  - URL: Collects the direct link to each video for easy access.
  - Duration: Extracts video duration and formats it as HH:MM:SS based on YouTube’s duration display format.
  - Upload Date: Captures the relative time of video upload (e.g., "1 week ago") and processes it into a more standardized date format.
  - Comments: Counts the total comments on each video.
  
- **Additional Video Details Extraction:**

  - The scraper opens each video page to capture:
    - Views: The total number of views, which are displayed in a format that’s parsed and formatted for clarity.
    - Likes: Retrieves the like count, and supports parsing large values with suffixes like 'K' (thousands) and 'M' (millions).
    - Tags: Collects any tags associated with the video if available.
    - Comments Count: Gathers the total comments for further analysis.
  
- **Data Organization and Error Handling:**

  - If a specific data point (e.g., likes, tags) fails to load due to website changes or temporary issues, the scraper records a '-' instead, helping maintain data consistency even if some elements are missing.
  - Each video's data is organized into dictionaries, and any errors encountered during scraping are gracefully handled without interrupting the scraping process.
  
-  **Data Storage and Export to Excel: 📊**
  
  - The scraped data is stored in a Pandas DataFrame and then exported as an Excel file (<channel_name>_videos.xlsx), allowing for further analysis and easy accessibility.

### Excel File ScreenShots: 
![image](https://github.com/user-attachments/assets/c1600ef8-c067-4789-93f2-473d507303e1)

![image](https://github.com/user-attachments/assets/6c67d70d-42da-4621-899f-726b6bc20f8a)
