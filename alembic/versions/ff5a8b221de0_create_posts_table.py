"""create posts table

Revision ID: ff5a8b221de0
Revises: 
Create Date: 2024-08-07 22:33:42.212794

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ff5a8b221de0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("recipes")
