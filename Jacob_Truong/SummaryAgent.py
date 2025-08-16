from GeminiAPI import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SummaryAgent():
    """
    An agent that uses Google APIs to analyse and process data gathered by
    the CompanyResearchAgent.
    """

    def __init__(self, company_name: str):
        """
        Initialises the agent and configures the Gemini API.

        Args:
            company_name (str): The name of the company to analyse.
        """

        self.company_name = company_name

        # Initialise Gemini API client
        self.llm = GeminiAPI()

    def summarise_background(self, text: str) -> str:
        """
        Uses the LLM to summarise the company's background, focusing on key facts.

        Args:
            text (str): The pre-cleaned background text from the company's website.

        Returns:
            str: A summary of the company's history and milestones.
        """

        logging.info("Sending background text to LLM for summarisation...")

        prompt = f"""You are a professional insurance underwriter writing a report on the company {self.company_name}.
        Given the following scraped data, write a detailed report on the company. Note that the data may be contain noises and/or scraping artifacts,
        so use your best judgment to analyse the data and extract the most relevant information. Do not make up any information.
        The output should be in 2 to 5 paragraphs, suitable to be included for a Nature of Operations report. Make sure to include
        information on its history, when it was founded, its key milestones, and its current operations. The tone should be factual and professional.
        Do not include a header, title, or any other introductory text.
        Use British English spelling and terminology throughout the analysis.

        --- TEXT ---

        {text if text else 'No background text available.'}
        --- END TEXT ---
        """
        try:
            response = self.llm.generate_content(prompt)
            logging.info("Successfully received summary from LLM.")
            return str(response.text).strip().replace("�", "")
        except Exception as e:
            logging.error(f"LLM summarisation failed: {e}")
            
            if "500 INTERNAL" in str(e):
                raise RuntimeError("IMPORTANT: 500 INTERNAL ERROR IS A SERVER-SIDED ERROR. CHANGING TO ANOTHER MODEL COULD HELP.")
            
            return "Error: Could not summarise the background text."

    def list_products_services(self, text: str) -> str:
        """
        Uses the LLM to identify and list the company's main products or services.

        Args:
            text (str): The pre-cleaned text from the company's products/services page.

        Returns:
            str: A string containing a bulleted list of the company's main products or services.
        """

        logging.info("Sending products text to LLM for extraction...")

        prompt = f"""You are a professional insurance underwriter writing a report on the company {self.company_name}.
        Given the following scraped data, identify and list the main products or services offered. Note that the data may be contain noises and/or scraping artifacts,
        so use your best judgment to analyse the data and extract the most relevant information. Ensure all core products and services are included. Do not make up any information.
        For each item, provide a single, one-line description and any relevant risk notes on the same line. Return the output as a bulleted-formatted text, with each item starting with a '-'.
        Do not include a header, title, or any other introductory text.
        Use British English spelling and terminology throughout the analysis.

        --- TEXT ---

        {text if text else 'No product text available.'}
        --- END TEXT ---
        """
    
        try:
            response = self.llm.generate_content(prompt)
            # Split the response into a list and clean it up
            products = [line.strip('* ').strip() for line in str(response.text).strip().split('\n') if line.strip()]
            logging.info(f"Successfully extracted {len(products)} products/services.")
            return "\n".join(products).replace("�", "")
        except Exception as e:
            logging.error(f"LLM product extraction failed: {e}")

            if "500 INTERNAL" in str(e):
                raise RuntimeError("IMPORTANT: 500 INTERNAL ERROR IS A SERVER-SIDED ERROR. CHANGING TO ANOTHER MODEL COULD HELP.")
        
            return "Error: Could not extract products/services."