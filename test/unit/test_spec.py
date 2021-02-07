from mamba import description, it
from expects import expect, equal

from src.lib.database import Database

database = Database('test/tmp.db')
database.delete_existing_db()
database.load_or_create()

with description('PnTest') as self:
    with it('does the job'):
        expect(1).to(equal(1))
