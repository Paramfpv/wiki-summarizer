import wikipedia
import streamlit as st

def summarize_wiki(page_title, num_sentences=3):
    """Fetches a Wikipedia summary, handles potential errors,
    and returns a truncated version with an option to expand."""

    try:
        page = wikipedia.page(page_title)
        summary = page.summary
    except wikipedia.DisambiguationError as e:
        st.error(f"Disambiguation required: {e}")
        options = [link.title for link in e.options]
        option = st.selectbox("Choose the appropriate page:", options)
        return summarize_wiki(option, num_sentences)  # Recursive call
    except wikipedia.PageError as e:
        st.error(f"Page not found: {e}")
        return None

    # Truncate the summary to a user-specified number of sentences
    sentences = summary.split(". ")
    truncated_summary = ". ".join(sentences[:num_sentences]) + "..."

    # Offer option to see the full summary
    expand_button = st.button("See Full Summary")
    if expand_button:
        st.write(summary)

    return truncated_summary

st.title("Wiki Summarizer")

page_title = st.text_input("Enter the name of the Wikipedia page:", key="page_title")

if page_title:
    summary = summarize_wiki(page_title)

    if summary:
        st.subheader("Summary:")
        st.write(summary)
        st.write("**Note:** This is a truncated summary. Click 'See Full Summary' for more details.")
