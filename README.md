# Website Summarizer & Memory Chatbot (LangChain + Groq)

Two small LLM projects built with LangChain and Groq:

1. **Website summarizer**: give it a URL and get a short, friendly summary back.
2. **Memory chatbot**: a terminal chat loop that remembers earlier turns of the conversation.

## Features

**Website summarizer**
- Fetches pages with `requests` using browser-like headers
- Adds `https://` automatically if the URL has no scheme
- Catches request failures (timeouts, 403s, bad URLs) and returns a readable error instead of crashing
- Removes `script`, `style`, `nav`, `header`, `footer`, `img` and `input` tags with BeautifulSoup before extracting the title and body text
- Summarizes with a LangChain LCEL chain: `prompt | model | parser`

**Memory chatbot**
- Uses `MessagesPlaceholder` so past turns are inserted into every prompt
- History starts empty and builds itself after each turn
- Ignores empty input and handles API errors without losing the conversation
- Sends only the last 20 messages to stay within token limits

## Tech stack

Python, LangChain (`langchain-core`, `langchain-groq`), Groq (`openai/gpt-oss-120b`), requests, BeautifulSoup, python-dotenv

## Project structure

```
webcontent/
├── scraper.py          # fetch_website_contents(url): fetch + clean page text
├── summarizer.py       # prompt | model | parser chain (or your notebook)
├── memory_chat.py      # terminal chatbot with conversation memory
├── requirements.txt
├── .gitignore
└── .env                # your API key (not committed)
```

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project folder with your Groq key (get one at [console.groq.com](https://console.groq.com)):

   ```
   GROQ_API_KEY=your_key_here
   ```

   No quotes or spaces around `=`.

## Usage

**Summarize a website**

```python
from summarizer import summarize

print(summarize("https://example.com"))
```

Example output: a short, friendly 2-line summary of the page.

**Chat with memory**

```bash
python memory_chat.py
```

```
You: My name is Sam.
Bot: Nice to meet you, Sam!
You: What's my name?
Bot: Your name is Sam.
```

Type `quit` or `exit` to stop.

## How it works

```python
chain = prompt | model | parser
```

- `ChatPromptTemplate` holds the instruction with a `{website}` placeholder
- `ChatGroq` sends the formatted prompt to Groq and returns the reply
- `StrOutputParser` converts the reply into a plain string

For memory, LLMs are stateless, so the chatbot keeps a `history` list of `HumanMessage` and `AIMessage` objects and passes it into the prompt through `MessagesPlaceholder("history")` on every call.

## Limitations

- JavaScript-rendered pages return little content with `requests`
- Very long pages can exceed token limits; there is no truncation or chunking yet
- If a fetch fails, the error text currently flows into the prompt instead of stopping before the model call
- Chat history is stored in memory only and resets when the script stops

## Next steps

- Truncate or chunk long pages
- Short-circuit on fetch errors before calling the model
- Use Playwright for JavaScript-heavy sites
- Persist chat history per session (for example with a database)

## Security

Never commit your `.env` file. It is listed in `.gitignore`.
