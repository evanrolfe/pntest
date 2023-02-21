import sqlite3
from entities.variable import Variable
from repos.variable_repo import VariableRepo
from lib.database import Database

class TestVariableRepo:
    def test_inserting_and_fetching_a_var(self, database, cleanup_database):
        repo = VariableRepo()
        variable = Variable(key="baseUrl", value="pntest.com", source_type=Variable.SOURCE_TYPE_GLOBAL)
        repo.save(variable)

        assert variable.id is not None
        assert variable.key == "baseUrl"
        assert variable.value == "pntest.com"
        assert variable.created_at is not None

        variable2 = repo.find_by_key("baseUrl")
        assert variable2 is not None
        assert variable2.id is not None
        assert variable2.key == "baseUrl"
        assert variable2.value == "pntest.com"
        assert variable2.created_at is not None

    def test_find_all_global(self, database, cleanup_database):
        repo = VariableRepo()
        variable1 = Variable(key="var1", value="helloworld", source_type=Variable.SOURCE_TYPE_GLOBAL)
        variable2 = Variable(key="var2", value="helloworld", source_type=Variable.SOURCE_TYPE_GLOBAL)
        variable3 = Variable(key="var3", value="helloworld", source_type=Variable.SOURCE_TYPE_REQUEST, source_id=123)
        repo.save(variable1)
        repo.save(variable2)
        repo.save(variable3)

        global_vars = repo.find_all_global()
        result_ids = [v.id for v in global_vars]

        assert len(global_vars) == 2
        assert variable1.id in result_ids
        assert variable2.id in result_ids
