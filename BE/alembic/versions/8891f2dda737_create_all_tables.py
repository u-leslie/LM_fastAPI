"""Create all tables

Revision ID: 8891f2dda737
Revises: bb298a12a0e4
Create Date: 2024-11-19 06:36:22.309986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8891f2dda737'
down_revision: Union[str, None] = 'bb298a12a0e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drivers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('vehicle_number', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_drivers_id'), 'drivers', ['id'], unique=False)
    op.create_index(op.f('ix_drivers_name'), 'drivers', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('shipments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('origin', sa.String(), nullable=True),
    sa.Column('destination', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shipments_id'), 'shipments', ['id'], unique=False)
    op.create_table('deliveries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('delivery_status', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('shipment_id', sa.Integer(), nullable=True),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['shipment_id'], ['shipments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deliveries_id'), 'deliveries', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_deliveries_id'), table_name='deliveries')
    op.drop_table('deliveries')
    op.drop_index(op.f('ix_shipments_id'), table_name='shipments')
    op.drop_table('shipments')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_drivers_name'), table_name='drivers')
    op.drop_index(op.f('ix_drivers_id'), table_name='drivers')
    op.drop_table('drivers')
    # ### end Alembic commands ###
