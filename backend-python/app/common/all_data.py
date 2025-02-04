from crud.games import GamesData
from crud.games_statuses import GamesStatusesData
from crud.projects import ProjectsData
from crud.socials import SocialsData
from sqlalchemy.ext.asyncio import AsyncSession


class AllData:
    def __init__(self) -> None:
        self.GAMES = GamesData()
        self.GAMES_STATUSES = GamesStatusesData()
        self.PROJECTS = ProjectsData()
        self.SOCIALS = SocialsData()

    async def setup(self, session: AsyncSession) -> None:
        await self.GAMES.setup(session)
        await self.GAMES_STATUSES.setup(session)
        await self.PROJECTS.setup(session)
        await self.SOCIALS.setup(session)


all_data = AllData()
