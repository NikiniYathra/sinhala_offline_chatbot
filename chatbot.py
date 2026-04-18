import json
import time
import requests
from prompts import MAIN_SYSTEM_PROMPT, FEW_SHOT_EXAMPLES, REWRITE_PROMPT
from utils import is_low_quality_sinhala

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"


def check_ollama_status():
    try:
        response = requests.get(OLLAMA_BASE_URL, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_installed_models():
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return [m["name"] for m in data.get("models", [])]
    except requests.RequestException:
        return []


def build_history_text(chat_history, history_limit=5):
    history_text = ""
    for msg in chat_history[-history_limit:]:
        role = "පරිශීලකයා" if msg["role"] == "user" else "සහායකයා"
        history_text += f"{role}: {msg['content']}\n"
    return history_text.strip()


def get_style_instruction(response_mode="simple"):
    if response_mode == "detailed":
        return """
පිළිතුර තරමක් විස්තරාත්මකව, නමුත් සංවිධානාත්මකව සහ ස්වාභාවිකව දෙන්න.
එකම අදහස හෝ එකම වාක්‍යය නැවත නැවත නොකියන්න.
අදහස් වෙන්වූ කෙටි ඡේද හෝ ලැයිස්තු ලෙස ඉදිරිපත් කරන්න.
අනවශ්‍ය පුරවචන සහ පුනරාවර්තන වළකින්න.
"""
    return """
පිළිතුර කෙටි, සරල, පැහැදිලි ආකාරයෙන් දෙන්න.
එකම අදහස දෙවරක් නොකියන්න.
"""


def build_prompt(user_input, chat_history, history_limit=5, response_mode="simple"):
    history_text = build_history_text(chat_history, history_limit)
    style_instruction = get_style_instruction(response_mode)

    if history_text:
        return f"""
{FEW_SHOT_EXAMPLES}

{style_instruction}

පහත සංවාද ඉතිහාසය සලකා බලන්න.

{history_text}

දැන් පරිශීලකයාගේ නව පණිවිඩයට පිරිසිදු, ස්වාභාවික සිංහලෙන් පිළිතුරු දෙන්න.

පරිශීලකයා: {user_input}
සහායකයා:
""".strip()

    return f"""
{FEW_SHOT_EXAMPLES}

{style_instruction}

පරිශීලකයා: {user_input}
සහායකයා:
""".strip()


def ollama_generate(model_name, prompt, system_prompt, stream=False, response_mode="simple"):
    num_predict = 180 if response_mode == "detailed" else 90

    payload = {
        "model": model_name,
        "prompt": prompt,
        "system": system_prompt,
        "stream": stream,
        "options": {
            "temperature": 0.2,
            "top_p": 0.8,
            "repeat_penalty": 1.18,
            "num_predict": num_predict
        }
    }

    return requests.post(
        OLLAMA_GENERATE_URL,
        json=payload,
        stream=stream,
        timeout=180
    )


def rewrite_to_clean_sinhala(model_name, raw_text):
    rewrite_prompt = f"{REWRITE_PROMPT}\n{raw_text}"

    try:
        response = ollama_generate(
            model_name=model_name,
            prompt=rewrite_prompt,
            system_prompt=MAIN_SYSTEM_PROMPT,
            stream=False,
            response_mode="simple"
        )
        response.raise_for_status()
        data = response.json()
        rewritten = data.get("response", "").strip()
        return rewritten if rewritten else raw_text
    except requests.RequestException:
        return raw_text


def generate_response(
    model_name,
    user_input,
    chat_history,
    history_limit=5,
    auto_rewrite=True,
    response_mode="simple"
):
    prompt = build_prompt(
        user_input=user_input,
        chat_history=chat_history,
        history_limit=history_limit,
        response_mode=response_mode
    )
    start_time = time.time()

    try:
        response = ollama_generate(
            model_name=model_name,
            prompt=prompt,
            system_prompt=MAIN_SYSTEM_PROMPT,
            stream=False,
            response_mode=response_mode
        )
        response.raise_for_status()
        data = response.json()
        reply = data.get("response", "").strip()

        if not reply:
            reply = "කණගාටුයි, පිළිතුරක් ලබා දීමට නොහැකි විය."

        if auto_rewrite and is_low_quality_sinhala(reply):
            reply = rewrite_to_clean_sinhala(model_name, reply)

        elapsed = time.time() - start_time
        return reply, elapsed, None

    except requests.RequestException as e:
        elapsed = time.time() - start_time
        return None, elapsed, f"Ollama connection error: {str(e)}"


def stream_response_chunks(
    model_name,
    user_input,
    chat_history,
    history_limit=5,
    auto_rewrite=True,
    response_mode="simple"
):
    prompt = build_prompt(
        user_input=user_input,
        chat_history=chat_history,
        history_limit=history_limit,
        response_mode=response_mode
    )
    start_time = time.time()

    try:
        response = ollama_generate(
            model_name=model_name,
            prompt=prompt,
            system_prompt=MAIN_SYSTEM_PROMPT,
            stream=True,
            response_mode=response_mode
        )
        response.raise_for_status()

        full_text = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                chunk = data.get("response", "")
                full_text += chunk
                yield chunk, None, None

        if auto_rewrite and is_low_quality_sinhala(full_text):
            full_text = rewrite_to_clean_sinhala(model_name, full_text)

        elapsed = time.time() - start_time
        yield None, elapsed, full_text.strip()

    except requests.RequestException as e:
        elapsed = time.time() - start_time
        yield None, elapsed, f"Ollama connection error: {str(e)}"