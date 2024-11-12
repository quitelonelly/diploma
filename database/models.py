from sqlalchemy import Table, Column, String, MetaData, BigInteger, ForeignKey, LargeBinary

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

# Таблица с файлами
files_table = Table(
    "files",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("id_task", BigInteger, ForeignKey("tasks.id")),
    Column("file_name", String),
    Column("file_data", LargeBinary)
)

# Таблица с исполнителями задач
responsible_table = Table(
    "responsible",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("id_task", BigInteger, ForeignKey("tasks.id")),
    Column("id_user", BigInteger, ForeignKey("users.id")),
)

# Таблица с подзадачами
subtask_table = Table(
    "subtasks",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("id_task", BigInteger, ForeignKey("tasks.id")),
    Column("subtaskname", String),
    Column("status", String),
)

