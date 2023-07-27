# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .bank_account_response import BankAccountResponse
from .card_response import CardResponse
from .check_response import CheckResponse
from .custom_payment_method_response import CustomPaymentMethodResponse


class PaymentMethodResponse_BankAccount(BankAccountResponse):
    type: typing_extensions.Literal["bankAccount"]

    class Config:
        allow_population_by_field_name = True


class PaymentMethodResponse_Card(CardResponse):
    type: typing_extensions.Literal["card"]

    class Config:
        allow_population_by_field_name = True


class PaymentMethodResponse_Check(CheckResponse):
    type: typing_extensions.Literal["check"]

    class Config:
        allow_population_by_field_name = True


class PaymentMethodResponse_Custom(CustomPaymentMethodResponse):
    type: typing_extensions.Literal["custom"]

    class Config:
        allow_population_by_field_name = True


PaymentMethodResponse = typing.Union[
    PaymentMethodResponse_BankAccount,
    PaymentMethodResponse_Card,
    PaymentMethodResponse_Check,
    PaymentMethodResponse_Custom,
]