"""books table description

Revision ID: 67b24878abb8
Revises: 21ae37a26d22
Create Date: 2025-05-21 09:53:11.426021

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "67b24878abb8"
down_revision: Union[str, None] = "21ae37a26d22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("books", sa.Column("description", sa.Text(), nullable=True))

    # set null to existing rows
    op.execute(
        'UPDATE books ' \
        'SET description = NULL'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("books", "description")
    # ### end Alembic commands ###
