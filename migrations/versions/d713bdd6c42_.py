"""empty message

Revision ID: d713bdd6c42
Revises: None
Create Date: 2016-06-07 14:33:08.474698

"""

# revision identifiers, used by Alembic.
revision = 'd713bdd6c42'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('md5_name', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('modify_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('image_id'),
    sa.UniqueConstraint('md5_name')
    )
    op.create_table('post',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('zh_title', sa.String(), nullable=True),
    sa.Column('en_title', sa.String(), nullable=True),
    sa.Column('md_content', sa.String(), nullable=True),
    sa.Column('html_content', sa.String(), nullable=True),
    sa.Column('is_top', sa.Boolean(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('modify_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('post_id'),
    sa.UniqueConstraint('en_title')
    )
    op.create_table('tag',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('tag_name')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post_tag',
    sa.Column('pt_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id'], ),
    sa.PrimaryKeyConstraint('pt_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tag')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_table('post')
    op.drop_table('image')
    ### end Alembic commands ###
