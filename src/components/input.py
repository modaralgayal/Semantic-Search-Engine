def take_input():
    user_query = input("Enter your query here (c to exit): ").strip()

    if user_query.strip().lower() == "c":
        return None

    if len(user_query) == 0 or len(user_query) > 30:
        raise ValueError("Invalid input: Either empty or too large.")
    
    return  user_query
