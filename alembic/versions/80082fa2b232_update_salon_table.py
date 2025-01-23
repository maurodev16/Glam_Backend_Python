"""update_salon_table

Revision ID: 80082fa2b232
Revises: f4c711e6a5b8
Create Date: 2025-01-13 15:25:41.702212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80082fa2b232'
down_revision: Union[str, None] = 'f4c711e6a5b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
