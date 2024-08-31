import typing as t

from searcher.company.model import Company, company_tag, CompanyName, TagName


def get_models() -> t.List[t.Any]:
    return [
        Company,
        company_tag,
        CompanyName,
        TagName
    ]
