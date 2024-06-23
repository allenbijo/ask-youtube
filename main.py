from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


def get_transcript(video_url):
	video_id = video_url.split("=")[-1]
	transcript = YouTubeTranscriptApi.get_transcript(video_id)
	s = ""
	for line in transcript:
		s += (f"{line['text']} ")
	return s

def ask_llm(transcript, question):
	question_to_ask = "This is the transcript of a youtube video. " + transcript + " \n\nNow, I have a question for you answer in plain text only: " + question
	# Gemini model
	genai.configure(api_key=os.environ['GEMINI_API_KEY'])
	# Choose a model that's appropriate for your use case.
	model = genai.GenerativeModel('gemini-1.5-flash')
	llm_response = model.generate_content(question_to_ask)
	return llm_response



# Example usage
video_url = "https://www.youtube.com/watch?v=PJXtXN-PW60"
transcript = get_transcript(video_url)

question = "What is the verdict of this video?"
answer = ask_llm(transcript, question)
print(answer.text)
