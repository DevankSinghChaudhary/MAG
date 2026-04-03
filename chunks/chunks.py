def chunks(output):
    chunks = []
    fixed = {}
    dynamic = {}
    for key, value in output.items():
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