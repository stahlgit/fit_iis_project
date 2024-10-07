from typing import Optional, Sequence, Type, TypeVar

from sqlalchemy import MetaData, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped

T = TypeVar("T", bound="BaseModelMixin")


class Base(DeclarativeBase):
    metadata = MetaData(schema="public")


class CreateException(Exception):
    pass


class MissingRequiredFieldException(Exception):
    pass


class BaseModelMixin:
    """
    Base repository class that wraps CRUD methods plus some other useful stuff.
    """

    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class
    id: Mapped[int]

    def update_model(self, **kwargs):
        """
        @brief Updates the model with the given values.
        @param kwargs The values to update.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    async def get(cls: Type[T], id: int, session: AsyncSession) -> Optional[T]:
        """
        @brief Gets an object by identifier
        @param id  The identifier
        @param session The session
        @return The object by identifier or None if not found.
        """
        return await session.get(cls, id)

    @classmethod
    async def get_all(cls: Type[T], session: AsyncSession) -> Sequence[T]:
        """
        @brief Gets all objects
        @param session The session
        @return All objects
        """
        try:
            return (await session.execute(select(cls).order_by(cls.id))).scalars().all()
        except Exception:
            return (await session.execute(select(cls))).scalars().all()

    @classmethod
    async def get_count(cls: Type[T], session: AsyncSession) -> int:
        """
        @brief Gets the count of objects.
        @param session The session
        @return The count of objects.
        """
        count = (await session.execute(select(func.count()).select_from(cls))).scalar()
        if count is None:
            return 0
        return count

    @classmethod
    async def get_by(cls: Type[T], session: AsyncSession, **kwargs) -> Sequence[T]:
        """
        @brief Gets objects by the given criteria.
        @param session The session
        @param kwargs The criteria.
        @return The objects that match the criteria.
        """
        return (await session.execute(select(cls).filter_by(**kwargs))).scalars().all()

    @classmethod
    async def get_one_by(cls: Type[T], session: AsyncSession, **kwargs) -> Optional[T]:
        """
        @brief Gets objects by the given criteria.
        @param session The session
        @param kwargs The criteria.
        @return The objects that match the criteria.
        """
        return (
            (await session.execute(select(cls).filter_by(**kwargs))).scalars().first()
        )

    @classmethod
    async def exists(cls: Type[T], id: int, session: AsyncSession) -> bool:
        """
        @brief Determines if the given object exists.
        @param id  The identifier.
        @param session The session
        @return True if it exists, false if not.
        """
        return (
            await session.execute(
                select(func.count()).select_from(cls).filter_by(id=id)
            )
        ).scalar() != None

    @classmethod
    async def create(cls: Type[T], session: AsyncSession, **kwargs) -> T:
        """
        @brief Creates an object.
        @param session database session
        @param kwargs arguments.
        @return The new object.
        """
        transaction = cls(**kwargs)
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction

    @classmethod
    async def bulk_create(cls: Type[T], session: AsyncSession, items: list) -> None:
        """
        @brief Creates multiple objects in bulk.
        @param session database session
        @param items List of BaseModel instances to create.
        @return List of created objects.
        """
        try:
            a = [
                cls(**{attr: getattr(item, attr) for attr in item.__dict__.keys()})
                for item in items
            ]
            session.add_all(a)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Error occurred during bulk creation: {e}")
            raise CreateException(f"Error occurred during bulk creation: {e}")

    @classmethod
    async def update(
        cls: Type[T], session: AsyncSession, id: int, **kwargs
    ) -> Optional[T]:
        """
        @brief Updates the given object.
        @param session database session
        @param id identifier.
        @param kwargs arguments.
        @return object if it succeeds, None if it fails.
        """
        obj = await cls.get(id, session)
        if obj is None:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def delete(cls: Type[T], session: AsyncSession, id: int) -> None:
        """
        @brief Deletes the given object.
        @param session database session
        @param id identifier.
        @return object if it succeeds, None if it fails.
        """
        obj = await cls.get(id, session)
        if obj is None:
            return None
        await session.delete(obj)
        await session.commit()
