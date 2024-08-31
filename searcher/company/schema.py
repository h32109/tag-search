import typing as t
from pydantic import BaseModel


class CompanyResponse(BaseModel):
    company_name: str


class TagResponse(BaseModel):
    name: str


class CompanyTagResponse(CompanyResponse):
    tags: t.List[str]


class TagNameRequest(BaseModel):
    tag_name: t.Dict[str, str]


class CompanyCreateRequest(BaseModel):
    company_name: t.Dict[str, str]
    tags: t.List[TagNameRequest]
