# This file was auto-generated by Fern from our API Definition.

# flake8: noqa
# fmt: off
# isort: skip_file

from __future__ import annotations

import typing

import pydantic
import typing_extensions

from .parameter_id import ParameterId


class DeepEqualityCorrectnessCheck(pydantic.BaseModel):
    expected_value_parameter_id: ParameterId = pydantic.Field(alias="expectedValueParameterId")

    class Validators:
        """
        Use this class to add validators to the Pydantic model.

            @DeepEqualityCorrectnessCheck.Validators.field("expected_value_parameter_id")
            def validate_expected_value_parameter_id(v: ParameterId, values: DeepEqualityCorrectnessCheck.Partial) -> ParameterId:
                ...
        """

        _expected_value_parameter_id_validators: typing.ClassVar[
            typing.List[DeepEqualityCorrectnessCheck.Validators.ExpectedValueParameterIdValidator]
        ] = []

        @typing.overload  # type: ignore
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["expected_value_parameter_id"]
        ) -> typing.Callable[
            [DeepEqualityCorrectnessCheck.Validators.ExpectedValueParameterIdValidator],
            DeepEqualityCorrectnessCheck.Validators.ExpectedValueParameterIdValidator,
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "expected_value_parameter_id":
                    cls._expected_value_parameter_id_validators.append(validator)
                return validator

            return decorator

        class ExpectedValueParameterIdValidator(typing_extensions.Protocol):
            def __call__(self, v: ParameterId, *, values: DeepEqualityCorrectnessCheck.Partial) -> ParameterId:
                ...

    @pydantic.validator("expected_value_parameter_id")
    def _validate_expected_value_parameter_id(
        cls, v: ParameterId, values: DeepEqualityCorrectnessCheck.Partial
    ) -> ParameterId:
        for validator in DeepEqualityCorrectnessCheck.Validators._expected_value_parameter_id_validators:
            v = validator(v, values=values)
        return v

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Partial(typing.TypedDict):
        expected_value_parameter_id: typing_extensions.NotRequired[ParameterId]

    class Config:
        frozen = True
        allow_population_by_field_name = True