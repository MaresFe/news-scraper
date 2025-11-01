📰 News Scraper
A Python-based web scraping tool with GUI that automatically collects news headlines, descriptions, and links from multiple news sources.
Show Image
Show Image
✨ Features

Multi-Source Scraping: Collects news from BBC News and Reuters
User-Friendly GUI: Clean interface built with Tkinter
Real-time Updates: Shows scraping progress in real-time
Excel Export: Save scraped data to Excel files (.xlsx)
Error Handling: Robust error handling and reporting
Threading: Non-blocking UI during scraping operations

🚀 Getting Started
Prerequisites

Python 3.8 or higher
Internet connection

Installation

Clone this repository:

bashgit clone https://github.com/MaresFe/news-scraper.git
cd news-scraper

Install required packages:

bashpip install -r requirements.txt
Usage

Run the application:

bashpython web_scraper.py

Click "🔍 Scrape News" to start scraping
View results in the text area
Click "💾 Export to Excel" to save data

📊 Data Collected
For each article, the scraper collects:

Title: Article headline
Description: Brief summary (when available)
Link: Full URL to the article
Source: News website name
Scraped_Date: Timestamp of when data was collected

🌐 Supported News Sources

BBC News (bbc.com/news)
Reuters (reuters.com/world)

🛠️ Technical Details
Libraries Used

requests: HTTP requests to fetch web pages
BeautifulSoup4: HTML parsing and data extraction
pandas: Data manipulation and Excel export
tkinter: GUI framework
openpyxl: Excel file creation

How It Works

Sends HTTP GET requests to news websites
Parses HTML content using BeautifulSoup
Extracts article information using CSS selectors
Stores data in structured format (dictionaries)
Displays results in GUI
Exports data to Excel using pandas

⚠️ Important Notes
Legal & Ethical Considerations

Respect robots.txt: Always check website's robots.txt file
Rate Limiting: Don't send too many requests too quickly
Terms of Service: Review each website's ToS before scraping
Personal Use: This tool is for educational/personal use only
Data Attribution: Always credit the source when using scraped data

Technical Limitations

Websites may change their HTML structure, breaking the scraper
Some websites may block scraping attempts
Requires stable internet connection
May need updates when source websites change layout

🔧 Customization
Adding New Sources
To add a new news source, create a new method in the NewsScraper class:
pythondef scrape_new_source(self):
    url = "https://example.com/news"
    response = requests.get(url, headers=self.headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Add your scraping logic here
    return articles, error
Then add it to the scrape_all() method.
🐛 Troubleshooting
Problem: "No articles found"

Check internet connection
Website might have changed structure
Try updating the CSS selectors

Problem: Installation errors

Ensure Python 3.8+ is installed
Try: pip install --upgrade pip
Install packages one by one

Problem: Excel export fails

Ensure openpyxl is installed
Check write permissions in directory

📝 Future Enhancements

 Add more news sources
 Keyword filtering
 Scheduled automatic scraping
 Database storage option
 Advanced search and filtering
 CSV export option
 Dark mode

🤝 Contributing
Contributions are welcome! Feel free to:

Add new news sources
Improve error handling
Enhance the GUI
Fix bugs
Improve documentation

📜 License
This project is licensed under the MIT License.
⚖️ Disclaimer
This tool is for educational purposes only. Users are responsible for:

Complying with websites' Terms of Service
Respecting copyright and intellectual property
Using scraped data ethically and legally
Not overloading websites with requests

Always scrape responsibly!
👤 Author
Yakamoz Demir

GitHub: @yMaresFe


⭐ If you find this project useful, please consider giving it a star!
