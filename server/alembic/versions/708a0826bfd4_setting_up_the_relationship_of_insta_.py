"""setting up the relationship of insta_posts table to insta_users using foreign_key

Revision ID: 708a0826bfd4
Revises: 8fb24f950704
Create Date: 2023-06-08 12:19:17.982104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708a0826bfd4'
down_revision = '8fb24f950704'
branch_labels = None
depends_on = None


def upgrade():
    # addition of foriegnKey as user_key_id column
    op.add_column('insta_posts',
                  sa.Column('post_published', sa.Boolean,
                            nullable=False, server_default='True'))
    op.add_column('insta_posts',
                  sa.Column('post_created_at', sa.TIMESTAMP(timezone=True),
                            nullable=False, server_default=sa.text('now()'))),
    op.add_column('insta_posts', sa.Column(
        'user_key_id', sa.Integer,  nullable=False)),
    # this is how we add foriegn key relation with alembic sqlalchemy
    op.create_foreign_key('insta_posts_users_foriegn_key', source_table='insta_posts', referent_table='insta_users', local_cols=[
                          'user_key_id'], remote_cols=['user_id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('insta_posts_users_foriegn_key',
                       table_name='insta_posts'),
    op.drop_column('insta_posts', 'post_published'),
    op.drop_column('insta_posts', 'post_created_at'),
    op.drop_column('insta_posts',  'user_key_id')
    pass
