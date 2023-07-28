"""求：一维数组的动态和
给你一个数组 nums 。数组「动态和」的计算公式为：runningSum[i] = sum(nums[0]…nums[i]) 。

请返回 nums 的动态和。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/running-sum-of-1d-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""

class Solution:
    def runningSum(self, nums):
<<<<<<< HEAD
        """"""
        n = len(nums)
        for i in range(1, n):  # 列表第一位不变，故从第2位开始计算
            nums[i] = nums[i-1] + nums[i]   # 计算列表的动态之后
=======
        n = len(nums)
        for i in range(1, n):
            nums[i] = nums[i] + nums[i-1]
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
        return nums


if __name__ == "__main__":
    run = Solution()
    result = run.runningSum(nums=[1, 1, 1, 1, 5])

    print(result)