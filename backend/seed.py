from decimal import Decimal
from datetime import datetime, timedelta

from database import SessionLocal
from models import (
    Usuario,
    Productor,
    Producto,
    Categoria,
    MovimientoInventario,
    Comprador,
    PreferenciaComprador,
    Match,
    ExperienciaTuristica,
    OfertaCultural,
)


def cargar_datos():

    db = SessionLocal()

    try:

        # ==================================================
        # LIMPIAR DATOS ANTERIORES
        # ==================================================

        print("Limpiando datos anteriores...")

        db.query(Match).delete()
        db.query(PreferenciaComprador).delete()
        db.query(MovimientoInventario).delete()
        db.query(Producto).delete()
        db.query(Productor).delete()
        db.query(Comprador).delete()
        db.query(ExperienciaTuristica).delete()
        db.query(OfertaCultural).delete()
        db.query(Categoria).delete()
        db.query(Usuario).delete()

        db.commit()


        # ==================================================
        # CATEGORIAS
        # ==================================================

        print("Creando categorías...")

        categorias = [
            Categoria(
                nombre="Ganadería",
                modulo="productivo",
                descripcion="Productos relacionados con la ganadería."
            ),

            Categoria(
                nombre="Piscicultura",
                modulo="productivo",
                descripcion="Producción y comercialización de peces."
            ),

            Categoria(
                nombre="Agricultura",
                modulo="productivo",
                descripcion="Productos agrícolas de los Llanos."
            ),

            Categoria(
                nombre="Artesanía",
                modulo="cultural",
                descripcion="Artesanías y productos elaborados a mano."
            ),

            Categoria(
                nombre="Gastronomía",
                modulo="cultural",
                descripcion="Gastronomía tradicional llanera."
            ),

            Categoria(
                nombre="Música",
                modulo="cultural",
                descripcion="Música y expresiones artísticas llaneras."
            ),

            Categoria(
                nombre="Turismo rural",
                modulo="turistico",
                descripcion="Experiencias de turismo rural."
            ),

            Categoria(
                nombre="Cabalgata",
                modulo="turistico",
                descripcion="Experiencias de cabalgata llanera."
            ),

            Categoria(
                nombre="Pesca deportiva",
                modulo="turistico",
                descripcion="Experiencias de pesca deportiva."
            ),
        ]

        db.add_all(categorias)
        db.flush()


        # Diccionario para encontrar categorías fácilmente

        categorias_dict = {
            categoria.nombre: categoria
            for categoria in categorias
        }


        # ==================================================
        # USUARIOS
        # ==================================================

        print("Creando usuarios...")

        usuarios = [

            Usuario(
                nombre="Carlos",
                apellido="Rodríguez",
                email="carlos.productor@llanoia.com",
                telefono="3001112233",
                password_hash="demo123",
                tipo_usuario="productor",
                municipio="Yopal",
                departamento="Casanare",
                direccion="Vereda La Guafilla",
            ),

            Usuario(
                nombre="María",
                apellido="Gómez",
                email="maria.productora@llanoia.com",
                telefono="3002223344",
                password_hash="demo123",
                tipo_usuario="productor",
                municipio="Villanueva",
                departamento="Casanare",
                direccion="Vereda Caribayona",
            ),

            Usuario(
                nombre="Juan",
                apellido="Martínez",
                email="juan.comprador@llanoia.com",
                telefono="3003334455",
                password_hash="demo123",
                tipo_usuario="comprador",
                municipio="Yopal",
                departamento="Casanare",
                direccion="Zona comercial",
            ),

            Usuario(
                nombre="Laura",
                apellido="Pérez",
                email="laura.comprador@llanoia.com",
                telefono="3004445566",
                password_hash="demo123",
                tipo_usuario="comprador",
                municipio="Villavicencio",
                departamento="Meta",
                direccion="Centro",
            ),

            Usuario(
                nombre="Pedro",
                apellido="Suárez",
                email="pedro.turismo@llanoia.com",
                telefono="3005556677",
                password_hash="demo123",
                tipo_usuario="turismo",
                municipio="Restrepo",
                departamento="Meta",
                direccion="Vereda Caney Alto",
            ),

            Usuario(
                nombre="Ana",
                apellido="Vargas",
                email="ana.cultura@llanoia.com",
                telefono="3006667788",
                password_hash="demo123",
                tipo_usuario="cultural",
                municipio="Villavicencio",
                departamento="Meta",
                direccion="Barrio La Grama",
            ),
        ]

        db.add_all(usuarios)
        db.flush()


        # ==================================================
        # PRODUCTORES
        # ==================================================

        print("Creando productores...")

        productor_1 = Productor(
            usuario_id=usuarios[0].id,
            nombre_finca="Finca El Horizonte",
            tipo_produccion="Piscicultura y ganadería",
            descripcion=(
                "Finca dedicada a la producción de cachama "
                "y ganado bovino."
            ),
        )

        productor_2 = Productor(
            usuario_id=usuarios[1].id,
            nombre_finca="Finca La Esperanza",
            tipo_produccion="Agricultura",
            descripcion=(
                "Producción de plátano, yuca y productos agrícolas."
            ),
        )

        db.add_all([
            productor_1,
            productor_2
        ])

        db.flush()


        # ==================================================
        # PRODUCTOS
        # ==================================================

        print("Creando productos...")

        cachama = Producto(
            productor_id=productor_1.id,
            categoria_id=categorias_dict["Piscicultura"].id,
            nombre="Cachama Plateada",
            descripcion=(
                "Cachama fresca producida en estanques "
                "de la región."
            ),
            unidad_medida="kg",
            precio_unitario=Decimal("18000"),
            cantidad_disponible=Decimal("500"),
            imagen_url=None,
        )

        carne = Producto(
            productor_id=productor_1.id,
            categoria_id=categorias_dict["Ganadería"].id,
            nombre="Carne de res",
            descripcion=(
                "Carne de ganado criado en finca llanera."
            ),
            unidad_medida="kg",
            precio_unitario=Decimal("24000"),
            cantidad_disponible=Decimal("300"),
            imagen_url=None,
        )

        platano = Producto(
            productor_id=productor_2.id,
            categoria_id=categorias_dict["Agricultura"].id,
            nombre="Plátano Hartón",
            descripcion=(
                "Plátano hartón cultivado en el municipio "
                "de Villanueva."
            ),
            unidad_medida="kg",
            precio_unitario=Decimal("4500"),
            cantidad_disponible=Decimal("1000"),
            imagen_url=None,
        )

        yuca = Producto(
            productor_id=productor_2.id,
            categoria_id=categorias_dict["Agricultura"].id,
            nombre="Yuca",
            descripcion=(
                "Yuca fresca cultivada en la región."
            ),
            unidad_medida="kg",
            precio_unitario=Decimal("3000"),
            cantidad_disponible=Decimal("800"),
            imagen_url=None,
        )

        db.add_all([
            cachama,
            carne,
            platano,
            yuca
        ])

        db.flush()


        # ==================================================
        # MOVIMIENTOS DE INVENTARIO
        # ==================================================

        print("Creando movimientos de inventario...")

        movimientos = [

            MovimientoInventario(
                producto_id=cachama.id,
                tipo_movimiento="entrada",
                cantidad=Decimal("600"),
                motivo="Producción inicial",
            ),

            MovimientoInventario(
                producto_id=cachama.id,
                tipo_movimiento="salida",
                cantidad=Decimal("100"),
                motivo="Venta a restaurante",
            ),

            MovimientoInventario(
                producto_id=carne.id,
                tipo_movimiento="entrada",
                cantidad=Decimal("300"),
                motivo="Producción inicial",
            ),

            MovimientoInventario(
                producto_id=platano.id,
                tipo_movimiento="entrada",
                cantidad=Decimal("1000"),
                motivo="Cosecha",
            ),

            MovimientoInventario(
                producto_id=yuca.id,
                tipo_movimiento="entrada",
                cantidad=Decimal("800"),
                motivo="Cosecha",
            ),
        ]

        db.add_all(movimientos)


        # ==================================================
        # COMPRADORES
        # ==================================================

        print("Creando compradores...")

        comprador_1 = Comprador(
            usuario_id=usuarios[2].id,
            nombre_negocio="Restaurante El Estribo",
            tipo_negocio="Restaurante",
            descripcion=(
                "Restaurante especializado en gastronomía "
                "llanera."
            ),
        )

        comprador_2 = Comprador(
            usuario_id=usuarios[3].id,
            nombre_negocio="Mercado Llanero",
            tipo_negocio="Supermercado",
            descripcion=(
                "Comercio dedicado a productos regionales."
            ),
        )

        db.add_all([
            comprador_1,
            comprador_2
        ])

        db.flush()


        # ==================================================
        # PREFERENCIAS DE COMPRADORES
        # ==================================================

        print("Creando preferencias...")

        preferencias = [

            PreferenciaComprador(
                comprador_id=comprador_1.id,
                categoria_id=categorias_dict["Piscicultura"].id,
                producto_interes="Cachama Plateada",
                cantidad_minima=Decimal("100"),
                cantidad_maxima=Decimal("500"),
                precio_maximo=Decimal("20000"),
                frecuencia="semanal",
                municipio_preferido="Yopal",
            ),

            PreferenciaComprador(
                comprador_id=comprador_2.id,
                categoria_id=categorias_dict["Agricultura"].id,
                producto_interes="Plátano Hartón",
                cantidad_minima=Decimal("200"),
                cantidad_maxima=Decimal("1000"),
                precio_maximo=Decimal("5000"),
                frecuencia="semanal",
                municipio_preferido="Villanueva",
            ),

            PreferenciaComprador(
                comprador_id=comprador_2.id,
                categoria_id=categorias_dict["Ganadería"].id,
                producto_interes="Carne de res",
                cantidad_minima=Decimal("50"),
                cantidad_maxima=Decimal("300"),
                precio_maximo=Decimal("26000"),
                frecuencia="quincenal",
                municipio_preferido="Yopal",
            ),
        ]

        db.add_all(preferencias)


        # ==================================================
        # EXPERIENCIAS TURÍSTICAS
        # ==================================================

        print("Creando experiencias turísticas...")

        experiencia_1 = ExperienciaTuristica(
            usuario_id=usuarios[4].id,
            categoria_id=categorias_dict["Cabalgata"].id,
            nombre="Cabalgata por los Llanos",
            descripcion=(
                "Recorrido a caballo por paisajes naturales "
                "del Meta."
            ),
            ubicacion="Restrepo, Meta",
            duracion_horas=Decimal("3"),
            capacidad=10,
            precio=Decimal("80000"),
            imagen_url=None,
        )

        experiencia_2 = ExperienciaTuristica(
            usuario_id=usuarios[4].id,
            categoria_id=categorias_dict["Pesca deportiva"].id,
            nombre="Jornada de pesca llanera",
            descripcion=(
                "Experiencia de pesca deportiva acompañada "
                "por guías locales."
            ),
            ubicacion="Restrepo, Meta",
            duracion_horas=Decimal("5"),
            capacidad=8,
            precio=Decimal("120000"),
            imagen_url=None,
        )

        db.add_all([
            experiencia_1,
            experiencia_2
        ])


        # ==================================================
        # OFERTAS CULTURALES
        # ==================================================

        print("Creando ofertas culturales...")

        oferta_1 = OfertaCultural(
            usuario_id=usuarios[5].id,
            categoria_id=categorias_dict["Artesanía"].id,
            nombre="Sombreros llaneros artesanales",
            descripcion=(
                "Sombreros elaborados artesanalmente "
                "por productores de la región."
            ),
            municipio="Villavicencio",
            precio=Decimal("85000"),
            imagen_url=None,
        )

        oferta_2 = OfertaCultural(
            usuario_id=usuarios[5].id,
            categoria_id=categorias_dict["Música"].id,
            nombre="Presentación de música llanera",
            descripcion=(
                "Presentación musical con instrumentos "
                "tradicionales llaneros."
            ),
            municipio="Villavicencio",
            precio=Decimal("350000"),
            imagen_url=None,
        )

        oferta_3 = OfertaCultural(
            usuario_id=usuarios[5].id,
            categoria_id=categorias_dict["Gastronomía"].id,
            nombre="Taller de cocina llanera",
            descripcion=(
                "Taller sobre preparación de platos "
                "tradicionales de los Llanos."
            ),
            municipio="Villavicencio",
            precio=Decimal("60000"),
            imagen_url=None,
        )

        db.add_all([
            oferta_1,
            oferta_2,
            oferta_3
        ])


        # ==================================================
        # GUARDAR TODO
        # ==================================================

        db.commit()

        print()
        print("==========================================")
        print("✅ DATOS DE PRUEBA CREADOS")
        print("==========================================")
        print()
        print("Usuarios: 6")
        print("Productores: 2")
        print("Productos: 4")
        print("Compradores: 2")
        print("Preferencias: 3")
        print("Experiencias turísticas: 2")
        print("Ofertas culturales: 3")
        print("Movimientos inventario: 5")
        print()
        print("Datos cargados correctamente.")


    except Exception as e:

        db.rollback()

        print()
        print("❌ ERROR CARGANDO DATOS")
        print(e)

        raise

    finally:

        db.close()


if __name__ == "__main__":
    cargar_datos()