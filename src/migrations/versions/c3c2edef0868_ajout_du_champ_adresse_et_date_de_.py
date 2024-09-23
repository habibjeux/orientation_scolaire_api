"""Ajout du champ adresse et date de naissance dans Utilisateur

Revision ID: c3c2edef0868
Revises: 278e47796ba6
Create Date: 2024-09-23 20:20:35.040752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3c2edef0868'
down_revision = '278e47796ba6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eleve', schema=None) as batch_op:
        batch_op.drop_column('date_naissance')

    with op.batch_alter_table('enseignant', schema=None) as batch_op:
        batch_op.drop_column('date_naissance')

    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_naissance', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('adresse', sa.String(length=255), nullable=True))
        batch_op.alter_column('mot_de_passe',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.alter_column('mot_de_passe',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)
        batch_op.drop_column('adresse')
        batch_op.drop_column('date_naissance')

    with op.batch_alter_table('enseignant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_naissance', sa.DATE(), autoincrement=False, nullable=True))

    with op.batch_alter_table('eleve', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_naissance', sa.DATE(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
