# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-29 10:12
# ---
# 占内存较少
# 爬虫（用python批量下载图片） 把所有图片都放到list中，占用内存；每获得一个图片，把图片保存；
"""
Python 迭代器在很多场景下都非常有用。以下是一些应用场景的例子：

遍历数据集：当你有一个较大的数据集（如列表或元组）需要遍历时，你可以使用迭代器。这比一次性加载整个数据集到内存中更有效，因为迭代器允许你一次处理一个元素，而不是一次性处理所有元素。
无限序列：如果你有一个无限序列（例如，自然数、斐波那契数列等），你可以使用迭代器来有效地获取序列的元素。由于迭代器只需要存储当前元素和下一个元素的索引，所以它们在处理大量数据时非常有效。
异步处理：Python 的 asyncio 库使用迭代器来处理异步操作。通过 asyncio.as_completed() 函数，我们可以对一个异步生成器（也就是一个迭代器）进行迭代，当异步操作完成时，返回的结果就会被消费。
生成器和生成器表达式：生成器和生成器表达式是 Python 中的迭代器。它们允许你创建自定义的迭代器，这对于处理大量数据或实现复杂的迭代逻辑非常有用。
自定义迭代器：如果你需要创建一个对象，该对象的行为类似于迭代器（即，它有一个 __iter__() 方法返回一个有 __next__() 方法的对象），那么你可以创建一个自定义迭代器。这使得你的代码更易于理解和维护，因为其他程序员可以清楚地看到你的对象支持迭代。
在函数式编程中使用：Python 的函数式编程工具（如 map(), filter() 和 reduce()）都依赖于迭代器。这些函数需要一个可迭代的对象作为输入，因此使用迭代器非常有用。
数据库操作：当你从数据库中获取大量数据时，使用迭代器是很重要的。这样你可以一次只处理一行数据，而不是一次性加载整个数据集到内存中。
总的来说，迭代器在处理大量数据、异步操作、自定义行为以及函数式编程等场景下非常有用。它们提供了一种灵活且高效的方式来处理和操作数据。

"""
class Myiter():
    def __init__(self,start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.start >= self.end:
            raise StopIteration
        self.start +=1
        return self.start-1


if __name__ == '__main__':

     for i in Myiter(1, 5):
         print(i)