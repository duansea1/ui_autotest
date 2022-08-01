from collections import Counter

class Solution:

	def findLeastNumOfUniqueInts(self, arr, k):
		cnts = sorted(Counter(arr).values())
		print('统计：', Counter(arr))
		print("获取keys", Counter(arr).keys())
		print("排序", cnts)
		size = len(cnts)    # 不同位数统计
		total = i = 0
		while i < size and total+cnts[i] <= k:
			total = total + cnts[i]
			i += 1
			print("统计后的位数：", size-1)
		return size-i


if __name__ == "__main__":
	s = Solution().findLeastNumOfUniqueInts([2, 3, 4, 3, 5], 2)
	print(s)

