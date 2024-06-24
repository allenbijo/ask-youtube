from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def get_transcript(video_url):
	video_id = video_url.split("=")[1]
	transcript = YouTubeTranscriptApi.get_transcript(video_id)
	s = ""
	for line in transcript:
		s += (f"{line['text']} ")
	return s


def ask_llm(transcript, question, key):
	question_to_ask = "This is the transcript of a youtube video. " + transcript + " \n\nNow, I have a question for you answer in unformatted text only: " + question
	# Gemini model
	genai.configure(api_key=key)
	# Choose a model that's appropriate for your use case.
	model = genai.GenerativeModel('gemini-1.5-flash')
	llm_response = model.generate_content(question_to_ask)
	return llm_response


if __name__ == "__main__":

	st.title("Ask a question about a youtube video")
	if not os.environ.get('GEMINI_API_KEY'):
		st.sidebar.write("Couldn't find GEMINI_API_KEY in .env")
		key = st.sidebar.text_input("Enter GEMINI API KEY", type="password")
	else:
		key = os.environ.get('GEMINI_API_KEY')

	if key:
		if video_url := st.text_input("Enter the youtube video URL"):
			transcript = get_transcript(video_url)
			_, c, _ = st.columns(3)
			with c:
				st.markdown(f'![Alt text](https://i.ytimg.com/vi/{video_url.split("=")[-1]}/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAkpTh1x8TlNksn9I4nYpFnTAzkiA "a title")')
			if question := st.text_input("Enter your question"):
				answer = ask_llm(transcript, question, key)
				st.balloons()
				st.write(answer.text)
