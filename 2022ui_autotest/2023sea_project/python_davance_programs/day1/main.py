# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月22日 10:47
# ---
from book import Book,BookMange
def welcome():
    print("*****************************欢迎进入图书管理系统******************")
    print("1、显示所有图书；\n2、添加图书\n 3、删除图书\n 4、查找图书\n 5、退出图书\n 6、清空图书")
    print("***********************************************")

def get_choose_number():
    """获得用户输入的菜单编号"""
    choose_number = input("请输入菜单编号:")
    # if isinstance(choose_number,int):
    # isdigit 判断是不是数字
    if not choose_number.isdigit() or choose_number not in ["1","2","3","4","5"]:
        return -1
    return int(choose_number)


def main():
    bm = BookMange()
    while True:
        welcome()
        number = get_choose_number()  # 获得使用者输入的菜单
        print(number)
        if number == 1:
            bm.show_book()

        elif number == 2:
            # num = input('请输入书的编号：')
            num = bm.last_book_id + 1   # 使用了装饰器，不需要加()
            print('编号：',num)
            book_name = input("请输入书名“")
            book_positon = input("请输入位置")
            book = Book(num, book_name, book_positon)  # 显示图书的类
            # print(f"'''''''''{book}'''''")
            bm.add_book(book)  # 添加图书
            print('图书馆：', bm.book_list[0].num)
        elif number == -1:
            print('输入的不是数字')
            continue
        elif number == 3:
            bm.clean()  # 清空book_list
            continue
        elif number == 4:
            bm.save()  # 保存book_list
            continue
        else:
            break
def f1(s: str):
    return s.lower()


if __name__ == "__main__":
    main()

