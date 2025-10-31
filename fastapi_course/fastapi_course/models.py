from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


# registry() vai registrar as dataclasses que virarão tabelas
table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    todos: Mapped[list[Todo]] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )

    # ao selecionar um user (select), vai trazer a lista com todos por causa
    # do lazy='selectin', o cascade='all, delete-orphan' é pra dizer que ao
    # excluir um usuarios, os todos dele precisam ser excluidos também


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
