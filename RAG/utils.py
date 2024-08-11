from langchain_google_genai import GoogleGenerativeAI
from RAG.config import GOOGLE_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def generate_analysis_and_tips(user_input):
    try:
        analysis_prompt = ["Analyze this coding interview question and keep the answer extremely concise: " + user_input]
        tips_prompt = ["Provide tips for answering this coding interview question and keep the answer extremely short: " + user_input]
        
        analysis = llm.generate(analysis_prompt)
        tips = llm.generate(tips_prompt)

        return analysis, tips
    except Exception as e:
        raise ValueError(f"Error generating analysis and tips: {str(e)}")