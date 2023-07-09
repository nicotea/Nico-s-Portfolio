# streamlit app basic template with docker 
import streamlit as st

st.set_page_config(page_title="Home", page_icon='🏠', initial_sidebar_state="expanded")


def main():
    st.title("Nico's Portfolio - Streamlit App")
    st.subheader("Welcome to my portfolio!")
    st.write("The goal of this app is to showcase my work and projects.")

if __name__ == '__main__':
    main()