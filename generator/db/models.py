from peewee_aio import Manager, AIOModel, fields

from config.base import settings

manager = Manager(settings.db_url)


@manager.register
class UserEmails(AIOModel):
    user_id = fields.UUIDField(primary_key=True, unique=True)
    email = fields.CharField()
    name = fields.CharField(null=True)


@manager.register
class Likes(AIOModel):
    id = fields.UUIDField()
    user = fields.ForeignKeyField(UserEmails)
    counter = fields.SmallIntegerField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(null=True)
    last_sent_at = fields.DateTimeField(null=True)


@manager.register
class Notifications(AIOModel):
    id = fields.UUIDField()
    user_id = fields.ForeignKeyField(UserEmails)
    type = fields.CharField()


async def handler():
    async with manager:
        async with manager.connection():
            tables = [
                UserEmails,
                Likes,
                Notifications,
            ]
            for table in tables:
                await table.create_table()


if __name__ == '__main__':
    import asyncio

    asyncio.run(handler())
