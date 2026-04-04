import requests
import urllib.parse
import re
import base64

# Ссылочки, откуда берем вкусняшки 🍰
URLS = [
    "https://sub.obbhod.online/sub",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/refs/heads/main/kizyakbeta6.txt",
    "https://gitverse.ru/api/repos/bywarm/rser/raw/branch/master/selected.txt",
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

def decode_base64_if_needed(text):
    # Пытаемся раскодировать base64 🪄
    try:
        clean_text = text.strip()
        # Добавляем выравнивание (padding), если его не хватает для правильной расшифровки
        padding = len(clean_text) % 4
        if padding:
            clean_text += '=' * (4 - padding)
        
        decoded_bytes = base64.b64decode(clean_text)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Если внутри появились протоколы VPN, значит это точно была подписка в base64! 🥰
        if '://' in decoded_str:
            return decoded_str
    except Exception:
        pass # Если не получилось, значит это был обычный текст, ничего страшного 🌸
    
    return text

def main():
    raw_links = []
    
    # 1. Скачиваем все тексты 📥
    for url in URLS:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                # Сначала проверяем на base64 и раскодируем, если нужно ✨
                decoded_content = decode_base64_if_needed(resp.text)
                raw_links.extend(decoded_content.splitlines())
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
                
                # На всякий случай заменяем и закодированные версии этих смайликов ✨
                link = link.replace('%F0%9F%A5%AD', '🦎').replace('%F0%9F%94%A5', '🦎')
                
                filtered_links.append(link)

    # 3. Сохраняем результат в файл `sub.txt` 💾
    with open('sub.txt', 'w', encoding='utf-8') as f:
        f.write(HEADER)
        for link in filtered_links:
            f.write(link + '\n')
    
    print(f"Готово, зайка! ✨ Собрано {len(filtered_links)} отличных серверов! 🥰")

if __name__ == '__main__':
    main()
