"""creation of insta_users table

Revision ID: 8fb24f950704
Revises: 9428fa079e29
Create Date: 2023-06-08 12:02:39.245940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fb24f950704'
down_revision = '9428fa079e29'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('insta_users',
                    sa.Column('user_id', sa.Integer,
                              nullable=False),
                    sa.Column('user_email', sa.String, nullable=False),
                    sa.Column('user_password', sa.String, nullable=False),
                    sa.Column('user_created_at', sa.TIMESTAMP(
                        timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.Column('user_updated_at', sa.TIMESTAMP(
                        timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('user_email')
                    )
    pass


def downgrade():
    op.drop_table('insta_users')
    pass
