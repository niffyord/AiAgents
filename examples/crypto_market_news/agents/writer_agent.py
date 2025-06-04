from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a crypto market analyst. Using provided search summaries for"
    " ETH and BTC, write a concise report under 150 words that highlights"
    " notable trends, price movements and important regulatory or adoption"
    " news. Provide two or three follow-up questions for additional"
    " research." 
)


class CryptoReport(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_questions: list[str]


writer_agent = Agent(
    name="CryptoWriterAgent",
    instructions=PROMPT,
    model="gpt-4.1",
    output_type=CryptoReport,
)
