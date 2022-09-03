import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

ENTITY_DB_METADATA = sa.MetaData()

ENTITY_TABLE = sa.Table(
    "entity",
    ENTITY_DB_METADATA,
    sa.Column("entity_id", postgresql.UUID(), primary_key=True),
    sa.Column("bar_value_object_attribute_0", sa.TEXT(), nullable=False),
    sa.Column("bar_value_object_attribute_1", sa.Integer(), nullable=False),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)

CHILD_ENTITY_TABLE = sa.Table(
    "child_entity",
    ENTITY_DB_METADATA,
    sa.Column("child_entity_id", postgresql.UUID(), primary_key=True),
    sa.Column("attribute_a", sa.TEXT(), nullable=False),
    sa.Column("attribute_b", sa.Integer(), nullable=False),
    sa.Column("attribute_c", sa.NUMERIC(), nullable=False),
)

ENTITY_CHILD_ENTITY_TABLE = sa.Table(
    "entity_child_entity",
    ENTITY_DB_METADATA,
    sa.Column("entity_child_entity_id", postgresql.UUID(), primary_key=True),
    sa.Column("entity_id", postgresql.UUID(), nullable=False, index=True),
    sa.Column("child_entity_id", postgresql.UUID(), nullable=False, index=True),
    sa.ForeignKeyConstraint(
        ("entity_id",),
        ["entity.entity_id"],
    ),
    sa.ForeignKeyConstraint(
        ("child_entity_id",),
        ["child_entity.child_entity_id"],
    ),
    sa.UniqueConstraint(
        "entity_id",
        "child_entity_id",
    ),
)
