# ---------------------------------------------------------
# AI-Powered Business & Market Intelligence Agent
# DS Intern Hackathon May 2026
# Created by: Khushi Kumari
# ---------------------------------------------------------

# Import required libraries
import os
import requests
import pandas as pd
import streamlit as st

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS


# ---------------------------------------------------------
# Load API Key
# ---------------------------------------------------------

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


# ---------------------------------------------------------
# Function 1: Search Public Web Sources
# ---------------------------------------------------------
def search_web(query, max_results=5):
    """
    This function searches public web sources using DDGS.

    It returns:
    - title
    - URL
    - snippet

    This helps satisfy the hackathon requirement:
    public websites, blogs, public posts, news, and directories.
    """

    results = []

    try:
        search_results = DDGS().text(
            query,
            max_results=max_results
        )

        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

    except Exception as e:
        st.error(f"Search error: {e}")

    return results


# ---------------------------------------------------------
# Function 2: Extract Text From Website
# ---------------------------------------------------------
def extract_website_text(url):
    """
    This function visits a public webpage URL and extracts useful text.

    It removes HTML tags and keeps paragraph text.

    This satisfies hackathon requirement:
    transforming public unstructured information into structured insights.
    """

    try:
        # Browser-like headers to avoid simple blocking
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Request webpage
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract paragraph text
        paragraphs = soup.find_all("p")

        text = " ".join(
            para.get_text(strip=True)
            for para in paragraphs
        )

        # Limit text length so AI prompt does not become too large
        return text[:2500]

    except Exception:
        return ""


# ---------------------------------------------------------
# Function 3: Clean and Structure Sources
# ---------------------------------------------------------
def collect_public_data(company, industry, region, track):
    """
    This function creates search queries based on selected track.

    Then it collects public data from search results.

    It returns:
    - source list
    - combined extracted text
    """

    # Different queries for different hackathon tracks
    if "Competitor" in track:
        queries = [
            f"{company} competitors in {industry} {region}",
            f"top companies in {industry} {region}",
            f"{company} market positioning competitors"
        ]

    elif "Product Marketing" in track:
        queries = [
            f"{company} product marketing positioning {industry}",
            f"{industry} product messaging examples {region}",
            f"{company} alternatives product comparison"
        ]

    else:
        queries = [
            f"{company} competitors {industry} {region}",
            f"{company} product marketing positioning",
            f"{industry} market trends {region}"
        ]

    all_sources = []
    combined_text = ""

    # Search each query
    for query in queries:
        results = search_web(query, max_results=4)

        for item in results:
            url = item["url"]

            # Avoid duplicate URLs
            if url and url not in [source["url"] for source in all_sources]:

                # Extract webpage content
                extracted_text = extract_website_text(url)

                source_data = {
                    "title": item["title"],
                    "url": url,
                    "snippet": item["snippet"],
                    "extracted_text": extracted_text[:800]
                }

                all_sources.append(source_data)

                # Add extracted text to combined research text
                combined_text += f"\n\nSOURCE TITLE: {item['title']}\n"
                combined_text += f"URL: {url}\n"
                combined_text += f"SNIPPET: {item['snippet']}\n"
                combined_text += f"EXTRACTED TEXT: {extracted_text[:1200]}\n"

    return all_sources[:10], combined_text[:9000]


