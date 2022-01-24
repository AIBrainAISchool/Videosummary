from flask import Flask, jsonify, request
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from os import environ


summarizer= pipeline('summarization')
app = Flask(__name__)

def getTranscript(video_id):
    summarized_text = "Invalid URL"
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript[0:5]
        result = ""
        for i in transcript:
            result += ' ' + i['text']

        num_iters = int(len(result)/1000)
        summarized_text = []
        for i in range(0, num_iters + 1):
            start = 0
            start = i * 1000
            end = (i + 1) * 1000
            out = summarizer(result[start:end])
            out = out[0]
            out = out['summary_text']
            summarized_text.append(out)

    #  summarized_text = summarized_text[0]
        print(summarized_text)
    except Exception as e:
        print("Please provide a valid video id",e)

    return summarized_text
@app.route('/health')
def index():
    return "Working"

@app.route('/summary', methods=['POST'])
def summary():
    data = request.json
    url = data["url"]
    video_id = url.split("=")[1]
    summarized_text = getTranscript(video_id)

    return jsonify(summarized_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=environ.get('PORT',5000))
