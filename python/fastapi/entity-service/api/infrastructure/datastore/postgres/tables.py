import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

ENTITY_DB_METADATA = sa.MetaData()

ENTITY_TABLE = sa.Table(
    "entity",
    ENTITY_DB_METADATA,
    sa.Column("entity_id", postgresql.UUID(), primary_key=True),
    sa.Column("foo_value_object_id", postgresql.UUID(), nullable=False),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(
        ("foo_value_object_id",),
        ["foo_value_object.foo_value_object_id"],
    ),
)

FOO_VALUE_OBJECT_TABLE = sa.Table(
    "foo_value_object",
    ENTITY_DB_METADATA,
    sa.Column("foo_value_object_id", postgresql.UUID(), primary_key=True),
    sa.Column("attribute_0", sa.TEXT(), nullable=False),
    sa.Column("attribute_1", sa.Integer(), nullable=False),
    sa.Column("attribute_2", sa.NUMERIC(), nullable=False),
    sa.UniqueConstraint("attribute_0", "attribute_1", "attribute_2"),
)

BAR_VALUE_OBJECT_TABLE = sa.Table(
    "bar_value_object",
    ENTITY_DB_METADATA,
    sa.Column("bar_value_object_id", postgresql.UUID(), primary_key=True),
    sa.Column("bar_value", sa.TEXT(), nullable=False, unique=True),
)

ENTITY_BAR_VALUE_OBJECT_TABLE = sa.Table(
    "entity_bar_value_object",
    ENTITY_DB_METADATA,
    sa.Column("entity_bar_value_object_id", postgresql.UUID(), primary_key=True),
    sa.Column("entity_id", postgresql.UUID(), nullable=False, index=True),
    sa.Column("bar_value_object_id", postgresql.UUID(), nullable=False, index=True),
    sa.ForeignKeyConstraint(
        ("entity_id",),
        ["entity.entity_id"],
    ),
    sa.ForeignKeyConstraint(
        ("bar_value_object_id",),
        ["bar_value_object.bar_value_object_id"],
    ),
    sa.UniqueConstraint(
        "entity_id",
        "bar_value_object_id",
    ),
)
