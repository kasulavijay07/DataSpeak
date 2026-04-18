import html
import time

import streamlit as st
import speech_recognition as sr
import streamlit.components.v1 as components

from langchain_helper import format_database_result, get_few_shot_db_chain
from visualization_helper import format_with_chart


st.set_page_config(
    page_title="DataSpeak - Natural Language Database Analytics",
    page_icon="DS",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-repo",
        "Report a bug": "https://github.com/your-repo/issues",
        "About": "# DataSpeak - Clean, conversational analytics for your database.",
    },
)

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

st.title("DataSpeak")
st.caption("Ask plain-language questions and get clean, visual answers from your t-shirt database in seconds.")

with st.sidebar:
    st.markdown("## DataSpeak")
    st.markdown(
        """
A clean analytics assistant for retail database insights.

- Natural language questions
- Voice-to-text capture
- Auto-generated charts
- No SQL required
"""
    )
    st.markdown("## Data Focus")
    st.markdown(
        """
- Inventory checks
- Sales overview
- Discount impact
- Brand and size comparisons
"""
    )
    st.markdown("## Voice Support")
    st.markdown(
        """
Best on Chrome, Edge, and Safari.

Tip: speak a short, clear question. The text will be automatically captured.
"""
    )

with st.container():
    input_col, btn_col = st.columns([4, 1])
    with input_col:
        question = st.text_input(
            "Ask a question",
            placeholder="Example: Which brand has the highest stock right now?",
            value=st.session_state.selected_question,
            key="question_input",
            label_visibility="collapsed",
        )
    with btn_col:
        ask_pressed = st.button("Ask", use_container_width=True, type="primary")

    with st.expander("🎙️ Voice capture", expanded=False):
        try:
            host = st.context.headers.get("Host", "")
            proto = st.context.headers.get("X-Forwarded-Proto", "")
            is_secure = "localhost" in host or "127.0.0.1" in host or proto == "https"
            if not is_secure:
                st.error("⚠️ Voice capture requires HTTPS or localhost.")
        except Exception:
            pass

        audio = st.experimental_audio_input("Record your question", key="audio_recorder", label_visibility="collapsed")

        if audio is not None:
            if "last_processed_audio" not in st.session_state or st.session_state.last_processed_audio != audio:
                st.session_state.last_processed_audio = audio
                with st.spinner("Transcribing..."):
                    try:
                        r = sr.Recognizer()
                        with sr.AudioFile(audio) as source:
                            audio_data = r.record(source)
                            text = r.recognize_google(audio_data)
                            if text:
                                st.session_state.selected_question = text
                                st.rerun()
                    except sr.UnknownValueError:
                        st.error("Could not understand audio")
                    except sr.RequestError as e:
                        st.error(f"Could not request results; {e}")
                    except Exception as e:
                        st.error(f"Error processing audio: {e}")

st.write("### Try one of these")
examples = [
    "How many Nike t-shirts do we have in stock?",
    "What is the average price of white t-shirts?",
    "Which brand has the most t-shirts available?",
    "What total revenue comes from all S-size t-shirts?",
    "Show stock distribution by color.",
]

example_cols = st.columns(5)
for i, example in enumerate(examples):
    with example_cols[i % 5]:
        if st.button(example, key=f"example_{i}", use_container_width=True):
            st.session_state.selected_question = example
            st.rerun()

st.divider()

if ask_pressed or (question and question != ""):
    with st.spinner("Running your database analysis..."):
        try:
            chain = get_few_shot_db_chain()
            raw_result = chain.run(question)

            formatted_response = format_database_result(raw_result, question)
            vis_result = format_with_chart(question, raw_result)

            has_chart = bool(vis_result and vis_result.get("chart") is not None)
            has_table = bool(vis_result and vis_result.get("table_data") is not None)
            is_single_value = bool(vis_result and vis_result.get("metadata", {}).get("is_single_value"))
            chart_type = vis_result.get("chart_type", "") if vis_result else ""

            answer_tab, chart_tab, table_tab, debug_tab = st.tabs(["💬 Answer", "📈 Chart", "📊 Table", "🛠️ Debug"])

            with answer_tab:
                st.markdown(f"**Question:** {question}")
                st.info(formatted_response)

                if is_single_value:
                    value = vis_result["metadata"].get("value", "N/A")
                    if isinstance(value, (int, float)):
                        if value >= 1000:
                            value_str = f"{value:,.0f}"
                        elif isinstance(value, float):
                            value_str = f"{value:,.2f}"
                        else:
                            value_str = f"{value:,}"
                    else:
                        value_str = str(value)

                    st.metric(label="Computed result", value=value_str)

            with chart_tab:
                if has_chart:
                    try:
                        chart_fig = vis_result["chart"]
                        st.plotly_chart(
                            chart_fig,
                            use_container_width=True,
                            config={
                                "displayModeBar": True,
                                "displaylogo": False,
                                "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                            },
                        )
                    except Exception as viz_error:
                        st.error(f"Unable to render chart: {viz_error}")
                        if vis_result.get("error"):
                            st.warning(f"Visualization details: {vis_result.get('error')}")
                elif not has_chart and not has_table and not is_single_value:
                    st.info("No visualization available for this query.")
                else:
                    st.info("Chart not applicable for this result.")

            with table_tab:
                if has_table:
                    table_df = vis_result["table_data"]
                    if table_df is not None and not table_df.empty:
                        try:
                            st.dataframe(
                                table_df,
                                use_container_width=True,
                                hide_index=False,
                            )
                        except Exception as table_error:
                            st.error(f"Unable to render table: {table_error}")
                            st.write(table_df)
                else:
                    st.info("Table data not applicable for this result.")

            with debug_tab:
                st.markdown("**Raw Database Output**")
                st.code(str(raw_result))
                st.markdown("**Visualization Info**")
                st.code(
                    f"Type: {vis_result.get('chart_type', 'N/A') if vis_result else 'N/A'}\n"
                    f"Created: {vis_result.get('chart') is not None if vis_result else False}\n"
                    f"Error: {vis_result.get('error', '') if vis_result else ''}"
                )

            st.session_state.selected_question = ""

        except Exception as e:
            error_msg = str(e)
            st.error(f"Error processing your request: {error_msg}")

            if "sql syntax" in error_msg.lower() or "syntax" in error_msg.lower():
                st.info("Tip: simplify or rephrase the question to avoid ambiguous SQL generation.")
            elif "connection" in error_msg.lower() or "database" in error_msg.lower():
                st.info("Tip: verify database credentials and confirm the database service is running.")
            elif "column" in error_msg.lower() or "table" in error_msg.lower():
                st.info("Tip: your question may reference unavailable fields; try a broader query.")
            else:
                st.info("Tip: try a shorter query and retry.")
