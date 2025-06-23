"""create new table address

Revision ID: 4d7cb7b824d5
Revises: 7e02ee6146d7
Create Date: 2025-06-04 14:00:27.689143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d7cb7b824d5'
down_revision: Union[str, None] = '7e02ee6146d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("address",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("address_1",sa.String(),nullable=True),
                    sa.Column("address_2",sa.String(),nullable=True),
                    sa.Column("city",sa.String(),nullable=True),
                    sa.Column("state",sa.String(),nullable=True),
                    sa.Column("country",sa.String(),nullable=True),
                    sa.Column("postal_code",sa.String(),nullable=True)
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("address")
