"""AI services module for email generation.

Provides AI-powered email content generation using LLM models.
Generates structured email messages with subject and content.
"""

from api.ai.llms import get_openai_llm
from api.ai.schemas import EmailMessage


def generate_email_message(query: str, tone: str = "professional") -> EmailMessage:
    """Generate email content using AI based on user prompt.
    
    Uses LLM (Groq/LLaMA) to generate a structured email with subject
    and content based on the user's natural language prompt.
    
    Args:
        query: User's natural language prompt describing the email
               (e.g., "Write a follow-up email to client about project")
    
    Returns:
        EmailMessage: Structured email with subject and content fields
        
    Example:
        >>> email = generate_email_message("Thank you email for interview")
        >>> print(email.subject)
        "Thank You for the Interview Opportunity"
        >>> print(email.content)
        "Dear Hiring Manager, I wanted to express..."
    """
    # Get base LLM model instance
    llm_base = get_openai_llm()
    
    # Configure LLM to output structured EmailMessage format
    llm = llm_base.with_structured_output(EmailMessage)
    
    # Tone-specific instructions
    tone_instructions = {
        "professional": "Use formal, business-appropriate language.",
        "casual": "Use friendly, relaxed language.",
        "friendly": "Use warm, approachable language.",
        "formal": "Use very formal, respectful language."
    }
    
    tone_instruction = tone_instructions.get(tone.lower(), tone_instructions["professional"])
    
    # Prepare conversation messages for the LLM
    messages = [
        (
            "system",
            f"You are a helpful assistant for research and composing plaintext emails. "
            f"Do not use markdown in your response only use plain text. {tone_instruction}"
        ),
        ("human", f"{query}"),
    ]
    
    # Invoke LLM and return structured email
    return llm.invoke(messages)
