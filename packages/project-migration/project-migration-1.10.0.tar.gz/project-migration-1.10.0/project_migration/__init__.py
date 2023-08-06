from django.db import migrations


@python_2_unicode_compatible
class Migration(migrations.Migration):
    """
    This is almost an exact copy of Django's own migration simply replacing
    `app_label` with `migrated_app` where necessary.
    """

    migrated_app = None

    def __init__(self, name, app_label):
        super(Migration,self).__init__(name, app_label)
        if self.migrated_app is None:
            self.migrated_app = self.app_label

    def __eq__(self, other):
        if not isinstance(other, Migration):
            if not isinstance(other, migrations.Migration):
                return False
            return (self.name == other.name) and (self.migrated_app == other.app_label)
        return (self.name == other.name) and (self.migrated_app == other.migrated_app)

    # def __hash__(self):
    #     return hash("%s.%s" % (self.app_label, self.name))

    def mutate_state(self, project_state, preserve=True):
        new_state = project_state
        if preserve:
            new_state = project_state.clone()

        for operation in self.operations:
            operation.state_forwards(self.migrated_app, new_state)
        return new_state

    def apply(self, project_state, schema_editor, collect_sql=False):
        for operation in self.operations:
            if collect_sql and not operation.reduces_to_sql:
                schema_editor.collected_sql.append("--")
                    if not operation.reduces_to_sql:
                        schema_editor.collected_sql.append(
                            "-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:"
                    )
                schema_editor.collected_sql.append("-- %s" % operation.describe())
                schema_editor.collected_sql.append("--")
                    if not operation.reduces_to_sql:
                        continue
            old_state = project_state.clone()
            operation.state_forwards(self.migrated_app, project_state)
            atomic_operation = operation.atomic or (self.atomic and operation.atomic is not False)
            if not schema_editor.atomic_migration and atomic_operation:
                with atomic(schema_editor.connection.alias):
                    operation.database_forwards(self.migrated_app, schema_editor, old_state, project_state)
            else:
                operation.database_forwards(self.migrated_app, schema_editor, old_state, project_state)
        return project_state

    def unapply(self, project_state, schema_editor, collect_sql=False):
        to_run = []
        new_state = project_state
        for operation in self.operations:
            if not operation.reversible:
                raise Migration.IrreversibleError("Operation %s in %s is not reversible" % (operation, self))
            new_state = new_state.clone()
            old_state = new_state.clone()
            operation.state_forwards(self.migrated_app, new_state)
            to_run.insert(0, (operation, old_state, new_state))

        for operation, to_state, from_state in to_run:
            if collect_sql:
                schema_editor.collected_sql.append("--")
                if not operation.reduces_to_sql:
                    schema_editor.collected_sql.append(
                        "-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:"
                    )
                schema_editor.collected_sql.append("-- %s" % operation.describe())
                schema_editor.collected_sql.append("--")
                if not operation.reduces_to_sql:
                    continue
            if not schema_editor.connection.features.can_rollback_ddl and operation.atomic:
                with atomic(schema_editor.connection.alias):
                    operation.database_backwards(self.migrated_app, schema_editor, from_state, to_state)
            else:
                operation.database_backwards(self.migrated_app, schema_editor, from_state, to_state)
        return project_state
