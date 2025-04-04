from datetime import date, timedelta
from faker import Faker
import random
from typing import List, Optional, Dict, Any


class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker
        
    def zip_code(self) -> str:
        """Генерирует валидный почтовый индекс в формате 12345 или 12345-6789"""
        if random.choice([True, False]):
            return self.faker.zipcode()
        return f"{self.faker.zipcode()}-{self.faker.zipcode_plus4()[:4]}"
    
    def address(self) -> dict:
        """Генерирует полный адрес"""
        return {
            "street": self.faker.street_address(),
            "extra": self.faker.secondary_address() if random.choice([True, False]) else None,
            "city": self.faker.city(),
            "state": self.faker.state_abbr(),
            "zipCode": self.zip_code(),
            "county": self.faker.country()
        }
    
    def company(self) -> dict:
        """Генерирует информацию о компании"""
        designators = ["LLC", "Inc.", "Corp.", "Ltd.", "LP", "LLP"]
        return {
            "name": self.faker.company().split(",")[0],  # Берем только название без обозначения
            "designator": random.choice(designators),
            "address": self.address(),
            "mailing_address": self.address()
        }
    
    def contact(self) -> dict:
        """Генерирует контактную информацию"""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        return {
            "firstName": first_name,
            "lastName": last_name,
            "email": self.faker.email(),
            "mobile": self.faker.phone_number()
        }
    
    def member(self) -> dict:
        """Генерирует информацию о члене организации"""
        is_individual = random.choice([True, False])
        return {
            "isIndividual": is_individual,
            "firstName": self.faker.first_name() if is_individual else None,
            "lastName": self.faker.last_name() if is_individual else None,
            "companyName": None if is_individual else self.faker.company().split(",")[0],
            "address": self.address(),
            "percentOfOwnership": random.randint(1, 100)
        }
    
    def agent(self) -> dict:
        """Генерирует информацию об агенте"""
        is_individual = random.choice([True, False])
        return {
            "isIndividual": is_individual,
            "firstName": self.faker.first_name(),
            "lastName": self.faker.last_name(),
            "companyName": "" if is_individual else self.faker.company().split(",")[0],
            "address": self.address()
        }
    
    def organizer(self) -> dict:
        """Генерирует информацию об организаторе"""
        is_individual = random.choice([True, False])
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        address = self.address()
        
        return {
            "isIndividual": is_individual,
            "firstName": first_name,
            "lastName": last_name,
            "middleName": self.faker.first_name() if random.choice([True, False]) else None,
            "companyName": None if is_individual else self.faker.company().split(",")[0],
            "email": self.faker.email(),
            "phone": self.faker.phone_number(),
            "addressStreet": address["street"],
            "addressExtra": address["extra"],
            "addressState": address["state"],
            "addressCity": address["city"],
            "addressZipCode": address["zipCode"],
            "addressCountry": "US",
            "addressCounty": address["county"]
        }
    
    def entity_data(self) -> dict:
        """Генерирует полный набор данных для сущности"""
        entity_types = ["LLC", "Corporation", "Partnership", "Sole Proprietorship"]
        activity_types = ["Professional Services", "Retail", "Manufacturing", "Technology", "Real Estate"]
        
        # Создаем от 1 до 5 членов
        members_count = random.randint(1, 5)
        members = [self.member() for _ in range(members_count)]
        
        return {
            "entityType": random.choice(entity_types),
            "entityState": self.faker.state_abbr(),
            "activityType": random.choice(activity_types),
            "naicsCode": random.randint(100000, 999999),
            "company": self.company(),
            "contact": self.contact(),
            "isManagerManaged": random.choice([True, False]),
            "members": members,
            "agent": self.agent(),
            "organizer": self.organizer()
        }
    
    def credentials(self) -> dict:
        """Генерирует учетные данные"""
        return {
            "username": self.faker.user_name(),
            "password": self.faker.password(length=12),
        }
    
    def root_model(self) -> dict:
        """Генерирует полную модель данных"""
        return {
            "state": self.faker.state_abbr(),
            "credentials": self.credentials(),
            "data": self.entity_data()
        }



fake = Fake(faker=Faker())