from __future__ import annotations

import typing

import pydantic
import typing_extensions

from .error_info import ErrorInfo
from .running_submission_state import RunningSubmissionState
from .workspace_run_details import WorkspaceRunDetails
from .workspace_traced_update import WorkspaceTracedUpdate

T_Result = typing.TypeVar("T_Result")


class _Factory:
    def running(self, value: RunningSubmissionState) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(
            __root__=_WorkspaceSubmissionUpdateInfo.Running(type="running", value=value)
        )

    def ran(self, value: WorkspaceRunDetails) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(__root__=_WorkspaceSubmissionUpdateInfo.Ran(**dict(value), type="ran"))

    def stopped(self) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(__root__=_WorkspaceSubmissionUpdateInfo.Stopped(type="stopped"))

    def traced(self) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(__root__=_WorkspaceSubmissionUpdateInfo.Traced(type="traced"))

    def traced_v_2(self, value: WorkspaceTracedUpdate) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(
            __root__=_WorkspaceSubmissionUpdateInfo.TracedV2(**dict(value), type="tracedV2")
        )

    def errored(self, value: ErrorInfo) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(
            __root__=_WorkspaceSubmissionUpdateInfo.Errored(type="errored", value=value)
        )

    def finished(self) -> WorkspaceSubmissionUpdateInfo:
        return WorkspaceSubmissionUpdateInfo(__root__=_WorkspaceSubmissionUpdateInfo.Finished(type="finished"))


