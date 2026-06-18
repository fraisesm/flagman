from data.repositories.stats_repository import StatsRepository


class GetStatsHandler:
    def __init__(self, stats_repository: StatsRepository):
        self.stats_repository = stats_repository

    def handle(self) -> dict:
        return self.stats_repository.get_summary()
