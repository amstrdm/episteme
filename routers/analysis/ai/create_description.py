from openai import OpenAI
from dotenv import load_dotenv
import os
import yfinance as yf


ENV_PATH = os.getenv("ENV_PATH")
load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in create_description.py!")

client = OpenAI(api_key=OPENAI_API_KEY)


prompt = """
You are an investment analysis assistant. Your task is to generate a comprehensive company profile for a given stock using fundamental and stable data sources. Focus on creating an overall description that outlines the company’s core business, key products, market segments, and long-term outlook. Follow these instructions:

Core Business Overview:

Describe what the company does, including its primary industry and business model.
Highlight its flagship products or services (e.g., ARS’s nasal spray) and explain their purpose in the market.
You are free to use the web and research as much infomation as you need to understand the company and it's strategy better.
Market and Competitive Positioning:

Summarize the target market and overall market opportunity.
Discuss the company’s competitive advantages or unique value propositions relative to its peers.
Long-Term Outlook and Sentiment:

Provide an overall sentiment based on the company’s fundamentals, such as growth potential, financial stability, and strategic direction.
Emphasize long-term prospects rather than short-term catalysts or recent news.
Data Synthesis:

Incorporate fundamental data (e.g., market cap, revenue trends, key financial metrics) and qualitative insights from reliable sources such as official filings, investor presentations, and reputable financial platforms.
Do not include time-sensitive or recent news items.

The user should get a good broad idea of what the company does and what it is. Use easy to understand language and avoid complicated jargon.
Output Format:

Present the profile as a single, clear, and concise paragraph.
Ensure that the final output gives a complete picture of the company’s stable, long-term characteristics and overall outlook.
Your final output should provide investors with a robust, long-term overview of the company, including its business model, market opportunity, and inherent strengths or weaknesses.
---

"""

def generate_company_description(ticker: str):
    yf_ticker = yf.Ticker(ticker)
    company_info = yf_ticker.info

    response = client.responses.create(
        model = "gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input = [
            {
                "role": "user",
                "content": prompt+f"Company description:\n{company_info}\n",
            }
        ]
    )

    return response.output_text

if __name__ == "__main__":

    print(generate_company_description(ticker="TSLA"))