class WorkspaceSubmissionUpdateInfo(pydantic.BaseModel):
    factory: typing.ClassVar[_Factory] = _Factory()

    def get_as_union(
        self,
    ) -> typing.Union[
        _WorkspaceSubmissionUpdateInfo.Running,
        _WorkspaceSubmissionUpdateInfo.Ran,
        _WorkspaceSubmissionUpdateInfo.Stopped,
        _WorkspaceSubmissionUpdateInfo.Traced,
        _WorkspaceSubmissionUpdateInfo.TracedV2,
        _WorkspaceSubmissionUpdateInfo.Errored,
        _WorkspaceSubmissionUpdateInfo.Finished,
    ]:
        return self.__root__

    def visit(
        self,
        running: typing.Callable[[RunningSubmissionState], T_Result],
        ran: typing.Callable[[WorkspaceRunDetails], T_Result],
        stopped: typing.Callable[[], T_Result],
        traced: typing.Callable[[], T_Result],
        traced_v_2: typing.Callable[[WorkspaceTracedUpdate], T_Result],
        errored: typing.Callable[[ErrorInfo], T_Result],
        finished: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self.__root__.type == "running":
            return running(self.__root__.running)
        if self.__root__.type == "ran":
            return ran(self.__root__)
        if self.__root__.type == "stopped":
            return stopped()
        if self.__root__.type == "traced":
            return traced()
        if self.__root__.type == "tracedV2":
            return traced_v_2(self.__root__)
        if self.__root__.type == "errored":
            return errored(self.__root__.errored)
        if self.__root__.type == "finished":
            return finished()

    __root__: typing_extensions.Annotated[
        typing.Union[
            _WorkspaceSubmissionUpdateInfo.Running,
            _WorkspaceSubmissionUpdateInfo.Ran,
            _WorkspaceSubmissionUpdateInfo.Stopped,
            _WorkspaceSubmissionUpdateInfo.Traced,
            _WorkspaceSubmissionUpdateInfo.TracedV2,
            _WorkspaceSubmissionUpdateInfo.Errored,
            _WorkspaceSubmissionUpdateInfo.Finished,
        ],
        pydantic.Field(discriminator="type"),
    ]

    @pydantic.root_validator
    def _validate(cls, values: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        value = typing.cast(
            typing.Union[
                _WorkspaceSubmissionUpdateInfo.Running,
                _WorkspaceSubmissionUpdateInfo.Ran,
                _WorkspaceSubmissionUpdateInfo.Stopped,
                _WorkspaceSubmissionUpdateInfo.Traced,
                _WorkspaceSubmissionUpdateInfo.TracedV2,
                _WorkspaceSubmissionUpdateInfo.Errored,
                _WorkspaceSubmissionUpdateInfo.Finished,
            ],
            values.get("__root__"),
        )
        for validator in WorkspaceSubmissionUpdateInfo.Validators._validators:
            value = validator(value)
        return {**values, "__root__": value}

    class Validators:
        _validators: typing.ClassVar[
            typing.List[
                typing.Callable[
                    [
                        typing.Union[
                            _WorkspaceSubmissionUpdateInfo.Running,
                            _WorkspaceSubmissionUpdateInfo.Ran,
                            _WorkspaceSubmissionUpdateInfo.Stopped,
                            _WorkspaceSubmissionUpdateInfo.Traced,
                            _WorkspaceSubmissionUpdateInfo.TracedV2,
                            _WorkspaceSubmissionUpdateInfo.Errored,
                            _WorkspaceSubmissionUpdateInfo.Finished,
                        ]
                    ],
                    typing.Union[
                        _WorkspaceSubmissionUpdateInfo.Running,
                        _WorkspaceSubmissionUpdateInfo.Ran,
                        _WorkspaceSubmissionUpdateInfo.Stopped,
                        _WorkspaceSubmissionUpdateInfo.Traced,
                        _WorkspaceSubmissionUpdateInfo.TracedV2,
                        _WorkspaceSubmissionUpdateInfo.Errored,
                        _WorkspaceSubmissionUpdateInfo.Finished,
                    ],
                ]
            ]
        ] = []

        @classmethod
        def validate(
            cls,
            validator: typing.Callable[
                [
                    typing.Union[
                        _WorkspaceSubmissionUpdateInfo.Running,
                        _WorkspaceSubmissionUpdateInfo.Ran,
                        _WorkspaceSubmissionUpdateInfo.Stopped,
                        _WorkspaceSubmissionUpdateInfo.Traced,
                        _WorkspaceSubmissionUpdateInfo.TracedV2,
                        _WorkspaceSubmissionUpdateInfo.Errored,
                        _WorkspaceSubmissionUpdateInfo.Finished,
                    ]
                ],
                typing.Union[
                    _WorkspaceSubmissionUpdateInfo.Running,
                    _WorkspaceSubmissionUpdateInfo.Ran,
                    _WorkspaceSubmissionUpdateInfo.Stopped,
                    _WorkspaceSubmissionUpdateInfo.Traced,
                    _WorkspaceSubmissionUpdateInfo.TracedV2,
                    _WorkspaceSubmissionUpdateInfo.Errored,
                    _WorkspaceSubmissionUpdateInfo.Finished,
                ],
            ],
        ) -> None:
            cls._validators.append(validator)

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    class Config:
        frozen = True


class _WorkspaceSubmissionUpdateInfo:
    class Running(pydantic.BaseModel):
        type: typing_extensions.Literal["running"]
        value: RunningSubmissionState

        class Config:
            frozen = True

    class Ran(WorkspaceRunDetails):
        type: typing_extensions.Literal["ran"]

        class Config:
            frozen = True

    class Stopped(pydantic.BaseModel):
        type: typing_extensions.Literal["stopped"]

        class Config:
            frozen = True

    class Traced(pydantic.BaseModel):
        type: typing_extensions.Literal["traced"]

        class Config:
            frozen = True

    class TracedV2(WorkspaceTracedUpdate):
        type: typing_extensions.Literal["tracedV2"]

        class Config:
            frozen = True

    class Errored(pydantic.BaseModel):
        type: typing_extensions.Literal["errored"]
        value: ErrorInfo

        class Config:
            frozen = True

    class Finished(pydantic.BaseModel):
        type: typing_extensions.Literal["finished"]

        class Config:
            frozen = True


WorkspaceSubmissionUpdateInfo.update_forward_refs()