import asyncio

def ask():
    while True:
        name = input("Enter Name: ").strip()
        if name:
            break
        print("Cannot be empty!")
    while True:
        f_n = int(input("Enter Followers: "))
        if f_n:
            break
        print("Cannot be empty!")
    while True:
        asking = input("Enter Bio: ").strip()
        if asking:
            break
        print("Cannot be empty!")
    while True:
        try:
            c = int(input("Enter number of captions: "))
            if c<0:
                print("Enter positive value!")
            elif c:
                break
        except ValueError:
            print("Cannot be empty!")
    caption = []
    for i in range(c):
        while True:
            acaption = input(f"Enter Caption {i+1}: ")
            if not acaption:
                print("Cannot be empty!")
                continue
            caption.append(acaption)
            break
    return {
            "name": name,
            "followers": f_n,
            "bio": asking, 
            "caption": caption
            }

def improved_output(ai_output): 
    start = ai_output.find("{")
    end = ai_output.rfind("}")
    end_output = ai_output[start:end+1]
    return end_output
