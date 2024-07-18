import google.generativeai as genai
from src import app
from PIL import Image
import json

INFO_PROMPT = "Based on the content of the document in the uploaded images, define it’s category(Administrative,Financial,Human Resources,Technical), subcategory(Correspondence,Policies and procedures,Meeting minutes,Reports,Forms,Contracts and agreements,Invoices,Budgets,Financial statements ,Expense reports,Tax documents,Payroll records,Purchase orders,Resumes and job applications,Employee contracts,Performance reviews,Time sheets,Benefits information,Training materials,Employee handbooks,Termination and resignation documents,Product manuals,Specifications,Engineering drawings,Software documentation,Troubleshooting guides,Technical reports,Project plans), a path(category/subcategory/year/semester/month in full letters), a list of the most important properties(key/value) and an appropriate file name for it (no exetension) and return them in json format only."

class GeminiConnector():
    def __init__(self) :
        self.config = genai.configure(api_key=app.config['GEMINI_API_KEY'])
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def extractInfo(self, files):
        imgs = [Image.open(file) for file in files]
        response = self.model.generate_content([INFO_PROMPT] + imgs, stream=True)
        response.resolve()
        response = response.text.replace("json","").replace("```","")
        return json.loads(response.encode("utf-8"))