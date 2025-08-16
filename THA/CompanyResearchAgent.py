import requests
from GoogleMapsAPI import *
from GeminiAPI import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CompanyResearchAgent():
    """
    This agent is responsible for programmatically scraping a company's website.
    Its main tasks include identifying key pages, extracting text, and finding one physical company address.
    NOTE: The scraping logic used in this project is *extremely* basic and is only intended for demonstration purposes.
    NOTE: For production use, more complex implementations would be required, such as handling pagination, rate limiting,
    domain redirection, content filtering, as well as leveraging the use of sitemaps and structured data (e.g., JSON-LD) when available.
    """

    def __init__(self, company_name: str, company_url: str):
        """
        Initialises the agent with the company name and URL.

        Args:
            company_name (str): The name of the company to analyse.
            company_url (str): The URL of the company's website.
        """
        self.company_name = company_name
        self.base_url = company_url

        # NOTE: This User-Agent string is taken from my own browser to simulate a real user.
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'}

        # Commonly used keywords for identifying key pages. More keywords can be added depending on targeted websites - NOTE: This would at times require manual adjustments.
        self.link_keywords = {
            "background": ["about", "history", "company", "background"],
            "products": ["products", "services", "solutions", "what we do"],
            "contact": ["imprint", "contact-us", "contact", "locations", "address", "find us", "stores"]
        }
        # Initialise Google Maps API client
        self.maps_client = GoogleMapsAPI()

        # Initialise Gemini API client
        self.llm = GeminiAPI()

    def _fetch_page_content(self, url: str) -> BeautifulSoup | None:
        """Fetches and parses the HTML content of a given URL. The content is then used by other methods to extract information.

        Args:
            url (str): The homepage URL to fetch content from.

        Returns:
            BeautifulSoup | None: The parsed HTML content or None if an error occurred.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Could not fetch content from {url}. Error: {e}")
            return None

    def find_key_page_urls(self) -> dict:
        """
        Finds URLs for key pages of interest (i.e. About, Products, Contact) from the homepage.
        NOTE: This method only finds the first presumed matching link for each category.

        Returns:
            dict: A dictionary mapping page categories to one absolute URL.
        """
        logging.info(f"Searching for key page URLs on {self.base_url}...")
        homepage_soup = self._fetch_page_content(self.base_url)
        if not homepage_soup:
            return {}

        # Default to homepage URL, so if a specific page isn't found, we can use the homepage for its content
        found_links = {key: self.base_url for key in self.link_keywords}
        found_links_count = 0

        for a_tag in homepage_soup.find_all('a', href=True):
            link_text = a_tag.get_text(strip=True).lower() # E.g. contact us
            link_href = a_tag['href'] # E.g. /contact-us

            # Remove links that are not from the same domain as the homepage
            # NOTE: This might not work well when a site recently migrated to a new domain and has
            # not updated its internal links yet, even when they redirect back to the new domain.
            if urlparse(link_href).netloc not in urlparse(self.base_url).netloc:
                continue

            for category, keywords in self.link_keywords.items():
                if found_links[category] == self.base_url:
                    # If a keyword is found in the link's text or href, we consider it a match.
                    # if any(keyword in link_text or keyword in link_href for keyword in keywords):
                    # NOTE: In this case, we are only checking the href for keywords. Adjust as needed.
                    if any(keyword in link_href for keyword in keywords):
                        absolute_url = urljoin(self.base_url, link_href)
                        found_links[category] = absolute_url
                        logging.info(f"Found '{category}' page link: {absolute_url} (matched on text='{link_text}' or href='{link_href}')")
                        found_links_count += 1
                        break # Stop checking keywords for this link and move to the next <a> tag

            # Stop the search if we have all the links we need
            if found_links_count == len(self.link_keywords):
                break

        # Log any missing specific pages
        if found_links["background"] == self.base_url:
            logging.warning("No specific 'background' page found. Will use homepage for background text.")
        if found_links["products"] == self.base_url:
            logging.warning("No specific 'products' page found. Will use homepage for products text.")
        if found_links["contact"] == self.base_url:
            logging.warning("No specific 'contact' page found. Will use homepage for contact text.")

        return found_links
    
    def find_key_page_urls_many(self) -> dict:
        """
        Finds URLs for key pages of interest (i.e. About, Products, Contact) from the homepage.
        NOTE: This method finds all presumed matching links for each category.

        Returns:
            dict: A dictionary mapping page categories to multiple candidate absolute URLs.
        """
        logging.info(f"Searching for key page URLs on {self.base_url}...")
        homepage_soup = self._fetch_page_content(self.base_url)
        if not homepage_soup:
            return {}

        # Default to homepage URL, so if a specific page isn't found, we can use the homepage for its content
        found_links = {key: [self.base_url] for key in self.link_keywords}

        for a_tag in homepage_soup.find_all('a', href=True):
            link_text = a_tag.get_text(strip=True).lower() # E.g. contact us
            link_href = a_tag['href'] # E.g. /contact-us

            # Remove links that are not from the same domain as the homepage
            # NOTE: This might not work well when a site recently migrated to a new domain and has
            # not updated its internal links yet, even when they redirect back to the new domain.
            if urlparse(link_href).netloc not in urlparse(self.base_url).netloc:
                continue

            for category, keywords in self.link_keywords.items():
                # If a keyword is found in the link's text or href, we consider it a match.
                # if any(keyword in link_text or keyword in link_href for keyword in keywords):
                # NOTE: In this case, we are only checking the href for keywords. Adjust as needed.
                for keyword in keywords:
                    if keyword in link_href or keyword in link_text:
                        absolute_url = urljoin(self.base_url, link_href)
                        if absolute_url in found_links[category]:
                            continue
                        found_links[category].append(absolute_url)
                        logging.info(f"Found '{category}' page link: {absolute_url} (matched on text='{link_text}' or href='{link_href}')")

        # Log any missing specific pages
        if len(found_links["background"]) == 1:
            logging.warning("No specific 'background' page found. Will use only homepage for background text.")
        if len(found_links["products"]) == 1:
            logging.warning("No specific 'products' page found. Will use only homepage for products text.")
        if len(found_links["contact"]) == 1:
            logging.warning("No specific 'contact' page found. Will use only homepage for contact text.")

        return found_links
    

    def extract_text_from_url(self, url: str) -> str:
        """
        Extracts all visible text from a given URL.
        
        Args:
            url (str): The URL to extract text from.
            
        Returns:
            str: A string containing the extracted text from the page.
        """
        logging.info(f"Extracting main content text from {url}...")
        page_soup = self._fetch_page_content(url)
        if not page_soup:
            return ""

        # NOTE: Depending on the website structure, it might be necessary to filter the content more aggressively. I decided not
        # to use these filters for this implementation as some websites are not built with good semantic HTML in mind.
        # # Find the primary content tag. This works well if the website follows common web design patterns.
        # main_content_tags = page_soup.find('main') or \
        #                     page_soup.find('body') or \
        #                     page_soup.find('article') or \
        #                     page_soup.find('div', class_=re.compile(r'main|content'))
        
        # # If we found a main tag, we use that and ignore the rest of the page
        # if main_content_tags:
        #     logging.info("Found a primary content tag (<main>, <article>, etc.). Extracting text from it.")
        #     target_soup = main_content_tags
        # # Otherwise, use the full page content after removing noisy tags
        # else:
        #     logging.warning("No primary content tag found. Falling back to removing noisy tags.")
        # tags_to_remove = ['nav', 'aside', 'script', 'style', 'form']
        # for tag in page_soup(tags_to_remove):
        #     tag.decompose()
        target_soup = page_soup

        return target_soup.get_text(separator=' ', strip=True)

    # NOTE: This is the programmatic extraction method
    def extract_specific_address_block(self, text: str) -> str | None:
        """
        Extracts the first full address block that matches the regex pattern.
        NOTE: Requires no costly LLM calls. Drawback: Limited to regex pattern matching, aka lacking robustness.

        Args:
            text (str): The text to search within (e.g., content from a contact page).

        Returns:
            str | None: The full matched block of address text, or None.
        """

        # Note: This is a heuristic pattern for a US address.
        pattern = r"\b(\d{1,5}\s(?:[A-Za-z0-9\s.,#-]+?)\b[A-Z]{2}\b\s\d{5}(?:-\d{4})?)\b"
        
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            # Extract the first full address block
            found_block = match.group(1).strip().replace("�", "")
            # Clean up extra whitespace within the block
            found_block = " ".join(found_block.split())
            logging.info(f"Successfully extracted specific block: {found_block}")
            return found_block
        
        logging.warning("Could not find an address block matching the specific pattern.")
        return None

    # NOTE: This method uses a language model for extraction
    def extract_specific_address_block_llm(self, address_text: str) -> str:
        """
        Uses a language model to extract the address block from the given text.
        NOTE: Extreme robustness from not having to rely on regex patterns. Drawback: Might lead to high inference costs when scaling up and hallucinations.

        Args:
            address_text (str): The text containing the address information.

        Returns:
            str: The extracted address block, or an empty string if no address is found.
        """

        logging.info("Sending address text to LLM for extraction...")

        prompt = f"""
        You are given text scraped from a company's contact page. This text contains a lot of noise and/or scraping artifacts.
        Your task is to analyse the text and extract the full address of the company's location. If there are multiple addresses
        found in the text, return the first one or the one that is most relevant. Note that the full address might have varying
        formats depending on the country. Strictly return the full address without any additional commentary or text. Do not make
        up addresses; if none are found on the page, simply return an empty string.

        --- TEXT ---
        {address_text}

        """
        
        try:
            response = self.llm.generate_content(prompt)
            logging.info("Successfully received address extraction from LLM.")
            return str(response.text).strip().replace("�", "")
        except Exception as e:
            logging.error(f"LLM address extraction failed: {e}")

            if "500 INTERNAL" in str(e):
                raise RuntimeError("IMPORTANT: 500 INTERNAL ERROR IS A SERVER-SIDED ERROR. CHANGING TO ANOTHER MODEL COULD HELP.")

            return "Error: Could not extract address."

    def run_full_research(self) -> dict:
        """
        Performs full fetching and extraction of company information.

        Returns:
            dict: A dictionary containing the extracted company information.
        """
        logging.info(f"\n----- Starting Full Research for {self.company_name} -----")
        
        # --------------------- SINGLE PAGE APPROACH -----------------------------
        # # Find the page URLs of interest
        # key_urls = self.find_key_page_urls()

            
        # # Extract text from each page
        # background_text = self.extract_text_from_url(key_urls["background"])
        # products_text = self.extract_text_from_url(key_urls["products"])
        # contact_text = self.extract_text_from_url(key_urls["contact"])
        # ------------------------------------------------------------------------

        # ------------------- MULTI PAGE APPROACH --------------------------------
        key_urls = self.find_key_page_urls_many()

        background_text = ""
        products_text = ""
        contact_text = ""

        for url in key_urls["background"]:
            background_text += "\n" + self.extract_text_from_url(url)
        for url in key_urls["products"]:
            products_text += "\n" + self.extract_text_from_url(url)
        for url in key_urls["contact"]:
            contact_text += "\n" + self.extract_text_from_url(url)
        # ------------------------------------------------------------------------

        # --------------- Find a company location address ------------------------
        # NOTE: Change the extraction method depending on scaling needs
        # address = self.extract_specific_address_block(contact_text)
        address = self.extract_specific_address_block_llm(contact_text)
        # ------------------------------------------------------------------------

        # Extract discrete location information from the address
        location_info = self.maps_client.extract_location_info_from_address(address)

        scraped_data = {
            "background_text": background_text,
            "products_text": products_text,
            "raw_address": address,
            "location_info": location_info
        }
        
        logging.info("----- Company Research Complete -----")
        return scraped_data