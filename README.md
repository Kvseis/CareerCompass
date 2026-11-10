# 🧭 CareerCompass Discord Botu

Gənclərin və karyerasını dəyişmək istəyənlərin özlərinə uyğun karyera yolunu tapmalarına kömək edən **AI-powered Discord botu**.

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


## 🗃️ Baza Strukturu (SQLite)

| Cədvəl | Məlumat |
|--------|---------|
| `users` | Discord ID, username, qeydiyyat tarixi |
| `test_results` | Test cavabları + AI tövsiyələri (JSON) |
| `favorites` | Sevilənlərə əlavə edilmiş karyeralar |
| `explore_history` | Hansı sahələri kəşf etdiklər |



## 🛠️ Texnologiyalar

- **Python 3.11+**
- **discord.py 2.5** — Slash commands, Buttons, Select Menus
- **Google Gemini AI** — Fərdi tövsiyələr
- **SQLite** — Lokal baza
- **python-dotenv** — Mühit dəyişənləri
