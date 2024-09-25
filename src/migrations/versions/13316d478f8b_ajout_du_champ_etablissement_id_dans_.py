"""Ajout du champ etablissement_id dans Eleve

Revision ID: 13316d478f8b
Revises: 7055047e207a
Create Date: 2024-09-25 12:47:02.465536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13316d478f8b'
down_revision = '7055047e207a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eleve', schema=None) as batch_op:
        batch_op.add_column(sa.Column('etablissement_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'etablissement', ['etablissement_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eleve', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('etablissement_id')

    # ### end Alembic commands ###
