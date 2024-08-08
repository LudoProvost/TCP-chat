import socket
import argparse


def launch_server(ip, port, name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print("Waiting for a client to connect...")
        conn, addr = s.accept()
        with conn:
            # print(f"connected by {addr}")

            messager_name = conn.recv(1024).decode("utf-8")
            try:
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if data == "":
                        print("Client disconnected, terminating connection.")
                        conn.close()
                        exit()
                    print(messager_name, "\b:", data)
                    message_to_send = input("Enter the message you want to send: ")
                    message_bytes = message_to_send.encode("utf-8")
                    conn.sendall(message_bytes)
            except KeyboardInterrupt:
                conn.close()
                print("connection terminated.")


def launch_client(ip, port, name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        # send name and receive server name
        name_bytes = name.encode("utf-8")
        s.sendall(name_bytes)
        try:
            while True:
                message_to_send = input("Enter the message you want to send: ")
                message_bytes = message_to_send.encode("utf-8")
                s.sendall(message_bytes)
                data = s.recv(1024).decode("utf-8")
                if data == "":
                    print("Connection closed.")
                    s.close()
                    exit()
                print("Server:", data)
        except KeyboardInterrupt:
            s.close()
            print("Connection terminated.")


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--client")
parser.add_argument("-l", "--listen")
parser.add_argument("-n", "--name")

args = parser.parse_args()


# detect server
if args.listen is not None:
    ip_port = args.listen.split(":")
    launch_server(ip_port[0], int(ip_port[1]), args.name)

# detect client
elif args.client is not None:
    ip_port = args.client.split(":")
    launch_client(ip_port[0], int(ip_port[1]), args.name)

else:
    print("wrong inputs")
