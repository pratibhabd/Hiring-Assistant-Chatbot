from uuid import uuid4
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
os.environ["GROQ_MODEL"]


def generate_questions(user_role:str, user_experience:float,
                       tech_stack:str)->str:
    print("Generating questions...")
    """
    Generate interview questions using Groq LLM based on tech stack
    """

    # Create prompt
    prompt = f"""
    You are a technical interviewer.

    Generate 5 interview questions for a candidate with the following tech stack:
    Candidate details:
    - Role: {user_role}
    - Experience: {user_experience}
    - Tech Stack: {tech_stack}

    Questions should:
    - Be clear and concise
    -Don't include writing a code or implementing in any programming
     language questions, let it be simple theory questions and scenario based questions only
    - Cover fundamentals and practical experience
    - Increase in difficulty based on role an experience given
    Return only the questions in numbered format.
    """

    # Initialize client — Groq() automatically reads GROQ_API_KEY from env
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    chat_completion = client.chat.completions.create(
        model=model_name,  # you can change to mixtral-8x7b or llama3-70b
        messages=[
            {"role": "user", "content": prompt }],
        temperature=0.3
    )
    # Print the assistant's reply
    return chat_completion.choices[0].message.content

def evaluate_answers(role:str, experience:float, tech_stack:str, question:str, answer:str):
    prompt = f"""
    You are a technical interviewer evaluator.

    Evaluate the following answers for a candidate appropriately:
      
    Candidate details:
    - Role: {role}
    - Experience: {experience}
    - Tech Stack: {tech_stack}

    Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer briefly:
    - Give a score out of 5
    - One-line feedback
    - If answers are irrelevant ask the candidate to 
    answer the question correctly kindly to pass the interview from next onwards.
       """

    # Initialize client — Groq() automatically reads GROQ_API_KEY from env
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    chat_completion = client.chat.completions.create(
        model=model_name,  # you can change to mixtral-8x7b or llama3-70b
        messages=[
            {"role": "user", "content": prompt}],
        temperature=0.3
    )
    # Print the assistant's reply
    return chat_completion.choices[0].message.content
