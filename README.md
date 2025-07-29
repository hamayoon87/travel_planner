
# 🧭 Travel Planner API

A FastAPI-based backend that plans trips by fetching real-time flight data using the Amadeus API. It is designed to integrate seamlessly with agentic AI tools like IBM watsonx Orchestrate, LangChain, or custom agents.

## ✨ Features

- ✅ REST API to plan trips via `/plan-trip`
- ✈️ Real-time flight search powered by the Amadeus API
- 🌍 Integration-ready for agent-based workflows (watsonx, LangChain, etc.)
- 🔐 Secure via environment variables (no API keys in code)
- ☁️ Easily deployable (tested on [Render](https://render.com))

---

## 🛠️ Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Amadeus for Developers API](https://developers.amadeus.com/)
- [Uvicorn](https://www.uvicorn.org/) ASGI server
- Python 3.9+

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/your-username/travel_planner.git
cd travel_planner
```

### 2. Set up environment variables

Create a `.env` file:

```env
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret
```

Make sure `.env` is **not** committed to Git:

```bash
echo ".env" >> .gitignore
```

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the API locally

```bash
uvicorn main:app --reload
```

Access docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Deploying on Render

1. Push to a GitHub repo.
2. Create a **new Web Service** on [Render](https://render.com/).
3. Add environment variables:
   - `AMADEUS_API_KEY`
   - `AMADEUS_API_SECRET`
4. Set build command (if needed):
   ```bash
   pip install -r requirements.txt
   ```
5. Set start command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```

Once deployed, your API will be available at:  
`https://your-app.onrender.com/plan-trip`

---

## 📡 Endpoint Example

### POST `/plan-trip`

```json
{
  "origin": "BER",
  "destination": "MUC",
  "start_date": "2025-08-01",
  "end_date": "2025-08-05",
  "travelers": 1
}
```

Response:

```json
{
  "flights": [
    {
      "departure_airport": "BER",
      "arrival_airport": "MUC",
      "departure_time": "2025-08-01T13:20:00",
      "arrival_time": "2025-08-01T20:00:00",
      "duration": "PT6H40M",
      "price": "338.36"
    },
    ...
  ],
  "message": "Trip for guest from BER to MUC planned."
}
```

---

## 🤖 Integrating with AI Agents

This API can be used as a tool in:

- **IBM watsonx Orchestrate**
- **LangChain** tools/agents
- **OpenAI Function Calling**
- Any agentic workflow that supports OpenAPI schemas

### OpenAPI Spec File

You can generate the OpenAPI schema like this:

```python
# Inside main.py
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    ...
    with open("openapi_watsonx.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
```

Upload this file to watsonx Orchestrate to register the tool.

---

## 📁 Project Structure

```
travel_planner/
├── main.py          # FastAPI app and endpoint
├── travel.py        # Core flight logic
├── utils.py         # Amadeus auth, helper functions
├── requirements.txt
├── .env             # API credentials (not committed)
└── README.md
```

---

## 🙈 Security Note

Do **not** commit `.env` or API keys. Use secure environment variables on Render or other platforms.

---

## 📬 License

MIT License — feel free to use, fork, and extend.
