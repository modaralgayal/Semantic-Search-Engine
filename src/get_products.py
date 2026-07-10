import requests


def get_posts():
    url = "https://dummyjson.com/products?select=title"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            titles = [p["title"] for p in posts["products"]]

            print("These are the posts: ", titles)
            return titles
        else:
            print("Error: ", response.status_code)
            return None
    except Exception as e:
        return "Error occurred: " + e



def run(): 
    get_posts()
    return True

if __name__=="__main__":
    run()


