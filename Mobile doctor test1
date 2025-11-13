import streamlit as st
import datetime

# Mock AI diagnosis logic (simple rule-based; replace with real ML model for production)
def diagnose(symptoms):
    symptoms_lower = [s.lower() for s in symptoms]
    if "fever" in symptoms_lower and "cough" in symptoms_lower:
        return "Common Cold", ["Rest in bed", "Drink plenty of fluids", "Take over-the-counter pain relievers"], {"Medicine": "Acetaminophen", "Dosage": "500mg", "Frequency": "Every 4-6 hours as needed", "Duration": "5 days or until symptoms improve"}
    elif "headache" in symptoms_lower and "nausea" in symptoms_lower:
        return "Migraine", ["Lie down in a dark room", "Apply a cold compress to your forehead", "Avoid bright lights and loud noises"], {"Medicine": "Ibuprofen", "Dosage": "200mg", "Frequency": "Every 6 hours as needed", "Duration": "Until headache subsides"}
    else:
        return "General Fatigue", ["Get adequate sleep", "Stay hydrated", "Eat balanced meals"], {"Medicine": "Multivitamin", "Dosage": "1 tablet", "Frequency": "Once daily", "Duration": "Ongoing as needed"}

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

# Main App
def main():
    st.set_page_config(page_title="Mobile Doctor", page_icon="🩺", layout="wide")
    
    # Check for follow-up (after 2+ days)
    if st.session_state.logged_in and (datetime.datetime.now() - st.session_state.last_visit).days >= 2:
        st.warning("Welcome back! How are you feeling? Have your symptoms improved?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, I'm better"):
                st.success("Great! Stay healthy.")
        with col2:
            if st.button("No, still unwell"):
                st.info("Please consult a doctor or re-enter symptoms in AI Diagnosis.")
    
    # Sidebar Navigation (using built-in Streamlit)
    with st.sidebar:
        st.title("🩺 Mobile Doctor")
        selected = st.radio(
            "Navigate:",
            ["Login", "Home", "AI Diagnosis", "Results", "Remedies", "Notifications"],
            index=0 if not st.session_state.logged_in else 1
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
    st.markdown("Enter your details to access the app.")
    
    # Simple login form (built-in, no external library)
    email = st.text_input("Email or Phone Number")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:  # Mock validation (in production, check against a DB)
            st.session_state.logged_in = True
            st.session_state.user = email
            st.success(f"Welcome, {email}!")
            st.rerun()
        else:
            st.error("Please enter valid credentials.")
    
    st.markdown("---")
    st.info("For Google login, integrate OAuth in production (e.g., via Firebase). This is a simulated login.")

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
    st.markdown("Describe your symptoms step-by-step. Our AI will analyze them.")
    
    # Simple chatbox (built-in, no external library)
    user_input = st.text_input("Enter a symptom (e.g., 'fever' or 'I have a headache'):", key="symptom_input")
    if st.button("Add Symptom"):
        if user_input:
            st.session_state.symptoms.append(user_input)
            st.session_state.chat_history.append(f"You: {user_input}")
            st.session_state.chat_history.append("AI: Symptom noted. Any more symptoms? (e.g., cough, nausea)")
            st.rerun()
    
    # Display chat history
    st.subheader("Chat History:")
    for msg in st.session_state.chat_history:
        st.write(msg)
    
    if st.button("Get Diagnosis"):
        if st.session_state.symptoms:
            disease, remedies, medicine = diagnose(st.session_state.symptoms)
            st.session_state.diagnosis = {"disease": disease, "remedies": remedies, "medicine": medicine}
            st.success("Diagnosis complete! Check the Results page.")
        else:
            st.error("Please enter at least one symptom first.")

def results_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("📊 Diagnosis Results")
    if st.session_state.diagnosis:
        st.subheader(f"Diagnosed Disease: {st.session_state.diagnosis['disease']}")
        st.markdown("**Based on symptoms:** " + ", ".join(st.session_state.symptoms))
    else:
        st.info("No diagnosis yet. Go to AI Diagnosis to get started.")

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
        st.markdown("**Step-by-Step Remedies/Cure:**")
        for i, remedy in enumerate(st.session_state.diagnosis['remedies'], 1):
            st.write(f"{i}. {remedy}")
    else:
        st.info("No remedies yet. Complete a diagnosis first.")

def notifications_page():
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
    st.title("🔔 Notifications & Reminders")
    if st.session_state.diagnosis:
        med = st.session_state.diagnosis['medicine']
        st.info(f"Reminder: Take {med['Medicine']} ({med['Dosage']}) {med['Frequency']} for {med['Duration']}.")
        # Simulate notification (in production, integrate with scheduling/push libraries)
        if st.button("Set Reminder"):
            st.success("Reminder set! (Simulated - in a real app, this would send alerts at set times.)")
    else:
        st.info("No notifications. Complete a diagnosis first.")

if __name__ == "__main__":
    main()
