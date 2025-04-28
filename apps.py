# importing libraries
import streamlit as st
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# reading datasets
item = pd.read_csv('item.csv')
customer = pd.read_csv('customer.csv')
order = pd.read_csv('order.csv')
product = pd.read_csv('product.csv')
review = pd.read_csv('review.csv')

# merging datasets
item = item.merge(order, on='order_id', how='inner')
df_apriori = item.merge(product[['product_id', 'product_category_name_english']], on='product_id', how='left')
item_cust = item.merge(customer, on='customer_id', how='left')

# Streamlit App
st.title("Product Recommendation System")
st.write("This app recommends products using **Markov Chains** and **Association Rule Mining**.")

# 1. Cold Start Recommendation
def cold_start():
    """Recommend top 5 highest-rated products."""
    df_cold = item.merge(review, on='order_id', how='inner')
    df_cold = df_cold.groupby('product_id').agg({'review_score': 'mean'}).reset_index()
    top_products = df_cold.sort_values(by='review_score', ascending=False).head(5)
    return list(top_products['product_id'])

# 2. Association Rule Mining for Cross-Selling
def apriori_recommendation():
    """Generate cross-selling recommendations using Association Rule Mining."""
    df_apriori_clean = df_apriori.dropna(subset=['product_category_name_english'])
    transactions = df_apriori_clean.groupby('order_id')['product_category_name_english'].unique().tolist()

    # Encoding transactions
    te = TransactionEncoder()
    transaction_data = te.fit_transform(transactions)
    transaction_df = pd.DataFrame(transaction_data, columns=te.columns_)

    # Finding frequent itemsets
    frequent_itemsets = apriori(transaction_df, min_support=0.0005, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)

    # Preprocess rules
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0] if isinstance(x, frozenset) else x)
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x)[0] if isinstance(x, frozenset) else x)

    return rules

# 3. Markov Chain for Sequential Recommendations
def markov_chain_recommendation():
    """Generate product chains using Markov Chain modeling."""
    item['quantity'] = 1
    basket = item.groupby(['order_id', 'product_id'])['quantity'].sum().unstack().fillna(0).astype(int)
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)

    # Frequent itemsets and rules
    frequent_itemsets = apriori(basket, min_support=0.0001, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)

    # Create Markov chain transitions
    chains = {}
    for _, row in rules.iterrows():
        ant = row['antecedents']
        cons = row['consequents']
        chains[ant] = cons

    return chains

# User Input for Recommendations
user_id = st.text_input("Enter User ID:", "")
if user_id:
    if item_cust[item_cust['customer_unique_id'] == user_id].shape[0] > 0:
        user_products = list(item_cust[item_cust['customer_unique_id'] == user_id]['product_id'].unique())
        chains = markov_chain_recommendation()
        rules = apriori_recommendation()

        recommendations = []

        # Check for Markov Chain matches
        for prod in user_products:
            if prod in chains:
                recommendations.extend(chains[prod])

        # Check for Association Rule matches
        for prod in user_products:
            prod_category = df_apriori[df_apriori['product_id'] == prod]['product_category_name_english'].values[0]
            consequents = rules[rules['antecedents'] == prod_category]['consequents']
            recommendations.extend(list(consequents))

        # Remove duplicates and limit recommendations
        recommendations = list(set(recommendations))[:5]
        if not recommendations:
            recommendations = cold_start()
    else:
        recommendations = cold_start()

    st.subheader("Recommended Products:")
    st.write(recommendations)
else:
    st.info("Enter a User ID to get recommendations.")
