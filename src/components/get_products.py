import requests


def get_posts():
    """Fetch all products from DummyJSON and return searchable text strings."""
    all_products = []
    skip = 0
    limit = 30

    while True:
        resp = requests.get(
            "https://dummyjson.com/products",
            params={"limit": limit, "skip": skip, "select": "title,description,category"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        products = data["products"]

        if not products:
            break

        for p in products:
            # Combine title + description + category into one searchable string
            text = f"{p['title']} — {p['description']} [{p['category']}]"
            all_products.append(text)

        skip += limit

    print(f"  Fetched {len(all_products)} real products from DummyJSON", flush=True)
    return all_products