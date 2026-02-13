# POO y su importancia en sistemas escalables (GIC)

La Programación Orientada a Objetos (POO) permite modelar un dominio mediante clases y objetos, agrupando datos (atributos) y comportamiento (métodos). En sistemas escalables, esto mejora la mantenibilidad porque cada clase tiene una responsabilidad clara y el código queda modular.

En este proyecto, la entidad Cliente se modela como una clase base y se extiende mediante herencia en ClienteRegular, ClientePremium y ClienteCorporativo. Esta decisión reduce duplicación y facilita la extensión: para agregar un nuevo tipo de cliente se crea una nueva subclase y se define su comportamiento específico.

El polimorfismo se aplica mediante el método beneficio(), que permite que distintos tipos de cliente respondan de forma diferente con la misma interfaz. Además, el uso de validaciones y una excepción personalizada (ValidacionError) mejora la robustez: el sistema controla errores esperados sin detener la ejecución.

Finalmente, la separación por capas (menú, servicios y modelos) hace que el sistema sea más escalable, porque permite cambiar la interfaz (por ejemplo, GUI o API en el futuro) sin reescribir la lógica de negocio ni el modelo.
