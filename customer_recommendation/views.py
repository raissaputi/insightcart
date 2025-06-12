import pandas as pd
import os
from django.shortcuts import render

# Peta nama pendek → panjang (boleh disesuaikan)
CLUSTER_NAME_MAPPING = {
    "Bulk Toy": "Bulk Toy & Game Buyers",
    "Stationery": "Stationery & Decorative",
    "Lighting": "Home Lighting Specialists",
    "Core Shoppers": "Core Regular Shoppers",
    "Antique Glass": "Antique Glass Collectors",
    "Ornamental": "Ornamental Decoration",
    "Educational": "Educational Products"
}

def recommend_items_view(request):
    cluster_id = request.GET.get("id")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    profiles_path = os.path.join(base_dir, 'data', 'Product_Profiles.csv')
    rec_path = os.path.join(base_dir, 'data', 'Cross-Selling_Recommendations.csv')

    df_profiles = pd.read_csv(profiles_path)
    df_profiles['cluster'] = df_profiles['cluster'].astype(str).str.strip()
    clusters = df_profiles['cluster'].dropna().unique().tolist()

    if not cluster_id:
        cluster_id = clusters[0]

    items = []
    recommendation_map = {}

    if cluster_id:
        df_filtered = df_profiles[df_profiles['cluster'] == cluster_id]
        items = df_filtered['item'].dropna().unique().tolist()

        # Buat mapping rekomendasi per item
        df_rules = pd.read_csv(rec_path)
        df_rules.fillna("", inplace=True)
        for item in items:
            recs = df_rules[df_rules['trigger_products_str'].str.contains(item, na=False)]
            rec_list = recs['recommended_products_str'].dropna().unique().tolist()
            recommendation_map[item] = rec_list

    import json
    context = {
        'clusters': clusters,
        'selected_cluster': cluster_id,
        'items': items,
        'recommendation_map_json': json.dumps(recommendation_map),
    }
    return render(request, 'customer_recommendation/item_list.html', context)


def recommend_results_view(request):
    item_name = request.GET.get("name")
    recommendations = []

    if item_name:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rec_path = os.path.join(base_dir, 'data', 'Cross-Selling_Recommendations.csv')
        df = pd.read_csv(rec_path)
        for _, row in df.iterrows():
            ant = str(row['trigger_products_str']).strip()
            cons = str(row['recommended_products_str']).strip()
            if item_name in ant:
                recommendations.append({
                    'recommend': cons,
                    'confidence': row.get('confidence', ''),
                    'lift': row.get('lift', '')
                })

    return render(request, 'customer_recommendation/recommendation_results.html', {
        'item_name': item_name,
        'recommendations': recommendations
    })
