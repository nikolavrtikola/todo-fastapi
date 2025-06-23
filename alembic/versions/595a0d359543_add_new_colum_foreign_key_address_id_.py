"""add new colum foreign key address_id for table Users

Revision ID: 595a0d359543
Revises: 4d7cb7b824d5
Create Date: 2025-06-05 12:04:14.597954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '595a0d359543'
down_revision: Union[str, None] = '4d7cb7b824d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("address_id",sa.Integer(),nullable=True))
    op.create_foreign_key("address_users_fk",
                          source_table="users",referent_table="address",
                          local_cols=["address_id"],remote_cols=["id"],
                          ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("address_users_fk",table_name="users")
    op.drop_column("users","address_id")
