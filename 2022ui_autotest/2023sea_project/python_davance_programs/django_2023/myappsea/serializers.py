# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-22 19:06
# ---
"""
一、序列化器
a、如果使用DRF来实现序列化、反序列化、数据操作，在serializers.py文件中
b、文件名称推荐serializers

"""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from interfaces.models import Interfaces
from .models import Projects


class InterfaceSerializer(serializers.Serializer):
    """
    1、自定义序列化类实际上也是Field的子类
    2、所以自定义的序列化器类可以作为另一个序列化器中的字段
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    leader = serializers.CharField()

# 1.可以在类外自定义校验函数
# 2.第一个参数为待校验的值
# 3、如果校验不通过，必须抛出serializers.ValidationError（）异常，同时可以指定具体的报错信息
# 4、UniqueValidator校验器，可以使用msg指定自定义报错信息
# 5、校验规则的执行顺序？？
#   对字段类型进行校验--》依次执行validators列表中的校验规则--》从右到左依次验证其他规则--》调用单字段校验方法

def is_contains_keyword(value):
    if '项目' not in value:
        raise serializers.ValidationError('项目名称中必须包含【项目】关键字')


class ProjectSerializer(serializers.Serializer):
    """
    定义序列化器类：
    c、必须继承Serializers类
    d、定义的序列化器类中，字段名要与模型类中的字段名保持一致
    e、定义的序列化器的字段（类属性）为field子类
    f、默认定义哪些字段，那么那些字段返回给前端
    h、常用的序列化字段类型：Iter、char、BOol、Date
    i、可以在序列化器字段值中指定不同的选项：(label='项目id', help_text='项目ID', max_value=1000, min_value=1)
    g、默认定义哪些字段，前端必须传递哪些字段。这些字段也会输出

    9、定义的序列化器字段中，required默认为True，说明默认定义的字段必须得输入和输出
    如果在序列化器中，设置required=FALSE，那么前端用户可以不用传递该字段（校验时会忽略该字段，所以不会报错）
    -如果未定义某个模型中的字段，那么该字段不会输入，也不会输出
    -前端必须输入该字段name，但必须进行反序列化输出(, write_only=True---只写进行判断，不返回)
    如果，在序列化器中定义的字段，默认allow_null=False--不允许输入null；；如果为True，则该字段允许传null
    13、在序列化器中，定义CharField字段，默认allow_blank=True,可以为空
    14、default参数可以指定默认值

    """
    # id = serializers.IntegerField(label='项目id', help_text='项目ID', max_value=1000, min_value=1)
    # 可以在序列化器字段上使用validators指定自定义的校验规则
    # 2、validators必须是序列类型（列表），在列表中可以添加多个校验规则
    # 3、DRF框架自带UniqueValidator校验器，必须得使用queryset指定查询集对象，用于对该字段进行校验
    # 4、UniqueValidator校验器，可以使用msg指定自定义报错信息
    name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=20,
                                 min_length=5, write_only=False, allow_null=False,
                                 error_messages={'min_length': '名称过短不能少于5位',
                                                 'max_value': '超过最大长度限制'},
                                 validators=[UniqueValidator(queryset=Projects.objects.all(),
                                                             message='项目名称不能重复'), is_contains_keyword])
    leader = serializers.CharField(label='项目负责人', help_text='项目负责人')
    is_excue = serializers.BooleanField()

    # 1、如果定义了一个模型类中没有的字段，并且该字段需要输出（序列化输出）
    # 2、需要在create方法、update方法中的模型对象上，添加动态的属性即可
    # token = serializers.CharField(read_only=True)

    # 3、如果定义了一个模型类中没有的字段，并且该字段需要输入（反序列化输入）
    # 4、需要在create方法、update方法之前pop（）掉
    # sms_code = serializers.CharField(write_only=True)

    # 1、DateTimeField 可以使用format参数指定格式化字符
    # 2、可以任意使用序列化的字段，自定义错误提示信息
    # 3、使用校验选项名，作为key，自定义msg错误信息
    update_time = serializers.DateTimeField(label='更新时间', help_text='更新时间',
                                            format='%Y-%m-%d %H:%M:%S',
                                            error_messages={'required': 'updatetime该字段必填'}, required=False)
    # 一、关联字段（从表字段）
    # 1、可以定义PrimaryKeyRelatedField来关联表的外键值
    # 2、如果通过【父表获取从表】数据，需要使用从表模型类名小写_set 作为序列化器类中的关联字段名称
    # 3、如果在定义模型类的外键字段时，指定了 releated_name参数，那么会把releated_name参数名作为序列化器的字段返回
    # 4、PrimaryKeyRelatedField字段，指定read_only=True，或者指定queryset参数，否则会报错
    # 5、如果知道read_only=true,那么该字段序列化输出
    interToP = serializers.PrimaryKeyRelatedField(label='项目所属接口id', help_text='项目所属接口-1id'
                                                        , read_only=True, many=True)

    #     , queryset=Interfaces.objects.all()

    # 1、使用StringRelatedField字段，将关联字段模型类中的__str__方法返回值作为该字段的值
    # 2、StringRelatedField添加 many=True，该字段仅序列化输出
    # interfaces_set = serializers.StringRelatedField( many=True)

    # 2、使用SlugRelatedField字段，将关联模型类中的某个字段，作为该字段的返回值.
    # 2、添 many = True，该字段仅序列化输出.
    # 3、如果该字段需要进行反序列化输入，那必须指定queryset参数，同时关联字段必须有唯一约束.
    # interfaces_set = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Interfaces.objects.all()).

    # interfaces_set = InterfaceSerializer

    # 可以在序列化器类中对单个字段进行校验
    # 2、单字段的校验方法名称，必须把validate_字段名称，如：validate_name--对name校验
    # 3、如果校验不通过，必须返回serializers.ValidationError('项目名称必须以【项目】结尾')异常
    # 4、如果校验通过，通常需要将校验的字段返回
    # 5、如果该地段在定义时添加的校验规则不通过，则不会调用自定义的校验方法
    def validate_name(self, attr: str):
        if not attr.endswith('项目'):
            raise serializers.ValidationError('项目名称必须以【项目】结尾')
        return attr

    # 1、可以在序列化器类中对多个字段进行联合校验
    # 2、使用固定的validate，会接收上面校验通过之后的字典数据
    # 3、当所有字段定义时添加的校验规则都通过，且每个字典的单字段校验方法通过的情况下，才会调用validate
    def validate(self, attrs):
        if len(attrs.get('leader')) <=4 or not attrs.get('is_excue'):
            raise serializers.ValidationError('项目名称不能少于4位、leader必须存在')
        return attrs

    def to_internal_value(self, data):
        """
        date：2024-1-28-

        """
        # 1、to_internal_value方法，是所有字段开始校验时入口方法（最先调用的方法）
        # 2、会依次对序列化器类的各个序列化器字段进行校验：
        #  对字段类型进行校验--》依次执行validators列表中的校验规则--》从右到左依次验证其他规则--》调用单字段校验方法
        # to_internal_value调用结束后，会调用validate方法
        tmp = super().to_internal_value(data)
        # 对各个单字段校验结束后的数据进行修改
        return tmp

    def to_representation(self, instance):
        # 1、to_representation，是所有字段开始校验时入口方法（最先调用的方法）
        # 2|会一次对序列化器类的各个序列化器字段进行校验
        #  -对字段类型进行校验--》依次验证validators列表中的校验规则--》从右到左依次验证其他规则--》调用单字段校验方法
        # to_internal_value调用结束---》调用多字段联合校验方法validate方法

        tmp = super().to_representation(instance)
        # 对各个单字段校验结束之后的数据进行修改
        return tmp

    def create(self, validated_data: dict):
        myname = validated_data.pop('myname')
        myage = validated_data.pop('myage')
        # validated_data.pop('sms_code')
        project_obj = Projects.objects.create(**validated_data)
        # project_obj.token = "XXXcode"
        return project_obj

    def update(self, instance, validated_data):
        # 同时传递Instance和data参数时，会调用update方法
        instance.name = validated_data.get('name') or instance.name
        instance.leader = validated_data.get('leader') or instance.leader
        instance.desc = validated_data.get('desc') or instance.desc
        instance.is_excue = validated_data.get('is_excue') or instance.is_excue
        instance.save()
        return instance


class ProjectModelSerializer(serializers.ModelSerializer):
    """
    可以模型序列化器类
    1、继承serializers.ModelSerializer类或其子类
    2、需要在meta内部指定model、fields
    3、model指定模型类（需要生成序列化器的模型类）
    4、fields指定模型类中哪些字段需要自动生成序列化器字段
    5、会给id主键、有指定auto_now_add
    """
    # 修改自动生成的序列化器字段-todo：参考课程20210521_模型序列化器
    # 方式一：
    # a、可以重新定义模型类中同名的字段；；
    # b、自定义字段的优先级会更高(会覆盖自动生成的序列化器字段)
    #
    name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=20,
                                 min_length=5, write_only=False, allow_null=False,
                                 error_messages={'min_length': '名称过短不能少于5位',
                                                 'max_value': '超过最大长度限制'},
                                 validators=[UniqueValidator(queryset=Projects.objects.all(),
                                                             message='项目名称不能重复'), is_contains_keyword])
    # 定义关联字段
    interfaces_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    token = serializers.CharField(read_only=True)
    class Meta:
        model = Projects
        # fields = "__all__"   # 指定模型类中的所有字段
        # fields元祖中必须指定进行序列化或反序列化操作的所有字段名称，其他的字段需要转化
        fields = ("id", "name", 'leader', 'interfaces_set', 'token')  # 指定部分模型类中的字段
        # exclude = ('desc')  # 【排除字段】可以指定exclude模型类中哪些字段不需要序列化字段
        extra_kwargs={
            'leader':{
                'label':'负责人',
                'max_length':2,
                'read_only':True,
            },
            'is_excue':{
                'required':True
            }
        }

    def create(self, validated_data):
        """
        a、继承Serializer之后，ModelSerializer中实现了createhe update方法
        b、如果父类提供的create和update方法不满足需要时，可以重写create和update方法，最后调用父类的create方法

        """
        validated_data.pop('myname')
        validated_data.pop('myage')
        instance = super().create(validated_data)
        instance.token = 'token--XX'
        return instance