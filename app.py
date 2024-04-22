import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from database import Database

load_dotenv()

def fetch_data(search_query='', filter_by=None, order_by=None, order_direction='ASC'):
    with Database(os.getenv('supabaseURL')) as db:
        query = "SELECT * FROM books WHERE "
        query_conditions = []

        if search_query:
            query_conditions.append("(title ILIKE %s OR description ILIKE %s)")
        
        if filter_by and filter_by in ['rating', 'price']:
            query_conditions.append(f"{filter_by} IS NOT NULL")
        
        final_query = query + (" AND ".join(query_conditions) if query_conditions else "TRUE")

        if order_by:
            final_query += f" ORDER BY {order_by} {order_direction}"

        params = [f'%{search_query}%', f'%{search_query}%'] if search_query else []
        df = pd.read_sql(final_query, db.con, params=params)
        return df

def main():
    st.title('Book Data Query and Filter App')

    search_query = st.text_input("Search by book name or description")
    filter_option = st.selectbox("Filter by:", options=['None', 'rating', 'price'], index=0)
    order_option = st.selectbox("Order by:", options=['ASC', 'DESC'], index=0)

    if st.button("Search/Fetch Data"):
        if not search_query and filter_option == 'None':
            st.warning("Please enter a search term or choose a filter option.")
            return
        
        df = fetch_data(search_query, 
                        filter_by=(filter_option if filter_option != 'None' else None),
                        order_by='price' if filter_option == 'price' else 'rating',  
                        order_direction=order_option.lower())
        
        if df.empty:
            st.write("No results found.")
        else:
            st.write("Results:")
            st.dataframe(df, width=700)

if __name__ == "__main__":
    main()
