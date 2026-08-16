import asyncio, zipfile, io, os
import httpx

TOKEN = "8598876960:AAGjyLm3nRrvDRNEexibsPpZ-Jcu-K5IuDc"  # از BotFather
CHAT_ID = 1320040305                            # از getUpdates
DATA_DIR = os.environ.get("DATA_DIR", "/data") # همون مسیر دیتای پنل

async def send_backup():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(DATA_DIR):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, DATA_DIR))
    buf.seek(0)

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            "https://api.telegram.org/bot%s/sendDocument" % TOKEN,
            data={"chat_id": CHAT_ID, "caption": "بکاپ خودکار پنل RVG"},
            files={"document": ("rvg-backup.zip", buf.getvalue(), "application/zip")},
        )
        print("HTTP", r.status_code, r.text[:200])

if __name__ == "__main__":
    asyncio.run(send_backup())
