# HappyRobot API

This project is a containerized API built with **FastAPI**, designed to support the call-handling and freight load management workflow for HappyRobot. It also includes a live dashboard for visual insights.

## 🚚 API Endpoints

### `GET /loads/{load_id}`
Returns the full details of a specific load from the dataset, including:
- Origin and destination
- Pickup and delivery windows
- Equipment required
- Commodity info
- Loadboard rate, weight, miles, and special notes

### `POST /calls`
Logs a call result submitted by the workflow. Payload format:

```json
{
  "mc_number": "12345",
  "load_id": "11111",
  "initial_rate": "4000",
  "final_rate": "3500",
  "outcome": "Successful",
  "sentiment": "Positive"
}
```

### `GET /calls`
Returns all call entries logged so far.

### `GET /dashboard/dashboard.html`
Serves a real-time dashboard that visualizes:
- Outcome distribution (Successful vs. Unsuccessful)
- Sentiment analysis
- Initial vs. Final rate comparison

---

## 🔐 Authentication

All endpoints are protected with an API key.

### Header format:
```
x-api-key: roman-for-happyrobot-2025
```

---

## ☁️ Deployment

This API is containerized with Docker and deployed to **Google Cloud Run**.

To redeploy:

```bash
gcloud builds submit --tag gcr.io/happyrobotloads2025/load-api
gcloud run deploy load-api --image gcr.io/happyrobotloads2025/load-api --platform managed --region us-central1 --allow-unauthenticated --set-env-vars ROMANHAPPYROBOT_2025=roman-for-happyrobot-2025
```

---

## 🌐 Live API Base URL

```
https://load-api-325799305155.us-central1.run.app
```

You can access:
- `/loads/{load_id}` to look up a load
- `/calls` to post or fetch call summaries
- `/dashboard/dashboard.html` to view the dashboard

---

## 📁 Project Structure

```
.
├── main.py                 # FastAPI app
├── Dockerfile              # Docker config
├── requirements.txt        # Python dependencies
├── loads_sample.csv        # Source data for loads
├── static/
│   └── dashboard.html      # Dashboard UI (Chart.js)
```

---

## 📊 Dashboard

The dashboard is dynamically rendered using Chart.js and pulls live data from the `/calls` endpoint to display:
- Successful vs. Unsuccessful call volume
- Sentiment breakdown
- Rate trends by load ID

---

## 📝 License

This project was developed for a technical challenge and is intended for demonstration purposes.
