import fastapi as fa
import typing as t

from searcher.company.schema import (
    CompanyResponse,
    CompanyTagResponse,
    CompanyCreateRequest,
    TagNameRequest
)

from searcher.company.service import (
    company_service
)

router = fa.APIRouter()


@router.get("/search",
            response_model=t.List[CompanyResponse])
async def search_company_name(
        query: str,
        x_wanted_language: str = fa.Header(...)
):
    companies = await company_service.search_company_name(query, x_wanted_language)
    return companies


@router.get("/companies/{company_name}",
            response_model=CompanyTagResponse)
async def get_company_by_name(
        company_name: str,
        x_wanted_language: str = fa.Header(...)
):
    company = await company_service.get_company_by_name(company_name, x_wanted_language)
    if not company:
        raise fa.HTTPException(status_code=404, detail="Company not found")
    return company


@router.post(
    "/companies",
    response_model=CompanyTagResponse)
async def create_company(
        payload: CompanyCreateRequest,
        x_wanted_language: str = fa.Header(...),
):
    return await company_service.create_company(payload, x_wanted_language)


@router.get(
    "/tags",
    response_model=t.List[CompanyResponse])
async def get_companies_by_tag(
        query: str,
        x_wanted_language: str = fa.Header(...)
):
    return await company_service.search_companies_by_tag(query, x_wanted_language)


@router.put(
    "/companies/{company_name}/tags",
    response_model=CompanyTagResponse)
async def update_company_tags(
        company_name: str,
        tags: t.List[TagNameRequest],
        x_wanted_language: str = fa.Header(...)
):
    return await company_service.add_tags_to_company(company_name, tags, x_wanted_language)


@router.delete(
    "/companies/{company_name}/tags/{tag_name}",
    response_model=CompanyTagResponse)
async def delete_company_tag(
        company_name: str,
        tag_name: str,
        x_wanted_language: str = fa.Header(...),
):
    return await company_service.delete_tag_from_company(company_name, tag_name, x_wanted_language)
