import motor.motor_asyncio
import calendar
from datetime import datetime, timedelta


class ResponseMaker:
    def __init__(self):
        self.db_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        self.current_db = self.db_client["test"]
        self.collection = self.current_db["sample_collection"]
        self.decide = {'hour': 1, 'day': 24, 'month': -1}

    async def slicer(self, start, end, hours):
        try:
            st = datetime.fromisoformat(start)
            en = datetime.fromisoformat(end)
        except ValueError as e:
            return {'{dataset: invalid iso, labels:[]}'}
        response = {"dataset": [], "labels": []}
        while st <= en:
            group = hours
            if hours == -1:
                group = calendar.monthrange(st.year, st.month)[1] * 24
            query = {
                "dt": {
                    "$gte": st,
                    "$lt": st + timedelta(hours=group)
                }
            }
            results = self.collection.find(query)
            value = 0
            async for record in results:
                if st == en:
                    continue
                value += record["value"]
            response["dataset"].append(value)
            response["labels"].append(st.isoformat())
            st += timedelta(hours=group)
        return response

    async def make_a_slice(self, start, end, group):
        return await self.slicer(start, end, self.decide[group])


