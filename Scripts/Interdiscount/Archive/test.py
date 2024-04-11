import re

title_raw3 = 'APPLE iPhone 13 (128 GB, (PRODUCT)RED, 6.1", 12 MP, 5G)'
title_raw2 = 'APPLE iPhone 15 Pro (128 GB, Titan Schwarz, 6.1", 48 MP, 5G)'
title_raw = 'NOTHING Phone (2a) (128 GB, Schwarz, 6.7", 50 MP, 5G)'
title_raw4 = 'NOTHING Phone (2) (5G, 256 GB, 6.7", 50 MP, Grau)'

brand_match = re.match(r'^(\w+)', title_raw)
if brand_match:
    brand = brand_match.group(1)
else:
    pass  # Skip if brand is not found

# Extract model
model_match = re.search(rf'{re.escape(brand)}\s+(.+?)\s*\(', title_raw)
if model_match:
    model = model_match.group(1)
else:
    pass

parenthesis = re.search(r"\((.*?)\)[^()]*$", title_raw).group(1)
parenthesis_list = parenthesis.split(", ")

memory = None
camera = None
network = None
screen = None
color_list = []

for item in parenthesis_list:
    if re.search(r'\d+\s*(?:GB|TB|MB)', item):
        memory = item
    elif re.search(r'\d+\s*MP', item):
        camera = item
    elif re.search(r'\d+G\b', item):
        network = item
    elif re.search(r'^\d+$', item) or re.search(r'^[^a-zA-Z]+$', item):
        # Checks if the string contains only digits or other characters
        screen = item
    else:
        color_list.append(item)

    color = ", ".join(color_list)


if brand == "NOTHING":
    memory_match = re.search(r'\((\d+ GB)', memory)
    model_match = re.search(r'^([^()]+)', memory)
    if memory_match:
        memory = memory_match.group(1)
    if model_match:
        model = model + " " + model_match.group(1)
    else:
        pass

print(brand)
print(model)
