from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger, ForeignKey

metadata_obj = MetaData()

# Таблица с пользователями
users_table = Table(
    "users",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("username", String),
    Column("userpass", String),
    Column("permissions", String)
)

# Таблица со ВСЕМИ задачами
tasks_table = Table(
    "tasks",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("taskname", String),
)

# Таблица с подзадачами
subtasks_table = Table(
    "subtasks",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("id_task", BigInteger, ForeignKey("tasks.id")),
    Column("id_user", BigInteger, ForeignKey("users.id")),
    Column("subtaskname", String),
)

