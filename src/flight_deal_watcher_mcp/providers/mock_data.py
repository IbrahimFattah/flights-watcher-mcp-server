"""Static templates used by the mock provider.

The dates are generated at runtime, but the route patterns, times, and price
bases live here so the project is easy to inspect and extend.
"""

from __future__ import annotations

MOCK_ROUTE_TEMPLATES: dict[tuple[str, str], list[dict[str, object]]] = {
    ("AMM", "DOH"): [
        {
            "template_id": "amm-doh-qr-nonstop",
            "primary_airline": "Qatar Airways",
            "checked_bag_included": True,
            "base_price_usd": 235.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "DOH",
                    "departure_time": "08:05",
                    "duration_minutes": 185,
                    "flight_number": "QR401",
                    "airline": "Qatar Airways",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "DOH",
                    "destination": "AMM",
                    "departure_time": "13:40",
                    "duration_minutes": 185,
                    "flight_number": "QR402",
                    "airline": "Qatar Airways",
                }
            ],
        },
        {
            "template_id": "amm-doh-rj-nonstop",
            "primary_airline": "Royal Jordanian",
            "checked_bag_included": True,
            "base_price_usd": 212.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "DOH",
                    "departure_time": "14:20",
                    "duration_minutes": 190,
                    "flight_number": "RJ650",
                    "airline": "Royal Jordanian",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "DOH",
                    "destination": "AMM",
                    "departure_time": "18:50",
                    "duration_minutes": 190,
                    "flight_number": "RJ651",
                    "airline": "Royal Jordanian",
                }
            ],
        },
        {
            "template_id": "amm-doh-fz-1stop",
            "primary_airline": "Flydubai",
            "checked_bag_included": False,
            "base_price_usd": 176.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "DXB",
                    "departure_time": "06:15",
                    "duration_minutes": 185,
                    "flight_number": "FZ142",
                    "airline": "Flydubai",
                },
                {
                    "origin": "DXB",
                    "destination": "DOH",
                    "departure_time": "10:25",
                    "duration_minutes": 75,
                    "flight_number": "FZ019",
                    "airline": "Flydubai",
                },
            ],
            "inbound_segments": [
                {
                    "origin": "DOH",
                    "destination": "DXB",
                    "departure_time": "15:15",
                    "duration_minutes": 70,
                    "flight_number": "FZ020",
                    "airline": "Flydubai",
                },
                {
                    "origin": "DXB",
                    "destination": "AMM",
                    "departure_time": "18:20",
                    "duration_minutes": 190,
                    "flight_number": "FZ143",
                    "airline": "Flydubai",
                },
            ],
        },
    ],
    ("AMM", "IST"): [
        {
            "template_id": "amm-ist-rj-nonstop",
            "primary_airline": "Royal Jordanian",
            "checked_bag_included": True,
            "base_price_usd": 198.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "IST",
                    "departure_time": "09:10",
                    "duration_minutes": 145,
                    "flight_number": "RJ308",
                    "airline": "Royal Jordanian",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "IST",
                    "destination": "AMM",
                    "departure_time": "20:05",
                    "duration_minutes": 145,
                    "flight_number": "RJ309",
                    "airline": "Royal Jordanian",
                }
            ],
        },
        {
            "template_id": "amm-ist-tk-nonstop",
            "primary_airline": "Turkish Airlines",
            "checked_bag_included": True,
            "base_price_usd": 226.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "IST",
                    "departure_time": "16:00",
                    "duration_minutes": 150,
                    "flight_number": "TK817",
                    "airline": "Turkish Airlines",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "IST",
                    "destination": "AMM",
                    "departure_time": "22:10",
                    "duration_minutes": 150,
                    "flight_number": "TK816",
                    "airline": "Turkish Airlines",
                }
            ],
        },
        {
            "template_id": "amm-ist-pc-1stop",
            "primary_airline": "Pegasus",
            "checked_bag_included": False,
            "base_price_usd": 154.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "SAW",
                    "departure_time": "05:55",
                    "duration_minutes": 135,
                    "flight_number": "PC701",
                    "airline": "Pegasus",
                },
                {
                    "origin": "SAW",
                    "destination": "IST",
                    "departure_time": "09:45",
                    "duration_minutes": 75,
                    "flight_number": "PC119",
                    "airline": "Pegasus",
                },
            ],
            "inbound_segments": [
                {
                    "origin": "IST",
                    "destination": "SAW",
                    "departure_time": "14:30",
                    "duration_minutes": 70,
                    "flight_number": "PC120",
                    "airline": "Pegasus",
                },
                {
                    "origin": "SAW",
                    "destination": "AMM",
                    "departure_time": "18:00",
                    "duration_minutes": 135,
                    "flight_number": "PC700",
                    "airline": "Pegasus",
                },
            ],
        },
    ],
    ("AMM", "DXB"): [
        {
            "template_id": "amm-dxb-rj-nonstop",
            "primary_airline": "Royal Jordanian",
            "checked_bag_included": True,
            "base_price_usd": 205.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "DXB",
                    "departure_time": "07:20",
                    "duration_minutes": 195,
                    "flight_number": "RJ612",
                    "airline": "Royal Jordanian",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "DXB",
                    "destination": "AMM",
                    "departure_time": "12:25",
                    "duration_minutes": 195,
                    "flight_number": "RJ613",
                    "airline": "Royal Jordanian",
                }
            ],
        },
        {
            "template_id": "amm-dxb-ek-nonstop",
            "primary_airline": "Emirates",
            "checked_bag_included": True,
            "base_price_usd": 244.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "DXB",
                    "departure_time": "13:35",
                    "duration_minutes": 190,
                    "flight_number": "EK904",
                    "airline": "Emirates",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "DXB",
                    "destination": "AMM",
                    "departure_time": "17:10",
                    "duration_minutes": 190,
                    "flight_number": "EK903",
                    "airline": "Emirates",
                }
            ],
        },
        {
            "template_id": "amm-dxb-fz-budget",
            "primary_airline": "Flydubai",
            "checked_bag_included": False,
            "base_price_usd": 168.0,
            "outbound_segments": [
                {
                    "origin": "AMM",
                    "destination": "DXB",
                    "departure_time": "22:45",
                    "duration_minutes": 200,
                    "flight_number": "FZ144",
                    "airline": "Flydubai",
                }
            ],
            "inbound_segments": [
                {
                    "origin": "DXB",
                    "destination": "AMM",
                    "departure_time": "03:35",
                    "duration_minutes": 200,
                    "flight_number": "FZ145",
                    "airline": "Flydubai",
                }
            ],
        },
    ],
}
