niche = { "niche": "Car","audience": "Hagemaru","Value":["gap1","gap2"]}
fixed = {}
dynamic = {}


def main():
    chunks = []
    for key, value in niche.items():
        if isinstance(value, list):
            dynamic[key]=value
        else:
            fixed[key]=value

    for key, value in dynamic.items():
        for items in value:
            chunk = fixed.copy()
            chunk[key]=items
            chunks.append(chunk)
    return chunks

print(main())
