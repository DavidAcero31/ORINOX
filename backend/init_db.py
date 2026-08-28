from database import engine
from models import Base


def crear_tablas():
    print("Creando tablas de LLANO IA...")

    Base.metadata.create_all(bind=engine)

    print("Tablas creadas correctamente.")


if __name__ == "__main__":
    crear_tablas()