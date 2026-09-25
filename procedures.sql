-- ============================================================
-- Procedimientos y funciones almacenadas del blog.
-- Siguen el patrón visto en clase: procedures/functions sueltos
-- (sin package), sin COMMIT interno (lo controla el cliente
-- Python después de cada callproc), y manejo de errores con
-- RAISE_APPLICATION_ERROR + SQL%ROWCOUNT / NO_DATA_FOUND /
-- DUP_VAL_ON_INDEX.
--
-- Codigos de error usados (rango -20000 a -20999, reservado
-- para errores de aplicacion en Oracle):
--   -20001  email duplicado             (user_insert)
--   -20002  usuario no encontrado       (user_get)
--   -20011  articulo no encontrado      (article_get)
--   -20012  articulo no encontrado      (article_update)
--   -20013  articulo no encontrado      (article_delete)
--   -20014  atributo de orden invalido  (article_all_ordenado)
--   -20031  nombre de tag duplicado     (tag_insert)
--   -20032  tag ya asociado al articulo (tag_associate)
--   -20041  nombre de categoria duplicado (category_insert)
--   -20042  categoria ya asociada       (category_associate)
--
-- Ejecuta esto DESPUES de schema.sql
-- ============================================================

-- ================= Usuarios =================

CREATE OR REPLACE PROCEDURE user_insert(
    p_name    IN  VARCHAR2,
    p_email   IN  VARCHAR2,
    p_user_id OUT NUMBER
) IS
BEGIN
    INSERT INTO users(name, email) VALUES (p_name, p_email)
    RETURNING user_id INTO p_user_id;
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20001, 'El email ya esta registrado: ' || p_email);
END user_insert;
/

CREATE OR REPLACE PROCEDURE user_get(
    p_user_id IN  NUMBER,
    p_name    OUT VARCHAR2,
    p_email   OUT VARCHAR2
) IS
BEGIN
    SELECT name, email INTO p_name, p_email
      FROM users
     WHERE user_id = p_user_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'No existe el usuario = ' || p_user_id);
END user_get;
/

CREATE OR REPLACE FUNCTION fn_existe_email(p_email IN VARCHAR2) RETURN NUMBER IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM users WHERE email = p_email;
    RETURN v_count;
END fn_existe_email;
/

-- ================= Articulos =================

CREATE OR REPLACE PROCEDURE article_insert(
    p_user_id    IN  NUMBER,
    p_title      IN  VARCHAR2,
    p_text       IN  VARCHAR2,
    p_article_id OUT NUMBER
) IS
BEGIN
    INSERT INTO articles(user_id, title, article_date, text)
    VALUES (p_user_id, p_title, SYSDATE, p_text)
    RETURNING article_id INTO p_article_id;
END article_insert;
/

CREATE OR REPLACE PROCEDURE article_update(
    p_article_id IN NUMBER,
    p_title      IN VARCHAR2,
    p_text       IN VARCHAR2
) IS
BEGIN
    UPDATE articles
       SET title = p_title,
           text  = p_text
     WHERE article_id = p_article_id;
    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20012, 'No existe el articulo = ' || p_article_id);
    END IF;
END article_update;
/

CREATE OR REPLACE PROCEDURE article_delete(
    p_article_id IN NUMBER
) IS
BEGIN
    DELETE FROM articles WHERE article_id = p_article_id;
    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20013, 'No existe el articulo = ' || p_article_id);
    END IF;
END article_delete;
/

CREATE OR REPLACE PROCEDURE article_get(
    p_article_id   IN  NUMBER,
    p_title        OUT VARCHAR2,
    p_article_date OUT DATE,
    p_text         OUT VARCHAR2,
    p_user_id      OUT NUMBER
) IS
BEGIN
    SELECT title, article_date, text, user_id
      INTO p_title, p_article_date, p_text, p_user_id
      FROM articles
     WHERE article_id = p_article_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20011, 'No existe el articulo = ' || p_article_id);
END article_get;
/

