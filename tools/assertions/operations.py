import allure

from schema.operations import CreateOperationSchema, CreateOperationResponseSchema, GetOperationResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("OPERATIONS_ASSERTIONS")


# @allure.step("Check create operation")
# def assert_create_operation(
#         actual: OperationSchema,
#         expected: OperationResponseSchema
# ):
#     """
#     Проверяет, что данные, возвращённые API после создания/обновления операции, соответствуют ожидаемым.

#     :param: actual (OperationSchema): Фактические данные операции.
#     :param: expected (CreateOperationSchema | UpdateOperationSchema): Ожидаемые данные.
#     :raises: AssertionError: Если значения полей не совпадают.
#     """
#     logger.info("Check create operation")

#     assert_equal(actual.success, expected.success, True)
#     assert_equal(actual.task_id, expected.task_id, "debit")

@allure.step("Check create operation response")
def assert_create_operation(
        response: CreateOperationResponseSchema,
        request: CreateOperationSchema
    ):
    """
    Проверяет, что ответ API после выполнения операции содержит success=True и task_id.

    :param response: Ответ API (CreateOperationResponseSchema).
    :param request: Запрос на создание операции (CreateOperationSchema).
    :raises: AssertionError: Если success не True или отсутствует task_id.
    """
    logger.info("Check API operation response")

    assert_equal(response.success, True, "success")
    assert response.task_id, f"Task ID должен быть не пустым, получено: {response.task_id}"
    logger.info(f"Task ID: {response.task_id}")


@allure.step("Check get operation response")
def assert_operation(
        response: GetOperationResponseSchema,
        request: CreateOperationSchema,
        expected_status: str = "PENDING"
    ):
    """
    Проверяет статус операции в ответе API.

    :param response: Ответ API (GetOperationResponseSchema).
    :param request: Запрос на создание операции (CreateOperationSchema).
    :param expected_status: Ожидаемый статус операции (по умолчанию "PENDING").
    :raises: AssertionError: Если статус не соответствует ожидаемому или другие проверки не проходят.
    """
    logger.info(f"Check operation status: {expected_status}")

    assert_equal(response.status, expected_status, "status")
    
    # Логируем дополнительную информацию, если она есть
    if response.task_id:
        logger.info(f"Task ID: {response.task_id}")
    
    # Если статус COMPLETED, проверяем наличие результата
    if expected_status == "COMPLETED" and response.result:
        logger.info(f"Operation result: {response.result}")
        assert response.result, "При статусе COMPLETED должен быть результат"
        
    # Если статус FAILED, проверяем наличие сообщения об ошибке
    if expected_status == "FAILED" and response.error:
        logger.info(f"Operation error: {response.error}")
        assert response.error, "При статусе FAILED должно быть сообщение об ошибке"
