import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

AUTHZ_DB_METADATA = sa.MetaData()

IDENTITY_TABLE = sa.Table(
    "identity",
    AUTHZ_DB_METADATA,
    sa.Column("identity_id", postgresql.UUID(), primary_key=True),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)

ROLE_TABLE = sa.Table(
    "role",
    AUTHZ_DB_METADATA,
    sa.Column("role_id", postgresql.UUID(), primary_key=True),
    sa.Column("name", sa.TEXT(), nullable=False),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)

PERMISSION_TABLE = sa.Table(
    "permission",
    AUTHZ_DB_METADATA,
    sa.Column("permission_id", postgresql.UUID(), primary_key=True),
    sa.Column("name", sa.TEXT(), nullable=False),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)

RESOURCE_TYPE_TABLE = sa.Table(
    "resource_type",
    AUTHZ_DB_METADATA,
    sa.Column("resource_type_id", postgresql.UUID(), primary_key=True),
    sa.Column("name", postgresql.UUID(), primary_key=True),
)

RESOURCE_TABLE = sa.Table(
    "resource",
    AUTHZ_DB_METADATA,
    sa.Column("resource_id", postgresql.UUID(), primary_key=True),
    sa.Column("resource_type_id", postgresql.UUID(), nullable=False, index=True),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(
        ("resource_type_id",),
        ["resource_type.resource_type_id"],
    ),
)


IDENTITY_ROLE_TABLE = sa.Table(
    "identity_role",
    AUTHZ_DB_METADATA,
    sa.Column("identity_role_id", postgresql.UUID(), primary_key=True),
    sa.Column("identity_id", postgresql.UUID(), nullable=False, index=True),
    sa.Column("role_id", postgresql.UUID(), nullable=False, index=True),
    sa.ForeignKeyConstraint(
        ("identity_id",),
        ["identity.identity_id"],
    ),
    sa.ForeignKeyConstraint(
        ("role_id",),
        ["role.role_id"],
    ),
    sa.UniqueConstraint(
        "identity_id",
        "role_id",
    ),
)


