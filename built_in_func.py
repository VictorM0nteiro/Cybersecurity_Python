# - Tuple: (1, 2, 3, 4, 5) - uses () and is immutable (can't be modified after creation)
# - List: [1, 2, 3, 4, 5] - uses [] and is mutable (can be modified)
#exemple with a list of numbers:
numbers = [5, 2, 8, 1, 9, 3]
sorted_numbers = sorted(numbers)
print("Original list:", numbers)
print("Sorted list:", sorted_numbers)


text = ["victor","jair","lula","dilma","bolsonaro"]
sorted_text = sorted(text)
print("sorted text: ", sorted_text)

reverse_sorted_numbers = sorted(numbers, reverse=True)
print("reverse sorted list: ", reverse_sorted_numbers)
