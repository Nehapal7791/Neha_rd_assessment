import csv
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def init_driver():
    """Initialize and return a Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def fetch_tools_data(url):
    """Fetch tools and their story counts from the tools page."""
    logging.info(f"Fetching tools data from URL: {url}")
    
    driver = init_driver()
    driver.get(url)
    
    try:
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.l1aa8ob6'))
        )
        rows = driver.find_elements(By.CSS_SELECTOR, 'tr.l1aa8ob6')
        tools_data = []
        for row in rows:
            try:
                tool_name_element = row.find_element(By.TAG_NAME, 'th').find_element(By.TAG_NAME, 'a')
                tool_name = tool_name_element.text.strip()
                story_count_td = row.find_elements(By.TAG_NAME, 'td')[1]
                story_count = story_count_td.text.strip()
                
                tools_data.append([tool_name, story_count])
            except Exception as e:
                logging.debug(f"Skipping row due to error: {e}")
        
        logging.debug(f"Extracted {len(tools_data)} tools.")
        return tools_data
    except Exception as e:
        logging.error(f"Failed to fetch tools data: {e}")
        return None
    finally:
        driver.quit()

def fetch_tool_details(url, tool_name):
    """Fetch detailed stories from a tool's individual page."""
    logging.info(f"Fetching details for tool: {tool_name} from URL: {url}")
    
    driver = init_driver()
    driver.get(url)
    
    try:
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.l1aa8ob6'))
        )
        story_elements = driver.find_elements(By.CSS_SELECTOR, 'tr.l1aa8ob6')
        details = []
        for story in story_elements:
            try:
                story_name = story.find_element(By.CSS_SELECTOR, 'a').text.strip()
                works_with_cell = story.find_elements(By.CSS_SELECTOR, 'td')[1]  
                works_with_items = works_with_cell.find_elements(By.CSS_SELECTOR, 'a div.t1wlghw4 div.t69s27n div.taaq09w span')
                works_with = ", ".join([item.text.strip() for item in works_with_items]) or "N/A"
                num_actions = story.find_elements(By.CSS_SELECTOR, 'td')[2].text.strip()
                author_cell = story.find_elements(By.CSS_SELECTOR, 'td')[-1]  
                author = author_cell.text.strip()
                try:
                    author = author_cell.find_element(By.CSS_SELECTOR, 'strong').text.strip()
                except:
                    pass  
                
                details.append([tool_name, story_name, works_with, num_actions, author])
            except Exception as e:
                logging.debug(f"Skipping story due to error: {e}")
                
        logging.debug(f"Extracted {len(details)} stories.")
        return details
    except Exception as e:
        logging.error(f"Failed to fetch tool details: {e}")
        return None
    finally:
        driver.quit()

def fetch_all_stories(url):
    """Fetch all stories from the given URL."""
    logging.info(f"Fetching all stories from URL: {url}")
    
    driver = init_driver()
    driver.get(url)
    
    try:
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.l1aa8ob6'))
        )
        story_elements = driver.find_elements(By.CSS_SELECTOR, 'tr.l1aa8ob6')
        stories = []
        for story in story_elements:
            try:
                story_name = story.find_element(By.CSS_SELECTOR, 'a').text.strip()
                works_with_cell = story.find_elements(By.CSS_SELECTOR, 'td')[1]
                works_with_items = works_with_cell.find_elements(By.CSS_SELECTOR, 'a div.t1wlghw4 div.t69s27n div.taaq09w span')
                works_with = ", ".join([item.text.strip() for item in works_with_items]) or "N/A"
                num_actions = story.find_elements(By.CSS_SELECTOR, 'td')[2].text.strip()
                author_cell = story.find_elements(By.CSS_SELECTOR, 'td')[-1]
                author = author_cell.text.strip()
                try:
                    author = author_cell.find_element(By.CSS_SELECTOR, 'strong').text.strip()
                except:
                    pass
                
                stories.append([story_name, works_with, num_actions, author])
            except Exception as e:
                logging.debug(f"Skipping story due to error: {e}")
                
        logging.debug(f"Extracted {len(stories)} stories.")
        return stories
    except Exception as e:
        logging.error(f"Failed to fetch all stories: {e}")
        return None
    finally:
        driver.quit()

def save_to_csv(data, output_file, headers):
    """Save the fetched data to a CSV file."""
    if not data:
        logging.error("No data to save to CSV.")
        return

    try:
        logging.debug(f"Saving data to {output_file}: {data[:5]}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        logging.info(f"Data has been written to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write data to {output_file}: {e}")

def scrape_and_save(url):
    """Fetch and save data for tools, tool details, and all stories."""
    logging.info(f"Starting the scrape process for URL: {url}")
    
    # Fetch tools and story counts
    tools_data = fetch_tools_data(url)
    if tools_data:
        save_to_csv(tools_data, "All_tool_names_with_stories.csv", ['Tool Name', 'Number of Stories'])
        
        all_details = []
        for tool_name, _ in tools_data:
            tool_url = f"https://www.tines.com/library/tools/{tool_name.lower().replace(' ', '-')}/"
            details = fetch_tool_details(tool_url, tool_name)
            if details:
                all_details.extend(details)
        
        save_to_csv(all_details, "tool_details.csv", ['Tool Name', 'Story Name', 'Works With', 'No. of Actions', 'Author'])
    else:
        logging.error("No tool data fetched from the page.")
    
    # Fetch all stories
    all_stories_url = "https://www.tines.com/library?view=all"
    all_stories_data = fetch_all_stories(all_stories_url)
    save_to_csv(all_stories_data, "all_stories.csv", ['Story', 'Works With', 'No. of Actions', 'Author'])

if __name__ == "__main__":
    tools_url = "https://www.tines.com/library/tools/"
    scrape_and_save(tools_url)
