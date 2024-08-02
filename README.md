# fasthtml-gemini
Creating a FastHTML chat app with the Gemini API in &lt; 80 Lines of Code  

Huge thanks to the FastHTML team for the exciting new framework and for the examples. 
This example is quick adjustment of their [chatbot example](https://github.com/AnswerDotAI/fasthtml-example/tree/main/02_chatbot) to use Gemini vs Claude / Claudette.

![Chat image](images/image1.png "Chat app")

### Setup

Get a Gemini [API Key](https://ai.google.dev/gemini-api/docs/api-key) 

```
export API_KEY="<your-api-key>"
```

Or use [dotenv](https://pypi.org/project/python-dotenv/)

```
pip install -r requirements.txt
```

To run the application from the main folder:
```
python3 app.py
```