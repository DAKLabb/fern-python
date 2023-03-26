# This file was auto-generated by Fern from our API Definition.

from ....core.exceptions.fern_http_exception import FernHTTPException
from ..types.movie_id import MovieId


class InvalidMovieError(FernHTTPException):
    def __init__(self, error: MovieId):
        super().__init__(status_code=400, name="InvalidMovieError", content=error)