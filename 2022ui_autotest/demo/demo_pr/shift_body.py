# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-03 14:16
# ---
import re
body = {"AGENT_REGISTER_MERCHANT_QUERY","/merchant/register",{"success":"true","result":"{\"applyNo\":\"202311071511160620021401\",\"merchantName\":\"深圳市都美服装有限责任公司\",\"merchantNo\":\"805001911185\",\"merchantShortName\":\"都美\",\"respCode\":\"APPLY_SUCCESS\",\"respMsg\":\"受理成功\",\"resultList\":[{\"applyStatus\":\"AUDIT\",\"businessType\":\"1\",\"seqNo\":\"202311071511178740021404\"},{\"applyStatus\":\"AUDIT\",\"businessType\":\"2\",\"seqNo\":\"202311071511179100021409\"},{\"applyStatus\":\"AUDIT\",\"businessType\":\"3\",\"seqNo\":\"202311071511179030021407\"}],\"status\":\"PROCESSING\",\"storeNo\":\"2000005001921158\",\"transNo\":\"fU0BjyNqhe70580412031239929857\"}","errorCode":null,"errorMsg":null,"sign":"13748f1d8f61f7ce6f84c51b91b29b82981619175c64b7439c60de449d566be70be68cf8f5c4c6d537904cf33478365ff15addbbb76968398b0f9c96677e78cece81de9c7fbc599f9355523e36a304477d824d4dbe53a2b083d93da5b5749bd4d093740982b1537aa43d668dd1edf486abdcbafed5d1556b75215c2dc4723953"}}
print(body)
print(str(body).encode('utf-8').decode('unicode_escape'))


