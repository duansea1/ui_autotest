
# ʲô�ǵ���ģʽ
# ʲô��װ��������������װ�����ĵ���˳��
# __new__ ��__init__������
# supershi shenm

# ʵ��һ���࣬ǰ5�δ��������Ժ󴴽�����5���е�һ��
import random
class Myclass(object):
    objs = []

    def __new__(cls, *args, **kwargs):
        if len(cls.objs) < 5:
            obj = super().__new__(cls)
            cls.objs.append(obj)
        else:
            obj = random.choice(cls.objs)
        return obj
