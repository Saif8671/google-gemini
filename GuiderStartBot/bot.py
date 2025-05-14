import PyPDF2
import requests

class EventAssistantBot:
    def __init__(self, api_key, pdf_path):
        self.api_key = api_key
        self.pdf_text = self.extract_pdf(pdf_path)
        self.system_prompt = """
You are a friendly Event Information Assistant. Your primary purpose is to answer questions about the event described in the provided context. Follow these guidelines:

1. You can respond to basic greetings like "hi", "hello", or "how are you" in a warm, welcoming manner
2. For event information, only provide details that are present in the context
3. If information is not in the context, politely say "I'm sorry, I don't have that specific information about the event"
4. Keep responses concise but conversational
5. Do not make assumptions beyond what's explicitly stated in the context
6. Always prioritize factual accuracy while maintaining a helpful tone
7. Do not introduce information that isn't in the context
8. If unsure about any information, acknowledge uncertainty rather than guess
9. You may suggest a few general questions users might want to ask about the event
10. Maintain a warm, friendly tone in all interactions
11. You should refer to yourself as "Event Bot"
"""

    def extract_pdf(self, path):
        try:
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return ''.join(page.extract_text() for page in reader.pages)
        except Exception as e:
            return f"Error reading PDF: {e}"

    def post_process_response(self, response, query):
        query_lower = query.lower()
        if any(word in query_lower for word in ["lunch", "food", "eat"]):
            points = []
            if "provided to all" in response:
                points.append("• Lunch will be provided to all participants who have checked in at the venue.")
            if "cafeteria" in response.lower() and "floor" in response.lower():
                if "1:00" in response and "2:00" in response:
                    points.append("• It will be served in the Cafeteria on the 5th floor between 1:00 PM and 2:00 PM IST.")
            if "check-in" in response.lower():
                points.append("• Ensure you've completed check-in at the registration desk to be eligible.")
            if "volunteer" in response.lower():
                points.append("• Ask a volunteer for directions to the cafeteria.")
            return "Regarding lunch:\n\n" + "\n".join(points) if points else response
        return response

    def answer_question(self, query):
        prompt = f"Event information: {self.pdf_text}\n\nQuestion: {query}\n\nGuidelines:\n{self.system_prompt}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        try:
            r = requests.post(url, json=payload, headers=headers)
            data = r.json()
            if "candidates" in data and data["candidates"]:
                response = "\n".join(part.get("text", "") for part in data["candidates"][0]["content"]["parts"])
                return self.post_process_response(response, query)
            return data.get("error", {}).get("message", "Unexpected error from model.")
        except Exception as e:
            return f"Error: {e}"
