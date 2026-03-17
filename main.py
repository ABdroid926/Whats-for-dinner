import streamlit as st
import os
import time 

from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
st.set_page_config(page_title="Whats For Dinner", page_icon="🥪")
st.title('Whats For Dinner 🥪 || Recipe Recommender ')


with st.sidebar:
    st.header("Settings")
    if st.button('Clear App Cache'):
      
        st.cache_data.clear()
      
        if 'last_recipe' in st.session_state:
            del st.session_state['last_recipe']
        st.success("Cache Cleared! Ready for a fresh start.")


@st.cache_data(show_spinner=False)
def generate_recommendations(input_text):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7
        )
        prompt = f"Given the ingredients: {input_text}, suggest five easy-to-cook step-by-step recipes."
        response = llm.invoke(prompt)
        return response.content
    
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
        
            placeholder = st.empty()
            for seconds_left in range(60, 0, -1):
                placeholder.error(f"⏳ Quota limit reached. Please wait {seconds_left}s before retrying...")
                time.sleep(1)
            placeholder.success("🔄 You can try again now!")
            return None
        else:
            st.error(f"An error occurred: {error_msg}")
            return None

with st.form('my_form'):
    user_input = st.text_area('Enter your preferred ingredients (separated by commas):')
    submitted = st.form_submit_button('Get Recipe Recommendations')

if submitted:
    if not user_input.strip():
        st.warning("Please enter some ingredients first!")
    else:
        with st.spinner('Tasty Food Is A Moment Away...'):
            recipe = generate_recommendations(user_input)
            st.session_state['last_recipe'] = recipe


if 'last_recipe' in st.session_state:
    st.markdown("---")
    st.markdown("### 📝 Your Custom Recipe")
    st.write(st.session_state['last_recipe'])
