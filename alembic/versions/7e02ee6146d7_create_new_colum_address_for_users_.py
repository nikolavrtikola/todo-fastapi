"""create new colum address for Users database

Revision ID: 7e02ee6146d7
Revises: 
Create Date: 2025-06-04 13:53:48.494978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e02ee6146d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("phone_number",sa.String(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","phone_number")
