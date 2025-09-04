from types import GenericAlias, UnionType
from typing import Any, get_origin, get_args

from pydantic import BaseModel as pyBaseModel

from app.core.base.base_enum import BaseEnum
from app.core.utils.utils import Utils


class BaseModel(pyBaseModel):

    class Config:
        use_enum_values = True

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

    @classmethod
    def required_fields(cls) -> list:
        return cls.__get_fields(required=True)

    @classmethod
    def optional_fields(cls) -> list:
        return cls.__get_fields(required=False)

    @classmethod
    def get_fields(cls) -> list:
        return cls.__get_fields()

    @classmethod
    def __get_fields(cls, recursive: bool = True, required: bool | None = None) -> list:
        result = []
        for name, field in cls.model_fields.items():
            if required is not None and((required and not field.is_required()) or (not required and field.is_required())):
                continue
            t = field.annotation
            if recursive and isinstance(t, type) and issubclass(t, BaseModel):
                result.append({name: t.__get_fields(recursive=True)})
            else:
                result.append(name)
        return result

    @classmethod
    def create_instance(cls, params):
        for name, field in cls.model_fields.items():
            t = field.annotation
            if isinstance(t, type) and issubclass(t, BaseModel):
                sub_params = params.get(name)
                sub_params[name] = t.create_instance(sub_params).dict()
            if isinstance(t, GenericAlias) and t.__origin__ == list:
                sub_class = t.__args__[0] if t.__args__ else None
                sub_items = []
                for elem in params.get(name, []):
                    if isinstance(sub_class, type) and issubclass(sub_class, BaseModel):
                        elem = sub_class.create_instance(elem).dict()
                    sub_items.append(elem)
                params[name] = sub_items
        return cls(**params)

    @classmethod
    def sanityze_fields(cls, params: dict) -> dict:
        result = {}

        if not isinstance(params, dict):
            return result

        for name, field in cls.model_fields.items():
            if name not in params:
                continue

            item_type = field.annotation
            item_value = params.get(name)

            if isinstance(item_type, type) and issubclass(item_type, BaseModel) and isinstance(item_value, dict):
                result[name] = item_type.sanityze_fields(item_value)
                continue

            if isinstance(item_type, GenericAlias) and item_type.__origin__ == list:
                if not isinstance(item_value, list):
                    continue

                nested_item_type = item_type.__args__[0] if item_type.__args__ else None
                nested_item_value = []

                for elem in params.get(name, []):
                    if isinstance(nested_item_type, type) and issubclass(nested_item_type, BaseModel) and isinstance(elem, dict):
                        elem = nested_item_type.sanityze_fields(elem)
                        if not elem:
                            continue

                        nested_item_value.append(elem)

                    if isinstance(elem, nested_item_type):
                        nested_item_value.append(elem)

                result[name] = nested_item_value
                continue

            origin = get_origin(item_type)
            if origin is UnionType:
                for arg in get_args(item_type):
                    if isinstance(arg, type) and issubclass(arg, BaseModel) and isinstance(item_value, dict):
                        result[name] = arg.sanityze_fields(item_value)
                        break

                    if isinstance(arg, GenericAlias) and arg.__origin__ == list:
                        if not isinstance(item_value, list):
                            break

                        nested_item_type = arg.__args__[0] if arg.__args__ else None
                        nested_item_value = []

                        for elem in params.get(name, []):
                            if isinstance(nested_item_type, type) and issubclass(nested_item_type,
                                                                                 BaseModel) and isinstance(elem, dict):
                                elem = nested_item_type.sanityze_fields(elem)
                                if not elem:
                                    continue

                                nested_item_value.append(elem)

                            if isinstance(elem, nested_item_type):
                                nested_item_value.append(elem)

                            if issubclass(nested_item_type, BaseEnum):
                                if nested_item_type(elem):
                                    nested_item_value.append(elem)

                        result[name] = nested_item_value
                        break
                    # TODO: Chiedere confronto sulla posizione
                    if issubclass(arg, BaseEnum) and arg(item_value):
                        result[name] = item_value
                        continue

                    if isinstance(item_value, arg):
                        result[name] = item_value
                        continue
                continue

            if isinstance(item_value, item_type):
                result[name] = item_value
                continue

        return result

    @classmethod
    @property
    def __hierarchy_annotations__(cls) -> str:
        return Utils.merge_dict(cls.__annotations__, super(cls, cls).__annotations__)

    def dict_filtered(self, exclude_fields=None) -> dict:
        if exclude_fields is None:
            exclude_fields = {}
        return self.model_dump(exclude=exclude_fields)


if __name__ == "__main__":
    class PersonModel(BaseModel):
        first_name: str
        last_name: str

    p = PersonModel(**{"first_name": "Mario", "last_name": "Rossi"})

    print(p.__hierarchy_annotations__)
    print(PersonModel.__hierarchy_annotations__)

    # class ClassModel(BaseModel):
    #     rappresentante: PersonModel
    #     alunni: list[PersonModel]
    #     aula: str | None = None
    #     aule: list[str]
    #
    #
    # data = {"rappresentante": PersonModel, "aula": 7, "aule": ["6", "5", {"a", "r"}, 5, PersonModel(**{"first_name": "Nome", "last_name": "", "last_name_2": ""}).dict()],
    #         "alunni": []}
    # p1 = ClassModel.sanityze_fields(data)
    # print(p1)

