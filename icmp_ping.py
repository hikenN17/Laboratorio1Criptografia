#!/usr/bin/env python3
from scapy.all import IP, ICMP, send
import argparse

def send_message_icmp(dest_ip: str, message: str):
    """
    Envía un mensaje carácter por carácter en paquetes ICMP (Echo Request).
    - `dest_ip`: dirección IP destino (ej. 8.8.8.8)
    - `message`: texto a enviar (ya cifrado previamente si corresponde)
    """
    print(f"[INFO] Texto a enviar   : {message}")
    print(f"[INFO] Enviando a       : {dest_ip}")
    for ch in message:
        pkt = IP(dst=dest_ip)/ICMP()/ch.encode()
        send(pkt, verbose=False)
        print(f"[DEBUG] Enviado paquete con payload: {ch!r}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enviar texto dentro de paquetes ICMP")
    parser.add_argument("dest_ip", help="Dirección IP de destino (ej: 8.8.8.8)")
    parser.add_argument("text", help="Texto a enviar (si tiene espacios, usar comillas)")
    args = parser.parse_args()

    send_message_icmp(args.dest_ip, args.text)
