import google.generativeai as genai
import os
from serpapi import SerpApiClient

class SerpAPIClient:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            raise ValueError("SERP_API_KEY must be provided via argument or SERP_API_KEY env variable.")
    
    def search(self, company_name):
        try:
            # Define parameters for the SerpApi search
            extracted_data = []
            queries = [
                company_name + ' company details',
                'what is the acquisition history of ' + company_name,
                'what are companies related to ' + company_name,
                'what is the latest news on ' + company_name
            ]
            for q in queries:
                params = {
                    "engine": "google",
                    "q": q,
                    "api_key": os.getenv("SERP_API_KEY"),
                    "location": "New York, United States" # Current location, as per your request
                }

                # Perform the search using SerpApi
                search = SerpApiClient(params)
                results = search.get_json()
                extracted_data.append('Result for ' + q + '\n')
                try:
                    if 'answer_box' in results:
                        for res in results['answer_box']:
                            extracted_data.append(f"Google Answer Box:\nTitle: {res.get('title', 'N/A')}\nSnippet: {res.get('snippet', 'N/A')}\nKeywords: {res.get('snippet_highlighted_words', 'N/A')}\nSource: {res.get('link', 'N/A')}\n")
                except Exception as e:
                    print(str(e))
                try:
                    if 'organic_results' in results:
                        for res in results['organic_results']:
                            extracted_data.append(f"Related Questions:\nQuestion: {res.get('question', 'N/A')}\nTitle: {res.get('title', 'N/A')}\nSnippet: {res.get('snippet', 'N/A')}\nKeywords: {res.get('snippet_highlighted_words', 'N/A')}\nSource: {res.get('link', 'N/A')}\Date: {res.get('date', 'N/A')}")
                except Exception as e:
                    print(str(e))
                try:
                    if 'knowledge_graph' in results:
                        for res in results['knowledge_graph']:
                            extracted_data.append(f"Knowledge Graph:\Title: {res.get('title', 'N/A')}\Type: {res.get('type', 'N/A')}\Description: {res.get('description', 'N/A')}\n")
                except Exception as e:
                    print(str(e))
                try:
                    if 'related_questions' in results:
                        for rel_ques in results['related_questions']:
                            extracted_data.append(f"Related Questions:\nQuestion: {rel_ques.get('question', 'N/A')}\nTitle: {rel_ques.get('title', 'N/A')}\nSnippet: {rel_ques.get('snippet', 'N/A')}\nSource: {rel_ques.get('link', 'N/A')}\n")
                except Exception as e:
                    print(str(e))
            return extracted_data

        except Exception as e:
            raise Exception(e)