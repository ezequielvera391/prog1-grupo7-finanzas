# Gitflow del Proyecto – Guía práctica para el equipo (versión simple)

> **Propósito**: establecer un proceso claro y repetible para colaborar con Git. La idea es que **nadie trabaje sobre `master`** y que cada feature se desarrolle en una rama propia y se integre mediante Pull Requests (PR).

**Imagen sugerida**: un diagrama simple mostrando `master` en el centro y ramas de feature que salen y vuelven con un PR.

---

## 1) Conceptos clave

* **`master`**: rama protegida. Nunca se trabaja ni se pushea directamente aquí.
* **Ramas de feature**: una rama por cada tarea. Formato: `<nombreabreviado-nombredelafeature>`.

  * Ejemplo: `everarod-abm-ingresos`.
* **Commits**: hacé todos los que necesites en tu rama.
* **Integración**: cuando termines y pruebes tu trabajo, hacés un push y abrís un PR.

![Git flow](/assets-doc/image-1.png)

---

## 2) Flujo diario (resumen)

1. Actualizá `master` local.
2. Creá tu rama de feature desde `master`.
3. Trabajá y hacé commits.
4. Antes de pushear, sincronizá con `master` (si hubo cambios de tus compañeros).
5. Subí tu rama (push).
6. Abrí un PR desde la web.

---

## 3) Paso a paso con comandos

### 3.1. Asegurate de partir de `master` actualizado

```bash
git checkout master
# Ahora estás en master

git fetch origin
git pull origin master
# Tenés el master local actualizado
```

### 3.2. Creá tu rama de feature

```bash
git checkout -b everarod-abm-ingresos
# Deberías ver que cambió la branch de 'master' a 'everarod-abm-ingresos'
```

![Nueva branch 'everarod-abm-ingresos'](/assets-doc/image-2.png)

### 3.3. Trabajá y hacé commits

```bash
# Ver estado de cambios
git status

# Preparar archivos para commit
git add <archivo1> <archivo2>

# Hacer un commit con mensaje claro
git commit -m "feat(ingresos): alta y edición básica de registros"
```

> Explicación breve: `git add` selecciona qué cambios querés guardar. `git commit` los guarda en tu rama con un mensaje. El mensaje debe ser claro, por ejemplo: `feat`, `fix`, `docs`, etc.

### 3.4. Traé novedades de master durante el desarrollo

Si tus compañeros subieron cambios mientras trabajabas, podés sobreescribir su trabajo. Antes de subir tu rama, actualizala con `master`.

```bash
# Estando en tu rama de feature
git fetch origin
git merge origin/master
# Si aparecen conflictos, resolvelos y luego:
git commit
```

![Resolver conflictos](/assets-doc/image-3.png)

### 3.5. Subí tu rama al remoto

```bash
git push --set-upstream origin everarod-abm-ingresos
# Próximos pushes
git push
```

**Imagen sugerida**: VS Code mostrando la opción de sincronizar cambios con el remoto.

---

## 4) Cuando la feature esté lista y probada → creá el PR

**Checklist previo al PR**

* [ ] Probaste el script de Python y funciona.
* [ ] Revisaste el diff y quitaste cambios accidentales.

### 4.1. Crear el PR desde la web (GitHub como ejemplo)

1. Subí tu rama (`git push`).
2. Abrí el repo en el navegador, hacé click en “Compare & pull request”.
3. **Base**: `master` | **Compare**: `tu-rama`.
4. Poné un título claro.
5. Crear PR.

**Imagen sugerida**: captura de GitHub mostrando la creación de un PR.

### 4.2. Revisión y merge

* Este punto aplica **solo si te hacen comentarios** sobre tu desarrollo.
* Corregí en tu código, hacé nuevos commits y pushealos: el PR se actualiza automáticamente.
* Cuando esté aprobado, se hace merge a `master` desde la web.
* Luego borrá tu rama (GitHub muestra el botón) y actualizá tu `master` local.

**Imagen sugerida**: captura de GitHub con el botón de “Merge” y “Delete branch”.

---

## 5) Problemas comunes y cómo resolverlos

* **“No puedo pushear, dice ‘rejected’”** → Traé cambios y reintentá:

  ```bash
  git fetch origin
  git merge origin/tu-rama
  git push
  ```

* **“Me equivoqué y trabajé en `master`”** (si todavía **no pusheaste**) → Salvá tus cambios moviéndolos a una rama:

  ```bash
  git checkout -b tu-rama-nueva
  git push --set-upstream origin tu-rama-nueva
  git checkout master
  git reset --hard origin/master
  ```

* **Conflictos al mergear con `origin/master`** → Abrí los archivos, resolvé, luego:

  ```bash
  git add <archivos-resueltos>
  git commit
  git push
  ```

**Imagen sugerida**: editor mostrando un conflicto con las marcas `<<<<<<<`, `=======`, `>>>>>>>`.

---

## 6) Cierre

Si tenés dudas, pedí una mano. La prioridad es que el proceso sea claro y repetible.
