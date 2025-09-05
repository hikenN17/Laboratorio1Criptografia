from scapy.all import sniff, ICMP, Raw
import re
from wordfreq import zipf_frequency
import threading

message = []
stop_capture = False  # Variable global para detener sniff

def handle_packet(pkt):
    if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
        if pkt[ICMP].type == 8:  # Echo Request
            data = pkt[Raw].load
            if len(data) >= 1:
                message.append(data[:1].decode(errors="ignore"))
                print("Texto Capturado:", data[:1].decode(errors="ignore"))

def caesar_bruteforce(text):
    results = []
    for shift in range(26):
        decrypted = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                decrypted.append(chr((ord(ch) - base - shift) % 26 + base))
            else:
                decrypted.append(ch)
        results.append(("Shift %2d" % shift, "".join(decrypted)))
    return results

def frequency_heuristic(results, language="es"):
    best_score = -1
    best_idx = 0
    for i, (_, text) in enumerate(results):
        words = re.findall(r"[a-zA-Záéíóúüñ]+", text.lower())
        score = sum(zipf_frequency(word, language) for word in words)
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx

def print_results(results, probable_idx):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    for i, (title, text) in enumerate(results):
        if i == probable_idx:
            print(f"{GREEN}{title}: {text}{RESET}")
        else:
            print(f"{title}: {text}")

def wait_for_exit():
    global stop_capture
    while True:
        entry = input()
        if entry.strip().lower() == "salir":
            stop_capture = True
            break

if __name__ == "__main__":
    print("Listening for ICMP packets... (esciba 'salir' y presione ENTER para finalizar)")
    thread = threading.Thread(target=wait_for_exit, daemon=True)
    thread.start()
    while not stop_capture:
        sniff(filter="icmp", prn=handle_packet, store=0, timeout=1)
    message_str = "".join(message)
    print("\n---- Texto por descifrar ----")
    print(message_str)
    results = caesar_bruteforce(message_str)
    probable_idx = frequency_heuristic(results, language="es")
    print("\n---- Posibles textos originales ----")
    print_results(results, probable_idx)
    print("\n---- Texto Original Mas Probable ----")
    print(f"{results[probable_idx][1]}")