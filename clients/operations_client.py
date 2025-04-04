import allure
from httpx import Response

from clients.base_client import BaseClient, get_http_client
from config import Settings
from schema.operations import CreateOperationSchema, CreateOperationResponseSchema
from tools.routes import APIRoutes


class OperationsClient(BaseClient):
    """
    Клиент для взаимодействия с сайтами.
    """
    @allure.step("Get operation by id {operation_id}")
    def get_operation_api(self, operation_id: int) -> Response:
        """
        Получить операцию по идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера с информацией об операции.
        """
        return self.get(f"{APIRoutes.GET_RESULT}/{operation_id}")

    @allure.step("Create operation")
    def create_operation_api(self, operation: CreateOperationSchema) -> Response:
        """
        Создать операцию.

        :param operation: Данные для создания новой операции.
        :return: Ответ от сервера с информацией о созданной операции.
        """
        return self.post(
            APIRoutes.VALIDATE_DATA,
            json=operation.model_dump(mode='json', by_alias=True)
        )

    # @allure.step("Get list of operations")
    # def get_operations_api(self) -> Response:
    #     return self.get(APIRoutes.OPERATIONS)

    # @allure.step("Update operation by id {operation_id}")
    # def update_operation_api(
    #         self,
    #         operation_id: int,
    #         operation: UpdateOperationSchema
    # ) -> Response:
    #     return self.patch(
    #         f"{APIRoutes.OPERATIONS}/{operation_id}",
    #         json=operation.model_dump(mode='json', by_alias=True, exclude_none=True)
    # )

    # @allure.step("Delete operation by id {operation_id}")
    # def delete_operation_api(self, operation_id: int) -> Response:
    #     return self.delete(f"{APIRoutes.OPERATIONS}/{operation_id}")

    def create_operation(self) -> CreateOperationResponseSchema:
        """
        Упрощенный метод для создания новой операции.

        Этот метод создает операцию с помощью схемы `CreateOperationSchema`, отправляет запрос
        на создание, а затем преобразует ответ в объект `CreateOperationResponseSchema`.

        :return: Объект `OperationSchema`, представляющий созданную операцию.
        """
        request = CreateOperationSchema()
        response = self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)


def get_operations_client(settings: Settings) -> OperationsClient:
    return OperationsClient(client=get_http_client(settings.fake_bank_http_client))
