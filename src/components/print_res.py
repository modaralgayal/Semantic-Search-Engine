def print_search_results(ranked_indices, top_scores, products):
    print("\n" + "=" * 80)
    print("TOP SEARCH RESULTS")
    print("=" * 80)

    for rank, (idx, score) in enumerate(
        zip(ranked_indices, top_scores), start=1
    ):
        print(f"{rank}. {products[idx]:<45} Distance: {score:.4f}")

    print("=" * 80)
    return True
