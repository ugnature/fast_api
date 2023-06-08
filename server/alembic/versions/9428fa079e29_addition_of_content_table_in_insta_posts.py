"""addition of content table in insta_posts

Revision ID: 9428fa079e29
Revises: 5a042951a31e
Create Date: 2023-06-08 11:44:38.926151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9428fa079e29'
down_revision = '5a042951a31e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('insta_posts', sa.Column(
        'post_content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('insta_posts', 'post_content')
    pass
