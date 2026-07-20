import numpy as np
import requests


def get_posts():
    adjectives = [
        "Red",
        "Blue",
        "Wireless",
        "Portable",
        "Organic",
        "Premium",
        "Compact",
        "Heavy-duty",
    ]
    nouns = [
        "Headphones",
        "Water Bottle",
        "Keyboard",
        "Charger",
        "Backpack",
        "Lamp",
        "Blender",
        "Chair",
    ]

    document_phrases = [
        f"{np.random.choice(adjectives)} {np.random.choice(nouns)} model {i}"
        for i in range(10000)  # scale this up as needed: 1k, 10k, 100k, 1M
    ]
    return document_phrases
