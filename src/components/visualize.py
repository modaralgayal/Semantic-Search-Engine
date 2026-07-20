import matplotlib.pyplot as plt


def visualize(top_scores, best_result, best_res_idx, best_res_score):
    values = top_scores.tolist()[0]
    fix, ax = plt.subplots()
    ax.scatter(range(len(values)), values)
    ax.set_ylim(-0.05, 1)
    ax.annotate(
        best_result,
        xy=(best_res_idx, best_res_score),
        xycoords="data",
        xytext=(best_res_idx + 5, best_res_score - 0.15),
        textcoords="data",
        va="top",
        ha="left",
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.show()
