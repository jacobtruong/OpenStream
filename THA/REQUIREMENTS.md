# Nature of Operations (NOP) Report – Take-Home Assignment

## Situation
You want to automate the task of insurance underwriters.

## What are NOP Reports and underwriters?
A **Nature of Operations (NOP) Report** describes what a company does, where it operates, and any factors that might affect its risk profile.
In insurance, underwriters are the people who use this report to decide whether to insure a company and what terms to offer.
For this exercise, you will create an NOP report using:
- An **LLM** (Large Language Model) for text summarization.
- **Satellite imagery** for basic visual checks.
- Any other necessary libraries or APIs for this task.

## Purpose of the Assignment
You will:
1. Research a real company.
2. Summarize key operational details.
3. Use satellite imagery to inspect the company's physical sites.
4. Present your findings in a **Markdown report**.

**Overall, your system takes two pieces of information (company name and website URL) and generates a markdown report about the company.**

The goal is not to become an insurance expert, but to show your ability to:
- Collect, process, and summarize public data.
- Work with an API.
- Present structured, clear findings.
- Use Object-Oriented Programming (OOP) principles.

## Time Tracking & Submission
Please note that completion time is recorded and will be considered in evaluation.
If you can complete the assessment early, please submit it early.

Your submission must include:
1. **Code** used for data collection and processing (with your API key removed).
2. **Final Markdown report** following the structure below.

## Prerequisites (Setup)
- You will need a **Google Cloud API key**.
  You can create one for free. This task should stay within the free tier.
  You will use it for:
  - **LLM API calls** (Gemini API) to summarize text.
  - **Satellite imagery retrieval** (e.g., Google Maps Static API).
  - Any other Google API you think is useful.
- **Important**: Do not share your API key in your submission.

## Input
- **Company name**
- **Company website URL**

You may use the following company or any other company:
Company name: Texwin
Company website: https://texwin.com/

## Tasks

### 1. Company Background
**Task**: Research and summarize the company's history and key milestones.

Use the LLM API to summarize:
- Year founded and any major milestones

### 2. Products / Services
**Task**: Identify and list the company's main offerings.

List:
- Main products or services (one line each)

### 3. Location & Visual Assessment
**Task**: Research and analyze one of the company's physical locations using satellite imagery.

**Steps to complete:**
1. **Locate a company office/facility** - Find the address of at least one company location
2. **Retrieve satellite imagery** - Use Google Maps Static API or similar to get a satellite view
3. **Conduct visual analysis** - Examine the satellite image and provide:
   - **Address details** (city, state, country)
   - **Flood risk assessment** - Evaluate proximity to water bodies, coastlines, or flood zones
   - **Building condition analysis** - Assess visible roof condition, structural integrity, and any signs of damage or deterioration

**Deliverable**: Include the satellite image and your analysis findings in your report.


## Technical Requirements & OOP Approach

### Code Structure
We encourage you to use **Object-Oriented Programming** to organize your code.
Here's one example:

```python
class CompanyResearchAgent:
    def research_company(self):
        pass

class SatelliteAnalysisAgent:
    def analyze_satellite_imagery(self):
        pass

class ReportGenerator:
    def generate_markdown(self):
        pass
```
Please note this code is an example, and you may come up with your own design.


## Output Format
Submit a single **Markdown (.md)** file with the following structure:

1. **Background**
   2–5 short paragraphs with key facts and citations.
2. **Products & Services**
   Bulleted list with one-line explanations and any relevant risk notes.
3. **Location Details**
   For a company's site/ office:
   - Address
   - Satellite image
   - Findings (roof condition, flood hazard, other observations)
4. **Assumptions**
   Any assumptions

## Deliverables
- **Code** (without your API key) that gathers and processes data.
- **Final Markdown Report** named in the format:
  `nop_<company_slug>.md`
  Example: `nop_texwin.md`

## Constraints
- Do not share your API key.
- Do not include confidential data.
- **Following OOP principles is a plus.**
- **Do not share this assessment file with friends or colleagues.**

## Submission
Zip file named firstname_lastname.zip containing:
  - Your code (with API keys removed)
  - Your final Markdown report

## Getting Started Tips
1. **Start with the class design** - sketch out your classes before coding.
2. **Test APIs individually** - make sure each API works before integrating.
3. **Keep it simple** - focus on clean, working code rather than complex features. We are aware everyone is busy. Please focus on the core functions mentioned above.

## Hint
1. You may use LLM calls to format the markdown file.
2. Google has APIs necessary for this task.