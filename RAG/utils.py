from langchain_google_genai import GoogleGenerativeAI
from RAG.config import GOOGLE_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def generate_analysis_and_tips(user_input):
    analysis = llm.generate("Analyze this coding interview question: " + user_input)
    tips = llm.generate("Provide tips for answering this coding interview question: " + user_input)
    return analysis, tips