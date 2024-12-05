# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-06-05 9:50
# ---
import socket


def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))

    expected_seq = 0
    while True:
        packet, client_address = server_socket.recvfrom(2048)
        seq_number = int(packet[:10].decode().strip())
        data = packet[10:]

        if seq_number == expected_seq:
            print(f"Received in-order packet: {data.decode()} with seq {seq_number}")
            # 发送ACK
            ack = f"ACK {seq_number}".encode()
            server_socket.sendto(ack, client_address)
            expected_seq += 1
        else:
            print(f"Received out-of-order packet: {data.decode()} with seq {seq_number}")


if __name__ == "__main__":
    udp_server()