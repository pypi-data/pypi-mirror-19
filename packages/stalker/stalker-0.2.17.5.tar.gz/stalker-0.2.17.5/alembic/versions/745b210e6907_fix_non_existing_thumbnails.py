"""fix non existing thumbnails

Revision ID: 745b210e6907
Revises: f2005d1fbadc
Create Date: 2016-06-27 17:52:24.381000

"""

# revision identifiers, used by Alembic.
revision = '745b210e6907'
down_revision = '258985128aff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # fix SimpleEntities with non existing thumbnail_id's
    op.execute(
        """
        update
          "SimpleEntities"
        set thumbnail_id = NULL
        where
          "SimpleEntities".thumbnail_id is not NULL
          and not exists(
            select
              thum.id
            from "SimpleEntities" as thum
            where thum.id = "SimpleEntities".thumbnail_id
          )
        """
    )


def downgrade():
    # do nothing
    pass
