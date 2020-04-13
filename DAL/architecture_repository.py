from sqlalchemy.orm import Session

from DAL import schemas, db_models


def get_architecture_by_id(db: Session, arch_id: int) -> db_models.Architecture:
    return db.query(db_models.Architecture).filter(db_models.Architecture.id == arch_id).first()


def store_new_architecture(db: Session, architecture: str) -> db_models.Architecture:
    db_architecture = db_models.Architecture(data=architecture)
    db.add(db_architecture)
    db.commit()
    db.refresh(db_architecture)

    return db_architecture
