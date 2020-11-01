# Reference: https://docs.streamlit.io/en/latest/getting_started.html
# Reference for hosting: https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3
# Importing Libraries
from airtable import Airtable
import streamlit as st  # creating web-app
import pandas as pd  # managing data
import numpy as np  # managing data for model
import os

################################################


# Accessing API
api_key = os.environ['AIRTABLE_API_KEY']
base_key = os.environ['AIRTABLE_FREELANCE_BASE_KEY']
table_name = 'freelancers'
airtable = Airtable(base_key, table_name, api_key)
dt = airtable.get_all()
df = pd.DataFrame.from_records((r['fields'] for r in dt))


# Functions
def string_to_list(series):
    stripped_skills_list = series.str.strip('][')
    split_skills_list = stripped_skills_list.str.split(', ')
    return split_skills_list


def rate_by_skill(data):
    exploded_df = data.explode('skills_list')
    results = exploded_df.groupby(['skills_list'])[
        'hourly_rate'].agg(['mean', 'count'])
    return results.sort_values(by=['count'], ascending=False)


# Cleaning df
df['skills_list'] = string_to_list(df['skills_list'])


# Building web app
st.title("Freelance Hourly Rate Data")
st.markdown(
    "Welcome! This app provides data and trends of freelancer hourly rates.")
st.write(df.groupby(['date_accessed'])['hourly_rate'].mean())
st.write(rate_by_skill(df))