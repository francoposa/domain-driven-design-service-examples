"""entity tables

Revision ID: bc5e8a52b218
Revises: 
Create Date: 2022-05-01 09:16:57.276686

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "00000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bar_value_object",
        sa.Column("bar_value_object_id", postgresql.UUID(), nullable=False),
        sa.Column("bar_value", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("bar_value_object_id"),
        sa.UniqueConstraint("bar_value"),
    )
    op.create_table(
        "foo_value_object",
        sa.Column("foo_value_object_id", postgresql.UUID(), nullable=False),
        sa.Column("attribute_0", sa.TEXT(), nullable=False),
        sa.Column("attribute_1", sa.Integer(), nullable=False),
        sa.Column("attribute_2", sa.NUMERIC(), nullable=False),
        sa.PrimaryKeyConstraint("foo_value_object_id"),
        sa.UniqueConstraint("attribute_0", "attribute_1", "attribute_2"),
    )
    op.create_table(
        "entity",
        sa.Column("entity_id", postgresql.UUID(), nullable=False),
        sa.Column("foo_value_object_id", postgresql.UUID(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ("foo_value_object_id",),
            ["foo_value_object.foo_value_object_id"],
        ),
        sa.PrimaryKeyConstraint("entity_id"),
    )
    op.create_table(
        "entity_bar_value_object",
        sa.Column("entity_bar_value_object_id", postgresql.UUID(), nullable=False),
        sa.Column("entity_id", postgresql.UUID(), nullable=False),
        sa.Column("bar_value_object_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ("bar_value_object_id",),
            ["bar_value_object.bar_value_object_id"],
        ),
        sa.ForeignKeyConstraint(
            ("entity_id",),
            ["entity.entity_id"],
        ),
        sa.PrimaryKeyConstraint("entity_bar_value_object_id"),
        sa.UniqueConstraint("entity_id", "bar_value_object_id"),
    )
    op.create_index(
        op.f("ix_entity_bar_value_object_bar_value_object_id"),
        "entity_bar_value_object",
        ["bar_value_object_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_entity_bar_value_object_entity_id"),
        "entity_bar_value_object",
        ["entity_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_entity_bar_value_object_entity_id"),
        table_name="entity_bar_value_object",
    )
    op.drop_index(
        op.f("ix_entity_bar_value_object_bar_value_object_id"),
        table_name="entity_bar_value_object",
    )
    op.drop_table("entity_bar_value_object")
    op.drop_table("entity")
    op.drop_table("foo_value_object")
    op.drop_table("bar_value_object")
    # ### end Alembic commands ###
