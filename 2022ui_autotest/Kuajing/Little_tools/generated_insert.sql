INSERT INTO BAOFU_CGW.T_CHANNEL_EXTERNAL_ACCOUNT (RECORD_NO, CHANNEL_ID, IDENTITY, BANK_NAME, BANK_ACCOUNT_NAME,
                                                  BANK_ACCOUNT_NO, BANK_ACCOUNT_CCY, BANK_ACCOUNT_TYPE, BANK_CODE,
                                                  BANK_SUB_CODE, ACCOUNT_PROPERTIES, ROUTING_CODE, ROUTING_CODE_TYPE,
                                                  SWIFT_CODE, BANK_COUNTRY, BANK_ADDRESS, PAYEE_ADDRESS,
                                                  MIDDLE_BANK_SWIFT_CODE, MIDDLE_BANK_NAME, RESERVE_FIELD_ONE,
                                                  RESERVE_FIELD_TWO, RESERVE_FIELD_THREE, BANK_IBAN_NO, BANK_PAYEE_NO,
                                                  REMIT_REFERENCE, STATUS, REMARKS, CREATE_AT, CREATE_BY, UPDATE_AT,
                                                  UPDATE_BY, RESERVE_FIELD_FOUR, BANK_IDENTIFIER)
VALUES ('20250612103708538', '1200923023', 'CHANNEL_DBS', 'DEFAULT BANK NAME', null, '79900911836', 'VND', '1',
        null, null, null, null, null, null, 'VNM', null, null, null, null,
        null, null, null, null, '79900911836', null, '0', null, now(),
        'null', now(), 'null', null, null);