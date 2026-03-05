from models import Cable, Construction, Isolation, Twisting

from .base_crud import BaseCRUD

cable_crud = BaseCRUD(Cable)
isolation_crud = BaseCRUD(Isolation)
construction_crud = BaseCRUD(Construction)
twisting_crud = BaseCRUD(Twisting)
