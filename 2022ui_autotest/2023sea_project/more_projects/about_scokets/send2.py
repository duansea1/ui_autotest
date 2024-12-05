# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-06-05 9:52
# ---
import socket
import time

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    messages = [f"Message {i}".encode() for i in range(10)]  # 创建10个数据包
    window_size = 4
    base = 0
    next_seq_num = 0
    timeout = 1.0

    try:
        client_socket.settimeout(timeout)
        while base < len(messages):
            while next_seq_num < base + window_size and next_seq_num < len(messages):
                # 发送新的数据包
                msg = f"{next_seq_num:010d}".encode() + messages[next_seq_num]
                client_socket.sendto(msg, server_address)
                print(f"Sent: {messages[next_seq_num].decode()} with seq {next_seq_num}")
                next_seq_num += 1

            try:
                # 接收ACK
                ack, _ = client_socket.recvfrom(2048)
                ack_num = int(ack.decode().split()[1])
                print(f"Received ACK for {ack_num}")
                base = ack_num + 1
            except socket.timeout:
                print("Timeout, resending window")
                next_seq_num = base  # 重置序列号为窗口的基底
    finally:
        client_socket.close()

if __name__ == "__main__":
    udp_client()