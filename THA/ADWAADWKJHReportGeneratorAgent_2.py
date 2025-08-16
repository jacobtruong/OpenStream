from GeminiAPI import *
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReportGeneratorAgent():
    """
    An agent responsible for generating reports based on the collected data.
    """

    def __init__(self, company_name: str, address: str, location_info: dict, background: str, products: str, satellite_analysis: dict, assumptions: str = "It is assumed that the LLM correctly identified the property and its boundaries."):
        """
        Initialise the report generator agent with the necessary information.

        Args:
            company_name (str): The name of the company.
            address (str): The address of the company.
            location_info (dict): Information about the location (city, state, country).
            background (str): Background information about the company.
            products (str): Information about the company's products and services.
            satellite_analysis (dict): Results from the satellite analysis.
            assumptions (str): Any assumptions made during the analysis.
        """

        self.company_name = company_name
        self.address = address
        self.location_info = location_info if location_info else {"city": "Unknown", "state": "Unknown", "country": "Unknown"}
        self.background = background
        self.products = products
        self.image_path = satellite_analysis.get("image_path", "")
        self.analysis_text = satellite_analysis.get("analysis_text", "")
        self.assumptions = assumptions

        if not self.company_name or not self.address:
            raise ValueError("Company name and address are required.")

        if not self.background:
            raise ValueError("Background information is required.")

        if not self.products:
            raise ValueError("Product information is required.")

        if not self.image_path or not self.analysis_text:
            raise ValueError("Satellite analysis results are required.")

        # Initialise Gemini API client
        self.llm = GeminiAPI()

        logging.info("ReportGeneratorAgent initialised successfully.")

    def generate_report(self) -> str:
        """
        Use LLM to format the given data into a Markdown-formatted report.

        Returns:
            str: The generated report text in Markdown format.
        """
        logging.info("Generating report...")

        current_datetime = datetime.now()
        
        prompt = f"""Format the given information into a structured report in markdown format. Do not make any changes to the provided content.
        Do not include explicit ```markdown``` or any other code block indicators. Ensure that the markdown report is formatted properly 
        (line breaks, indentation, headings, spacing etc.) for the following structure:
        # Title: COMPANY NAME - Nature of Operations Report
        Date: DD-MM-YYYY - Time: HH:MM:SS
        ## 1. Background:
        ## 2. Products & Services:
        * **[PRODUCT/SERVICE NAME]**: [ORIGINAL CONTENT]
        ## 3. Location Details: 
        ### a. Address: [FULL GIVEN ADDRESS] - City: [CITY NAME] - State: [STATE NAME] - Country: [COUNTRY NAME]
        ### b. Satellite image:
        [SATELLITE IMAGE]
        ### c. Findings: 
        ## 4. Assumptions:

        --- DATA ---
        Company Name: {self.company_name}
        Date: {current_datetime.strftime("%d-%m-%Y")}
        Time: {current_datetime.strftime("%H:%M:%S")}
        Address: {self.address}
        Location: (CITY: {self.location_info.get("city", "Unknown")} - STATE: {self.location_info.get("state", "Unknown")} - COUNTRY: {self.location_info.get("country", "Unknown")})
        Background: {self.background}
        Products & Services: {self.products}
        Satellite Image: ![Satellite Image]({self.image_path})
        Findings: {self.analysis_text}
        Assumptions: {self.assumptions}
        """

        try:
            response = self.llm.generate_content(prompt)
            logging.info("Report generated successfully.")
            return str(response.text).strip().replace("�", "")
        except Exception as e:
            logging.error(f"LLM report generation failed: {e}")

            if "500 INTERNAL" in str(e):
                raise RuntimeError("IMPORTANT: 500 INTERNAL ERROR IS A SERVER-SIDED ERROR. CHANGING TO ANOTHER MODEL COULD HELP.")

            return "Error: Could not generate the report."