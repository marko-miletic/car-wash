"""add invoice_mode table

Revision ID: 930b055973d8
Revises: 1793c9022d90
Create Date: 2023-01-08 15:20:12.781050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930b055973d8'
down_revision = '1793c9022d90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoicemodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.Column('mode_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.ForeignKeyConstraint(['mode_id'], ['mode.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoicemodes_id'), 'invoicemodes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_invoicemodes_id'), table_name='invoicemodes')
    op.drop_table('invoicemodes')
    # ### end Alembic commands ###
