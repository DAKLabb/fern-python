# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx
import pydantic

from ...core.api_error import ApiError
from ...core.jsonable_encoder import jsonable_encoder
from ...core.remove_none_from_headers import remove_none_from_headers
from ...environment import FernIrEnvironment
from ..commons.types.problem_id import ProblemId


class HomepageClient:
    def __init__(
        self,
        *,
        environment: FernIrEnvironment = FernIrEnvironment.PROD,
        x_random_header: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        client: httpx.Client,
    ):
        self._environment = environment
        self._x_random_header = x_random_header
        self._token = token
        self._client = client

    def get_homepage_problems(self) -> typing.List[ProblemId]:
        _response = httpx.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "homepage-problems"),
            headers=remove_none_from_headers(
                {
                    "X-Random-Header": self._x_random_header,
                    "Authorization": f"Bearer {self._token}" if self._token is not None else None,
                }
            ),
            timeout=None,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[ProblemId], _response_json)  # type: ignore
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def set_homepage_problems(self, *, request: typing.List[ProblemId]) -> None:
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "homepage-problems"),
            json=jsonable_encoder(request),
            headers=remove_none_from_headers(
                {
                    "X-Random-Header": self._x_random_header,
                    "Authorization": f"Bearer {self._token}" if self._token is not None else None,
                }
            ),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncHomepageClient:
    def __init__(
        self,
        *,
        environment: FernIrEnvironment = FernIrEnvironment.PROD,
        x_random_header: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        client: httpx.AsyncClient,
    ):
        self._environment = environment
        self._x_random_header = x_random_header
        self._token = token
        self._client = client

    async def get_homepage_problems(self) -> typing.List[ProblemId]:
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "GET",
                urllib.parse.urljoin(f"{self._environment.value}/", "homepage-problems"),
                headers=remove_none_from_headers(
                    {
                        "X-Random-Header": self._x_random_header,
                        "Authorization": f"Bearer {self._token}" if self._token is not None else None,
                    }
                ),
                timeout=None,
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[ProblemId], _response_json)  # type: ignore
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def set_homepage_problems(self, *, request: typing.List[ProblemId]) -> None:
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.value}/", "homepage-problems"),
                json=jsonable_encoder(request),
                headers=remove_none_from_headers(
                    {
                        "X-Random-Header": self._x_random_header,
                        "Authorization": f"Bearer {self._token}" if self._token is not None else None,
                    }
                ),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
