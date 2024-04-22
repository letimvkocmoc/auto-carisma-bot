from datetime import datetime

from sqlalchemy import insert, select, update, func, and_, text, case
from sqlalchemy.orm import Session
from database.models import engine, currency


class SQL:
    session = Session(engine)

    def insert(self, name: str, rate: float, updated: str):
        data = insert(currency).values(
            name=name,
            rate=rate,
            updated=updated
        )
        self.session.execute(data)
        self.session.commit()

    def update(self, currency_id: int, rate: float, updated: str, last_request: str):
        data = update(currency).where(currency.c.id == currency_id).values(
            rate=rate,
            updated=updated,
            last_request=last_request
        )
        self.session.execute(data)
        self.session.commit()

    def get_currencies(self):
        data = select(currency.c.rate)
        request = self.session.execute(data)
        result = request.fetchall()
        return result

