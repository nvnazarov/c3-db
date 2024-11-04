"""Insert olympics.

Revision ID: 32ea79867b2c
Revises: 3e7b51cda3bd
Create Date: 2024-10-30 19:51:12.501232

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32ea79867b2c"
down_revision: Union[str, None] = "3e7b51cda3bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
INSERT INTO public.olympics(id, country_id, city, year, season)
VALUES  ('SYD2000', 'AUS', 'Sydney                                            ', 2000, 'summer'),
        ('ATH2004', 'GRE', 'Athens                                            ', 2004, 'summer');
        """
    )


def downgrade() -> None:
    op.execute("DELETE FROM public.olympics;")
