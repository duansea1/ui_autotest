"""
-------------------------------------------------
   File Name：   RSAUtil
   Description:  PYTHON-RSA 加密/解密、加签/验签
   Author:       CANGMU
   date：        2024/5/27
-------------------------------------------------
"""
import base64
import binascii
import hashlib
import logging

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
import rsa

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


class RSAUtil:

    def __init__(self, pfx_path, pfxpass, cer_path):
        """
        pfx_path: 私钥路径
        pfxpass: 私钥密码
        cer_path: 公钥liking
        """
        self.pfx_path = pfx_path
        self.pfxpass = pfxpass
        self.cer_path = cer_path

    def load_key(self, cert_file_path, password=None):
        """Load a key from a file, supporting PEM and PKCS#12 formats."""
        try:
            with open(cert_file_path, 'rb') as f:
                cert_data = f.read()

            if cert_file_path.endswith(('.pfx', '.p12')):
                private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                    cert_data,
                    password.encode() if password else None,
                    backend=default_backend()
                )
                pri_key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode()
                return rsa.PrivateKey._load_pkcs1_pem(pri_key_pem)
            else:
                certificate = x509.load_pem_x509_certificate(cert_data, backend=default_backend())
                pub_key_pem = certificate.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode()
                return rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_pem)
        except Exception as e:
            logger.error(f"Failed to load key from {cert_file_path}: {e}")
            raise

    def _chunk_data(self, data, chunk_size):
        while data:
            yield data[:chunk_size]
            data = data[chunk_size:]

    def pri_encrypt(self, encrypt_text):
        """Encrypt data using an RSA private key."""
        key = self.load_key(self.pfx_path, self.pfxpass)
        block_size = key.n.bit_length() // 8 - 11
        key_length = key.n.bit_length() // 8
        encrypt_text = base64.b64encode(encrypt_text.encode('utf-8'))
        out_data = bytes()

        for chunk in self._chunk_data(encrypt_text, block_size):
            chunk = rsa.pkcs1._pad_for_signing(chunk, key_length)
            num = rsa.transform.bytes2int(chunk)
            encrypted = rsa.core.encrypt_int(num, key.d, key.n)
            encrypted_bytes = rsa.transform.int2bytes(encrypted)

            # 确保加密数据填充前导零以匹配密钥长度
            pad_length = key_length - len(encrypted_bytes)
            padded_data = b'\x00' * pad_length + encrypted_bytes

            out_data += padded_data

        return out_data.hex()

    def pub_decrypt(self, decrypt_text):
        """Decrypt data using an RSA public key."""
        key = self.load_key(self.cer_path)
        block_size = key.n.bit_length() // 8
        decrypt_text = binascii.unhexlify(decrypt_text)
        out_data = bytes()

        for chunk in self._chunk_data(decrypt_text, block_size):
            num = rsa.transform.bytes2int(chunk)
            decrypted = rsa.core.decrypt_int(num, key.e, key.n)
            out_data += rsa.transform.int2bytes(decrypted)

        return base64.b64decode(out_data).decode('utf-8')

    def pub_encrypt(self, encrypt_text):
        """Encrypt data using an RSA public key."""
        key = self.load_key(self.cer_path)
        block_size = key.n.bit_length() // 8 - 11
        encrypt_text = base64.b64encode(encrypt_text.encode('utf-8'))
        out_data = bytes()

        for chunk in self._chunk_data(encrypt_text, block_size):
            encrypted = rsa.pkcs1.encrypt(chunk, key)
            out_data += encrypted

        return out_data.hex()

    def pri_decrypt(self, decrypt_text):
        """Decrypt data using an RSA private key."""
        key = self.load_key(self.pfx_path, self.pfxpass)
        block_size = key.n.bit_length() // 8
        decrypt_text = binascii.unhexlify(decrypt_text)
        out_data = bytes()

        for chunk in self._chunk_data(decrypt_text, block_size):
            decrypted = rsa.pkcs1.decrypt(chunk, key)
            out_data += decrypted

        return base64.b64decode(out_data).decode('utf-8')

    def sign_with_sha1(self, sign_text):
        """SHA1:Sign data using an RSA private key."""
        key = self.load_key(self.pfx_path, self.pfxpass)
        hash_value = hashlib.sha1(sign_text.encode('utf-8')).digest()
        signature = rsa.sign(hash_value, key, 'SHA-1')
        return binascii.hexlify(signature).decode()

    def verify_with_sha1(self, data, signature):
        """SHA1:Verify the signature of data using an RSA public key."""
        key = self.load_key(self.cer_path)
        hash_value = hashlib.sha1(data.encode('utf-8')).digest()
        try:
            rsa.verify(hash_value, binascii.unhexlify(signature), key)
            logger.info("SHA-1 Signature verification passed.")
            return True
        except rsa.VerificationError:
            logger.error("Signature verification failed.")
            return False

    def sign_with_sha256(self, sign_text):
        """SHA256:Sign data using an RSA private key."""
        key = self.load_key(self.pfx_path, self.pfxpass)
        hash_value = hashlib.sha256(sign_text.encode('utf-8')).digest()
        signature = rsa.sign(hash_value, key, 'SHA-256')
        return binascii.hexlify(signature).decode()

    def verify_with_sha256(self, data, signature):
        """SHA256:Verify the signature of data using an RSA public key."""
        key = self.load_key(self.cer_path)
        hash_value = hashlib.sha256(data.encode('utf-8')).digest()
        try:
            rsa.verify(hash_value, binascii.unhexlify(signature), key)
            logger.info("SHA-256 Signature verification passed.")
            return True
        except rsa.VerificationError:
            logger.error("SHA-256 Signature verification failed.")
            return False


# Example usage:
if __name__ == '__main__':
    testData = 'send_time=2018-01-24 13:25:33&msg_id=456795112&version=4.0.0.0&123=100000949&txn_type=03&member_id=100000749&user_id=123'
    pfx_path = 'C:\\Users\段海洋\\myfiles\\auto_files\\ui_autotest\\2022ui_autotest\\demo\\API_demo\KuaJing\\tools\\key_5181240821000008798@@2408281533000001302.pfx'
    pfxpass = '5181240821000008798_774480'
    cer_path = 'C:\\Users\段海洋\\myfiles\\auto_files\\ui_autotest\\2022ui_autotest\\demo\\API_demo\\KuaJing\\tools\\key_5181240821000008798@@2408281533000001302.cer'

    rsa_util = RSAUtil(pfx_path, pfxpass, cer_path)

    pri_en = rsa_util.pri_encrypt(testData)
    print("私钥加密内容：{}".format(pri_en))
    print("公钥解密内容：{}".format(rsa_util.pub_decrypt(pri_en)))

    pub_en = rsa_util.pub_encrypt(testData)
    print("公钥加密内容：{}".format(pub_en))
    print("私钥解密内容：{}".format(rsa_util.pri_decrypt(pub_en)))

    sha1_signature = rsa_util.sign_with_sha1(testData)
    print("私钥签名内容：{}".format(sha1_signature))
    print(rsa_util.verify_with_sha1(testData, sha1_signature))

    sha256_signature = rsa_util.sign_with_sha256(testData)
    print("私钥签名内容：{}".format(sha256_signature))
    print(rsa_util.verify_with_sha256(testData, sha256_signature))