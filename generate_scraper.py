import os
import google.generativeai as genai
from bs4 import BeautifulSoup
from clean_html import get_clean_html_content

def generate_scraper(url):
    """
    Generates a web scraper using the Gemini model based on the provided HTML file.
    """
    print(f"Generating the scraper for the given URL at {url} ...")
    html_content = get_clean_html_content(url)

    soup = BeautifulSoup(html_content, 'html.parser')
    html_structure = str(soup.prettify())

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    llm = genai.GenerativeModel(model_name="gemini-1.5-pro-002")
    prompt = f"""
    Create a Python web scraping application that extracts data from a given URL or directly from provided HTML content.  The application should adhere to the following specifications:

**1. Core Functionality:**

* Use the `requests` library to fetch the HTML content of the URL.  Include appropriate headers (e.g., a `User-Agent` header) to mimic a standard web browser.
* Use `BeautifulSoup` from the `bs4` library for parsing the HTML.
* Handle various HTML structures, including:
    * Information cards/containers (div, article, section with classes or IDs)
    * Tables (rows and cells)
    * Lists (ul, ol, li)
    * Text within headers (h1-h3) and paragraphs (p)

**2. Robustness and Error Handling:**

* Implement comprehensive error handling for:
    * Missing or malformed HTML elements.  The script should not crash but handle these situations gracefully.
    * Non-200 HTTP responses (e.g., 404 errors). Provide informative error messages.
    * Invalid or unreachable URLs.
    * Unexpected changes in the website's structure.  Provide a fallback mechanism (e.g., logging the error and returning partial data) instead of crashing.

**3. Pagination Handling:**

* Detect and handle pagination automatically.
* Iterate through all pages, scraping data from each, until no further pages are available.  The pagination mechanism might involve "Next" buttons, numbered links, or other methods.  The code should be adaptable.

**4. Data Structuring and Output:**

* Automatically assign meaningful and descriptive keys to the scraped data based on the context of the content.  For example, if scraping product information, keys like "product_name," "price," and "description" should be used.
* Return the scraped data as a JSON object with an indent of 4 for readability.
* Save the resulting JSON data to a file named `scraped_data.json` in the working directory.

**5. Input and Execution:**

* The function should accept two arguments:
    * `url`: The URL to scrape (string).
    * `html_content`:  Optional HTML content as a string. If provided, the scraper should use this content instead of fetching from the URL.
* Include an execution line at the end of the script that calls the scraping function with the `url` value provided as `{url}`. If `html_content` is provided, it should be used instead of fetching from the `url`.

** if the web page is about real estate properties or units the data will be similar to the following:

    "Reference": 49118,
    "unit_type": "Apartment",
    "area": "74 ~ 81",
    "developer_name": "Ora Developers",
    "location": "ZED , El Sheikh Zayed",
    "bedrooms": "1",
    "bathrooms": "1",
    "compound_name": "ZED",
    "sale_type": "Developer Sale",
    "finishing": "Finished",
    "amenities": "Terrace,Clubhouse,Underground parking,Business Hub,Sports Clubs",
    "img_link": [
        "https://prod-images.cooingestate.com/processed/property_image/image/238685/high.webp",
        "https://prod-images.cooingestate.com/processed/property_image/image/238674/high.webp",
        "https://prod-images.cooingestate.com/processed/property_image/image/238676/high.webp",
        "https://prod-images.cooingestate.com/processed/property_image/image/238678/high.webp",
        "https://prod-images.cooingestate.com/processed/property_image/image/238681/high.webp",
        "https://prod-images.cooingestate.com/processed/property_image/image/238683/high.webp"
    ],
    "link": ""

**Example Input (replace with actual values):**
html_content = ```{html_structure}``` # optional

**Output:**

The output should be *only* the Python code implementing the web scraper as described above.  Do not include any additional explanations, comments, or example usage within the code itself. Only the executable Python code should be provided.
    """

    try:
        scraper_code = llm.generate_content(prompt)
        return scraper_code.text
    except Exception as e:
        return f"An error occurred during Gemini API call: {e}"

# Example usage
if __name__ == "__main__":

    generated_scraper = generate_scraper("https://www.nawy.com/new-launches").strip().replace("python", "").replace("```","")

    with open("generated_scraper.py", "w") as f:
        f.write(generated_scraper)
    print("The scraper generated successfully.")
    
    os.system("python generated_scraper.py")
