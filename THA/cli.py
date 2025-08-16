import os
import sys
import argparse
from CompanyResearchAgent import *
from SummaryAgent import *
from SatelliteAnalysisAgent import *
from ReportGeneratorAgent import *
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate company research report')
    parser.add_argument('company_name', help='Name of the company to research')
    parser.add_argument('company_url', help='URL of the company website')
    parser.add_argument('-o', '--output', default='company_report.md', 
                       help='Output file name (default: company_report.md)')
    
    args = parser.parse_args()

    COMPANY_NAME = args.company_name
    COMPANY_URL = args.company_url

    print(f"Starting research for: {COMPANY_NAME}")
    print(f"Company URL: {COMPANY_URL}")

    # Step 1: Company Research
    company_research_agent = CompanyResearchAgent(COMPANY_NAME, COMPANY_URL)
    research_info = company_research_agent.run_full_research()

    raw_background = research_info.get("background_text", "No background text available")
    raw_products = research_info.get("products_text", "No products text available")
    address = research_info.get("raw_address", "No address found")
    location_info = research_info.get("location_info", {})

    # Step 2: Summarisation
    summary_agent = SummaryAgent(COMPANY_NAME)

    background_summary = summary_agent.summarise_background(raw_background)
    products_summary = summary_agent.list_products_services(raw_products)

    # Step 3: Satellite Analysis
    satellite_analysis_agent = SatelliteAnalysisAgent(COMPANY_NAME, address)
    satellite_analysis = satellite_analysis_agent.run_satellite_analysis()

    # Step 4: Report Generation
    report_generator_agent = ReportGeneratorAgent(COMPANY_NAME, address, location_info, background_summary, products_summary, satellite_analysis)
    report = report_generator_agent.generate_report()

    # Step 5: Output to Markdown file
    # NOTE: This step can be included in the ReportGeneratorAgent class, but I will keep it separate in this
    # implementation for the sake of clarity.
    with open(f"nop_{COMPANY_NAME.lower().replace(' ', '_')}.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()