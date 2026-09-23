# AI-Powered Business & Market Intelligence Agent

## DS Intern Hackathon May 2026

### Developed By

**Khushi Kumari**

---

# Project Overview

AI-Powered Business & Market Intelligence Agent is an AI-driven research assistant that helps marketing and sales teams understand a target company, its competitors, product positioning, market trends, and business opportunities.

The system collects publicly available web information, extracts useful content, filters duplicate sources, and uses AI to generate structured business intelligence reports.

The goal is to transform public and unstructured information into concise, actionable business insights.

---

# Hackathon Challenge

Build an AI assistant that helps a marketing or sales person understand:

* A target company
* Its competitors
* Product positioning
* Market trends
* Marketing messaging
* Business opportunities
* Outreach and lead-generation possibilities

The solution should convert public, unstructured information into useful business intelligence.

---

# Tracks Covered

## Track 1: Competitor Intelligence

Analyze and compare competitors for a company, domain, service line, or market segment.

### Capabilities

* Competitor identification
* Competitor comparison
* Competitive positioning analysis
* Market gap identification
* Opportunity analysis
* Strategic recommendations

---

## Track 2: Product Marketing Intelligence

Analyze how products and services are positioned, marketed, packaged, and communicated.

### Capabilities

* Product positioning analysis
* Marketing messaging analysis
* Similar product comparison
* Market trend analysis
* Communication strategy insights
* Product improvement recommendations

---

# Key Features

* Streamlit-based user interface
* Public web search integration
* Website content extraction
* Source collection and display
* Duplicate source filtering
* AI-powered business analysis
* Competitor intelligence reports
* Product marketing intelligence reports
* Business-readable report generation
* Downloadable report output
* AI usage disclosure
* Limitations and future improvements section

---

# Tech Stack

| Technology    | Purpose                     |
| ------------- | --------------------------- |
| Python        | Backend Development         |
| Streamlit     | User Interface              |
| Groq LLM      | AI Analysis & Summarization |
| DDGS          | Public Web Search           |
| BeautifulSoup | Website Content Extraction  |
| Requests      | Webpage Retrieval           |
| Pandas        | Data Processing             |
| Python Dotenv | API Key Management          |

---

# System Architecture

```text
User Input
↓
Track Selection
↓
Public Web Search Agent
↓
Data Collection
↓
Website Content Extraction
↓
Filtering & Deduplication
↓
Prompt Builder
↓
AI Business & Market Intelligence Agent
↓
Structured Report Generation
↓
Downloadable Output
```

---

# Prompt Flow / AI Workflow

### Step 1: User Input

The user provides:

* Company/Product Name
* Industry/Domain
* Region/Market
* Business Goal
* Track Selection

### Step 2: Public Web Research

The system searches publicly available web sources related to the user's request.

### Step 3: Data Extraction

Website content is extracted using BeautifulSoup.

### Step 4: Data Processing

The system:

* Removes duplicate URLs
* Filters collected content
* Structures extracted information

### Step 5: AI Analysis

Groq LLM analyzes collected information and generates:

* Competitor insights
* Product positioning insights
* Marketing messaging analysis
* Market trends
* Opportunities
* Risks
* Recommendations

### Step 6: Report Generation

A structured business intelligence report is generated and made available for download.

---

# Data Sources Used

The project uses publicly available information from:

* Public company websites
* Industry blogs
* Market research articles
* Public news articles
* Public directories
* Search engine results
* User-supplied company/product inputs

The system does **not** use:

* Private data
* Confidential data
* Paid datasets
* Protected information
* Internal company records

---

# Example Input

```text
Track:
Competitor Intelligence

Company:
Zomato

Industry:
Food Delivery

Region:
India

Goal:
Find top competitors and compare their positioning.
```

---

# Output Generated

The system generates:

* Executive Summary
* Company Overview
* Public Sources Used
* Competitor Analysis
* Competitor Ranking
* Competitor Comparison Table
* Product Positioning Analysis
* Marketing Messaging Analysis
* Market Trends
* SWOT Analysis
* Opportunities
* Risks and Challenges
* Strategic Recommendations
* AI Usage Disclosure
* Limitations
* Future Improvements

---

# Deliverables Coverage

| Hackathon Deliverable          | Status |
| ------------------------------ | ------ |
| Working Demo                   | ✅      |
| Competitor Intelligence        | ✅      |
| Product Marketing Intelligence | ✅      |
| Prompt Flow / AI Workflow      | ✅      |
| Public Data Sources            | ✅      |
| Data Extraction                | ✅      |
| Filtering & Deduplication      | ✅      |
| Business Intelligence Report   | ✅      |
| AI Usage Disclosure            | ✅      |
| Limitations                    | ✅      |
| Evaluation Sheet               | ✅      |

---

# Rules & Guardrails Followed

* Uses only public web information
* No private or confidential data is used
* AI usage is disclosed
* Limitations are clearly mentioned
* Structured business-readable output is generated
* API keys are stored securely using environment variables

---
# Demo Video

A complete demonstration video is included with the submission.

The video covers:

Project overview
Problem statement
System architecture
Public web source collection
Competitor Intelligence workflow
Product Marketing Intelligence workflow
AI-powered report generation
Final output walkthrough

Video Duration: Approximately 4–5 minutes

---

# How To Run

## Step 1: Create Virtual Environment

```bash
python -m venv venv
```

## Step 2: Activate Environment

```bash
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure API Key

Create a `.env` file:

```env
GROQ_API_KEY=my_actual_groq_api_key
```

For submission, include only:

```env
# .env.example
GROQ_API_KEY=your_groq_api_key_here
```

## Step 5: Run Application

```bash
streamlit run app.py
```

---

# Project Folder Structure

```text
AI_Business_Market_Intelligence_Agent/
│
├── app.py
├── requirements.txt
├── README.md
├── evaluation_sheet.md
├── .env.example
│
├── outputs/
│   └── sample_report.md
│
├── screenshots/
│
└── tests/
    ├── test_groq.py
    └── test_search.py
```

---

# Limitations

* Some websites may block scraping requests.
* Search results may vary over time.
* AI-generated insights should be manually verified.
* Exact market statistics may not always be available.
* This project is intended as a research assistant and prototype solution.

---

# Future Improvements

* News API integration
* RSS feed monitoring
* Social media monitoring
* PDF report generation
* Competitor ranking dashboard
* Interactive visualizations
* Source credibility scoring
* Multi-agent architecture
* Automated newsletter generation

---

# Conclusion

This project demonstrates how AI agents can collect public web information, extract useful content, and transform unstructured data into structured business intelligence.

By combining public web research, data extraction, filtering, and AI-powered analysis, the system provides actionable competitor intelligence and product marketing insights to support business decision-making.
