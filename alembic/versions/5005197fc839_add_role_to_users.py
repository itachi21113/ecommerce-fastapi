"""add role to users

Revision ID: 5005197fc839
Revises: 7c2ffe5ed5d7
Create Date: 2026-09-05 16:35:32.347226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5005197fc839'
down_revision: Union[str, Sequence[str], None] = '7c2ffe5ed5d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default="USER",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("users", "role")
