# Course Exchange Bot 🎓🤖

A lightweight Python Telegram bot built to help students exchange classes (swap courses). It integrates with MySQL, uses the Telegram Bot API, and can operate via a webhook (ngrok) or polling. The project demonstrates building functional chatbots, DB-driven matching logic, and building reliable user flows.

---

## Highlights

- ✅ Users can create a course exchange request with a course they HAVE and a course they WANT.
- ✅ Backend uses MySQL as persistent storage with helper functions for requests and users.
- ✅ Matching algorithm finds complementary open requests and marks them as matched.
- ✅ Bot supports contact sharing inside Telegram and uses the Telegram Keyboard markup.
- ✅ Easily run locally with ngrok for webhook-based development or run via polling for quick tests.

---

## Tech Stack

- Language: Python 3.8+
- Telegram SDK: python-telegram-bot (supports both Updater and Application usage; repo contains examples)
- DB: MySQL (via mysql-connector-python)
- HTTP/Local webhook: pyngrok (for exposing local webhooks) and Bottle (for the `internetbot.py` example)
- HTTP: requests
- Utilities: queue, datetime, and basic standard library modules

---

## Project Structure

- `bot.py` — Main bot implementation using `Updater` with webhook approach (pyngrok-driven). Includes conversational flow (start/have/want/confirm) backed by DB.
- `bot20.3.py` — Updated version showcasing `Application` (v20 style) from `python-telegram-bot` with polling/webhook examples.
- `queryRunner.py` — DB connection/runner using `mysql.connector` and environment configuration.
- `requestHelper.py`, `userHelper.py` — DB helper modules to create and fetch user requests; core business logic.
- `courseMatchFinder.py` — SQL-based matching routine to pair complementary user requests.
- `internetbot.py` — Bottle-based micro webhook example showing a very simple handler and a demonstration bot.
- Other files: helper scripts, `apikey.txt` (do NOT commit), `.env` (do NOT commit), and supporting scripts.

---

## Installation (Quick Start)

> NOTE: Do not commit `.env` or `apikey.txt` as they may contain secrets like `BOT_TOKEN` and DB credentials.

1. Clone this repo:

```powershell
git clone <repo-url>
cd "ASU Course Exchange Bot"
```

2. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file (or use environment variables). You can copy the sample provided:

```powershell
copy .env.example .env
notepad .env
```

5. Configure your `.env` with your BG credentials. Example variables (in `.env.example`):

```env
BOT_TOKEN=your_telegram_bot_token_here
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=supersecret
DB_DATABASE=asu_exchange_courses
```

6. Run the bot locally (example with `bot.py`) — this will start a webhook via ngrok:

```powershell
python bot.py
```

Or run the `bot20.3.py` for the newer application interface:

```powershell
python bot20.3.py
```

---

## Database

- The project uses MySQL; set DB env variables and ensure the schema exists. `dbschema.txt` contains the schema used. Adjust DB connection parameters in `.env` accordingly.

---

## Testing & Usage

- Use a Telegram Bot created via @BotFather. Set the token in your `.env`.
- Run the bot and start interacting from Telegram. Use /start and follow prompts (HAVE/WANT).
- The bot stores requests in MySQL and the `courseMatchFinder.py` script demonstrates match-finding.

---

## Security & Secrets

- Do NOT commit `.env` or `apikey.txt` to Git. They contain secrets like `BOT_TOKEN`.
- This repo already includes a `.gitignore` which excludes `.env` and other secrets. Double-check before pushing.
- If secrets were committed previously, follow fast steps to remove them from Git history (BFG, git-filter-repo) and rotate your tokens.

---

## Future Improvements (Nice-to-have)

- Add unit & integration tests.
- Build a Docker setup for easy deployment and containerization.
- Use GitHub Actions for CI and secret scanning & rotation procedures.
- Add a proper secrets manager (e.g., Azure Key Vault/AWS Secrets Manager) for production.
- Add more robust matching rules and scheduling to automatically notify users when matches appear.

---

## Contribution

- PRs are welcome! Please avoid including secrets in PRs.
- Add pre-commit hooks to check for secrets before merging (e.g., `detect-secrets` or `git-secrets`).

---

## Contact / Author

If you want any additional changes to this README or repo, feel free to contact the author or open an issue.

---
### License (GNU GPL v3)

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for details.
