import openai
from dotenv import load_dotenv
import os
from app.utils.transcription import transcribe_audio  # Importing the transcription function

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  

def gpt4_task(task_name: str, prompt: str, transcript_text: str) -> str:
    """
    Interacts with GPT-4 for various tasks using a structured prompt.
    """
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant analyzing audio transcripts."},
            {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript_text}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1500,
            temperature=0.7,
            top_p=1.0
        )

        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"OpenAI API Error during {task_name}: {e}")
        return None

def process_audio_tasks(audio_url: str) -> dict:
    """
    Transcribe the audio and process transcription with various GPT-4 tasks.
    """
    try:
        # Step 1: Transcribe the audio
        print("Starting transcription...")
        transcript_text = transcribe_audio(audio_url)  # Replace with your working transcription function

        # Debug: Ensure transcription is successful
        if not transcript_text:
            raise ValueError("Transcription failed or returned no text.")
        
        print("Transcription completed successfully.")
        print(f"Transcript Text:\n{transcript_text}")

        # Step 2: Process transcription with GPT-4
        tasks = {
            "Summary": "Provide a clear and concise summary of the meeting transcript. Highlight the main objectives, key discussions, significant outcomes, and any critical points raised.",
            "Speaker Identification": "Identify the total number of distinct speakers in the meeting based on the transcript. If possible, list them with their speaker labels (e.g., Speaker 1, Speaker 2) and provide any identifiable roles or contributions if discernible.",
            "Entity Detection": """
                Extract and categorize entities from the meeting transcript into the following groups:
                
                1.Persons: Names of individuals mentioned.
                2.Organizations: Names of companies, institutions, or teams.
                3.Projects: Names or titles of any ongoing or upcoming projects discussed.
                Provide the entities in a structured format.
            """,
            "Decisions": """
                List all the key decisions made during the meeting. For each decision, mention:
                
                1.What was decided?
                2.Who were the participants involved in the decision-making process?
                3.Who approved or finalized the decision (if mentioned)?
                Ensure clarity and structure in your response.
            """,
            "Keyword Frequency": """
                Identify the top 5-10 most frequently discussed keywords in the meeting transcript. For each keyword, provide:
                
                1.The keyword
                2.A brief explanation of its context or relevance in the meeting discussion
                3.Prioritize clarity and precision
            """,
            "Sentiment Analysis": "Analyze the overall sentiment of the meeting transcript. Classify it as Positive, Neutral, or Negative. Provide a brief reasoning for your classification, mentioning key phrases or tone indicators that support your analysis.",
            "Key Topics": """
                List the key topics or highlights discussed during the meeting. For each topic:
                
                1.Topic Name
                2.A brief summary of the discussion related to the topic
                3.Ensure clarity and avoid redundant details.
            """,
            "Action Items": """
                Extract all action items or tasks assigned during the meeting. For each task, include:
                
                -Task Description
                -Assigned By
                -Assigned To
                -Priority Level: Important, Urgent, or Non-Urgent
                -Organize your response into these three categories for clarity.
            """
        }

        responses = {}
        for task_name, prompt in tasks.items():
            responses[task_name] = gpt4_task(task_name, prompt, transcript_text)

        return {"result": responses}

    except Exception as e:
        print(f"Error in processing tasks: {e}")
        return {"result": {"error": str(e)}}
