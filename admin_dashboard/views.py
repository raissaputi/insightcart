from django.shortcuts import render
import pandas as pd
import os

def dashboard_view(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    basket_stats_path = os.path.join(base_dir, 'data', 'Basket_Statistics.csv')

    clusters = pd.read_csv(basket_stats_path)
    clusters.rename(columns={
        'Unnamed: 0': 'cluster',
        'jumlah_transaksi': 'total_transactions',
        'rata_rata_produk_per_transaksi': 'avg_spending'
    }, inplace=True)

    # Mapping nama pendek ke nama panjang
    CLUSTER_NAME_MAPPING = {
        "Bulk Toy": "Bulk Toy & Game Buyers",
        "Stationery": "Stationery & Decorative",
        "Lighting": "Home Lighting Specialists",
        "Core Shoppers": "Core Regular Shoppers",
        "Antique Glass": "Antique Glass Collectors",
        "Ornamental": "Ornamental Decoration",
        "Educational": "Educational Products"
    }

    clusters['cluster_fullname'] = clusters['cluster'].map(CLUSTER_NAME_MAPPING)

    context = {
        'clusters_data': clusters.to_dict('records'),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


def cluster_detail_view(request):
    cluster_id = request.GET.get("id")
    product_data = []

    if cluster_id is not None:
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            product_profiles_path = os.path.join(base_dir, 'data', 'Product_Profiles.csv')
            df = pd.read_csv(product_profiles_path)

            # Bersihkan string dan cocokkan
            df['cluster'] = df['cluster'].astype(str).str.strip()
            cluster_id = cluster_id.strip()

            df_cluster = df[df['cluster'] == cluster_id]
            product_data = df_cluster[['item', 'support']].to_dict('records')

        except Exception as e:
            print(f"Gagal memuat produk cluster {cluster_id}: {e}")

    context = {
        'cluster_id': cluster_id,
        'products': product_data,
    }
    return render(request, 'admin_dashboard/cluster_detail.html', context)
