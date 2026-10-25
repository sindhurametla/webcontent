# memory_chat.py
# Terminal chatbot with conversation memory that builds itself turn by turn.
# Run:  python memory_chat.py   (type 'quit' or 'exit' to stop)
#
# NOTE: history lives only in this process's memory, so it resets when the
# script stops. Production apps store it per session in a database.

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()  # reads GROQ_API_KEY from the .env file

# Keep only the most recent messages so long chats don't exceed token limits
MAX_MESSAGES = 20

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

# LLMs are stateless, so "memory" means sending past messages with every request.
# MessagesPlaceholder is the slot where that list of past messages is inserted.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant. Use the conversation history to stay consistent."),
    MessagesPlaceholder("history"),   # past turns, in order
    ("human", "{question}"),          # the new user question
])

# StrOutputParser turns the AIMessage into a plain string
chain = prompt | model | StrOutputParser()

history = []  # starts empty; grows by two messages per turn


def main():
    print("Chat with the bot (type 'quit' to exit).")
    while True:  # one loop iteration = one chat turn
        question = input("You: ")

        if question.strip().lower() in {"quit", "exit"}:
            break
        if not question.strip():  # ignore empty input
            continue

        try:
            answer = chain.invoke({
                "history": history[-MAX_MESSAGES:],  # send only recent turns
                "question": question,
            })
        except Exception as e:  # e.g. rate limit or network error
            print("Error:", e)
            continue  # history is untouched, so the chat can carry on

        print("Bot:", answer)

        # Append AFTER the call: the new question is already passed via {question}
        history.append(HumanMessage(question))
        history.append(AIMessage(answer))
        print(f"   (history now has {len(history)} messages)")


if __name__ == "__main__":
    main()