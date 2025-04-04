from http import HTTPStatus

import allure
import pytest

from clients.operations_client import OperationsClient
from schema.operations import CreateOperationSchema, CreateOperationResponseSchema, GetOperationResponseSchema, StateEnum
from tools.assertions.base import assert_status_code
from tools.assertions.operations import assert_operation, assert_create_operation
from tools.assertions.schema import validate_json_schema


@pytest.mark.operations
@pytest.mark.regression
class TestOperations:
    @allure.title("Get operation with status PENDING")
    def test_get_operation(
            self,
            operations_client: OperationsClient,
            function_operation: CreateOperationSchema
    ):
        response = operations_client.get_operation_api(function_operation.task_id)
        operation_response = GetOperationResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_operation(operation_response, function_operation, expected_status="PENDING")

        validate_json_schema(response.json(), operation_response.model_json_schema())

    @allure.title("Create operation")
    def test_create_operation(self, operations_client: OperationsClient):
        # Явно указываем штат Florida для избежания двойных запросов
        request = CreateOperationSchema(state=StateEnum.Florida)
        response = operations_client.create_operation_api(request)
        operation_response = CreateOperationResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_operation(operation_response, request)

        validate_json_schema(response.json(), operation_response.model_json_schema())

    @pytest.mark.parametrize("state", [state for state in StateEnum])
    @allure.title("Create operation with different states: {state}")
    def test_create_operation_with_different_states(self, operations_client: OperationsClient, state: StateEnum):
        """
        Проверяет создание операций с использованием всех возможных значений штатов.
        
        :param operations_client: Клиент для работы с API операций
        :param state: Значение штата из перечисления StateEnum
        """
        # Создаем запрос с конкретным штатом
        request = CreateOperationSchema(state=state)
        
        # Выполняем запрос к API
        response = operations_client.create_operation_api(request)
        operation_response = CreateOperationResponseSchema.model_validate_json(response.text)
        
        # Проверяем успешный статус ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        
        # Проверяем ответ API
        assert_create_operation(operation_response, request)
        
        # Логируем информацию о созданной операции
        allure.attach(
            f"Создана операция для штата {state.name} ({state.value})",
            name="Информация о штате",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Проверяем схему ответа
        validate_json_schema(response.json(), operation_response.model_json_schema())

