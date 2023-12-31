import re

PASCAL_CASE_TO_SNAKE_CASE_1 = re.compile(r'(.)([A-Z][a-z]+)')
PASCAL_CASE_TO_SNAKE_CASE_2 = re.compile(r'([a-z0-9])([A-Z])')


def pascal_case_to_snake_case(value: str) -> str:
    """Converts PascalCase to snake_case.

    Usage: `OneToOneField(related_name=pascal_case_to_snake_case(__qualname__))`
    """
    value = PASCAL_CASE_TO_SNAKE_CASE_1.sub(r'\1_\2', value)
    value = PASCAL_CASE_TO_SNAKE_CASE_2.sub(r'\1_\2', value).lower()
    return value


def default_related_names(value: str) -> dict:
    """Create both related names in snake case.

    Usage: `ForeignKey(**default_related_names(__qualname__))`
    """
    related_query_name = pascal_case_to_snake_case(value)
    related_name = f'{related_query_name}_set'
    return {
        'related_name': related_name,
        'related_query_name': related_query_name
    }


def ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def url_include(url_patterns: list, app_name: str) -> tuple:
    return url_patterns, app_name
