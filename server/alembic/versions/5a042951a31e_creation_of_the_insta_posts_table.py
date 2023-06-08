"""creation of the insta_posts table

Revision ID: 5a042951a31e
Revises: 8208521e7bc8
Create Date: 2023-06-08 11:35:14.830601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a042951a31e'
down_revision = '8208521e7bc8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('insta_posts',
                    sa.Column('id', sa.Integer, nullable=False,
                              primary_key=True),
                    sa.Column('post_title', sa.String, nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('insta_posts')
    pass
