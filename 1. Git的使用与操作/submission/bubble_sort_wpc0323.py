def bubble_sort(arr):
    arr = list(arr)
    n = len(arr)
    for i in range(n-1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j] , arr[j + 1] = arr[j + 1] , arr[j]
    return arr
if __name__== "__main__":
    print(bubble_sort([5,2,9,1]))            