from __future__ import annotations

import typing

import pydantic
import typing_extensions

from .declared_type_name import DeclaredTypeName
from .single_union_type_property import SingleUnionTypeProperty

T_Result = typing.TypeVar("T_Result")


class _Factory:
    def same_properties_as_object(self, value: DeclaredTypeName) -> SingleUnionTypeProperties:
        return SingleUnionTypeProperties(
            __root__=_SingleUnionTypeProperties.SamePropertiesAsObject(
                **dict(value), properties_type="samePropertiesAsObject"
            )
        )

    def single_property(self, value: SingleUnionTypeProperty) -> SingleUnionTypeProperties:
        return SingleUnionTypeProperties(
            __root__=_SingleUnionTypeProperties.SingleProperty(**dict(value), properties_type="singleProperty")
        )

    def no_properties(self) -> SingleUnionTypeProperties:
        return SingleUnionTypeProperties(
            __root__=_SingleUnionTypeProperties.NoProperties(properties_type="noProperties")
        )


class SingleUnionTypeProperties(pydantic.BaseModel):
    factory: typing.ClassVar[_Factory] = _Factory()

    def get(
        self,
    ) -> typing.Union[
        _SingleUnionTypeProperties.SamePropertiesAsObject,
        _SingleUnionTypeProperties.SingleProperty,
        _SingleUnionTypeProperties.NoProperties,
    ]:
        return self.__root__

    def visit(
        self,
        same_properties_as_object: typing.Callable[[DeclaredTypeName], T_Result],
        single_property: typing.Callable[[SingleUnionTypeProperty], T_Result],
        no_properties: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self.__root__.properties_type == "samePropertiesAsObject":
            return same_properties_as_object(self.__root__)
        if self.__root__.properties_type == "singleProperty":
            return single_property(self.__root__)
        if self.__root__.properties_type == "noProperties":
            return no_properties()

    __root__: typing_extensions.Annotated[
        typing.Union[
            _SingleUnionTypeProperties.SamePropertiesAsObject,
            _SingleUnionTypeProperties.SingleProperty,
            _SingleUnionTypeProperties.NoProperties,
        ],
        pydantic.Field(discriminator="properties_type"),
    ]


class _SingleUnionTypeProperties:
    class SamePropertiesAsObject(DeclaredTypeName):
        properties_type: typing.Literal["samePropertiesAsObject"] = pydantic.Field(alias="_type")

        class Config:
            allow_population_by_field_name = True

    class SingleProperty(SingleUnionTypeProperty):
        properties_type: typing.Literal["singleProperty"] = pydantic.Field(alias="_type")

        class Config:
            allow_population_by_field_name = True

    class NoProperties(pydantic.BaseModel):
        properties_type: typing.Literal["noProperties"] = pydantic.Field(alias="_type")

        class Config:
            allow_population_by_field_name = True


SingleUnionTypeProperties.update_forward_refs()