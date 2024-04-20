import os
from dotenv import load_dotenv
import streamlit as st
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Connect to Supabase
supabase_url = os.getenv('MY_SUPABASE_URL')
supabase_key = os.getenv('MY_SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def search_by_name(name):
    query = supabase.table('books').select('*').ilike('title', f'%{name}%').execute()
    return query.data

def search_by_description(description):
    query = supabase.table('books').select('*').ilike('description', f'%{description}%').execute()
    return query.data

def filter_by_rating(rating):
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    query = supabase.table('books').select('*').eq('rating', rating_map[rating]).execute()
    return query.data

def filter_and_order_by_price(price):
    query = supabase.table('books').select('*').lte('price', price).order('price', ascending=True).execute()
    return query.data

# Create the Streamlit app
def main():
    st.title("Book Data Query and Filter App")

    # Environment check (For debugging, remove in production)
    if not supabase_url or not supabase_key:
        st.error("Supabase credentials are not set in the environment variables.")
        return

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

    with st.expander("Filter by Rating"):
        rating = st.selectbox("Choose a rating:", ['One', 'Two', 'Three', 'Four', 'Five'])
        if st.button("Filter Ratings"):
            result = filter_by_rating(rating)
            st.write(result)

    with st.form("Filter by Price"):
        price = st.slider("Set maximum price:", min_value=0, max_value=1000, step=10, value=100)
        submitted = st.form_submit_button("Filter")
        if submitted:
            result = filter_and_order_by_price(price)
            st.write(result)

if __name__ == "__main__":
    
    main()
