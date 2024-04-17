import os
from dotenv import load_dotenv
import streamlit as st
from supabase import create_client, Client

# Load environment variables
load_dotenv() 

# Define the query and filter functions
def search_by_name(name):
    query = supabase.table('books').select('*').ilike('title', f'%{name}%').execute()
    return query.data

def search_by_description(description):
    query = supabase.table('books').select('*').ilike('description', f'%{description}%').execute()
    return query.data

def filter_and_order_by_rating(rating):
    query = supabase.table('books').select('*').gte('rating', rating).order('rating', desc=True).execute()
    return query.data

def filter_and_order_by_price(price):
    query = supabase.table('books').select('*').lte('price', price).order('price', ascending=True).execute()
    return query.data

# Create the Streamlit app
def main():
    st.title("Book Data Query and Filter App")

    with st.form("Search by Name"):
        name = st.text_input("Enter a book name to search:")
        submitted = st.form_submit_button("Search")
        if submitted and name:
            result = search_by_name(name)
            st.write(result)

    with st.form("Search by Description"):
        description = st.text_input("Enter description keywords:")
        submitted = st.form_submit_button("Search")
        if submitted and description:
            result = search_by_description(description)
            st.write(result)

    with st.form("Filter by Rating"):
        rating = st.slider("Choose a minimum rating:", min_value=0, max_value=5, step=0.1, value=3.0)
        submitted = st.form_submit_button("Filter")
        if submitted:
            result = filter_and_order_by_rating(rating)
            st.write(result)

    with st.form("Filter by Price"):
        price = st.slider("Set maximum price:", min_value=0, max_value=1000, step=10, value=100)
        submitted = st.form_submit_button("Filter")
        if submitted:
            result = filter_and_order_by_price(price)
            st.write(result)

if __name__ == "__main__":
    main()
