"""add apartment_number for address table

Revision ID: 87d83a55fd84
Revises: 595a0d359543
Create Date: 2025-06-09 10:35:34.698589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87d83a55fd84'
down_revision: Union[str, None] = '595a0d359543'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("address",sa.Column("apt_num",sa.Integer(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("address","apt_num")
