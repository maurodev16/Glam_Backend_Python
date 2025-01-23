"""update_salon_table

Revision ID: 235e12722b1c
Revises: 80082fa2b232
Create Date: 2025-01-13 15:28:12.110093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '235e12722b1c'
down_revision: Union[str, None] = '80082fa2b232'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
