# Importing libraries
import streamlit as st
import requests

# Base URL for the API
base_url = "http://127.0.0.1:4000/"

# Configuring the page
st.set_page_config(page_title="Product Recommendation", layout="centered", initial_sidebar_state="auto")

# Helper function to fetch recommendations from the API
def fetch_recommendations(user_id):
    try:
        response = requests.get(base_url + f"recommend/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch recommendations. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error connecting to the API: {e}"}

# Main function for the app
def main():
    st.markdown(
        """
        <style>
            h1, h2, h3 { color: white; text-align: center; }
            .recommendations { text-align: center; color: white; margin-top: 20px; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1>OList Store</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Welcome to our Store!</h2>", unsafe_allow_html=True)
    st.markdown("<h3>Please login to continue!</h3>", unsafe_allow_html=True)

    # User login input
    user_id = st.text_input("Enter UserID:")
    if st.button("Login"):
        if user_id:
            st.markdown("<h3 class='recommendations'>Here are some recommendations for you!</h3>", unsafe_allow_html=True)
            recommendations = fetch_recommendations(user_id)
            
            if "error" in recommendations:
                st.error(recommendations["error"])
            elif "details" not in recommendations:
                for product in recommendations:
                    st.write(product)
            else:
                st.warning("No recommendations available for this user.")
        else:
            st.warning("Please enter a valid UserID.")

    st.markdown("<hr style='height:10px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
    st.markdown("<h3 class='recommendations'>Have a look at our top products!</h3>", unsafe_allow_html=True)

    # Fetching top products
    top_products = fetch_recommendations("0000")
    if "error" in top_products:
        st.error(top_products["error"])
    elif "details" not in top_products:
        for product in top_products:
            st.write(product)
    else:
        st.warning("No top products available at the moment.")

# Run the app
if __name__ == "__main__":
    main()
