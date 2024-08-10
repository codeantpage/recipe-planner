"""add FK to recipes table

Revision ID: 878d3b1ea5c4
Revises: f4cdcb41da94
Create Date: 2024-08-08 11:10:15.879515

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "878d3b1ea5c4"
down_revision: Union[str, None] = "f4cdcb41da94"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("recipes", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "recipes_users_fk",
        source_table="recipes",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("recipes_users_fk", table_name="recipes")
    op.drop_column("recipes", "user_id")
