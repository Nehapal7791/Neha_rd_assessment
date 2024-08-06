# Tines Web Scraping Project

This project scrapes data from the Tines website, specifically extracting information about tools and their associated stories. The project generates three CSV files:

1. `All_tool_names_with_stories.csv` - Contains the list of tools and the number of stories under each tool.
2. `tool_details.csv` - Contains detailed stories for each tool.
3. `all_stories.csv` - Contains all stories listed on the "all stories" page.

### Platform

- Windows

### Software

- Python 3.7+
- Google Chrome browser

### Python Packages

- selenium
- webdriver_manager

## Setup

### Step 1: Clone the Repository

Clone this repository to your local machine using:

```sh
git clone https://github.com/Nehapal7791/Neha_rd_assessment.git
cd <Neha_RD_Assignment>
```

### Step 2: Install Python Packages

# Install the required Python packages using pip:

```sh
pip install selenium webdriver_manager
```

### Step 3: Run the Script

# Execute the main script to start the web scraping process:

```sh
python task.py
```

# Tines Web Scraping Project

## File Structure

- `main.py`: The main script that performs the web scraping and saves data to CSV files.

## Code Overview

The script includes the following main functions:

- `init_driver()`: Initializes and returns a Selenium WebDriver.
- `fetch_tools_data(url)`: Fetches tools and their story counts from the tools page.
- `fetch_tool_details(url, tool_name)`: Fetches detailed stories from a tool's individual page.
- `fetch_all_stories(url)`: Fetches all stories from the given URL.
- `save_to_csv(data, output_file, headers)`: Saves the fetched data to a CSV file.
- `scrape_and_save(url)`: Coordinates fetching and saving data for all tasks.

## Logging

The script uses logging to provide detailed output about the scraping process. Adjust the logging level as needed.

## Troubleshooting

If you encounter any issues:

- Ensure that you have installed all the required Python packages.

### References

- https://python-adv-web-apps.readthedocs.io/en/latest/scraping3.html#timing-matters (official documentation of webscrapping selenium)
- official documentation of logging libraries
- youtube videos for intial set
- open ai for debugging
