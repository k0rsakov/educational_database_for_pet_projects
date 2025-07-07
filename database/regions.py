import logging

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
# TODO (@k0rsakov): remove hardcoded on range regions
# https://github.com/k0rsakov/educational_database_for_pet_projects/issues/18
regions = [fake.unique.region() for i in range(78)]

logging.info(f"Total regions: {len(regions)}")
logging.info(f"Total unique regions: {len(set(regions))}")

df = pd.DataFrame(
    {
        "name": regions,
    },
)

df.to_sql(
    name="region",
    con=generate_db_uri(),
    index=False,
    if_exists="append",
)
