import requests
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

def call_llm(prompt):
    url = f"{OLLAMA_HOST}/api/generate"

    try:
        response = requests.post(
            url,
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            }
        )

        # ✅ Check HTTP error
        if response.status_code != 200:
            return f"Ollama error: {response.text}"

        data = response.json()

        # ✅ Safe access
        return data.get("response", "No response from model")

    except Exception as e:
        return f"LLM Error: {str(e)}"

# -------- FOLLOW-UP EMAIL --------
def generate_followup_email(lead, last_interaction):
    prompt = f"""
    Write a SHORT follow-up email (max 80 words).

    Tone:
    - Friendly
    - Startup founder style
    - Not formal or corporate

    Include:
    - Greeting
    - Reference to last discussion
    - One clear next step

    Investor: {lead.name}
    Stage: {lead.stage}
    Last interaction: {last_interaction.notes if last_interaction else "No prior interaction"}

    Output only email text. No extra explanation.
    """

    return call_llm(prompt)


# -------- SUMMARY --------
def summarize_interactions(interactions):
    notes = "\n".join([i.notes for i in interactions])

    prompt = f"""
    Summarize these investor interaction notes into key insights:

    {notes}
    """

    return call_llm(prompt)


# -------- SCORE --------
def score_lead(lead, interactions_count):
    score = 0

    if lead.net_worth_tier == "High":
        score += 50
    elif lead.net_worth_tier == "Medium":
        score += 30
    else:
        score += 10

    if lead.stage == "Interested":
        score += 30
    elif lead.stage == "Contacted":
        score += 20

    score += min(interactions_count * 5, 20)

    return score

def next_best_action(lead, last_interaction, days_since):
    prompt = f"""
    You are an assistant helping a startup founder manage investors.

    Analyze the situation and suggest the NEXT BEST ACTION.

    Rules:
    - Keep it under 2 lines
    - Be direct and actionable
    - Avoid generic advice

    Investor: {lead.name}
    Stage: {lead.stage}
    Days since last interaction: {days_since}
    Last interaction notes: {last_interaction.notes if last_interaction else "No prior interaction"}

    Give a SHORT actionable recommendation (1-2 lines).
    """

    return call_llm(prompt)