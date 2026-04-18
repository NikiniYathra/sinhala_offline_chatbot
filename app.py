import html
import streamlit as st
from chatbot import (
    check_ollama_status,
    get_installed_models,
    generate_response,
    stream_response_chunks
)
from utils import export_chat_text, format_seconds
from ui import (
    inject_css,
    model_display_name,
    render_header,
    render_metric_card,
    render_chat_bubble
)

st.set_page_config(
    page_title="සිංහල Offline Chatbot",
    page_icon="💬",
    layout="wide"
)

inject_css()


# =========================================================
# Session State
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Tharusha_Dilhara_Jayadeera/singemma"

if "comparison_model" not in st.session_state:
    st.session_state.comparison_model = "llama3:latest"

if "streaming_mode" not in st.session_state:
    st.session_state.streaming_mode = True

if "history_limit" not in st.session_state:
    st.session_state.history_limit = 5

if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = None

if "auto_rewrite" not in st.session_state:
    st.session_state.auto_rewrite = True

if "response_mode" not in st.session_state:
    st.session_state.response_mode = "simple"

# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ සැකසුම්</div>', unsafe_allow_html=True)

    ollama_ok = check_ollama_status()
    if ollama_ok:
        st.success("OLLAMA ක්‍රියාත්මක වේ")
    else:
        st.error("OLLAMA ක්‍රියාත්මක නොවේ")

    installed_models = get_installed_models()

    preferred_models = [
        "Tharusha_Dilhara_Jayadeera/singemma",
        "Tharusha_Dilhara_Jayadeera/singemma:latest",
        "llama3:latest",
        "gemma3:4b"
    ]

    available_choices = []
    for model in preferred_models:
        if model in installed_models and model not in available_choices:
            available_choices.append(model)

    for model in installed_models:
        if model not in available_choices:
            available_choices.append(model)

    if not available_choices:
        available_choices = preferred_models

    primary_index = 0
    if st.session_state.selected_model in available_choices:
        primary_index = available_choices.index(st.session_state.selected_model)

    st.session_state.selected_model = st.selectbox(
        "Default Model",
        options=available_choices,
        index=primary_index,
        format_func=model_display_name
    )

    comparison_choices = [m for m in available_choices if m != st.session_state.selected_model]
    if not comparison_choices:
        comparison_choices = available_choices

    comp_index = 0
    if st.session_state.comparison_model in comparison_choices:
        comp_index = comparison_choices.index(st.session_state.comparison_model)

    st.session_state.comparison_model = st.selectbox(
        "Comparison Model",
        options=comparison_choices,
        index=comp_index,
        format_func=model_display_name
    )

    st.session_state.response_mode = st.radio(
        "Response Mode",
        options=["simple", "detailed"],
        format_func=lambda x: "Simple Mode" if x == "simple" else "Detailed Mode"
    )

    st.session_state.streaming_mode = st.toggle(
        "Streaming Response",
        value=st.session_state.streaming_mode
    )

    st.session_state.auto_rewrite = st.toggle(
        "Auto Rewrite Sinhala",
        value=st.session_state.auto_rewrite,
        help="Mixed output එක පිරිසිදු සිංහලට නැවත ලියයි."
    )

    st.session_state.history_limit = st.slider(
        "History Memory Size",
        min_value=2,
        max_value=12,
        value=st.session_state.history_limit
    )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    if st.button("🗑️ Chat ඉතිහාසය මකන්න", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_response_time = None
        st.rerun()

    export_text = export_chat_text(
        st.session_state.messages,
        model_display_name(st.session_state.selected_model)
    )

    st.download_button(
        "📥 Chat Export කරන්න",
        data=export_text,
        file_name="sinhala_chat_export.txt",
        mime="text/plain",
        use_container_width=True,
        key="sidebar_export_btn"
    )

render_header()

# =========================================================
# Top metrics
# =========================================================
m1, m2, m3 = st.columns(3)

with m1:
    render_metric_card("Primary Model", model_display_name(st.session_state.selected_model))

with m2:
    mode_text = "Simple" if st.session_state.response_mode == "simple" else "Detailed"
    render_metric_card("Response Mode", mode_text)

with m3:
    time_text = "-"
    if st.session_state.last_response_time is not None:
        time_text = format_seconds(st.session_state.last_response_time)
    render_metric_card("Last Response Time", time_text)

# =========================================================
# Tabs
# =========================================================
tab_chat, tab_compare, tab_test = st.tabs(["💬 Chat", "⚖️ Model Comparison", "🧪 Testing Panel"])

# =========================================================
# Chat Tab
# =========================================================
with tab_chat:
    left_col, right_col = st.columns([3.2, 1.2], gap="large")

    with left_col:
        st.markdown('<div class="chat-shell"></div>', unsafe_allow_html=True)

        for msg in st.session_state.messages:
            render_chat_bubble(msg["role"], msg["content"])

        user_input = st.chat_input("ඔබගේ පණිවිඩය මෙහි ලියන්න...", key="main_chat_input")

    with right_col:
        st.markdown('<div class="quick-panel">', unsafe_allow_html=True)
        st.markdown('<div class="quick-panel-title">⚡ ඉක්මන් උදාහරණ</div>', unsafe_allow_html=True)

        samples = [
            "NLP කියන්නේ මොකක්ද?",
            "මට අද පාඩම් සැලැස්මක් දෙන්න.",
            "Explain machine learning",
            "ශ්‍රී ලංකාව ගැන කෙටි විස්තරයක් දෙන්න."
        ]

        selected_sample = None
        for i, prompt in enumerate(samples):
            if st.button(prompt, key=f"chat_sample_{i}", use_container_width=True):
                selected_sample = prompt

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
        st.download_button(
            "📥 Chat Export කරන්න",
            data=export_chat_text(
                st.session_state.messages,
                model_display_name(st.session_state.selected_model)
            ),
            file_name="sinhala_chat_export.txt",
            mime="text/plain",
            use_container_width=True,
            key="chat_tab_export_btn"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if selected_sample:
        user_input = selected_sample

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with left_col:
            render_chat_bubble("user", user_input)

            if st.session_state.streaming_mode:
                bubble_placeholder = st.empty()
                full_reply = ""

                for chunk, elapsed, final_data in stream_response_chunks(
                    model_name=st.session_state.selected_model,
                    user_input=user_input,
                    chat_history=st.session_state.messages[:-1],
                    history_limit=st.session_state.history_limit,
                    auto_rewrite=st.session_state.auto_rewrite,
                    response_mode=st.session_state.response_mode
                ):
                    if chunk is not None:
                        full_reply += chunk
                        safe_stream = html.escape(full_reply).replace("\n", "<br>")

                        bubble_placeholder.markdown(
                            f"""
                            <div class="chat-row assistant">
                                <div class="chat-bubble assistant">
                                    <div class="chat-meta">
                                        <span class="chat-avatar assistant">🤖</span>
                                        <span>සහායකයා</span>
                                    </div>
                                    <div class="chat-content">{safe_stream}▌</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        if isinstance(final_data, str) and final_data.startswith("Ollama connection error:"):
                            full_reply = "කණගාටුයි, OLLAMA සේවාවට සම්බන්ධ වීමට නොහැකි විය."
                        elif final_data:
                            full_reply = final_data
                        else:
                            full_reply = "කණගාටුයි, පිළිතුරක් ලබා දීමට නොහැකි විය."

                        st.session_state.last_response_time = elapsed
                        safe_stream = html.escape(full_reply).replace("\n", "<br>")
                        
                        bubble_placeholder.markdown(
                            f"""
                            <div class="chat-row assistant">
                                <div class="chat-bubble assistant">
                                    <div class="chat-meta">
                                        <span class="chat-avatar assistant">🤖</span>
                                        <span>සහායකයා</span>
                                    </div>
                                    <div class="chat-content">{safe_stream}</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                reply, elapsed, error = generate_response(
                    model_name=st.session_state.selected_model,
                    user_input=user_input,
                    chat_history=st.session_state.messages[:-1],
                    history_limit=st.session_state.history_limit,
                    auto_rewrite=st.session_state.auto_rewrite,
                    response_mode=st.session_state.response_mode
                )

                st.session_state.last_response_time = elapsed

                if error:
                    full_reply = "කණගාටුයි, OLLAMA සේවාවට සම්බන්ධ වීමට නොහැකි විය."
                else:
                    full_reply = reply

                render_chat_bubble("assistant", full_reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_reply
        })

# =========================================================
# Model Comparison Tab
# =========================================================
with tab_compare:
    st.markdown("### එකම ප්‍රශ්නයට models දෙකක පිළිතුරු සසඳන්න")

    compare_prompt = st.text_area(
        "Comparison Prompt",
        value="NLP කියන්නේ මොකක්ද?",
        height=120
    )

    if st.button("🔍 Compare Models", use_container_width=True):
        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.markdown(f"#### {model_display_name(st.session_state.selected_model)}")
            with st.spinner("Generating..."):
                reply1, time1, error1 = generate_response(
                    model_name=st.session_state.selected_model,
                    user_input=compare_prompt,
                    chat_history=[],
                    history_limit=st.session_state.history_limit,
                    auto_rewrite=st.session_state.auto_rewrite,
                    response_mode=st.session_state.response_mode
                )

                if error1:
                    st.error("පිළිතුර ලබා ගත නොහැකි විය.")
                else:
                    render_chat_bubble("assistant", reply1)
                    st.caption(f"Response Time: {format_seconds(time1)}")

        with c2:
            st.markdown(f"#### {model_display_name(st.session_state.comparison_model)}")
            with st.spinner("Generating..."):
                reply2, time2, error2 = generate_response(
                    model_name=st.session_state.comparison_model,
                    user_input=compare_prompt,
                    chat_history=[],
                    history_limit=st.session_state.history_limit,
                    auto_rewrite=st.session_state.auto_rewrite,
                    response_mode=st.session_state.response_mode
                )

                if error2:
                    st.error("පිළිතුර ලබා ගත නොහැකි විය.")
                else:
                    render_chat_bubble("assistant", reply2)
                    st.caption(f"Response Time: {format_seconds(time2)}")

# =========================================================
# Testing Panel
# =========================================================
with tab_test:
    st.markdown("### Sinhala Test Prompt Panel")
    st.markdown('<div class="small-note">මෙය screenshots සහ evaluation සඳහා භාවිතා කළ හැක.</div>', unsafe_allow_html=True)

    test_prompts = [
        "ඔබේ නම කුමක්ද?",
        "NLP කියන්නේ මොකක්ද?",
        "ශ්‍රී ලංකාව ගැන කෙටි විස්තරයක් දෙන්න.",
        "මට අද පාඩම් සැලැස්මක් දෙන්න.",
        "පරිසරය ආරක්ෂා කිරීම වැදගත් ඇයි?",
        "Explain machine learning",
        "Python භාෂාව ගැන කෙටි විස්තරයක් දෙන්න.",
        "Streamlit යනු කුමක්ද?",
        "Offline chatbot එකක වාසිය කුමක්ද?",
        "මට උදේට කළ හැකි සෞඛ්‍ය පුරුදු 3ක් කියන්න."
    ]

    selected_test = st.selectbox(
        "Test Prompt තෝරන්න",
        test_prompts
    )

    if st.button("▶ Run Selected Test", use_container_width=True):
        with st.spinner("Running selected test..."):
            reply, elapsed, error = generate_response(
                model_name=st.session_state.selected_model,
                user_input=selected_test,
                chat_history=[],
                history_limit=st.session_state.history_limit,
                auto_rewrite=st.session_state.auto_rewrite,
                response_mode=st.session_state.response_mode
            )

            if error:
                st.error("Test run එක අසාර්ථක විය.")
            else:
                st.markdown("#### Prompt")
                st.code(selected_test)

                st.markdown("#### Response")
                render_chat_bubble("assistant", reply)

                st.caption(f"Response Time: {format_seconds(elapsed)}")

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Quick Multi-Test Preview")

    if st.button("⚡ Run First 3 Tests", use_container_width=True):
        for i, prompt in enumerate(test_prompts[:3], start=1):
            st.markdown(f"#### Test {i}")
            st.markdown(f"**Prompt:** {prompt}")

            with st.spinner(f"Running test {i}..."):
                reply, elapsed, error = generate_response(
                    model_name=st.session_state.selected_model,
                    user_input=prompt,
                    chat_history=[],
                    history_limit=st.session_state.history_limit,
                    auto_rewrite=st.session_state.auto_rewrite,
                    response_mode=st.session_state.response_mode
                )

                if error:
                    st.error("පිළිතුර ලබා ගත නොහැකි විය.")
                else:
                    render_chat_bubble("assistant", reply)
                    st.caption(f"Response Time: {format_seconds(elapsed)}")

            st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)