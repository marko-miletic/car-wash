"""upgrade db tables fix

Revision ID: 1793c9022d90
Revises: ca534ea05906
Create Date: 2023-01-04 14:28:02.477899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1793c9022d90'
down_revision = 'ca534ea05906'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('base_discount', sa.Integer(), nullable=False),
    sa.Column('additional_discount', sa.Integer(), nullable=False),
    sa.Column('additional_discount_description', sa.String(length=150), nullable=False),
    sa.Column('valid_since', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_discount_id'), 'discount', ['id'], unique=False)
    op.create_table('mode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description')
    )
    op.create_index(op.f('ix_mode_id'), 'mode', ['id'], unique=False)
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('time_stamp', sa.DateTime(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('time_stamp')
    )
    op.create_index(op.f('ix_invoice_id'), 'invoice', ['id'], unique=False)
    op.create_table('program',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('mode_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mode_id'], ['mode.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_program_id'), 'program', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_program_id'), table_name='program')
    op.drop_table('program')
    op.drop_index(op.f('ix_invoice_id'), table_name='invoice')
    op.drop_table('invoice')
    op.drop_index(op.f('ix_mode_id'), table_name='mode')
    op.drop_table('mode')
    op.drop_index(op.f('ix_discount_id'), table_name='discount')
    op.drop_table('discount')
    # ### end Alembic commands ###