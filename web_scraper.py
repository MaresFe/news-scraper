"""
News Scraper - Web Scraping Tool
Scrapes news headlines, links, and dates from websites
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import threading
import re


class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_bbc_news(self):
        """Scrape news from BBC News"""
        try:
            url = "https://www.bbc.com/news"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find article containers
            news_items = soup.find_all('div', {'data-testid': 'card-text-wrapper'}, limit=20)
            
            for item in news_items:
                try:
                    # Extract title
                    title_tag = item.find('h2')
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    
                    # Extract link
                    link_tag = item.find_parent('a')
                    if link_tag and link_tag.get('href'):
                        link = link_tag['href']
                        if not link.startswith('http'):
                            link = 'https://www.bbc.com' + link
                    else:
                        link = 'N/A'
                    
                    # Extract description
                    desc_tag = item.find('p')
                    description = desc_tag.get_text(strip=True) if desc_tag else 'N/A'
                    
                    articles.append({
                        'Title': title,
                        'Description': description[:150] + '...' if len(description) > 150 else description,
                        'Link': link,
                        'Source': 'BBC News',
                        'Scraped_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except Exception as e:
                    continue
            
            return articles, None
            
        except Exception as e:
            return [], f"Error scraping BBC News: {str(e)}"
    
    def scrape_reuters(self):
        """Scrape news from Reuters"""
        try:
            url = "https://www.reuters.com/world/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find article links
            story_cards = soup.find_all('a', {'data-testid': 'Link'}, limit=20)
            
            for card in story_cards:
                try:
                    # Extract title
                    title_tag = card.find(['h3', 'h2', 'span'])
                    if not title_tag:
                        continue
                    
                    title = title_tag.get_text(strip=True)
                    if len(title) < 10:  # Skip if too short
                        continue
                    
                    # Extract link
                    link = card.get('href', 'N/A')
                    if link != 'N/A' and not link.startswith('http'):
                        link = 'https://www.reuters.com' + link
                    
                    articles.append({
                        'Title': title,
                        'Description': 'N/A',
                        'Link': link,
                        'Source': 'Reuters',
                        'Scraped_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except Exception as e:
                    continue
            
            return articles, None
            
        except Exception as e:
            return [], f"Error scraping Reuters: {str(e)}"
    
    def scrape_all(self, progress_callback=None):
        """Scrape news from all sources"""
        all_articles = []
        errors = []
        
        # Scrape BBC News
        if progress_callback:
            progress_callback("Scraping BBC News...")
        bbc_articles, bbc_error = self.scrape_bbc_news()
        if bbc_error:
            errors.append(bbc_error)
        else:
            all_articles.extend(bbc_articles)
        
       # # Scrape Reuters
 if progress_callback:
     progress_callback("Scraping Reuters...")
 reuters_articles, reuters_error = self.scrape_reuters()
            errors.append(reuters_error)
        else:
            all_articles.extend(reuters_articles)
        
        return all_articles, errors


class NewsScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("News Scraper - Web Scraping Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.scraper = NewsScraper()
        self.articles = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1e3a8a', height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📰 News Scraper",
            font=('Arial', 22, 'bold'),
            bg='#1e3a8a',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f8fafc')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Info
        info_label = tk.Label(
            main_frame,
            text="Automatically scrape latest news from BBC News and Reuters",
            font=('Arial', 10),
            bg='#f8fafc',
            fg='#64748b'
        )
        info_label.pack(pady=(0, 15))
        
        # Sources frame
        sources_frame = tk.LabelFrame(
            main_frame,
            text="News Sources",
            font=('Arial', 10, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        sources_frame.pack(fill='x', pady=(0, 15))
        
        sources_text = "✓ BBC News (bbc.com/news)\n✓ Reuters (reuters.com/world)"
        sources_label = tk.Label(
            sources_frame,
            text=sources_text,
            font=('Arial', 9),
            bg='#f8fafc',
            fg='#475569',
            justify='left'
        )
        sources_label.pack(padx=20, pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg='#f8fafc')
        btn_frame.pack(pady=10)
        
        # Scrape button
        self.scrape_btn = tk.Button(
            btn_frame,
            text="🔍 Scrape News",
            command=self.scrape_news,
            font=('Arial', 11, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        self.scrape_btn.pack(side='left', padx=5)
        
        # Export button
        self.export_btn = tk.Button(
            btn_frame,
            text="💾 Export to Excel",
            command=self.export_to_excel,
            font=('Arial', 11, 'bold'),
            bg='#16a34a',
            fg='white',
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.export_btn.pack(side='left', padx=5)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to scrape",
            font=('Arial', 9),
            bg='#f8fafc',
            fg='#64748b'
        )
        self.status_label.pack(pady=5)
        
        # Results frame
        results_frame = tk.LabelFrame(
            main_frame,
            text="Scraped Articles",
            font=('Arial', 10, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        results_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Text widget for results
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            font=('Consolas', 9),
            bg='#ffffff',
            fg='#1e293b',
            relief='flat',
            padx=10,
            pady=10
        )
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Counter label
        self.counter_label = tk.Label(
            main_frame,
            text="Total Articles: 0",
            font=('Arial', 10, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        self.counter_label.pack(pady=(10, 0))
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def scrape_news(self):
        self.scrape_btn.config(state='disabled')
        self.export_btn.config(state='disabled')
        self.results_text.delete(1.0, tk.END)
        self.articles = []
        
        def run_scraping():
            self.update_status("Scraping in progress...")
            
            articles, errors = self.scraper.scrape_all(self.update_status)
            
            self.articles = articles
            
            # Display results
            if articles:
                for idx, article in enumerate(articles, 1):
                    self.results_text.insert(tk.END, f"\n{'='*80}\n")
                    self.results_text.insert(tk.END, f"Article #{idx}\n")
                    self.results_text.insert(tk.END, f"Source: {article['Source']}\n")
                    self.results_text.insert(tk.END, f"Title: {article['Title']}\n")
                    if article['Description'] != 'N/A':
                        self.results_text.insert(tk.END, f"Description: {article['Description']}\n")
                    self.results_text.insert(tk.END, f"Link: {article['Link']}\n")
                    self.results_text.insert(tk.END, f"Scraped: {article['Scraped_Date']}\n")
                
                self.counter_label.config(text=f"Total Articles: {len(articles)}")
                self.export_btn.config(state='normal')
                self.update_status(f"✓ Successfully scraped {len(articles)} articles!")
            else:
                self.results_text.insert(tk.END, "No articles found.\n")
                self.update_status("No articles found")
            
            if errors:
                self.results_text.insert(tk.END, f"\n\n⚠️ Errors:\n")
                for error in errors:
                    self.results_text.insert(tk.END, f"- {error}\n")
            
            self.scrape_btn.config(state='normal')
        
        # Run in separate thread
        thread = threading.Thread(target=run_scraping)
        thread.daemon = True
        thread.start()
    
    def export_to_excel(self):
        if not self.articles:
            messagebox.showwarning("No Data", "No articles to export!")
            return
        
        try:
            # Create DataFrame
            df = pd.DataFrame(self.articles)
            
            # Generate filename
            filename = f"news_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Save to Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            
            messagebox.showinfo(
                "Success",
                f"Exported {len(self.articles)} articles to:\n{filename}"
            )
            self.update_status(f"✓ Exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")


def main():
    root = tk.Tk()
    app = NewsScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
