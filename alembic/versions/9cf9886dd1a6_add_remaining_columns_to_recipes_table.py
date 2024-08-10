"""add remaining columns to recipes table

Revision ID: 9cf9886dd1a6
Revises: 878d3b1ea5c4
Create Date: 2024-08-08 11:17:39.604293

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9cf9886dd1a6"
down_revision: Union[str, None] = "878d3b1ea5c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("recipes", "servings", type_=sa.SmallInteger)
    op.add_column("recipes", sa.Column("frequency", sa.SmallInteger))
    op.add_column("recipes", sa.Column("instructions", sa.ARRAY(sa.String)))
    op.add_column("recipes", sa.Column("time", sa.ARRAY(sa.SmallInteger)))
    op.add_column(
        "recipes",
        sa.Column(
            "is_prep_required", sa.Boolean, nullable=False, server_default="False"
        ),
    ),
    op.add_column(
        "recipes",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.alter_column("recipes", "servings", type_=sa.Integer)
    op.drop_column("recipes", "frequency")
    op.drop_column("recipes", "instructions")
    op.drop_column("recipes", "time")
    op.drop_column("recipes", "is_prep_required")
    op.drop_column("recipes", "created_at")
