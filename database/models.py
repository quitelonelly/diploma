from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger

metadata_obj = MetaData()

# Таблица с клиентами
users_table = Table(
    "users",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("username", String),
    Column("userpass", String),
)
