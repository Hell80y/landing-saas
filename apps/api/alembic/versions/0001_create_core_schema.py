"""create core schema tables

Revision ID: 0001_create_core_schema
Revises: 
Create Date: 2026-03-05 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_create_core_schema"
down_revision = None
branch_labels = None
depends_on = None


def _ts_columns() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    ]


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False, unique=True),
        sa.Column("billing_email", sa.String(length=320), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        *_ts_columns(),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="member"),
        *_ts_columns(),
    )

    op.create_table(
        "landings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("published_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        *_ts_columns(),
    )

    op.create_table(
        "landing_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("landing_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("landings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("combined_spec", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        *_ts_columns(),
    )

    op.create_foreign_key(
        "fk_landings_published_version",
        "landings",
        "landing_versions",
        ["published_version_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stripe_customer_id", sa.String(length=255), nullable=False, unique=True),
        sa.Column("stripe_subscription_id", sa.String(length=255), nullable=False, unique=True),
        sa.Column("plan", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        *_ts_columns(),
    )

    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True),
        sa.Column("landing_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("landings.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *_ts_columns(),
    )

    op.create_table(
        "jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True),
        sa.Column("queue", sa.String(length=100), nullable=False),
        sa.Column("task_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        *_ts_columns(),
    )

    op.create_table(
        "connect_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stripe_account_id", sa.String(length=255), nullable=False, unique=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("payouts_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_ts_columns(),
    )


def downgrade() -> None:
    op.drop_table("connect_accounts")
    op.drop_table("jobs")
    op.drop_table("events")
    op.drop_table("subscriptions")
    op.drop_constraint("fk_landings_published_version", "landings", type_="foreignkey")
    op.drop_table("landing_versions")
    op.drop_table("landings")
    op.drop_table("users")
    op.drop_table("tenants")
