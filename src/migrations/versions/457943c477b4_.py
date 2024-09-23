"""empty message

Revision ID: 457943c477b4
Revises: 
Create Date: 2024-09-23 18:51:10.423869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457943c477b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aptitude',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('calendrier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titre', sa.String(length=255), nullable=True),
    sa.Column('debut', sa.DateTime(), nullable=True),
    sa.Column('fin', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=50), nullable=True),
    sa.Column('serie', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commentaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competence_comportementale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('competence_specifique',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('etablissement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=True),
    sa.Column('adresse', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matiere',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('libelle', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('utilisateur',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prenom', sa.String(length=50), nullable=True),
    sa.Column('nom', sa.String(length=50), nullable=True),
    sa.Column('mot_de_passe', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('super_admin', 'gerant', 'enseignant', 'eleve', name='user_role_enum'), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('eleve',
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('matricule', sa.String(length=20), nullable=True),
    sa.Column('date_naissance', sa.Date(), nullable=True),
    sa.Column('metier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['metier_id'], ['metier.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('utilisateur_id')
    )
    op.create_table('enseignant',
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('matricule', sa.String(length=20), nullable=True),
    sa.Column('date_naissance', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('utilisateur_id')
    )
    op.create_table('gerant_etablissement',
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('etablissement_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['etablissement_id'], ['etablissement.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('utilisateur_id')
    )
    op.create_table('metier_matiere',
    sa.Column('metier_id', sa.Integer(), nullable=False),
    sa.Column('matiere_id', sa.Integer(), nullable=False),
    sa.Column('coefficient', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['matiere_id'], ['matiere.id'], ),
    sa.ForeignKeyConstraint(['metier_id'], ['metier.id'], ),
    sa.PrimaryKeyConstraint('metier_id', 'matiere_id')
    )
    op.create_table('ressource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titre', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('matiere_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['matiere_id'], ['matiere.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('appreciation_aptitude',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eleve_id', sa.Integer(), nullable=False),
    sa.Column('aptitude_id', sa.Integer(), nullable=False),
    sa.Column('calendrier_id', sa.Integer(), nullable=False),
    sa.Column('semestre', sa.Enum('1', '2', name='semestre_enum'), nullable=False),
    sa.ForeignKeyConstraint(['aptitude_id'], ['aptitude.id'], ),
    sa.ForeignKeyConstraint(['calendrier_id'], ['calendrier.id'], ),
    sa.ForeignKeyConstraint(['eleve_id'], ['eleve.utilisateur_id'], ),
    sa.PrimaryKeyConstraint('id', 'eleve_id', 'aptitude_id', 'calendrier_id', 'semestre')
    )
    op.create_table('appreciation_competence_comportementale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eleve_id', sa.Integer(), nullable=False),
    sa.Column('competence_id', sa.Integer(), nullable=False),
    sa.Column('calendrier_id', sa.Integer(), nullable=False),
    sa.Column('semestre', sa.Enum('1', '2', name='semestre_enum'), nullable=False),
    sa.ForeignKeyConstraint(['calendrier_id'], ['calendrier.id'], ),
    sa.ForeignKeyConstraint(['competence_id'], ['competence_comportementale.id'], ),
    sa.ForeignKeyConstraint(['eleve_id'], ['eleve.utilisateur_id'], ),
    sa.PrimaryKeyConstraint('id', 'eleve_id', 'competence_id', 'calendrier_id', 'semestre')
    )
    op.create_table('appreciation_competence_specifique',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eleve_id', sa.Integer(), nullable=False),
    sa.Column('competence_id', sa.Integer(), nullable=False),
    sa.Column('calendrier_id', sa.Integer(), nullable=False),
    sa.Column('semestre', sa.Enum('1', '2', name='semestre_enum'), nullable=False),
    sa.ForeignKeyConstraint(['calendrier_id'], ['calendrier.id'], ),
    sa.ForeignKeyConstraint(['competence_id'], ['competence_specifique.id'], ),
    sa.ForeignKeyConstraint(['eleve_id'], ['eleve.utilisateur_id'], ),
    sa.PrimaryKeyConstraint('id', 'eleve_id', 'competence_id', 'calendrier_id', 'semestre')
    )
    op.create_table('enseigner',
    sa.Column('enseignant_id', sa.Integer(), nullable=False),
    sa.Column('etablissement_id', sa.Integer(), nullable=False),
    sa.Column('matiere_id', sa.Integer(), nullable=False),
    sa.Column('classe_id', sa.Integer(), nullable=False),
    sa.Column('calendrier_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['calendrier_id'], ['calendrier.id'], ),
    sa.ForeignKeyConstraint(['classe_id'], ['classe.id'], ),
    sa.ForeignKeyConstraint(['enseignant_id'], ['enseignant.utilisateur_id'], ),
    sa.ForeignKeyConstraint(['etablissement_id'], ['etablissement.id'], ),
    sa.ForeignKeyConstraint(['matiere_id'], ['matiere.id'], ),
    sa.PrimaryKeyConstraint('enseignant_id', 'etablissement_id', 'matiere_id', 'classe_id', 'calendrier_id')
    )
    op.create_table('inscription',
    sa.Column('eleve_id', sa.Integer(), nullable=False),
    sa.Column('classe_id', sa.Integer(), nullable=False),
    sa.Column('etablissement_id', sa.Integer(), nullable=False),
    sa.Column('calendrier_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['calendrier_id'], ['calendrier.id'], ),
    sa.ForeignKeyConstraint(['classe_id'], ['classe.id'], ),
    sa.ForeignKeyConstraint(['eleve_id'], ['eleve.utilisateur_id'], ),
    sa.ForeignKeyConstraint(['etablissement_id'], ['etablissement.id'], ),
    sa.PrimaryKeyConstraint('eleve_id', 'classe_id', 'etablissement_id', 'calendrier_id')
    )
    op.create_table('interet_eleve',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('eleve_id', sa.Integer(), nullable=True),
    sa.Column('interet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['eleve_id'], ['eleve.utilisateur_id'], ),
    sa.ForeignKeyConstraint(['interet_id'], ['interet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('eleve_id', sa.Integer(), nullable=False),
    sa.Column('matiere_id', sa.Integer(), nullable=False),
    sa.Column('calendrier_id', sa.Integer(), nullable=False),
    sa.Column('semestre', sa.Enum('1', '2', name='semestre_enum'), nullable=False),
    sa.Column('note_cc1', sa.Float(), nullable=True),
    sa.Column('note_cc2', sa.Float(), nullable=True),
    sa.Column('note_composition', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['calendrier_id'], ['calendrier.id'], ),
    sa.ForeignKeyConstraint(['eleve_id'], ['eleve.utilisateur_id'], ),
    sa.ForeignKeyConstraint(['matiere_id'], ['matiere.id'], ),
    sa.PrimaryKeyConstraint('eleve_id', 'matiere_id', 'calendrier_id', 'semestre')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    op.drop_table('interet_eleve')
    op.drop_table('inscription')
    op.drop_table('enseigner')
    op.drop_table('appreciation_competence_specifique')
    op.drop_table('appreciation_competence_comportementale')
    op.drop_table('appreciation_aptitude')
    op.drop_table('ressource')
    op.drop_table('metier_matiere')
    op.drop_table('gerant_etablissement')
    op.drop_table('enseignant')
    op.drop_table('eleve')
    op.drop_table('utilisateur')
    op.drop_table('metier')
    op.drop_table('matiere')
    op.drop_table('interet')
    op.drop_table('etablissement')
    op.drop_table('competence_specifique')
    op.drop_table('competence_comportementale')
    op.drop_table('commentaire')
    op.drop_table('classe')
    op.drop_table('calendrier')
    op.drop_table('aptitude')
    # ### end Alembic commands ###
