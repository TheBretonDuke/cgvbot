from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_FILE_ID = "file-AUSaaumibhLwKS6LTgZ9dw"
OPENAI_MODEL = "gpt-4.1-nano-2025-04-14"
print("Using training file ID:", OPENAI_FILE_ID)

client = OpenAI()

try:
    ft_job = client.fine_tuning.jobs.create(
        training_file=OPENAI_FILE_ID,
        model=OPENAI_MODEL
    )
    print("Fine Tune Job has been created with id:", ft_job.id)
except Exception as e:
    print("Error creating fine tune job:", e)
