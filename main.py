# main.py
import requests
import time
import datetime
from keep_alive import keep_alive

# ====== CẤU HÌNH ======
TOKEN = "MTI5OTM4NjU2ODcxMjM5Mjc2NQ.GYorKm.MNYFKO7YNSnBT--W5rYMuFKcfvsDPFBvb7IlgA"              # ⚠️ KHÔNG nên dùng token người thật
CHANNEL_ID = "1369314469246795776"
WEBHOOK_URL = "https://discord.com/api/webhooks/1370990469986914396/2eSQecfWjuE3dZiDTC5Hx5Ip3DI6i6CtZq2Utb2OJFbBQPXdEjFUgemkzqNKWcbD5Lv6"  # webhook để gửi stats
API_BASE = "https://discord.com/api/v9"
MSG_URL = f"{API_BASE}/channels/{CHANNEL_ID}/messages"
HEADERS = {"authorization": TOKEN}

paused = False
sent_count = 0
last_handled_id = None
start_time = datetime.datetime.now()

# ====== HÀM HỖ TRỢ ======
def get_latest_message():
    """Lấy tin nhắn mới nhất trong kênh"""
    try:
        r = requests.get(MSG_URL, headers=HEADERS, params={"limit": 1}, timeout=10)
        if r.status_code == 200 and len(r.json()) > 0:
            return r.json()[0]
    except Exception as e:
        print("❌ Lỗi khi lấy tin nhắn:", e)
    return None

def send_message(content):
    """Gửi tin nhắn vào kênh"""
    global sent_count
    try:
        r = requests.post(MSG_URL, headers=HEADERS, data={"content": content}, timeout=10)
        if r.status_code in (200, 201):
            sent_count += 1
            return True
        else:
            print("⚠️ Gửi thất bại:", r.status_code, r.text[:200])
    except Exception as e:
        print("❌ Lỗi khi gửi:", e)
    return False

def format_uptime():
    """Trả về chuỗi uptime đẹp"""
    uptime = datetime.datetime.now() - start_time
    h, rem = divmod(int(uptime.total_seconds()), 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m}m {s}s"

def send_stats_embed_via_webhook():
    """Gửi embed màu xanh dương qua webhook"""
    embed = {
        "title": "<@1299386568712392765>",
        "description": (
            f"**https://cdn.discordapp.com/attachments/1336317526472134706/1424760335931281509/image0.gif:** {sent_count}\n"
            f"**Uptime:** {format_uptime()}"
        ),
        "color": 3447003  # màu xanh dương
    }
    data = {"embeds": [embed]}
    try:
        r = requests.post(WEBHOOK_URL, json=data, timeout=10)
        if r.status_code in (200, 204):
            print("✅ Đã gửi stats qua webhook.")
        else:
            print("⚠️ Gửi webhook thất bại:", r.status_code, r.text[:200])
    except Exception as e:
        print("❌ Lỗi khi gửi webhook:", e)

# ====== CHƯƠNG TRÌNH CHÍNH ======
def main():
    global paused, last_handled_id

    print("h")

    while True:
        latest = get_latest_message()
        if latest:
            msg_id = latest.get("id")
            content = latest.get("content", "").lower()

            # xử lý lệnh mới
            if msg_id and msg_id != last_handled_id:
                if "Please complete this within 10 minutes or it may result in a ban!" in content:
                    paused = True
                    print("🔴 Bot dừng vì có người gõ 'stop'")
                elif "!resume" in content:
                    paused = False
                    print("🟢 Bot tiếp tục vì có người gõ '!resume'")
                elif "!stats" in content:
                    print("📊 Gửi thống kê qua webhook...")
                    send_stats_embed_via_webhook()
                last_handled_id = msg_id

        # Nếu không tạm dừng thì gửi tin nhắn
        if not paused:
            if send_message("obuy 1"):
                print(f"Đã gửi (tổng: {sent_count})")
        else:
            print("⏸️ Bot đang tạm dừng...")

        time.sleep(3)  # tránh spam nhanh
# ======================================

if __name__ == "__main__":
    keep_alive()
    main()