CREATE OR REPLACE PROCEDURE article_all(
    p_cursor OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT article_id, title, article_date, user_id
          FROM articles
         ORDER BY article_date DESC;
END article_all;
/

CREATE OR REPLACE PROCEDURE article_all_ordenado(
    p_atributo IN  VARCHAR2,
    p_tipo     IN  VARCHAR2,
    p_cursor   OUT SYS_REFCURSOR
) IS
    v_orden VARCHAR2(10);
    v_sql   VARCHAR2(300);
BEGIN
    -- Whitelist: solo estas columnas se pueden usar para ordenar.
    -- El nombre de columna no se puede pasar como bind variable,
    -- por eso se concatena, y por eso se valida a mano primero
    -- (evita inyeccion SQL via el nombre de columna).
    IF p_atributo NOT IN ('TITLE', 'ARTICLE_DATE') THEN
        RAISE_APPLICATION_ERROR(-20014, 'Atributo de ordenamiento no permitido: ' || p_atributo);
    END IF;

    IF p_tipo = '1' THEN
        v_orden := 'ASC';
    ELSE
        v_orden := 'DESC';
    END IF;

    v_sql := 'SELECT article_id, title, article_date, user_id FROM articles ORDER BY '
              || p_atributo || ' ' || v_orden;

    OPEN p_cursor FOR v_sql;
END article_all_ordenado;
/

-- ================= Comentarios =================

CREATE OR REPLACE PROCEDURE comment_insert(
    p_article_id IN  NUMBER,
    p_name       IN  VARCHAR2,
    p_url        IN  VARCHAR2,
    p_comment_id OUT NUMBER
) IS
BEGIN
    INSERT INTO comments(article_id, name, url, comment_date)
    VALUES (p_article_id, p_name, p_url, SYSDATE)
    RETURNING comment_id INTO p_comment_id;
END comment_insert;
/

CREATE OR REPLACE PROCEDURE comment_all(
    p_article_id IN  NUMBER,
    p_cursor     OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT comment_id, name, url, comment_date
          FROM comments
         WHERE article_id = p_article_id
         ORDER BY comment_date;
END comment_all;
/

CREATE OR REPLACE FUNCTION fn_contar_comentarios(p_article_id IN NUMBER) RETURN NUMBER IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM comments WHERE article_id = p_article_id;
    RETURN v_count;
END fn_contar_comentarios;
/

-- ================= Tags =================

CREATE OR REPLACE PROCEDURE tag_insert(
    p_name   IN  VARCHAR2,
    p_url    IN  VARCHAR2,
    p_tag_id OUT NUMBER
) IS
BEGIN
    INSERT INTO tags(name, url) VALUES (p_name, p_url)
    RETURNING tag_id INTO p_tag_id;
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20031, 'Ya existe un tag con ese nombre: ' || p_name);
END tag_insert;
/

CREATE OR REPLACE PROCEDURE tag_associate(
    p_article_id IN NUMBER,
    p_tag_id     IN NUMBER
) IS
BEGIN
    INSERT INTO article_tags(article_id, tag_id) VALUES (p_article_id, p_tag_id);
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20032, 'Ese tag ya esta asociado a ese articulo.');
END tag_associate;
/

CREATE OR REPLACE PROCEDURE tags_by_article(
    p_article_id IN  NUMBER,
    p_cursor     OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT t.tag_id, t.name, t.url
          FROM tags t
          JOIN article_tags at ON at.tag_id = t.tag_id
         WHERE at.article_id = p_article_id;
END tags_by_article;
/

CREATE OR REPLACE PROCEDURE articles_by_tag(
    p_tag_name IN  VARCHAR2,
    p_cursor   OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT a.article_id, a.title, a.article_date
          FROM articles a
          JOIN article_tags at ON at.article_id = a.article_id
          JOIN tags t ON t.tag_id = at.tag_id
         WHERE t.name = p_tag_name;
END articles_by_tag;
/

-- ================= Categorias =================

CREATE OR REPLACE PROCEDURE category_insert(
    p_name        IN  VARCHAR2,
    p_url         IN  VARCHAR2,
    p_category_id OUT NUMBER
) IS
BEGIN
    INSERT INTO categories(name, url) VALUES (p_name, p_url)
    RETURNING category_id INTO p_category_id;
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20041, 'Ya existe una categoria con ese nombre: ' || p_name);
END category_insert;
/

CREATE OR REPLACE PROCEDURE category_associate(
    p_article_id  IN NUMBER,
    p_category_id IN NUMBER
) IS
BEGIN
    INSERT INTO article_categories(article_id, category_id)
    VALUES (p_article_id, p_category_id);
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20042, 'Esa categoria ya esta asociada a ese articulo.');
END category_associate;
/

CREATE OR REPLACE PROCEDURE categories_by_article(
    p_article_id IN  NUMBER,
    p_cursor     OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT c.category_id, c.name, c.url
          FROM categories c
          JOIN article_categories ac ON ac.category_id = c.category_id
         WHERE ac.article_id = p_article_id;
END categories_by_article;
/
