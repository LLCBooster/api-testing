from http import HTTPStatus
import time

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

    def wait_for_status_change(
            self, 
            operations_client: OperationsClient,
            task_id: str, 
            initial_status: str,
            max_retries: int = 10, 
            retry_delay: int = 3
    ) -> GetOperationResponseSchema:
        """
        Ожидает изменения статуса операции с повторными попытками.
        
        Args:
            operations_client: Клиент для работы с API операций
            task_id: Идентификатор задачи
            initial_status: Начальный статус, изменение которого ожидается
            max_retries: Максимальное количество попыток
            retry_delay: Задержка между попытками в секундах
        
        Returns:
            GetOperationResponseSchema: Ответ API с измененным статусом
            
        Raises:
            AssertionError: Если статус не изменился за максимальное число попыток
        """
        for attempt in range(max_retries):
            response = operations_client.get_operation_api(task_id)
            operation_response = GetOperationResponseSchema.model_validate_json(response.text)
            
            # Если статус изменился, возвращаем ответ
            if operation_response.status != initial_status:
                allure.attach(
                    f"Статус изменен с {initial_status} на {operation_response.status} на попытке {attempt + 1}",
                    name="Изменение статуса",
                    attachment_type=allure.attachment_type.TEXT
                )
                return operation_response
            
            # Логируем текущую попытку
            allure.attach(
                f"Попытка {attempt + 1}/{max_retries}: статус все еще {operation_response.status}",
                name="Ожидание изменения статуса",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Ждем перед следующей попыткой
            time.sleep(retry_delay)
        
        # Если статус не изменился после всех попыток, вызываем ошибку
        raise AssertionError(f"Статус операции не изменился с {initial_status} после {max_retries} попыток")

    @allure.title("Check operation status change over time")
    def test_operation_status_change(self, operations_client: OperationsClient):
        """
        Проверяет изменение статуса операции с течением времени.
        Ожидается, что сначала операция будет в статусе PENDING,
        а затем перейдет в другой статус.
        """
        # Создаем новую операцию
        request = CreateOperationSchema(state=StateEnum.Florida)
        response = operations_client.create_operation_api(request)
        operation_response = CreateOperationResponseSchema.model_validate_json(response.text)
        
        # Проверяем успешное создание операции
        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_operation(operation_response, request)
        
        # Получаем начальный статус операции
        task_id = operation_response.task_id
        initial_response = operations_client.get_operation_api(task_id)
        initial_operation = GetOperationResponseSchema.model_validate_json(initial_response.text)
        
        # Проверяем начальный статус
        assert_status_code(initial_response.status_code, HTTPStatus.OK)
        assert initial_operation.status == "PENDING", f"Начальный статус должен быть PENDING, получено: {initial_operation.status}"
        
        # Ждем изменения статуса
        changed_operation = self.wait_for_status_change(
            operations_client=operations_client,
            task_id=task_id,
            initial_status="PENDING",
            max_retries=10,  # Максимальное количество попыток
            retry_delay=3    # Время между попытками в секундах
        )
        
        # Проверяем, что статус изменился
        assert changed_operation.status != "PENDING", f"Статус должен был измениться с PENDING, но получено: {changed_operation.status}"
        
        # Дополнительные проверки в зависимости от ожидаемого конечного статуса
        assert changed_operation.status in ["COMPLETED", "FAILED"], f"Ожидался статус COMPLETED или FAILED, получено: {changed_operation.status}"
        
        # Если статус COMPLETED, проверяем наличие результата
        if changed_operation.status == "COMPLETED":
            assert changed_operation.result is not None, "Для завершенной операции должен быть результат"
        
        # Если статус FAILED, проверяем наличие ошибки
        if changed_operation.status == "FAILED":
            assert changed_operation.error is not None, "Для проваленной операции должно быть сообщение об ошибке"
        
        # Проверяем схему ответа
        validate_json_schema(initial_response.json(), initial_operation.model_json_schema())



    # @allure.title("Create operation")
    # def test_create_operation(self, operations_client: OperationsClient):
    #     # Явно указываем штат Florida для избежания двойных запросов
    #     request = CreateOperationSchema(state=StateEnum.Florida)
    #     response = operations_client.create_operation_api(request)
    #     operation_response = CreateOperationResponseSchema.model_validate_json(response.text)

    #     assert_status_code(response.status_code, HTTPStatus.OK)
    #     assert_create_operation(operation_response, request)

    #     validate_json_schema(response.json(), operation_response.model_json_schema())

    # @pytest.mark.parametrize("state", [state for state in StateEnum])
    # @allure.title("Create operation with different states: {state}")
    # def test_create_operation_with_different_states(self, operations_client: OperationsClient, state: StateEnum):
    #     """
    #     Проверяет создание операций с использованием всех возможных значений штатов.
        
    #     :param operations_client: Клиент для работы с API операций
    #     :param state: Значение штата из перечисления StateEnum
    #     """
    #     # Создаем запрос с конкретным штатом
    #     request = CreateOperationSchema(state=state)
        
    #     # Выполняем запрос к API
    #     response = operations_client.create_operation_api(request)
    #     operation_response = CreateOperationResponseSchema.model_validate_json(response.text)
        
    #     # Проверяем успешный статус ответа
    #     assert_status_code(response.status_code, HTTPStatus.OK)
        
    #     # Проверяем ответ API
    #     assert_create_operation(operation_response, request)
        
    #     # Логируем информацию о созданной операции
    #     allure.attach(
    #         f"Создана операция для штата {state.name} ({state.value})",
    #         name="Информация о штате",
    #         attachment_type=allure.attachment_type.TEXT
    #     )
        
    #     # Проверяем схему ответа
    #     validate_json_schema(response.json(), operation_response.model_json_schema())

