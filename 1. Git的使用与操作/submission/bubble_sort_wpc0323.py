def bubble_sort(arr):
    arr = list(arr)
    n = len(arr)
    if n <= 1:
        return arr
    for i in range(n-1):
        flag = True
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j] , arr[j + 1] = arr[j + 1] , arr[j]
                flag = False
        if flag:
            return arr
    return arr
if __name__== "__main__":
    print(bubble_sort([5,2,9,1]))            