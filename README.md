# Gestor Inteligente de Clientes (GIC) — Sistema de Gestión (Python)

Proyecto de consola en Python para la gestión de clientes de una empresa ficticia.  
Permite administrar distintos tipos de clientes (Regular, Premium y Corporativo), aplicar validaciones, persistir datos en JSON y registrar actividad en logs.

> El sistema persiste los datos en `base_datos/clientes.json`.  
> Incluye opción de reinicio manual mediante confirmación explícita.

---

## 🎯 Objetivo del proyecto

Desarrollar un sistema por consola que permita:

- Gestionar clientes de distintos tipos
- Aplicar herencia y polimorfismo correctamente
- Implementar validaciones y excepciones personalizadas
- Persistir información en archivos JSON
- Registrar actividad del sistema en logs
- Mantener una arquitectura modular y escalable

---

## ✅ Funcionalidades

### Menú principal

- Crear cliente  
- Listar clientes  
- Ver cliente por ID  
- Editar cliente  
- Eliminar cliente  
- Resetear datos  
- Salir  

### Detalles importantes

#### Crear cliente

- Permite elegir tipo: Regular, Premium o Corporativo
- Valida email, teléfono y campos obligatorios
- Premium incluye descuento
- Corporativo incluye razón social y RUT empresa
- Registra operación en logs

#### Editar cliente

- Permite modificar campos seleccionados
- Mantiene validaciones
- Registra operación en logs

#### Eliminar cliente

- Solicita confirmación
- Registra operación en logs

#### Resetear datos

- Requiere escribir exactamente "RESET"
- Reinicia el archivo JSON a una lista vacía
- Registra operación en logs

---

## 🧠 Conceptos aplicados

- Programación Orientada a Objetos
- Herencia
- Polimorfismo
- Excepciones personalizadas
- Persistencia en JSON
- Registro de actividad (logs)
- Arquitectura por capas

---

## 🧩 Modelado POO

Clase base:
- `Cliente`

Subclases:
- `ClienteRegular`
- `ClientePremium`
- `ClienteCorporativo`

El método `beneficio()` está implementado de forma polimórfica, permitiendo comportamiento distinto según el tipo de cliente.

---

## 🗂️ Estructura del proyecto

```text

GestorInteligenteDeClientes/
│ main.py
│ menu_cliente.py
│ README.md
│ .gitignore
│
├─ base_datos/
│ └─ clientes.json
│
├─ logs/
│ └─ actividad.log
│
├─ modelos/
│ └─ clientes.py
│
├─ servicios/
│ └─ clientes_servicios.py
│
└─ docs/
├─ diagrama_clases.puml
├─ uml_clientes.png
└─ pregunta.md

```

---

## ▶️ Cómo ejecutar el programa

1. Abrir una terminal en la carpeta raíz del proyecto  
2. Ejecutar:

```bash

python main.py

```
---
## 🧪 Ejemplo de uso

- Crear un cliente Premium con descuento 0.10
- Editar su email
- Listar clientes
- Eliminar cliente
- Revisar logs en `logs/actividad.log`

---

## 🛡️ Validaciones implementadas

- Email con formato básico válido
- Teléfono con solo números (mínimo 8 dígitos)
- Campos obligatorios no vacíos
- Descuento Premium entre 0 y 1
- Confirmación explícita para eliminación y reset

---

## 📝 Persistencia

Los datos se almacenan en:

`base_datos/clientes.json`

Cada cliente incluye el campo `"tipo"` para permitir reconstrucción correcta de la subclase correspondiente.

---

## 📘 UML

El diagrama de clases fue diseñado con PlantUML.  
Se encuentra en la carpeta `docs` como:

- `diagrama_clases.puml`
- `uml_clientes.png`

---

## 👤 Contexto académico

Proyecto desarrollado como ABP para aplicar:

- Programación Orientada a Objetos avanzada
- Herencia y polimorfismo
- Manejo de excepciones
- Persistencia de datos
- Separación de responsabilidades
- Buenas prácticas de organización y escalabilidad