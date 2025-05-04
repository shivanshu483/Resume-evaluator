import requests

# Replace with your Groq API key
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"

def evaluate_resume(resume_text, job_description):
    prompt = f"""
    You are a Resume Career Expert.

    Given the resume below, do the following:
    1. Suggest the best job role this person is suited for.
    2. Generate a suitable job description for that role based on their resume.

    Resume:
    {resume_text}
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()
    if 'choices' in result:
        return result['choices'][0]['message']['content']
    else:
        return f"Error: Expected 'choices' in response, but got {result}"

def evaluate_with_job_description(resume_text, job_description):
    prompt = f"""
    You are a Resume Career Expert.

    Given the resume below, and the job description provided, do the following:
    1. Calculate the percentage of suitability of this resume for the job.
    2. Provide a better job title suggestion for this applicant based on their qualifications.
    3. Provide a score and any feedback on how well the resume matches the job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()
    if 'choices' in result:
        return result['choices'][0]['message']['content']
    else:
        return f"Error: Expected 'choices' in response, but got {result}"