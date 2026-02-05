import random
import re
from app.core.config import settings

def is_valid_symptom_input(text: str) -> bool:
    text = text.strip().lower()

    if len(text) < 10:
        return False

    alpha_chars = sum(c.isalpha() for c in text)
    if alpha_chars / len(text) < 0.6:
        return False

    if re.fullmatch(r"(.)\1{5,}", text):
        return False

    return True



async def predict_disease(symptoms: str) -> str:
    if not is_valid_symptom_input(symptoms):
        return (
            "⚠️ The provided input doesn’t look like valid symptom information.\n\n"
            "Please describe your symptoms clearly, for example:\n"
            "• Fever and cough for 2 days\n"
            "• Headache with nausea\n"
            "• Stomach pain and diarrhea"
        )

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-test"):
        return rule_based_prediction(symptoms)

    return rule_based_prediction(symptoms)



def rule_based_prediction(symptoms: str) -> str:
    s = symptoms.lower()

    disease_map = {
        "fever": ["Seasonal Flu", "Viral Infection"],
        "cough": ["Common Cold", "Bronchitis"],
        "headache": ["Migraine", "Tension Headache"],
        "nausea": ["Food Poisoning", "Gastritis"],
        "vomiting": ["Gastroenteritis", "Food Poisoning"],
        "diarrhea": ["Gastroenteritis", "Irritable Bowel Syndrome"],
        "chest pain": ["Acid Reflux", "Cardiac-related condition"],
        "sore throat": ["Common Cold", "Pharyngitis"],
        "fatigue": ["Anemia", "Viral Infection"]
    }

    matched = set()

    for keyword, diseases in disease_map.items():
        if keyword in s:
            matched.update(diseases)

    if not matched:
        matched = {
            "General Viral Infection",
            "Stress-related Condition"
        }

    selected = random.sample(list(matched), min(2, len(matched)))

    return (
        f"Based on the symptoms described, possible conditions may include "
        f"{' and '.join(selected)}.\n\n"
        "⚠️ This information is not a medical diagnosis.\n"
        "Please consult a qualified healthcare professional for an accurate evaluation."
    )
