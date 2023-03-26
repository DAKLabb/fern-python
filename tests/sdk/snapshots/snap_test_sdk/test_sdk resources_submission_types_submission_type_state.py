# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import pydantic
import typing_extensions

from ...commons.types.key_value_pair import KeyValuePair
from ...commons.types.map_value import MapValue
from ...commons.types.variable_value import VariableValue
from .test_submission_state import TestSubmissionState
from .workspace_submission_state import WorkspaceSubmissionState


class SubmissionTypeState_Test(TestSubmissionState):
    type: typing_extensions.Literal["test"] = "test"

    class Config:
        frozen = True


class SubmissionTypeState_Workspace(WorkspaceSubmissionState):
    type: typing_extensions.Literal["workspace"] = "workspace"

    class Config:
        frozen = True


SubmissionTypeState = typing_extensions.Annotated[
    typing.Union[SubmissionTypeState_Test, SubmissionTypeState_Workspace], pydantic.Field(discriminator="type")
]
SubmissionTypeState_Test.update_forward_refs(KeyValuePair=KeyValuePair, MapValue=MapValue, VariableValue=VariableValue)