from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, RootModel

from tools.fakers import fake

class StateEnum(str, Enum):
    Kansas = "KS"
    Wyoming = "WY"
    Florida = "FL"
    Kentucky = "KY"
    Vermont = "VT"
    Arkansas = "AR"
    California = "CA"
    NorthCarolina = "NC"
    Idaho = "ID"
    Alabama = "AL"
    Louisiana = "LA"
    Georgia = "GE"
    Tennessee = "TN"
    Iowa = "IA"
    NewJersey = "NJ"
    SouthDakota = "SD"
    Oregon = "OR"
    Alaska = "AK"
    Missouri = "MO"
    Maryland = "MD"
    Nebraska = "NE"
    Nevada = "NV"
    SouthCarolina = "SC"
    Wisconsin = "WI"
    Pennsylvania = "PA"
    Washington = "WA"
    Colorado = "CO"
    Delaware = "DE"
    NewYork = "NY"
    NewHampshire = "NH"
    NewMexico = "NM"
    RhodeIsland = "RI"
    NorthDakota = "ND"
    Indiana = "IN"


class CreateOperationSchema(BaseModel):
    """
    Модель для создания новой операции заполнения сайта.
    
    Поля:
    - state (str): Штат
    - credentials(dict | None): Учетные данные
    - data (dict): Данные для заполнения формы
    """
    model_config = ConfigDict(populate_by_name=True)

    state: StateEnum = Field(StateEnum.Florida)
    credentials: dict | None = Field(default_factory=fake.credentials)
    data: dict = Field(default_factory=fake.entity_data)

class CreateOperationResponseSchema(BaseModel):
    """
    Модель ответа API после создания операции.
    
    Поля:
    - success (bool): Флаг успешного выполнения операции
    - task_id (str): Идентификатор созданной задачи
    """
    success: bool
    task_id: str

class GetOperationResponseSchema(BaseModel):
    """
    Модель ответа API при получении статуса операции.
    
    Поля:
    - status (str): Статус операции (например, "PENDING", "COMPLETED", "FAILED")
    - task_id (str, optional): Идентификатор задачи
    - result (dict, optional): Результат выполнения задачи, если она завершена
    - error (str, optional): Сообщение об ошибке, если задача завершилась неудачно
    """
    status: str
    task_id: str | None = None
    result: dict | None = None
    error: str | None = None
