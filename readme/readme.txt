
Modelo:
Hemos decidido estructurar la base de datos en tres entidades principales: Paciente, RegistroMedico, y HistorialMedico.

En la entidad Paciente, se almacena la información básica y única de cada paciente. 
	Los atributos de esta entidad son:
		ci: Identificador único del paciente (clave primaria, representa la cédula de identidad).
		nombre: Nombre del paciente.
		apellido: Apellido del paciente.
		fecha_nacimiento: Fecha de nacimiento del paciente.
		sexo: Sexo del paciente.
Esta entidad sirve como el punto central para identificar a los pacientes en el sistema.


La entidad RegistroMedico almacena la información detallada de cada evento médico asociado a un paciente. 
	Los atributos de esta entidad son:
		fecha: Fecha del registro médico.
		tipo: Tipo de registro médico.
		diagnostico: Diagnóstico médico.
		medico: Nombre del médico que atendió al paciente.
		institucion: Nombre de la institución médica.
		descripcion: Descripción del registro.
		medicacion: Información de la medicación prescrita.
Esta entidad es independiente y puede relacionarse con uno o varios pacientes a través de la entidad HistorialMedico.

La entidad HistorialMedico representa la relación entre un Paciente y sus correspondientes registros médicos. 
	Sus atributos son:
		paciente: Referencia al identificador único del paciente (ci) en la entidad Paciente.
		registros: Una lista o colección que contiene referencias a los registros médicos en la entidad RegistroMedico.
Esta entidad actúa como un vínculo de los datos de un paciente con sus registros médicos. 


Lenguaje de programacion y base de datos:
Elegimos Python con FastAPI y MongoDB porque cumplen perfectamente con los requisitos del proyecto: 
intercambio de datos en formato JSON mediante APIs REST y uso de una base de datos NoSQL. 
FastAPI destaca por su rapidez de desarrollo, facilidad de uso y alto rendimiento gracias a su arquitectura asincrónica. 
MongoDB permite almacenar datos en estructuras flexibles tipo JSON y ofrece un potente y sencillo lenguaje de consultas.

Endpoints de servicios:
Agregar paciente: POST http://127.0.0.1:8000/pacientes
Agregar registro medico: POST http://127.0.0.1:8000/registro/?ci=54343212 (ci de ejemplo)
Obtener historial de paciente: GET http://127.0.0.1:8000/historial/54343212 (ci de ejemplo)
Consultar registros por criterio: GET http://127.0.0.1:8000/registros/?medico=Dr.%20Pepe&tipo=consulta&institucion=Clinica ABC (los criterios pueden variar)

*En el git se encuentra un archivo (readme/postman/obligatorio_nosql.postman_collection) para importar en Postman con ejemplos de ejecucion.


Como ejecutar:
Es necesario tener instalado Docker Desktop, una vez instalado ejecutar el programa
y luego ir al directorio raiz del proyecto (ejemplo cd C:\Users\bruno\OneDrive\Documentos\GitHub\Obligatorio-NOSQL) 
y ejecutar el comando docker-compose up


Test JMeter:
Es necesario tener unstalado Apache JMeter.
Importar en JMeter el archivo "HTTP Request.jmx" ubicado en el git dentro del directorio "test".
Luego de importar ya se pueden correr los tests pulsando el boton Run.

