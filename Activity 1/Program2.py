numbers = list(range(1, 101))

countOf1 = ''.join(map(str, numbers)).count('1') #joins together the ints and shows the occurences of the int 1

print(f"The number 1 appears {countOf1} times in the list!")
