from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from newspaper import Article  # ✅ Import article extraction
import openai
import os

# Load OpenAI API key for summarization
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def search_google(query):
    """Automates Google search, extracts full article summary for the first result, and returns top results with links."""
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection
    options.binary_location = "/usr/bin/google-chrome"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com")

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = soup.select("div.tF2Cxc")  # Extract search result containers

        top_results = []
        first_result_url = None  # Store first URL for article extraction

        for i, result in enumerate(search_results[:5]):  # Limit to top 5 results
            title = result.select_one("h3").text if result.select_one("h3") else "No Title"
            link = result.select_one("a")["href"] if result.select_one("a") else "No Link"
            top_results.append(f"🔹 [{title}]({link})")  # Format with Markdown-style link

            if i == 0:  # First search result for full article summary
                first_result_url = link  

        if not top_results:
            print("⚠️ Google blocked the bot. Switching to DuckDuckGo...")
            return search_duckduckgo(query)

        # ✅ Fetch Full Article Summary from First Result
        if first_result_url:
            full_text = extract_text_from_url(first_result_url)
            summary = summarize_text(full_text) if full_text else "❌ Couldn't extract article."
            return f"**🔍 Search Results for:** _{query}_\n\n{summary}\n\n" + "\n".join(top_results)

        return top_results

    except Exception as e:
        print(f"⚠️ Error with Google search: {e}. Switching to DuckDuckGo...")
        return search_duckduckgo(query)  # Switch to DuckDuckGo if Google fails

    finally:
        driver.quit()


def search_duckduckgo(query):
    """Automates DuckDuckGo search if Google blocks the bot."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://duckduckgo.com/")

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = soup.select("h2 a")

        top_results = []
        for result in search_results[:5]:
            title = result.text
            link = result["href"]
            top_results.append(f"🔹 [{title}](https://duckduckgo.com{link})")  # Fix relative links

        return top_results if top_results else ["No results found. Try a different query."]

    except Exception as e:
        print(f"⚠️ Error with DuckDuckGo search: {e}")
        return ["No results found. Try a different query."]

    finally:
        driver.quit()


def summarize_text(text):
    """Use OpenAI to summarize a long text article."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Summarize the following article in a short, clear way."},
                {"role": "user", "content": text[:4000]}  # Limit to 4000 chars to fit API constraints
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"🚨 Error summarizing article: {e}"
from newspaper import Article

def extract_text_from_url(url):
    """Extract main text content from a webpage using newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"❌ Error extracting content: {e}")
        return None
