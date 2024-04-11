import re

title_raw = 'NOTHING Phone (2a) (128 GB, Schwarz, 6.7", 50 MP, 5G)'

brand_match = re.match(r'^(\w+)', title_raw)
if brand_match:
    brand = brand_match.group(1)
else:
    pass

print(brand_match[0])