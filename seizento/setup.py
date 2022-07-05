from seizento.repository import Repository
from seizento.user import ADMIN_USER


async def set_admin(transaction):
    repository = Repository(transaction=transaction)
    async with repository:
        await repository.set_user(ADMIN_USER)
