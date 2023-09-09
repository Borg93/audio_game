def pretty_print(response):
    for key, value in response.items():
        if isinstance(value, list):
            print(f"{key.capitalize()}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"{key.capitalize()}: {value}")
    print("-" * 50)  # separator line for clarity
