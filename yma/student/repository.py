from typing import List, Optional, Tuple
from tortoise.expressions import Q

from yma.repository import BaseRepository

from .models import Student


class StudentRepository(BaseRepository[Student]):
    def __init__(self):
        super().__init__(Student)

# class StudentRepository:
#     async def paginated(
#         self,
#         page: int,
#         page_size: int,
#         search: Optional[Q] = None,
#         order: Optional[List[str]] = None,
#         prefetch: Optional[List[str]] = None
#     ) -> Tuple[int, List[Student]]:
#         # Use default if no search
#         query = Student.filter(search) if search else Student.all()
#         if prefetch:
#             query = query.prefetch_related(*prefetch)
#         if order:
#             query = query.order_by(*order)
#         total = await query.count()
#         records = await query.offset((page - 1) * page_size).limit(page_size)
#         return total, list(records)

#     async def create(self, **kwargs) -> Student:
#         student = await Student.create(**kwargs)
#         return student

#     async def get(self, prefetch: Optional[List[str]] = None, **filters) -> Optional[Student]:
#         if prefetch:
#             return await Student.filter(**filters).first().prefetch_related(*prefetch)
#         else:
#             return await Student.filter(**filters).first()

#     async def list(self) -> List[Student]:
#         return await Student.all()

#     async def update(self, student: Student, **kwargs) -> Student:
#         for key, value in kwargs.items():
#             setattr(student, key, value)
#         await student.save()
#         return student

#     async def delete(self, student_id: int) -> bool:
#         student = await self.get(id=student_id)
#         if not student:
#             return False
#         await student.delete()
#         return True

#     async def exists(self, **kwards) -> bool:
#         return await Student.exists(**kwards)
