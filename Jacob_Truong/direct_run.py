from CompanyResearchAgent import *
from SummaryAgent import *
from SatelliteAnalysisAgent import *
from ReportGeneratorAgent import *
from dotenv import load_dotenv

# NOTE: This is a very basic implementation to showcase how the entire pipeline is utilised together
# In other words, this is not production-ready code and should be adapted for real-world use cases.


def main():
    # Load env variables.
    load_dotenv()

    # Step 0: Input
    # COMPANY_NAME = "OpenStream AI"
    # COMPANY_URL = "https://www.openstream.ai/"

    # COMPANY_NAME = "Texwin"
    # COMPANY_URL = "https://www.texwin.com/"

    # COMPANY_NAME = "AeroBotics Global"
    # COMPANY_URL = "https://aeroboticsglobal.com/"

    # COMPANY_NAME = "NFQ"
    # COMPANY_URL = "https://www.nfq.com/"

    COMPANY_NAME = "GRADION"
    COMPANY_URL = "https://www.gradion.com/"

    print(f"Starting research for: {COMPANY_NAME}")
    print(f"Company URL: {COMPANY_URL}")

    # Step 1: Company Research
    company_research_agent = CompanyResearchAgent(COMPANY_NAME, COMPANY_URL)
    research_info = company_research_agent.run_full_research()

    raw_background = research_info.get("background_text", "No background text available")
    raw_products = research_info.get("products_text", "No products text available")
    address = research_info.get("raw_address", "No address found")
    location_info = research_info.get("location_info", {})

    # Step 2: Background Summarisation and Product Listing
    summary_agent = SummaryAgent(COMPANY_NAME)

    background_summary = summary_agent.summarise_background(raw_background)
    products_summary = summary_agent.list_products_services(raw_products)

    # Step 3: Satellite Image Analysis
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