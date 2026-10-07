
from app.repositories.doomscroll_db import DoomscrollingRepository

from app.schemas.schemas import InputSchema, OutputSchema, OutputSchemaDays

class DoomscrollService:
    def __init__(self, repo: DoomscrollingRepository) -> None:
        self.repo = repo

    async def list_time(self, payload: int) -> OutputSchemaDays:

        result = await self.repo.calculate_all_time(days=payload)
        result = result.mappings().all()
        if not len(result):
            return OutputSchemaDays(apps=[], total=0)
        apps = [OutputSchema(app=row["app"], seconds=row["seconds"]) for row in result]
        total = sum([row["seconds"] for row in result])

        return OutputSchemaDays(apps=apps, total=total)
    
    async def list_avg_time(self, payload: int) -> OutputSchemaDays:

        result = await self.repo.calculate_avg_time(payload)
        result = result.mappings().all()
        if not len(result):
            return OutputSchemaDays(apps=[], total=0)
        
        apps = [OutputSchema(app=row["app"], seconds=row["seconds"]) for row in result]

        total = 0
        counter = 0
        for row in result:
            counter += 1
            total += row["seconds"]
        
        average = round(total/counter) 
        return OutputSchemaDays(apps=apps, total=average)
    
    async def load_info(self, payload: InputSchema) -> None:
            return await self.repo.load_info(payload)