from datetime import datetime
import re


def export_chat_text(messages, model_name):
    lines = []
    lines.append("Sinhala Offline Chatbot - Chat Export")
    lines.append(f"Model: {model_name}")
    lines.append(f"Exported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("-" * 60)

    for msg in messages:
        speaker = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{speaker}: {msg['content']}")
        lines.append("")

    return "\n".join(lines)


def format_seconds(seconds):
    return f"{seconds:.2f} s"


def english_ratio(text):
    if not text.strip():
        return 1.0

    english_chars = len(re.findall(r"[A-Za-z]", text))
    total_chars = len(re.findall(r"\S", text))

    if total_chars == 0:
        return 1.0

    return english_chars / total_chars


def has_bad_meta_text(text):
    bad_patterns = [
        "Here's a possible response",
        "AI assistant",
        "possible response",
        "Here is",
        "assistant:",
        "response:"
    ]

    lower = text.lower()
    return any(p.lower() in lower for p in bad_patterns)


def is_low_quality_sinhala(text):
    if not text or len(text.strip()) < 3:
        return True

    if has_bad_meta_text(text):
        return True

    if english_ratio(text) > 0.20:
        return True

    return False