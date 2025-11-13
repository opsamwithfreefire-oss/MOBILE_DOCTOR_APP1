import streamlit as st
import streamlit_authenticator as stauth
import datetime
import time
from streamlit_chat import message
from streamlit_option_menu import option_menu

# Mock user database (in production, use a secure DB)
users = {
    "user1": {"email": "user@example.com", "phone": "123-456-7890", "password": stauth.Hasher(['password']).generate()[0]},
    "user2": {"email": "user2@example.com", "phone": "987-654-3210", "password": stauth.Hasher(['password2']).generate()[0]}
}

# Mock AI diagnosis logic (simple rule-based; replace with real ML model)
def diagnose(symptoms):
    if "fever" in symptoms and "cough" in symptoms:
        return "Common Cold", ["Rest", "Drink fluids", "Take acetaminophen"], {"Medicine": "Acetaminophen", "Dosage": "500mg", "Frequency": "Every 4-6 hours", "Duration": "5 days"}
    elif "headache" in symptoms and "nausea" in symptoms:
        return "Migraine", ["Avoid triggers", "Apply cold compress"], {"Medicine": "Ibuprofen", "Dosage": "200mg", "Frequency": "Every 6 hours", "Duration": "As needed"}
    else:
        return "General Fatigue", ["Rest", "Hydrate"], {"Medicine": "Multivitamin", "Dosage": "1 tablet", "Frequency": "Daily", "Duration": "Ongoing"}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'symptoms' not in st.session_state:
    st.session_state.symptoms = []
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = None
if 'last_visit' not in st.session_state:
    st.session_state.last_visit = datetime.datetime.now()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Authenticator for login
authenticator = stauth.Authenticate(
    users,
    "mobile_doctor", "auth", cookie_expiry_days=30
)

# Main App
def main():
    st.set_page_config(page_title="Mobile Doctor", page_icon="🩺", layout="wide")
    
    # Check for follow-up (after 2+ days)
    if (datetime.datetime.now() - st.session_state.last_visit).days >= 2:
        st.warning("Welcome back! How are you feeling? Have your symptoms improved?")
        if st.button("Yes, I'm better"):
            st.success("Great! Stay healthy.")
        elif st.button("No, still unwell"):
            st.info("Please consult a doctor or re-enter symptoms.")
    
    # Sidebar Navigation
    with st.sidebar:
        selected = option_menu(
            "Mobile Doctor",
            ["Login", "Home", "AI Diagnosis", "Results", "Remedies", "Notifications"],
            icons=["🔐", "🏠", "🤖", "📊", "💊", "🔔"],
            menu_icon="🩺",
            default_index=0,
        )
    
    if selected == "Login":
        login_page()
    elif selected == "Home":
        home_page()
    elif selected == "AI Diagnosis":
        ai_diagnosis_page()
    elif selected == "Results":
        results_page()
    elif selected == "Remedies":
        remedies_page()
    elif selected == "Notifications":
        notifications_page()

def login_page():
    st.title("🔐 Login to Mobile Doctor")
    st.markdown("Secure access with Google, Email, or Phone.")
    
    # Google OAuth (requires setup: https://docs.streamlit.io/library/components/components-api)
    if st.button("Login with Google"):
        st.info("Google login simulated. In production, integrate OAuth.")
        st.session_state.logged_in = True
        st.session_state.user = "Google User"
        st.rerun()
    
    # Email/Phone Login
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status:
        st.session_state.logged_in = True
        st.session_state.user = username
        st.success(f"Welcome, {username}!")
        st.rerun()
    elif authentication_status == False:
        st.error("Invalid credentials.")
    elif authentication_status == None:
        st.warning("Please enter credentials.")

def home_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("🏠 Welcome to Mobile Doctor")
    st.markdown("Your AI-powered health assistant. Get diagnoses, remedies, and reminders.")
    st.image("https://via.placeholder.com/800x400?text=Health+Dashboard", use_column_width=True)  # Placeholder image
    st.session_state.last_visit = datetime.datetime.now()

def ai_diagnosis_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("🤖 AI Diagnosis Assistant")
    st.markdown("Chat with our AI to describe your symptoms.")
    
    # Chatbox
    user_input = st.text_input("Enter a symptom or describe your issue:", key="symptom_input")
    if st.button("Add Symptom"):
        if user_input:
            st.session_state.symptoms.append(user_input.lower())
            st.session_state.chat_history.append({"user": user_input, "bot": "Symptom noted. Any more?"})
            st.rerun()
    
    # Display chat history
    for chat in st.session_state.chat_history:
        message(chat["user"], is_user=True)
        message(chat["bot"])
    
    if st.button("Get Diagnosis"):
        if st.session_state.symptoms:
            disease, remedies, medicine = diagnose(st.session_state.symptoms)
            st.session_state.diagnosis = {"disease": disease, "remedies": remedies, "medicine": medicine}
            st.success("Diagnosis complete! Check Results.")
        else:
            st.error("Please enter symptoms first.")

def results_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("📊 Diagnosis Results")
    if st.session_state.diagnosis:
        st.subheader(f"Disease: {st.session_state.diagnosis['disease']}")
        st.markdown("**Remedies:**")
        for remedy in st.session_state.diagnosis['remedies']:
            st.write(f"- {remedy}")
    else:
        st.info("No diagnosis yet. Go to AI Diagnosis.")

def remedies_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("💊 Remedies & Medicine")
    if st.session_state.diagnosis:
        med = st.session_state.diagnosis['medicine']
        st.subheader("Medicine Details:")
        st.write(f"**Name:** {med['Medicine']}")
        st.write(f"**Dosage:** {med['Dosage']}")
        st.write(f"**Frequency:** {med['Frequency']}")
        st.write(f"**Duration:** {med['Duration']}")
        st.markdown("**Step-by-Step Cure:**")
        for i, remedy in enumerate(st.session_state.diagnosis['remedies'], 1):
            st.write(f"{i}. {remedy}")
    else:
        st.info("No remedies yet. Complete diagnosis first.")

def notifications_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("🔔 Notifications & Reminders")
    if st.session_state.diagnosis:
        med = st.session_state.diagnosis['medicine']
        st.info(f"Reminder: Take {med['Medicine']} ({med['Dosage']}) {med['Frequency']}.")
        # Simulate notification (in production, use scheduling libraries)
        if st.button("Set Reminder"):
            st.success("Reminder set! (Simulated - check back for alerts.)")
    else:
        st.info("No notifications. Complete diagnosis first.")

if __name__ == "__main__":
    main()
