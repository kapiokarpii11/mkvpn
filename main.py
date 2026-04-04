import requests
import urllib.parse
import re

# Ссылочки, откуда берем вкусняшки 🍰
URLS = [
    "https://sub.obbhod.online/sub",
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

def is_russian_server(link):
    # Декодируем ссылку, чтобы смайлики и русские буквы читались нормально 🔍
    decoded_link = urllib.parse.unquote(link).lower()
    
    # Ищем наши запрещенные словечки 🚫
    bad_words = ['russia', 'россия', '🇷🇺']
    
    for word in bad_words:
        if word in decoded_link:
            return True
            
    # Ищем точное слово "ru", чтобы не задеть другие страны с этими буквами 🌍
    if re.search(r'\bru\b', decoded_link):
        return True
        
    return False

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

    # 2. Оставляем только VPN-ссылки и фильтруем 🧹
    valid_protocols = ('vless://', 'vmess://', 'trojan://', 'ss://', 'ssr://', 'hysteria://', 'hysteria2://', 'tuic://')
    filtered_links = []
    
    for link in raw_links:
        link = link.strip()
        if link.startswith(valid_protocols):
            
            # Проверяем, не спряталась ли тут Россия 🇷🇺🚫
            if not is_russian_server(link):
                
                # Магия замены наших любимых ящерок! 🥭🔥 -> 🦎
                link = link.replace('🥭', '🦎').replace('🔥', '🦎')
                
                # На всякий случай заменяем и закодированные версии этих смайликов, если они есть ✨
                link = link.replace('%F0%9F%A5%AD', '🦎').replace('%F0%9F%94%A5', '🦎')
                
                filtered_links.append(link)

    # 3. Сохраняем результат в файл `sub.txt` 💾
    with open('sub.txt', 'w', encoding='utf-8') as f:
        f.write(HEADER)
        for link in filtered_links:
            f.write(link + '\n')
    
    print(f"Готово, зайка! ✨ Собрано {len(filtered_links)} отличных серверов без России! 🥰")

if __name__ == '__main__':
    main()
