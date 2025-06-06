from datetime import date, datetime, timedelta

import requests

START_DATE = datetime(2002, 1, 2)
END_DATE = datetime.today()


def data_ranges(start_date: datetime, end_date: datetime, span: int) -> list:
    ranges = []
    current_date = start_date

    while current_date <= end_date:
        date_span = min(current_date + timedelta(days=span - 1), end_date)
        ranges.append(
            (current_date.strftime("%Y-%m-%d"), date_span.strftime("%Y-%m-%d"))
        )
        current_date = date_span + timedelta(days=1)

    return ranges


def fetch_currencies(span: int = 93) -> list:
    url_template = (
        "https://api.nbp.pl/api/exchangerates/tables/A/{start}/{end}/?format=json"
    )
    ranges = data_ranges(START_DATE, END_DATE, span)
    all_data = []

    for start, end in ranges:

        url = url_template.format(start=start, end=end)
        try:
            response = requests.get(url)
            response.raise_for_status()
            all_data.append(response.json())
        except requests.HTTPError as e:
            continue

    return all_data
