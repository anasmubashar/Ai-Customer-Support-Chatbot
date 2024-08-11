from langchain_google_genai import GoogleGenerativeAI
from .config import GOOGLE_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def generate_analysis_and_tips(user_input):
    try:
        # Pass a list of strings to `llm.generate`
        prompts = [
            "Analyze this coding interview question and keep the answer extremely concise: " + user_input
        ]
        prompts2 = [
            "Provide tips for answering this coding interview question and keep the answer extremely short:" + user_input
        ]
        analysis = llm.generate(prompts)
        tips = llm.generate(prompts2)

        
        # # Print the type and content of responses
        # print("Responses type:", type(responses))
        # print("Responses content:", responses)
        
        # # Extract information based on what `LLMResult` provides
        # # Example if `LLMResult` has an attribute `text` or similar
        # analysis = responses[0].generations[0].text
        # tips = responses[1].generations[0].text
        
        # print(analysis, tips)
        return analysis, tips
    except Exception as e:
        raise ValueError(f"Error generating analysis and tips: {str(e)}")
