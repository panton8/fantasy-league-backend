
from typing import Type

from drf_spectacular.generators import SchemaGenerator as SchemaGeneratorBase


class SchemaGenerator(SchemaGeneratorBase):
    add_prefix = ''

    def parse(self, input_request, public):
        result = super().parse(input_request, public)

        return {
            f'{self.add_prefix}{path}': operation for path, operation in result.items()
        }


def get_schema_generator(prefix: str) -> Type:
    return type('SchemaGeneratorSpec', (SchemaGenerator, ), {'add_prefix': prefix})
