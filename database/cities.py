import logging
from random import randint

import pandas as pd
from faker import Faker
from PostgreSQL import generate_db_uri

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

fake = Faker(locale="ru_RU")

# TODO (@k0rsakov): remove hardcoded on range cities
# https://github.com/k0rsakov/educational_database_for_pet_projects/issues/19
cities = [fake.unique.city() for i in range(1000)]

logging.info(f"Total cities: {len(cities)}")
logging.info(f"Total unique cities: {len(set(cities))}")

# TODO (@k0rsakov): remove hardcoded on range regions
# https://github.com/k0rsakov/educational_database_for_pet_projects/issues/18
region_ids = [randint(a=1, b=78) for _ in cities]  # noqa: S311


df = pd.DataFrame(
    {
        "name":cities,
        "region_id": region_ids,
    },
)
# Использовать только после `regions`
df.to_sql(
    name="city",
    con=generate_db_uri(),
    if_exists="append",
    index=False,
)
