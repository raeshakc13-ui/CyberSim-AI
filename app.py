import streamlit as st
from dotenv import load_dotenv
import os
from anthropic import Anthropic


#--------------------------------------
#Loading claude API key 
#--------------------------------------
load_dotenv()

api_key=os.getenv("ANTHROPIC_API_KEY")
client=Anthropic(api_key=api_key)

if "messages" not in st.session_state:
  st.session_state.messages=[]

if "current_incident" not in st.session_state:
  st.session_state.current_incident=None

if "clear_input" not in st.session_state:
  st.session_state.clear_input=False

st.title("CyberSim AI")
st.write("AI-Powered Cybersecurity Incident Response Simulator")


scenarios= {
       "Phishing Attack":"""
       An employee received an email that appeared to come from the company's IT department. The employee clicked a link in the email and entered their company credentials. Ten minutes later, a login was detected from an unfamiliar location.""",

       "Suspicious login":"""
       The security team detected a successful login to an employee account from an unfamiliar location. The employee noramlly logs in from Texas, but the new login occurred from another country.""",

      "Malware Infection":"""
       A company workstation has suddenly become very slow. Several unfamiliar processes are running, and the employee reports that unexpected pop-ups have started appearing
       """
    }

incident=st.selectbox(
        "Choose a cybersecurity incident:",
        list(scenarios.keys())
 )

if st.session_state.current_incident!=incident:
   st.session_state.messages=[]
   st.session_state.current_incident=incident

st.subheader("Incident Scenario")
st. write(scenarios[incident])

st.subheader("Investigation Conversation")

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.write(message["content"])
    

st.subheader("Your investigation")
st.write("What would you investigate first?")

if st.session_state.clear_input:
  st.session_state.investigation_input=""
  st.session_state.clear_input=False

investigation=st.text_area(
  "Explain your reasoning.",
   key="investigation_input"
    )

if st.button("Submit Investigation"):
  if investigation.strip():
    
   st.session_state.messages.append(
    {
      "role":"user",
      "content":investigation
    }
  )
   message= client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    system=f"""
    You are CyberSim AI, a cybersecurity incident-response mentor.
    
    Current incident:
    {scenarios[incident]}
    
    Guide the student through the investigation. 
    Challenge their reasoning and ask useful follow-up questions. 
    Do not immediately reveal the full solution.
    """,
    messages=st.session_state.messages
  )
   st.session_state.messages.append(
    {
      "role":"assistant",
      "content":message.content[0].text
    }
)

   st.session_state.clear_input=True
   st.rerun()

 