# B.6 Loops: repeat a step for each item.
basket = ["apple", "apple", "bread"]
prices = {"apple": 0.45, "bread": 1.20}
total = 0
for item in basket:
    total = total + prices[item]
    print(item, round(total, 2))
