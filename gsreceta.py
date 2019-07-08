# coding=UTF-8
import json
from geoserver.catalog import Catalog
import sys
import geoserver.util
import os

class GSReceta:
    """ El proposito de esta clase es leer un archivo JSON y ejecutar una serie de comandos para configurar un geoserver usando GSConfig
    nombreArchivo

    Attributes
    ----------
    catalogo : Catalog
        Catalogo de GSConfig
    """

    JSON_COMANDOS = "comandos"

    JSON_COMANDO_CAMPO_ENTIDAD = "entidad"
    JSON_COMANDO_CAMPO_ACCION = "accion"
 
    JSON_ENUM_ENTIDAD_WORKSPACE = "workspace"
    JSON_ENUM_ENTIDAD_STORE = "store"
    JSON_ENUM_ENTIDAD_STYLE = "style"

    JSON_ENUM_ACCION_ALTA = "alta"

    JSON_WORKSPACE_NOMBRE = "nombre"
    JSON_WORKSPACE_URI = "uri"

    JSON_STORE_NOMBRE = "nombre"
    JSON_STORE_TIPO = "tipo"
    JSON_STORE_WORKSPACE = "workspace"
    JSON_STORE_PATH = "path"
    JSON_STORE_ESTILO_POR_DEFECTO = "estilo_por_defecto"


    JSON_STYLE_NOMBRE = "nombre"
    JSON_STYLE_PATH = "path"

    JSON_ENUM_STORE_TIPO_SHAPE = "shape"


    def __init__(self, unCatalogo):
        """ Constructor que toma un catalogo de GSConfig sobre el cual se ejecutara las operaciones
        
        Attributes
        ----------
        catalogo : Catalog
            Catalogo de GSConfig
        """
        self.catalogo = unCatalogo        


    def __validarJSONComandos(self,unArrayDeArray):
        """ Valida SOLAMENTE que exista el atributo 'comandos' en el archivo JSON y que tenga mas de un elemento.
        Attributes
        ----------
        unArrayDeArray : array
            Array de arrays conteniendo los comandos de la 'receta'
        """
        if unArrayDeArray is None:
            raise Exception("La receta JSON es invalida")
        if ( len(unArrayDeArray) == 0 ):
            raise Exception("No se han definido comandos en la receta JSON")

    def ejecutar(self,unaRutaAlJSON):
        """Ejecuta los comandos del archivo JSON mediante el catalogo de GSConfg

        Attributes
        ----------
        unaRutaAlJSON : str
            Ruta al archivo JSON con los comandos
        """
        print("INCIANDO ejecución del script: " + unaRutaAlJSON)
        #Almaceno el path al directorio donde esta el JSON. 
        #Se puede usar como directorio base para ir a tomar los shapes a una direccion relativa
        
        #Busca el path absoluto y luego se queda solo con el path (sin el nombre de archivo)
        self.directorioDeTrabajo = os.path.dirname(os.path.abspath(unaRutaAlJSON))

        with open(unaRutaAlJSON, 'r') as unArchivo:
            unaRecetaJSON = json.load(unArchivo)
            self.__validarJSONComandos(unaRecetaJSON[self.JSON_COMANDOS])
            for unComando in unaRecetaJSON[self.JSON_COMANDOS]:
                self.__ejecutarComando(unComando)
            print("FINALIZADO ejecución del script.")


    def __ejecutarComando(self, unComando):
        """Ejecuta un comando. Valida que la entidad del comando sea valido.

        Attributes
        ----------
        unComando : array
            Comando para ejecutar en parseado del JSON
        """
        print("Ejecutando el siguiente comando: ", unComando)

        unaEntidad = unComando[self.JSON_COMANDO_CAMPO_ENTIDAD]
        if unaEntidad == self.JSON_ENUM_ENTIDAD_WORKSPACE:
            self.__ejecutarComandoWorkspace(unComando)
        elif unaEntidad == self.JSON_ENUM_ENTIDAD_STORE:
            self.__ejecutarComandoStore(unComando)
        elif unaEntidad == self.JSON_ENUM_ENTIDAD_STYLE:
            self.__ejecutarComandoStyle(unComando)

        else:
            raise Exception("Entidad desconocida: " + unaEntidad)

    def __ejecutarComandoWorkspace(self, unComando):
        """Ejecuta un comando referido a un workspace. Valida que la acción del comando sea valido y que 
        los parametros sean los indicados.

        Attributes
        ----------
        unComando : array
            Comando para ejecutar en parseado del JSON
        """
        unaAccion = unComando[self.JSON_COMANDO_CAMPO_ACCION]
        if unaAccion == self.JSON_ENUM_ACCION_ALTA:
            unNombre = unComando[self.JSON_WORKSPACE_NOMBRE]
            unaURI = unComando[self.JSON_WORKSPACE_URI]
            self.__validar_atributo_no_vacio('workspace', 'alta', 'nombre', unNombre)
            self.__validar_atributo_no_vacio('workspace', 'alta', 'uri', unaURI)
            self.catalogo.create_workspace(unNombre, unaURI)

        else:
            raise Exception("Acción desconocida o no soportada aún: " + unaAccion)

    def __ejecutarComandoStore(self, unComando):
        """Ejecuta un comando referido a un stora . Valida que la acción del comando sea valido y que 
        los parametros sean los indicados.

        Attributes
        ----------
        unComando : array
            Comando para ejecutar en parseado del JSON
        """
        unaAccion = unComando[self.JSON_COMANDO_CAMPO_ACCION]
        if unaAccion == self.JSON_ENUM_ACCION_ALTA:

            unNombre = unComando[self.JSON_STORE_NOMBRE]
            unTipo = unComando[self.JSON_STORE_TIPO]
            unWorkspace = unComando[self.JSON_STORE_WORKSPACE]

            self.__validar_atributo_no_vacio('workspace', 'alta', 'nombre', unNombre)
            self.__validar_atributo_no_vacio('workspace', 'alta', 'tipo', unTipo)
            self.__validar_atributo_no_vacio('workspace', 'alta', 'workspace', unWorkspace)

            if unTipo == self.JSON_ENUM_STORE_TIPO_SHAPE:
                self.__ejecutarComandoStoreShape(unComando, unWorkspace, unNombre)

            else:
                raise Exception("Tipo de store desconocida o no soportada aun: " + unTipo)

            # Si se establecio el atributo opcional de estilo por defecto
            if self.JSON_STORE_ESTILO_POR_DEFECTO in unComando:
                unEstiloPorDefecto = unComando[self.JSON_STORE_ESTILO_POR_DEFECTO]
                self.__ejecutarCommandoStoreEstiloPorDefecto(unComando, unWorkspace, unNombre, unEstiloPorDefecto)

        else:
            raise Exception("Acción desconocida o no soportada aún: " + unaAccion)

    def __ejecutarCommandoStoreEstiloPorDefecto(self, unComando, unWorkspace, unaCapa, unEstiloPorDefecto):
        """Ejecuta un comando para asignar un estilo por defecto a una capa.

        Attributes
        ----------
        unComando : array
            Comando para ejecutar en parseado del JSON
        unWorkspace : string
            Nombre del espacio de trabajo
        unNombre : string
            Nombre de la capa
        unEstiloPorDefecto : string
            Nombre del estilo. El mismo debe existir previamente
        """        
        unObjetoEstilo = self.catalogo.get_style(unEstiloPorDefecto)
        print(unObjetoEstilo)
        unObjetoCapa = self.catalogo.get_layer(unWorkspace + ":" + unaCapa)
        print(unObjetoCapa)
        unObjetoCapa.default_style = unObjetoEstilo
        self.catalogo.save(unObjetoCapa)

    def __ejecutarComandoStoreShape(self, unComando, unWorkspace, unNombre):
        """Ejecuta un comando referido a un stora shape. Valida que el path del comando sea valido.

        Attributes
        ----------
        unComando : array
            Comando para ejecutar en parseado del JSON
        """        
        unPath = unComando[self.JSON_STORE_PATH]            
        self.__validar_atributo_no_vacio('workspace', 'alta', 'unPath', unPath)
        unPathAbsoluto = os.path.join(self.directorioDeTrabajo, unPath)
        unShapeYArchivosAsociados = geoserver.util.shapefile_and_friends(unPathAbsoluto)
        self.catalogo.create_featurestore(unNombre, unShapeYArchivosAsociados, unWorkspace)

    def __validar_atributo_no_vacio(self, unaEntidad, unaAccion, unaAtributo, unValor):
        """Valida que el parametro 'unValor', de tipo string, no sea nulo ni este vacio.
        En caso que el mismo sea vacio o nulo levanta una excepción indicando de que entidad, acción y atributo se trata.

        Attributes
        ----------
        unaEntidad : str
        unaAccion : str
        unaAtributo : str
        unValor : str

        """
        if (not unValor):
                raise Exception("El '" + unaAccion + "' de la entidad '" + unaEntidad + "' requiere que el atributo '" + unaAtributo + "' no este vacio")


    def __ejecutarComandoStyle(self, unComando):
        """Ejecuta un comando referido a un style (o estilo). Valida que la acción del comando sea valido y que 
        los parametros sean los indicados.

        Attributes
        ----------
        unComando : array
            Comando para ejecutar en parseado del JSON
        """ 
        unaAccion = unComando[self.JSON_COMANDO_CAMPO_ACCION]
        if unaAccion == self.JSON_ENUM_ACCION_ALTA:
            unNombre = unComando[self.JSON_STYLE_NOMBRE]
            unPath = unComando[self.JSON_STYLE_PATH]
            self.__validar_atributo_no_vacio('workspace', 'alta', 'nombre', unNombre)
            self.__validar_atributo_no_vacio('workspace', 'alta', 'path', unPath)
            unPathAbsoluto = os.path.join(self.directorioDeTrabajo, unPath)
            with open(unPathAbsoluto) as unArchivo:
                self.catalogo.create_style(unNombre, unArchivo.read())
            

        else:
            raise Exception("Acción desconocida o no soportada aún: " + unaAccion)


