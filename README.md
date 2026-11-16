# Transaction Analytics API

A FastAPI service that summarizes transaction amounts.

## Run

Install dependencies and start the API with either command:

```bash
pip install -r requirements.txt
# Option 1
python main.py
# Option 2
uvicorn main:app --reload
```

## Endpoint

`POST /analytics/summary`

Send a non-empty list of transactions:

```json
{
  "transactions": [
    {"id": 1, "amount": 10.0, "category": "food"},
    {"id": 2, "amount": 20.0, "category": "travel"}
  ]
}
```

The response contains the sum of all amounts and the median transaction amount:

```json
{
  "total_revenue": 30.0,
  "median_check": 15.0
}
```

The interactive API documentation is available at `/docs`.

Install the development dependencies and run the test suite with:

```bash
pip install -r requirements-dev.txt
pytest
```