# ---------------------------------------------------------
# Function 4: Ask AI Model
# ---------------------------------------------------------
def ask_ai(prompt):
    """
    This function sends the final structured research prompt
    to the LLM and returns the AI-generated report.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
                You are an AI-Powered Business and Market Intelligence Agent.

                Your job:
                - Analyze public business information
                - Identify competitors
                - Analyze product marketing
                - Compare positioning
                - Extract useful insights
                - Generate structured reports

                Rules:
                - Use only provided public source content and general reasoning.
                - Do not claim private or confidential information.
                - Clearly mention assumptions.
                - Include AI usage disclosure.
                - Include limitations.
                - Keep output professional and structured.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# Function 5: Build Prompt According to Track
# ---------------------------------------------------------
def build_prompt(track, company, industry, region, goal, public_data):
    """
    This function creates the final prompt for AI.

    It changes report structure based on selected hackathon track.
    """

    base_context = f"""
    Target Company/Product: {company}
    Industry/Domain: {industry}
    Region/Market: {region}
    Business Goal: {goal}

    Public Research Data Collected:
    {public_data}
    """

    if "Competitor" in track:
        return f"""
        You are working on HACKATHON TRACK 1: Competitor Intelligence.

        {base_context}

        Create a complete Competitor Intelligence Report.

        Include these sections:

        1. Executive Summary
        2. Target Company Overview
        3. Market Segment Understanding
        4. Public Sources Used
        5. Top Competitors Identified

        6. Top Competitor Ranking (MANDATORY)

        You MUST generate a ranking table.

        Columns:
        - Rank
        - Competitor Name
        - Reason for Ranking

        Ranking should be based on:
        - Market Presence
        - Brand Recognition
        - Product/Service Strength
        - Customer Reach
        - Competitive Positioning

        Important:
        - Do NOT include the target company itself.
        - Only rank competing companies.
        - Do NOT skip this section.

        7. Competitor Comparison Table
        Columns:
        - Competitor Name
        - Main Offering
        - Target Customers
        - Strengths
        - Weaknesses
        - Positioning

        8. Competitive Positioning Analysis
        9. Market Gaps
        10. Opportunities
        11. Risks and Threats
        12. Final Recommendations
        13. AI Usage Disclosure
        14. Limitations

        Important:
        - Mention that public web data was used.
        - Do not invent exact numbers.
        - If information is uncertain, say "Based on available public sources".
        - Do NOT include the target company itself in competitor rankings.
        - Do NOT include the target product/company itself in product rankings.
        - Format output in Markdown.
        """

    elif "Product Marketing" in track:
        return f"""
        You are working on HACKATHON TRACK 2: Product Marketing Intelligence.

        {base_context}

        Create a complete Product Marketing Intelligence Report.

        Include these sections:

        1. Executive Summary
        2. Product / Offering Overview
        3. Target Customer Segment
        4. Public Sources Used
        5. Product Positioning Analysis
        6. Marketing Messaging Analysis

        7. Product Ranking

        Create a ranked list of similar products based on:
        - Market Adoption
        - Product Features
        - Brand Recognition
        - Customer Reach
        - Product Positioning

        Include:
        - Rank
        - Product / Company Name
        - Reason for Ranking

        8. Similar Products / Alternatives

        9. Product Comparison Table
        Columns:
        - Product / Company
        - Main Features
        - Target Audience
        - Messaging Style
        - Strengths
        - Weaknesses

        10. Communication Strategy
        11. Common Marketing Keywords
        12. Market Trends
        13. Opportunities to Improve Positioning
        14. Final Recommendations
        15. AI Usage Disclosure
        16. Limitations

        Important:
        - Mention that public web data was used.
        - Do not invent exact numbers.
        - If information is uncertain, say "Based on available public sources".
        - Do NOT include the target company itself in competitor rankings.
        - Do NOT include the target product/company itself in product rankings.
        - Format output in Markdown.
        """

    else:
        return f"""
        You are creating a COMPLETE AI-Powered Business & Market Intelligence Report.

        {base_context}

        Cover both:
        - Competitor Intelligence
        - Product Marketing Intelligence

        Include these sections:

        1. Executive Summary
        2. Company / Product Overview
        3. Market Understanding
        4. Public Sources Used
        5. Target Customers

        6. Top Competitor Ranking

        Create a ranked table based on:
        - Market Presence
        - Brand Recognition
        - Product/Service Strength
        - Customer Reach
        - Competitive Positioning

        Include:
        - Rank
        - Competitor Name
        - Reason for Ranking

        7. Top Competitors

        8. Competitor Comparison Table

        9. Product Positioning Analysis
        10. Marketing Messaging Analysis
        11. Market Trends
        12. SWOT Analysis
        13. Business Opportunities
        14. Risks and Challenges
        15. Strategic Recommendations
        16. AI Usage Disclosure
        17. Limitations
        18. Future Improvements

        Important:
        - Mention that public web data was used.
        - Do not invent exact numbers.
        - If information is uncertain, say "Based on available public sources".
        - Do NOT include the target company itself in competitor rankings.
        - Do NOT include the target product/company itself in product rankings.
        - Format output in Markdown.
        """


# ---------------------------------------------------------
# Streamlit UI Starts Here
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Business & Market Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered Business & Market Intelligence Agent")

st.write("""
This AI assistant helps marketing and sales teams understand a target company,
its competitors, recent content activity, positioning, and possible outreach or lead-generation opportunities.
""")

st.info("""
This project follows DS Intern Hackathon May 2026: 
AI-Powered Business & Market Intelligence Agents.
""")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("Hackathon Tracks")

st.sidebar.write("""
**Track 1: Competitor Intelligence**  
Find and compare competitors for a company, domain, service line, or market segment.
""")

st.sidebar.write("""
**Track 2: Product Marketing Intelligence**  
Analyze how similar products are promoted, positioned, packaged, and communicated.
""")

st.sidebar.write("---")

st.sidebar.write("""
**Project Layers**
1. Public Web Search  
2. Data Extraction  
3. AI Analysis  
4. Business Report  
""")


# ---------------------------------------------------------
# User Inputs
# ---------------------------------------------------------

st.header("📝 Enter Research Details")

track = st.selectbox(
    "Select Hackathon Track",
    [
        "Track 1 - Competitor Intelligence",
        "Track 2 - Product Marketing Intelligence",
        "Complete Business & Market Intelligence"
    ]
)

company = st.text_input(
    "Enter Target Company / Product",
    placeholder="Example: Freshworks, Zomato, Salesforce, AI Voice Bot"
)

industry = st.text_input(
    "Enter Domain / Service Line / Market Segment",
    placeholder="Example: CRM, Food Delivery, ERP, Customer Support Automation"
)

region = st.text_input(
    "Enter Target Region / Market",
    placeholder="Example: India, US, Global"
)

goal = st.text_area(
    "Enter Business Goal",
    placeholder="Example: Understand competitors, positioning, product messaging, and opportunities."
)


# ---------------------------------------------------------
# Generate Button
# ---------------------------------------------------------

if st.button("🚀 Generate Business Intelligence Report"):

    if company.strip() == "" or industry.strip() == "" or region.strip() == "":
        st.warning("Please fill company/product, industry/domain, and region.")

    else:
        with st.spinner("Step 1: Searching public web sources..."):

            # Collect public data
            sources, public_data = collect_public_data(
                company,
                industry,
                region,
                track
            )

        # Show collected sources
        st.subheader("🔎 Public Sources Collected")

        if sources:
            source_df = pd.DataFrame([
                {
                    "Title": source["title"],
                    "URL": source["url"],
                    "Snippet": source["snippet"]
                }
                for source in sources
            ])

            st.dataframe(source_df, use_container_width=True)

        else:
            st.warning("No sources found. AI will use general business reasoning.")

        with st.spinner("Step 2: AI is analyzing collected public data..."):

            # Build final AI prompt
            final_prompt = build_prompt(
                track,
                company,
                industry,
                region,
                goal,
                public_data
            )

            # Generate final report
            report = ask_ai(final_prompt)

        st.success("Report generated successfully!")

        # Display report
        st.subheader("📄 Final Intelligence Report")
        st.markdown(report)

        # Download report
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name=f"{company}_business_market_intelligence_report.md",
            mime="text/markdown"
        )


# ---------------------------------------------------------
# Workflow Section
# ---------------------------------------------------------

st.write("---")
st.header("🔁 Agent Workflow")

st.code("""
User Input
↓
Track Selection
↓
Public Web Search Agent
↓
Data Extraction from Public Sources
↓
Filtering and Deduplication
↓
Prompt Builder
↓
AI Business & Market Intelligence Agent
↓
Structured Report Generation
↓
Downloadable Output
""")


# ---------------------------------------------------------
# Guardrails Section
# ---------------------------------------------------------

st.header("🛡️ Rules & Guardrails Followed")

st.write("""
- Uses only public web information.
- Does not use private, paid, confidential, or protected sources.
- Clearly discloses AI usage.
- Mentions limitations.
- Produces structured output for business use.
""")


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.write("---")
st.write("Created for DS Intern Hackathon May 2026 | Khushi Kumari")