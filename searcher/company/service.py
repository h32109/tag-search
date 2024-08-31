import pandas as pd
import typing as t

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from searcher.company.schema import CompanyCreateRequest, TagNameRequest
from searcher.globals import sql
from searcher.utils import transaction
from searcher.company.model import Company, CompanyName, TagName, company_tag
from searcher.service import ServiceBase, Service
from sqlalchemy.future import select
from sqlalchemy import insert, delete

from searcher.utils import get_path_from_root


class CompanyServiceBase(ServiceBase):
    settings: t.Any

    async def get_or_create_tag(self, name: str, language: str) -> TagName:
        stmt = select(TagName).where(TagName.language == language, TagName.name == name)
        result = await sql.session.execute(stmt)
        tag = result.scalar_one_or_none()
        if not tag:
            tag = TagName(language=language, name=name)
            sql.session.add(tag)
            await sql.session.flush()
        return tag

    @transaction
    async def init_database(self):
        file_path = get_path_from_root("db/data/company_tag_sample.csv")
        df = pd.read_csv(file_path)
        df = df.where(pd.notnull(df), None)

        for _, row in df.iterrows():
            company = Company()
            sql.session.add(company)
            await sql.session.flush()

            for lang in ['ko', 'en', 'ja']:
                if row[f'company_{lang}']:
                    name = str(row[f'company_{lang}'])
                    stmt = insert(CompanyName).values(company_id=company.id, language=lang, name=name)
                    await sql.session.execute(stmt)

            for lang in ['ko', 'en', 'ja']:
                if row[f'tag_{lang}']:
                    tags = str(row[f'tag_{lang}']).split('|')
                    for tag_name in tags:
                        tag_name = tag_name.strip()
                        if tag_name:
                            tag = await self.get_or_create_tag(tag_name, lang)
                            stmt = insert(company_tag).values(company_id=company.id, tag_id=tag.id)
                            await sql.session.execute(stmt)

        await sql.session.commit()

    async def configuration(self, settings):
        self.settings = settings
        await self.init_database()


class CompanyService(CompanyServiceBase):

    def get_company_name(self, company: Company, language: str) -> str:
        name = next((name.name for name in company.names if name.language == language), None)
        if name is None:
            name = next((name.name for name in company.names), None)
        return name

    async def get_company_by_name_query(self, company_name: str) -> t.Optional[Company]:
        stmt = select(Company).join(CompanyName).options(
            joinedload(Company.names),
            joinedload(Company.tags)
        ).where(CompanyName.name == company_name)
        result = await sql.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def search_company_name(self, query: str, language: str) -> t.List[t.Dict]:
        stmt = select(CompanyName.name).join(Company).where(
            CompanyName.language == language,
            CompanyName.name.like(f"%{query}%")
        ).distinct()

        result = await sql.session.execute(stmt)
        companies = result.scalars().all()

        return [{"company_name": name} for name in companies]

    async def get_company_by_name(self, company_name: str, language: str) -> t.Optional[t.Dict]:
        stmt = select(Company).join(CompanyName).options(
            joinedload(Company.names),
            joinedload(Company.tags)
        ).where(
            CompanyName.name == company_name
        )

        result = await sql.session.execute(stmt)
        company = result.unique().scalar_one_or_none()

        if not company:
            return None

        company_name = self.get_company_name(company, language)
        tags = [tag.name for tag in company.tags if tag.language == language]

        return {
            "company_name": company_name,
            "tags": tags
        }

    async def create_company(self, payload: CompanyCreateRequest, language: str) -> t.Dict:
        company = Company()
        sql.session.add(company)
        await sql.session.flush()

        for lang, name in payload.company_name.items():
            stmt = insert(CompanyName).values(company_id=company.id, language=lang, name=name)
            await sql.session.execute(stmt)

        for tag_data in payload.tags:
            for lang, name in tag_data.tag_name.items():
                tag = await self.get_or_create_tag(name, lang)
                stmt = insert(company_tag).values(company_id=company.id, tag_id=tag.id)
                await sql.session.execute(stmt)

        await sql.session.commit()

        company_name = payload.company_name.get(language)
        if company_name is None:
            company_name = next(iter(payload.company_name.values()), None)

        return await self.get_company_by_name(company_name, language)

    async def search_companies_by_tag(self, query: str, language: str) -> t.List[t.Dict]:
        tag_query = select(TagName).where(TagName.name == query)
        tag_result = await sql.session.execute(tag_query)
        tag = tag_result.scalar_one_or_none()

        if not tag:
            return []

        company_query = (
            select(Company)
            .join(company_tag)
            .join(CompanyName)
            .where(
                company_tag.c.tag_id == tag.id
            )
            .options(joinedload(Company.names))
            .distinct()
        )
        companies_result = await sql.session.execute(company_query)
        companies = companies_result.unique().scalars().all()

        return [{"company_name": self.get_company_name(company, language)} for company in companies]

    async def add_tags_to_company(self, company_name: str, tags: t.List[TagNameRequest], language: str) -> t.Dict:
        company = await self.get_company_by_name_query(company_name)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        for tag_input in tags:
            for lang, name in tag_input.tag_name.items():
                tag = await self.get_or_create_tag(name, lang)
                stmt = insert(company_tag).values(company_id=company.id, tag_id=tag.id)
                await sql.session.execute(stmt.prefix_with('IGNORE'))

        await sql.session.commit()
        return await self.get_company_by_name(company_name, language)

    async def delete_tag_from_company(self, company_name: str, tag_to_delete: str, language: str) -> t.Dict:
        company = await self.get_company_by_name_query(company_name)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        stmt = delete(company_tag).where(
            company_tag.c.company_id == company.id,
            company_tag.c.tag_id.in_(
                select(TagName.id).where(TagName.name == tag_to_delete)
            )
        )
        await sql.session.execute(stmt)

        await sql.session.commit()
        return await self.get_company_by_name(company_name, language)


company_service = Service.add_service(CompanyService)
