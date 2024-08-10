"""add servings to recipes table

Revision ID: e0e64385bc7a
Revises: ff5a8b221de0
Create Date: 2024-08-07 22:41:18.675373

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e0e64385bc7a"
down_revision: Union[str, None] = "ff5a8b221de0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("recipes", sa.Column("servings", sa.Integer()))


def downgrade() -> None:
    op.drop_column("recipes", "servings")
