"""
@Author    : team
@Date      : 2025/6/5 09:51
@Description: [文件功能的简要描述]
"""

import datetime
import re
import os
import hashlib

# SQL 模板
sql_template = """
INSERT INTO BAOFU_CGW.T_CHANNEL_EXTERNAL_ACCOUNT (RECORD_NO, CHANNEL_ID, IDENTITY, BANK_NAME, BANK_ACCOUNT_NAME,
                                                  BANK_ACCOUNT_NO, BANK_ACCOUNT_CCY, BANK_ACCOUNT_TYPE, BANK_CODE,
                                                  BANK_SUB_CODE, ACCOUNT_PROPERTIES, ROUTING_CODE, ROUTING_CODE_TYPE,
                                                  SWIFT_CODE, BANK_COUNTRY, BANK_ADDRESS, PAYEE_ADDRESS,
                                                  MIDDLE_BANK_SWIFT_CODE, MIDDLE_BANK_NAME, RESERVE_FIELD_ONE,
                                                  RESERVE_FIELD_TWO, RESERVE_FIELD_THREE, BANK_IBAN_NO, BANK_PAYEE_NO,
                                                  REMIT_REFERENCE, STATUS, REMARKS, CREATE_AT, CREATE_BY, UPDATE_AT,
                                                  UPDATE_BY, RESERVE_FIELD_FOUR, BANK_IDENTIFIER)
VALUES ('##RECORD_NO', '##CHANNEL_ID', '##IDENTITY', 'DEFAULT BANK NAME', null, '##BANK_ACCOUNT_NO', '##BANK_ACCOUNT_CCY', '##BANK_ACCOUNT_TYPE',
        null, null, null, null, null, null, '##BANK_COUNTRY', null, null, null, null,
        null, null, null, null, '##BANK_ACCOUNT_NO', null, '0', null, now(),
        'null', now(), 'null', null, null);
"""


class AccountNumberGenerator:
    """银行账号生成器"""
    PREFIX = "79900"
    MAX_LENGTH = 11

    @classmethod
    def generate(cls, base_no: str, identity: str) -> str:
        """生成符合要求的银行账号"""
        if identity != "CHANNEL_DBS":
            return base_no

        # 确保总长度不超过15位
        available_length = cls.MAX_LENGTH - len(cls.PREFIX)
        unique_part = cls._generate_unique_part(base_no, available_length)
        return f"{cls.PREFIX}{unique_part}"

    @staticmethod
    def _generate_unique_part(base_no: str, max_length: int) -> str:
        """生成唯一标识部分"""
        # 使用哈希确保唯一性同时控制长度
        hash_obj = hashlib.sha256(base_no.encode())
        hash_hex = hash_obj.hexdigest()

        # 取适当长度的数字部分
        digits = "".join([c for c in hash_hex if c.isdigit()])
        if len(digits) >= max_length:
            return digits[:max_length]

        # 如果数字不足，补充字母转换的数字
        supplement = "".join([str(ord(c) % 10) for c in hash_hex if c.isalpha()])
        return (digits + supplement)[:max_length]


def get_unique_time(index: int) -> str:
    """生成唯一时间戳"""
    now = datetime.datetime.now()
    timestamp = now + datetime.timedelta(milliseconds=index)
    return timestamp.strftime("%Y%m%d%H%M%S%f")[:17]  # 截取到毫秒位


def get_user_inputs() -> dict:
    """收集用户输入"""
    params = set(re.findall(r"##([A-Z_]+)", sql_template))
    params.discard("RECORD_NO")
    params.discard("BANK_ACCOUNT_NO")

    print("BANK_ACCOUNT_TYPE: 1:电商、2：GEP收款、3：B2B、4：服贸")
    print("IDENTITY: 格式为：CHANNEL_DBS等")
    print("CHANNEL_ID: 格式为：渠道编号")
    print("BANK_COUNTRY: 格式为：国家编号")
    print("\n请输入以下字段值：")
    return {param: input(f"{param}：").strip() for param in sorted(params)}


def generate_sql_statements(count: int, user_inputs: dict) -> list:
    """生成SQL语句列表"""
    sql_lines = []
    for i in range(count):
        line = sql_template
        timestamp = get_unique_time(i)
        record_no = timestamp
        base_account_no = timestamp

        bank_account_no = AccountNumberGenerator.generate(
            base_account_no,
            user_inputs["IDENTITY"]
        )

        line = line.replace("##RECORD_NO", record_no)
        line = line.replace("##BANK_ACCOUNT_NO", bank_account_no)

        for key, value in user_inputs.items():
            line = line.replace(f"##{key}", value)

        sql_lines.append(line.strip())
    return sql_lines


def write_to_file(sql_lines: list, file_path: str) -> None:
    """将SQL语句写入文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))
    print(f"\n✅ SQL 脚本已生成，文件路径：{file_path}")


def main():
    """主程序"""
    try:
        user_inputs = get_user_inputs()
        count = int(input("\n请输入要生成的记录条数："))

        if count <= 0:
            raise ValueError("记录条数必须大于0")

        sql_lines = generate_sql_statements(count, user_inputs)
        output_file = os.path.join(os.getcwd(), "generated_insert.sql")
        write_to_file(sql_lines, output_file)

        print(f"共生成 {count} 条记录")
        print("银行账号生成规则：")
        print("- CHANNEL_DBS: 前缀79900+唯一标识(总长度15位)")
        print("- 其他: 使用原始时间戳")

    except ValueError as e:
        print(f"输入错误: {e}")
    except Exception as e:
        print(f"程序出错: {e}")


if __name__ == "__main__":
    main()