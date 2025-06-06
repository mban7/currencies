from datetime import datetime

import models
from sqlalchemy.orm import Session


def save_currencies(db: Session, currency_data: list[list[dict]]):
    db_currencies = []

    for table_list in currency_data:
        if not isinstance(table_list, list):
            continue

        for table_entry in table_list:
            effective_date_str = table_entry.get("effectiveDate")
            rates = table_entry.get("rates", [])

            if not effective_date_str or not rates:
                continue

            try:
                effective_date = datetime.strptime(effective_date_str, "%Y-%m-%d")
            except ValueError:
                continue

            existing_codes = set(
                r.code
                for r in db.query(models.Currency)
                .filter(models.Currency.date == effective_date)
                .all()
            )

            for rate in rates:
                code = rate.get("code")
                if not code or code in existing_codes:
                    continue

                currency_obj = models.Currency(
                    name=rate.get("currency") or rate.get("country", ""),
                    code=code,
                    mid=rate["mid"],
                    date=effective_date,
                )
                db_currencies.append(currency_obj)

    if db_currencies:
        db.add_all(db_currencies)
        db.commit()
    else:
        pass

    return db_currencies
