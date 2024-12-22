from langchain.tools import tool
import pdfplumber
from openai import OpenAI

API_KEY = ''

@tool
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Description: Extracts text from a PDF file.
    Input: File path as a string, e.g., "agent_document/resume.pdf".
    Output: Extracted text from the PDF or an error message.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return f"output text: {text}"
    except Exception as e:
        return f"failed: {e}"

@tool
def generate_interview_questions(content: str) -> str:
    """
    Description: A tool for reviewing and rehearsing interview based on input resume. 
    Input: A resume.
    Output: 5 specific interview's questions.
    """
    try:
        client = OpenAI(
            api_key=API_KEY,  # This is the default and can be omitted
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional software manager, please review resume and ask 5 specific questions"},
                {"role": "user", "content": content},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"failed: {e}"

@tool
def generate_recommend_candidate_reasons(content: str) -> str:
    """
    Description: A tool designed to organize and summarize a candidate's strengths based on input resume. 
    Input: A resume.
    Output: 5 key reasons to recommend why the company should hire the candidate.
    """
    try:
        client = OpenAI(
            api_key=API_KEY,  # This is the default and can be omitted
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional candidate recommender. Please organize the input resume into 5 points that highlight the reasons why the company should hire this candidate."},
                {"role": "user", "content": content},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"failed: {e}"

# Register the tools for LangChain agents
TOOLS = [
    extract_text_from_pdf,
    generate_interview_questions,
    generate_recommend_candidate_reasons
]
