import streamlit as st
import pandas as pd
import numpy as np
from send_email_for_crew import send_email_to_crew
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="AI BA Randomizer", page_icon=":airplane:")
st.image('./air_india_logo.png')
st.title("BA Randomizer")

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

logged_in = False
if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    logged_in = True
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

if logged_in:
    # Initialize session state for seed
    if 'seed' not in st.session_state:
        st.session_state.seed = np.random.randint(0, 1000000)

    if 'emails_sent' not in st.session_state:
        st.session_state.emails_sent = False

    uploaded_file = st.file_uploader("Add the List of Staff strictly as per format communicated", type=["xlsx"])

    correct_file_added = False
    if uploaded_file is not None:
        try:
            staff_df = pd.read_excel(uploaded_file)
            # st.write(df)
            correct_file_added = True
        except Exception as e:
            st.error(f"Error reading file: {e}")

    percentage_input = st.number_input('Enter percentage of staff bound to go through BA test', 
                                value=25, min_value=0, max_value=100, disabled=correct_file_added==False)

    def randomize_staff(df, percentage):
        num_rows = len(df)
        num_samples = max(1, int(num_rows * percentage/100))  
        
        random_sample = df.sample(n=num_samples, random_state=st.session_state.seed)
        return random_sample

    def send_email_to_everyone(randomized_df):
        print('Sending email to everyone...')
        for index, row in randomized_df.iterrows():
            send_email_to_crew(row['Email'], row['Name'])
            break
        st.session_state.emails_sent = True


    if correct_file_added and percentage_input:
        randomized_df = randomize_staff(staff_df, percentage_input)
        st.write(randomized_df)

        if st.button('Send Email to everyone'):
            send_email_to_everyone(randomized_df)
        
        # Change the button label after emails are sent
        if st.session_state.emails_sent:
            st.success("Emails have been sent successfully.")

        # st.button('Send Email to everyone', on_click=send_email_to_everyone(randomized_df))
        
        