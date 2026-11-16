import pytest
from fastapi.testclient import TestClient

from main import AnalyticsRequest, app, get_analytics_summary


client = TestClient(app)


@pytest.mark.parametrize(
    ("amounts", "expected_total", "expected_median"),
    [
        ([10.0, 20.0, 30.0], 60.0, 20.0),
        ([10.0, 30.0], 40.0, 20.0),
        ([12.0], 12.0, 12.0),
        ([-10.0, 30.0], 20.0, 10.0),
    ],
)
def test_calculates_total_and_median(amounts, expected_total, expected_median):
    request = AnalyticsRequest(
        transactions=[
            {"id": index, "amount": amount, "category": "test"}
            for index, amount in enumerate(amounts, start=1)
        ]
    )

    result = get_analytics_summary(request)

    assert result.total_revenue == expected_total
    assert result.median_check == expected_median


def test_summary_endpoint_returns_summary():
    response = client.post(
        "/analytics/summary",
        json={
            "transactions": [
                {"id": 1, "amount": 10.0, "category": "food"},
                {"id": 2, "amount": 30.0, "category": "travel"},
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {"total_revenue": 40.0, "median_check": 20.0}


@pytest.mark.parametrize(
    "payload",
    [
        {"transactions": []},
        {"transactions": [{"id": 1, "category": "food"}]},
    ],
)
def test_summary_endpoint_rejects_invalid_transactions(payload):
    response = client.post("/analytics/summary", json=payload)

    assert response.status_code == 422
