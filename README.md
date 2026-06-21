# 🧭 CareerCompass Discord Botu

Gənclərin və karyerasını dəyişmək istəyənlərin özlərinə uyğun karyera yolunu tapmalarına kömək edən **AI-powered Discord botu**.

---

## 📁 Layihə Strukturu

```
career_compass/
├── bot.py               ← Ana bot faylı (bunu işlət)
├── config.py            ← Konfiqurasiya sabitleri
├── database.py          ← SQLite baza əməliyyatları
├── gemini_client.py     ← Gemini AI inteqrasiyası
├── career_data.json     ← Karyera bazası (doldurula bilər)
├── .env                 ← API açarları (bunu redaktə et)
├── requirements.txt     ← Python paketləri
│
├── cogs/                ← Bot komanda modulları
│   ├── welcome.py       ← /start, /about
│   ├── career_test.py   ← /test
│   ├── career_explore.py ← /explore
│   └── recommendations.py ← /recommend, /favorites, /chat
│
└── views/               ← Discord UI komponentləri
    ├── main_menu.py     ← Ana menyu
    ├── test_views.py    ← Test sualları
    ├── explore_views.py ← Karyera kəşfi
    └── result_views.py  ← Nəticə ekranı
```

---

## 🚀 Quraşdırma

### 1. Python 3.11+ quraşdır

### 2. Paketləri yüklə
```bash
pip install -r requirements.txt
```

### 3. `.env` faylını düzəlt
```env
DISCORD_TOKEN=sənin_discord_token
GEMINI_API_KEY=sənin_gemini_api_key
```

### 4. Discord Bot Quraşdırması
[Discord Developer Portal](https://discord.com/developers/applications) saytında:
1. Yeni Application yarat
2. "Bot" bölməsindən Token kopyala → `.env`-ə yapışdır
3. **Lazımi İcazələr (Permissions):**
   - `bot` scope
   - `applications.commands` scope
   - Permissions: `Send Messages`, `Use Slash Commands`, `Embed Links`, `Read Message History`
4. OAuth2 URL ilə botu serverə əlavə et

### 5. Gemini API Key
⚠️ **Vacib:** [Google AI Studio](https://aistudio.google.com/)-dan yeni API key yarat.
- **Free tier** üçün billing aktivləşdirilməlidir (aylıq $0 sınır var)
- Alternativ: Yeni Google hesabı ilə yeni API key yarat

### 6. Botu işlət
```bash
python bot.py
```

---

## 🎮 Bot Komandaları

| Komanda | Açıqlama |
|---------|----------|
| `/start` | Ana menyu ilə başla |
| `/test` | 5 sualdan ibarət karyera testini et |
| `/explore [sahə]` | Karyera sahələrini kəşf et |
| `/recommend [mətn]` | Özün haqqında yaz, AI tövsiyə etsin |
| `/chat [sual]` | AI ilə karyera haqqında söhbət et |
| `/favorites` | Saxladığın karyeraları gör |
| `/about` | Bot haqqında məlumat |

---

## 🗂️ `career_data.json` Formatı

Yeni karyera əlavə etmək üçün:

```json
{
  "sahə_adı": [
    {
      "id": "unikal_id",
      "name": "Karyera Adı",
      "emoji": "💻",
      "description": "Qısa təsvir",
      "skills": ["Bacarıq 1", "Bacarıq 2"],
      "roadmap": [
        "1. İlk addım",
        "2. İkinci addım"
      ],
      "resources": ["Resurs 1", "Resurs 2"],
      "salary_range": "$40,000 - $100,000/il",
      "work_style": "remote-friendly",
      "personality_match": ["creative", "analytical"],
      "difficulty": "medium",
      "demand": "high"
    }
  ]
}
```

**Mövcud sahələr:** `tech`, `design`, `health`, `business`, `media`, `psychology`

Yeni sahə əlavə etmək üçün `career_data.json`-a yeni key əlavə edin və `views/explore_views.py`-dakı `SECTORS` dictionaryna yeni sahəni daxil edin.

---

## 🗃️ Baza Strukturu (SQLite)

| Cədvəl | Məlumat |
|--------|---------|
| `users` | Discord ID, username, qeydiyyat tarixi |
| `test_results` | Test cavabları + AI tövsiyələri (JSON) |
| `favorites` | Sevilənlərə əlavə edilmiş karyeralar |
| `explore_history` | Hansı sahələri kəşf etdiklər |

---

## ⚠️ Bilinen Problemlər

**Gemini API Quota xətası (429):**
```
RESOURCE_EXHAUSTED: limit: 0
```
Bu, API key-in free tier limitinin bitdiyini göstərir. Həllər:
1. [Google AI Studio](https://aistudio.google.com/) → yeni API key yarat
2. Google Cloud-da billing aktivləşdir (pulsuz kredit var)
3. `gemini-2.5-flash` modelini yoxla (hətta daha yeni quota var)

---

## 🛠️ Texnologiyalar

- **Python 3.11+**
- **discord.py 2.5** — Slash commands, Buttons, Select Menus
- **Google Gemini AI** — Fərdi tövsiyələr
- **SQLite** — Lokal baza
- **python-dotenv** — Mühit dəyişənləri
