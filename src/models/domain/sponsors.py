from pydantic import BaseModel
from typing import Dict, Optional

from models.domain.cases import CasesRepository
import models.helpers.slug as sl


class Sponsor(BaseModel):
    slug: str
    name: str
    photo_url: Optional[str] = '/assets/who_is_it.jpeg'
    client_id: Optional[int] = None

    @property
    def omni_url(self):
        return f'/sponsors/{self.slug}'


class SponsorsRepository:
    def __init__(self, cases_repository: CasesRepository):
        self.cases_repository = cases_repository
        self.__data = None

    def get_all(self) -> Dict[str, Sponsor]:
        if self.__data is None:
            self.__build_data()

        return self.__data

    def get_by_slug(self, slug: str) -> Sponsor:
        if self.__data is None:
            self.__build_data()

        return self.__data.get(slug)

    def __build_data(self):
        all_cases = self.cases_repository.get_all().values()

        self.__data = {
            sl.generate(sponsor): Sponsor(slug=sl.generate(sponsor), name=sponsor, client_id=case.client_id)
            for case in all_cases
            if case.sponsor is not None
            for sponsor in case.sponsor.split(';')
        }