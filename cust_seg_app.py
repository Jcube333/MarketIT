import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image 
from sklearn.preprocessing import StandardScaler


image= Image.open('cust_seg.webp')
st.image(image, width=900)
st.title('Customer segmentation Dashboard')

st.markdown("""
Plan your marketing budget and strategies on the GO..!
* **Created passionately by:** Jaimin Judal and Milind Bhatnagar
* **Python libraries used :** base64, pandas, streamlit, seaborn, matplotlib, re
* **Data source:** Kaggle.com

""")

st.sidebar.header('Select Factors for Analysis')

budget_ip = st.sidebar.text_input("Marketing Budget:")

cust_type=["High Spenders, High app users","High spenders, low app users","Low spenders, high app users","Low spenders, low app users"]
selected_cust_clust = st.sidebar.selectbox('Customer Type', list(cust_type))

cust_csv={"High Spenders, High app users":"data/most_val.csv",
          "High spenders, low app users":"data/bit_attention.csv",
          "Low spenders, high app users":"data/more_attention.csv",
          "Low spenders, low app users":"data/most_attention.csv"}

@st.cache_resource
def load_data(selected_cust_clust):
    df = pd.read_csv(cust_csv[selected_cust_clust])
    df.drop(['Unnamed: 0'],axis=1,inplace=True)
    return df[['Email','state','Avatar','Avg_Session_Length']]

df = load_data(selected_cust_clust)


# Sidebar - State selection
cust_states = sorted(df.state.unique())
# sorted_unique_team = sorted(playerstats.Tm.unique())
selected_state = st.sidebar.multiselect('state', cust_states, cust_states)

# # Sidebar - Avg Length selection
value = st.sidebar.slider("Filter based on Average session length", min_value=30.0, max_value=35.0, step=1.0)

# # Filtering data
df_customers= df[(df.state.isin(selected_state)) & (df.Avg_Session_Length>=float(value))]

st.header('Display Customer Stats of Selected State(s)')
st.write('Data Dimension: ' + str(df_customers.shape[0]) + ' rows and ' + str(df_customers.shape[1]) + ' columns.')
st.dataframe(df_customers)

# Downloading filtered customer files
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="df_customers.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_customers), unsafe_allow_html=True)


def calc_stats(budget):
    
    no_most_val=pd.read_csv(cust_csv['High Spenders, High app users']).shape[0]

    no_bit_attention = pd.read_csv(cust_csv['High spenders, low app users']).shape[0]

    no_more_attention = pd.read_csv(cust_csv['Low spenders, high app users']).shape[0]

    no_most_attention = pd.read_csv(cust_csv['Low spenders, low app users']).shape[0]
     
    total = no_most_val + no_bit_attention +no_more_attention+no_most_attention
    budget_per_cust = budget/total

    alloc_budget = {"High Spenders, High app users":[0,no_most_val] , "High spenders, low app users":[round(no_bit_attention*budget_per_cust*0.2,2),no_bit_attention], "Low spenders, high app users":[round(no_more_attention*budget_per_cust*0.8,2),no_more_attention], "Low spenders, low app users":[round(no_most_attention*budget_per_cust,2),no_most_attention]}

    return alloc_budget




if budget_ip:
    budget_dict =calc_stats(int(budget_ip))
    allocated_budget=0
    for cust_type, budget in budget_dict.items():
           st.markdown(f"<h2 style='color: #1f77b4;'>{cust_type}</h2>", unsafe_allow_html=True)
           st.markdown(f"<h1 style='text-align: center; color: #ff7f0e;'>{budget[0]}</h1>", unsafe_allow_html=True)
           st.markdown(f"<h6 style='text-align: center; color: #ff7f0e;'>{round(budget[0]/budget[1],2)}/customer</h6>", unsafe_allow_html=True)
           st.button("Send Emails",key = cust_type)
           st.markdown("---")
           allocated_budget+=budget[0]


    st.markdown(f"<h1 style='text-align: center; color: #6ff76a;'>Saved Budget: {round(float(budget_ip),2)-allocated_budget}</h1>", unsafe_allow_html=True)










# import smtplib

# # for html messages
# from email.mime.text import MIMEText
# from email.message import EmailMessage
# from email.mime.multipart import   MIMEMultipart

# # for attachments
# from email import encoders
# from email.mime.base import MIMEBase
# import json



# #Login Credentials
# file=open("./config.json",'r')
# config=json.load(file)


# # HTML MESSAGE FORMATTING 

# Message = MIMEMultipart()
# Message['Subject']='Testing Purposes'
# Message['From']='jaiminjagdishjudal@gmail.com'
# for email in df_customers['email']:
#     Message['To'].append(email)

# htmlMsg=f'''<html>
# <body>
# <marquee>Hey, there get {x}% off on our yearly subscription </marquee>
# </body>
# </html>'''

# Message.attach(MIMEText(htmlMsg,'html'))

# # Adding attachments
# cv='Jaimin_2023.pdf'
# file2=open('./Jaimin_2023.pdf','rb')
# part=MIMEBase('application','octet-stream')
# part.set_payload(file2.read())
# encoders.encode_base64(part)
# part.add_header(
#     'Content-Disposition',
#     f'''Attachment;filename={cv}''',
# )


# Message.attach(part)

# s=smtplib.SMTP('smtp.gmail.com',587)
# s.starttls()
# s.login(config['email'],config['password'])

# try:
#  s.sendmail('jaiminjagdishjudal@gmail.com',email,Message.as_string())
# except Exception as e:
#     print(e)


# print("Email Sent Successfully")