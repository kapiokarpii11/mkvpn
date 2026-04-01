import requests
import re
import socket
import time

# Ссылочки, откуда берем вкусняшки 🍰
URLS = [
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/WHITELIST-ALL.txt",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/refs/heads/main/kizyakbeta6.txt",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/refs/heads/main/kizyaktestru.txt"
]

# Наш красивый заголовок для подписки 🎀
HEADER = """#profile-title: WRWR VPN🦎
#profile-desc: ura
#profile-description:🦎🦎🦎🦎🦎🦎
#profile-serverDescription: yeehaw
#profile-update-interval: 3
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=0;
#support-url: https://t.me/@RageTrip
#profile-web-page-url: https://t.me/@RageTrip
"""

def extract_host(link):
    # Ищем домен или IP-адрес в ссылке 🔍
    match = re.search(r'://(?:[^@/]+@)?([^:/?#]+)', link)
    if match:
        return match.group(1)
    return None

def resolve_ip(host):
    # Превращаем домен в IP-адрес 🪄
    try:
        return socket.gethostbyname(host)
    except:
        return None

def check_country_batch(ips):
    # Проверяем страны через бесплатный API (по 100 штук за раз, чтобы было быстро!) 🌍
    url = "http://ip-api.com/batch"
    result_ru = set()
    for i in range(0, len(ips), 100):
        batch = [{"query": ip} for ip in ips[i:i+100]]
        try:
            res = requests.post(url, json=batch).json()
            for record in res:
                # Если страна RU, то запоминаем этого хулигана 🚫
                if record.get("status") == "success" and record.get("countryCode") == "RU":
                    result_ru.add(record.get("query"))
        except Exception as e:
            print(f"Ой, ошибочка с API: {e} 😿")
        time.sleep(1) # Немного ждем, чтобы нас не заблокировали 🌸
    return result_ru

def main():
    raw_links = []
    
    # 1. Скачиваем все тексты 📥
    for url in URLS:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                raw_links.extend(resp.text.splitlines())
        except Exception as e:
            print(f"Ой, не удалось скачать {url}: {e} 🥺")

    # 2. Оставляем только VPN-ссылки (никаких текстовых комментариев!) 🧹
    valid_protocols = ('vless://', 'vmess://', 'trojan://', 'ss://', 'ssr://', 'hysteria://', 'hysteria2://', 'tuic://')
    filtered_links = []
    
    for link in raw_links:
        link = link.strip()
        if link.startswith(valid_protocols):
            # Магия замены! 🥭🔥 -> 🦎
            link = link.replace('🥭', '🦎').replace('🔥', '🦎')
            filtered_links.append(link)

    # 3. Вытаскиваем IP адреса для проверки 🕵️‍♀️
    link_data = []
    ips_to_check = set()
    
    for link in filtered_links:
        host = extract_host(link)
        if host:
            ip = resolve_ip(host)
            if ip:
                ips_to_check.add(ip)
                link_data.append({'link': link, 'ip': ip})
            else:
                # Если не смогли узнать IP, оставляем ссылочку на всякий случай ✨
                link_data.append({'link': link, 'ip': None})

    # 4. Ищем сервера из РФ 🇷🇺🚫
    print(f"Проверяю {len(ips_to_check)} уникальных IP... Жди, котик! ⏳")
    ru_ips = check_country_batch(list(ips_to_check))

    # 5. Собираем финальный чистенький списочек 🛁
    final_links = []
    for item in link_data:
        if item['ip'] not in ru_ips:
            final_links.append(item['link'])

    # 6. Сохраняем результат в файл `sub.txt` 💾
    with open('sub.txt', 'w', encoding='utf-8') as f:
        f.write(HEADER)
        for link in final_links:
            f.write(link + '\n')
    
    print(f"Готово, зайка! ✨ Собрано {len(final_links)} отличных серверов! 🥰")

if __name__ == '__main__':
    main()
