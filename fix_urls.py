import json

file_path = "itinerary_data.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# The new links that are guaranteed to work (Baidu Baike, Wikipedia, or stable sites)
new_urls = {
    "雅尼濕地玻璃觀景台": "https://baike.baidu.com/item/%E9%9B%85%E5%B0%BC%E5%9B%BD%E5%AE%B6%E6%B9%BF%E5%9C%B0%E5%85%AC%E5%9B%AD/22370830",
    "林拉景觀大道": "https://baike.baidu.com/item/%E6%9E%97%E6%8B%89%E5%85%AC%E8%B7%AF/17627471",
    "崗巴拉山口": "https://baike.baidu.com/item/%E5%B2%97%E5%B7%B4%E6%8B%89%E5%B1%B1%E5%8F%A3/2996969",
    "藏北草原風光": "https://baike.baidu.com/item/%E8%97%8F%E5%8C%97%E8%8D%89%E5%8E%9F/234771",
    "青海湖遠眺": "https://baike.baidu.com/item/%E9%9D%92%E6%B5%B7%E6%B9%96/133031",
    "麒麟灣公園": "https://baike.baidu.com/item/%E9%BA%92%E9%BA%9F%E6%B9%BE%E5%85%AC%E5%9B%AD/2691866",
    "水井巷商圈": "https://baike.baidu.com/item/%E6%B0%B4%E4%BA%95%E5%B7%B7/9054942"
}

for item in data:
    if "highlights" in item:
        for highlight in item["highlights"]:
            if highlight["name"] in new_urls:
                highlight["url"] = new_urls[highlight["name"]]
                print(f"Updated URL for: {highlight['name']}")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Finished updating itinerary_data.json.")
