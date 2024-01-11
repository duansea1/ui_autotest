# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-12-18 14:16
# ---

# TODO 新增不同场景的连签数据-2023.12.18
"""
工具1：新增连签数据
================实现说明：=======================
1、先查member表，查到符合条件的会员id：企微客户且是会员
2、zw_kyd_member_check_in表新增该会员的签到数据：member_no prog_day、last_date、last_prog_date、first_prog_date、is_max_prog_cycle
INSERT INTO `ucenter`.`zw_kyd_member_check_in`(`id`, `tenant_id`, `corp_id`, `member_no`, `prog_day`, `last_date`, `last_prog_date`, `first_prog_date`, `is_max_prog_cycle`, `is_deleted`, `created_at`, `updated_at`, `deleted_at`) VALUES (1, 237, 320, '540133129594068993', 5, '2023-12-17', '2023-12-17', '2023-12-13', 2, 2, '2023-12-14 15:48:03', '2023-12-18 13:54:28', NULL);

3、zw_kyd_member_check_in_record表新增签到数据，注意prog_day的变化
INSERT INTO `ucenter`.`zw_kyd_member_check_in_record`(`id`, `tenant_id`, `corp_id`, `member_no`, `check_date`, `is_prog_check`, `prog_day`, `reward`, `prog_reward`, `is_deleted`, `created_at`, `updated_at`, `deleted_at`) VALUES (1, 237, 320, '540133129594068993', '2023-12-10', 2, 1, 1, 0, 2, '2023-12-14 15:48:03', '2023-12-14 17:05:57', NULL);

4、zw_kyd_member_check_in_reward-记录积分奖励的赠送、send_type需要区分send_time、、send_state
INSERT INTO `ucenter`.`zw_kyd_member_check_in_reward`(`id`, `tenant_id`, `corp_id`, `member_no`, `check_date`, `type`, `prog_day`, `reward`, `send_type`, `send_time`, `send_state`, `attempt`, `reason`, `is_deleted`, `created_at`, `updated_at`, `deleted_at`) VALUES (19, 237, 320, '540133129594068993', '2023-12-17', 1, 5, 1, 1, '2023-12-17 10:32:38', 2, 0, '', 2, '2023-12-17 10:32:38', '2023-12-18 13:52:50', NULL);


"""

