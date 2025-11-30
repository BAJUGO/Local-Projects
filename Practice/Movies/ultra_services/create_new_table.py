from ..db import BaseClass, engine


def create_class(class_name: str, table_name: str, **columns):
    attributes = {"__tablename__": table_name}
    attributes.update(columns)
    return type(class_name, (BaseClass,), attributes)

    #! type позволяет создать класс с именем class_name, наследуемый от BaseClass (и других классов), а также с атрибутами attributes


def create_table(some_class):
    if hasattr(some_class, "__table__"):
        some_class.__table__.create(bind=engine)
    else:
        print("У этого класса нет __table__")

