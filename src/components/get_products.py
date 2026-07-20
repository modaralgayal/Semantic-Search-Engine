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
        for i in range(1000)  # scaled down for Render Free tier (1k instead of 10k)
    ]
    return document_phrases
