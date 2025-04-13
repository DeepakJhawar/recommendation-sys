import os
import json
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from annoy import AnnoyIndex
from flask_cors import CORS


meta_data = pd.read_csv("meta_All_Beauty.csv")
review_data = pd.read_csv("all_beauty.csv")
review_data.drop(columns=["title", "text", "images", "timestamp", "helpful_vote", "asin", "verified_purchase"], inplace=True)
grouped_data = review_data.groupby('parent_asin').filter(lambda x:x['rating'].count() >= 50)
popular_products = pd.DataFrame(grouped_data.groupby('parent_asin')['rating'].count())
most_popular = popular_products.sort_values('rating', ascending=False)
most_popular.reset_index(inplace=True)  

annoy_index = AnnoyIndex(5000, 'angular')
if not os.path.exists("product_similarity.index"):
    raise Exception("Index file not found")
annoy_index.load("product_similarity.index")
    
app = Flask(__name__)
CORS(app)

def get_content_based_similarity(idx, n_top=20):
    neighbors = annoy_index.get_nns_by_item(idx, n_top, include_distances=True)
    indices = neighbors[0]
    distances = neighbors[1]
    similarity = [1 - (dist / np.pi) for dist in distances]
    similar_items = list(zip(indices, similarity))
    sorted_similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    sorted_indices = [item[0] for item in sorted_similar_items]
    sorted_similarity = [item[1] for item in sorted_similar_items]
    sorted_meta_data = list(zip(meta_data.loc[sorted_indices, "parent_asin"], sorted_similarity))

    return sorted_meta_data

ratings_matrix = pd.read_csv('ratings_matrix.csv', index_col=0)
correlation_matrix = np.load('correlation_matrix.npy')

def get_collaborative_similarity(user_id, n_top=20):
    # Check if the user exists in the ratings matrix
    if user_id not in ratings_matrix.index:
        print(f"User {user_id} not found in the dataset.")
        return None

    # Get products rated highly by the user (rating > 0)
    liked_products = ratings_matrix.loc[user_id][ratings_matrix.loc[user_id] > 0].index
    if not liked_products.any():
        print(f"User {user_id} has not rated any products.")
        return None
    
    # Precompute similarity scores for all products (once, instead of in each loop)
    similar_products_dict = {}
    for product_id in liked_products:
        product_idx = list(ratings_matrix.columns).index(product_id)
        similarity_scores = correlation_matrix[product_idx]
        similar_products_dict[product_id] = similarity_scores
        
    # Find top n similar products for each liked product and update recommendations
    recommended_products = []
    for product_id, similarity_scores in similar_products_dict.items():
        similar_products_idx = np.argsort(similarity_scores)[::-1][1:n_top + 1]  # Skip the first (self-similarity)
        
        for idx in similar_products_idx:
            similar_product_id = ratings_matrix.columns[idx]
            similarity_score = similarity_scores[idx]
            recommended_products.append((similar_product_id, similarity_score))
    return recommended_products

def format_response(results, n_top=20):
    if isinstance(results, list):
        products = [product for product, _ in results]
    else:
        products = results
    results = meta_data.loc[meta_data['parent_asin'].isin(products)].iloc[:n_top]
    response = []
    for _, result in results.iterrows():
        image_data = result['images']
        if "'hi_res': '" in image_data:
            image_url = image_data.split("'hi_res': '")[1].split("'")[0]
        elif "'large': '" in image_data:
            image_url = image_data.split("'large': '")[1].split("'")[0]
        elif "'thumb': '" in image_data:
            image_url = image_data.split("'thumb': '")[1].split("'")[0]
        response.append({
            "title": result['title'],
            "image": image_url,
            "product_id": result['parent_asin'],
        })
    return response

def recommend_products_by_userID(user_id):
    recommended_products = get_collaborative_similarity(user_id)
    print(len(recommended_products))
    return format_response(recommended_products)


def recommand_content_based_similarity(user_id):
    rated_products = review_data[review_data['user_id'] == user_id]['parent_asin'].values
    
    # Step 8: Content-based filtering - Get recommendations based on product descriptions
    recommend = []
    for product in rated_products:
        idx = meta_data[meta_data['parent_asin'] == product].index[0]
        sim_scores = list(get_content_based_similarity(idx))
        recommend.extend(sim_scores)
    return format_response(recommend)

def recommand_hybrid_similarity(user_id):
    collaborative_recommendations = get_collaborative_similarity(user_id)
    rated_products = review_data[review_data['user_id'] == user_id]['parent_asin'].values
    
    # Step 8: Content-based filtering - Get recommendations based on product descriptions
    content_based_recommendations = []
    for product in rated_products:
        idx = meta_data[meta_data['parent_asin'] == product].index[0]
        sim_scores = list(get_content_based_similarity(idx))
        content_based_recommendations.extend(sim_scores)
            
    # Combine the recommendations from both models
    combined_recommendations = collaborative_recommendations + content_based_recommendations
    combined_recommendations = sorted(combined_recommendations, key=lambda x: x[1], reverse=True)
    
    return format_response(combined_recommendations)
    
# Define a simple route
@app.route('/')
def home():
    return list(set(ratings_matrix.index))[:100]

@app.route('/cold-start')
def cold_start():
    return format_response(most_popular["parent_asin"])

# API endpoint to get data (for example, returning JSON data)
@app.route('/recommend', methods=['GET'])
def get_data():
    user_id = request.args.get("user_id", "")
    model = request.args.get("model", "hybrid")
    if user_id == "":
        return jsonify({
            "message": "Please provide user_id",
            "status": "error"
        })
    
    if model == "collaborative":
        sorted_meta_data = recommend_products_by_userID(user_id)
    elif model == "content_based":
        sorted_meta_data = recommand_content_based_similarity(user_id)
    else:
        sorted_meta_data = recommand_hybrid_similarity(user_id)
    return jsonify(sorted_meta_data)

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
