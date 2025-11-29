# Earning API
- Now we test the API from https://financialmodelingprep.com
- Do registration there to get a api-key.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/J1NX5/earning_api
```

```bash
cd earnings-api
```

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
touch .env
```

The .env file need this variable
```
API_KEY=<Api-Key>
```

```bash
fastapi dev main.py
```
