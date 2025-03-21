import streamlit as st
import requests
import plotly.express as px
import time  

# API endpoint
API_URL = "https://analyzer-tts.onrender.com"

# Set page configurations
st.set_page_config(
    page_title="News Sentiment Analyzer",
    page_icon="📰",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Sentiment Analysis", "Settings"])

# Dark mode toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown("<style>body { background-color: #1E1E1E; color: white; }</style>", unsafe_allow_html=True)

# Home Page - Fetch and display news
if page == "Home":
    st.title("📰 AI-Powered News Sentiment Analyzer")
    st.write("Analyze the latest news, extract key topics, and convert summaries to Hindi speech!")

    # User input for company name
    company_name = st.text_input("🔍 Enter a Company Name:")
    
    col1, col2 = st.columns([1, 1])
    start_date = col1.date_input("📅 Start Date")
    end_date = col2.date_input("📅 End Date")

    if st.button("Fetch News"):
        if company_name:
            query_url = f"{API_URL}/fetch_news_data?company={company_name}"

            if start_date:
                query_url += f"&start_date={start_date.strftime('%Y-%m-%d')}"
            if end_date:
                query_url += f"&end_date={end_date.strftime('%Y-%m-%d')}"

            response = requests.get(query_url)

            if response.status_code == 200:
                st.session_state.news_data = response.json()
                st.session_state.audio_files = {}  # Reset audio files
            else:
                st.warning("⚠️ No articles found.")

    # Display news articles
    if "news_data" in st.session_state:
        st.subheader(f"📢 Fetched News Articles for {st.session_state.news_data['company']}")

        for i, article in enumerate(st.session_state.news_data["articles"]):
            with st.expander(f"📌 {article['title']}"):
                st.write(f"🔹 **Sentiment:** {article['sentiment']}")
                st.write(f"🔗 [Read More]({article['link']})")
                st.write(f"📅 Published Date: {article['publishedAt']}")
                st.write(f"📰 Source: **{article['source']}**")
                st.write(f"📌 **Keywords:** {', '.join(article['keywords'])}")

                # Generate Unique Key for Each Button
                unique_key = f"tts_{i}"

                # Button for generating text-to-speech
                if st.button(f"🎙️ Convert to Hindi {i+1}", key=unique_key):
                    with st.spinner("Generating Hindi audio... 🎧"):
                        tts_response = requests.post(f"{API_URL}/text_2_speech", json={"text": article["title"]})

                        if tts_response.status_code == 200:
                            audio_data = tts_response.json()

                            if "audio_file" in audio_data:
                                audio_file_url = f"{API_URL}{audio_data['audio_file']}"  # Fix missing "/"
                                st.session_state.audio_files[unique_key] = audio_file_url  # Store file path
                                st.success("✅ Audio generated successfully!")
                            else:
                                st.error("⚠️ Audio file not found in response.")

                        else:
                            st.error("❌ Failed to generate audio. Try again later.")

                # Play the generated audio if it exists
                if unique_key in st.session_state.audio_files:
                    st.audio(st.session_state.audio_files[unique_key])

# Sentiment Analysis Page - Display sentiment distribution chart
elif page == "Sentiment Analysis":
    st.title("📊 Sentiment Analysis")

    if "news_data" in st.session_state:
        sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for article in st.session_state.news_data["articles"]:
            sentiments[article["sentiment"]] += 1

        fig = px.pie(
            names=list(sentiments.keys()), 
            values=list(sentiments.values()), 
            title="Sentiment Distribution of Articles", 
            color_discrete_map={"Positive": "#2E8B57", "Negative": "#FF4500", "Neutral": "#FFD700"}
        )
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No data available. Please fetch news first.")

# Settings Page
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("🔧 No settings available yet. More features coming soon! 🚀")
