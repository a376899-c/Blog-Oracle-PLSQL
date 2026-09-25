-- =====================================================================
-- blog_schema.sql (ADAPTADO A LA SINTAXIS DE LOS DOCUMENTOS DEL CURSO)
-- =====================================================================

-- =====================================================================
-- 1. TABLAS (Sin IDENTITY ni ON DELETE CASCADE)
-- =====================================================================

CREATE TABLE users (
    user_id  NUMBER,
    name     VARCHAR2(100) NOT NULL,
    email    VARCHAR2(150) NOT NULL,
    CONSTRAINT pk_users PRIMARY KEY (user_id)
);
CREATE UNIQUE INDEX uq_users_email ON users (LOWER(email));

CREATE TABLE articles (
    article_id   NUMBER,
    user_id      NUMBER NOT NULL,
    title        VARCHAR2(200) NOT NULL,
    article_date DATE NOT NULL,
    article_text VARCHAR2(4000),
    CONSTRAINT pk_articles PRIMARY KEY (article_id),
    CONSTRAINT fk_articles_user FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE comments (
    comment_id   NUMBER,
    article_id   NUMBER NOT NULL,
    name         VARCHAR2(100) NOT NULL,
    url          VARCHAR2(300),
    comment_date DATE NOT NULL,
    CONSTRAINT pk_comments PRIMARY KEY (comment_id),
    CONSTRAINT fk_comments_article FOREIGN KEY (article_id) REFERENCES articles (article_id)
);

CREATE TABLE tags (
    tag_id NUMBER,
    name   VARCHAR2(100) NOT NULL,
    url    VARCHAR2(300),
    CONSTRAINT pk_tags PRIMARY KEY (tag_id)
);
CREATE UNIQUE INDEX uq_tags_name ON tags (LOWER(name));

CREATE TABLE article_tags (
    article_id NUMBER NOT NULL,
    tag_id     NUMBER NOT NULL,
    CONSTRAINT pk_article_tags PRIMARY KEY (article_id, tag_id),
    CONSTRAINT fk_at_article FOREIGN KEY (article_id) REFERENCES articles (article_id),
    CONSTRAINT fk_at_tag     FOREIGN KEY (tag_id)     REFERENCES tags (tag_id)
);

CREATE TABLE categories (
    category_id NUMBER,
    name        VARCHAR2(100) NOT NULL,
    url         VARCHAR2(300),
    CONSTRAINT pk_categories PRIMARY KEY (category_id)
);
CREATE UNIQUE INDEX uq_categories_name ON categories (LOWER(name));

CREATE TABLE article_categories (
    article_id  NUMBER NOT NULL,
    category_id NUMBER NOT NULL,
    CONSTRAINT pk_article_categories PRIMARY KEY (article_id, category_id),
    CONSTRAINT fk_ac_article  FOREIGN KEY (article_id)  REFERENCES articles (article_id),
    CONSTRAINT fk_ac_category FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

-- =====================================================================
-- 2. USUARIOS
-- =====================================================================

CREATE OR REPLACE PROCEDURE user_insert (
    p_name  IN users.name%TYPE,
    p_email IN users.email%TYPE,
    p_id    OUT users.user_id%TYPE
)
IS
BEGIN
    -- Se genera el ID calculando el maximo como alternativa a IDENTITY
    SELECT NVL(MAX(user_id), 0) + 1 INTO p_id FROM users;
    
    INSERT INTO users (user_id, name, email) 
    VALUES (p_id, p_name, p_email);
END;
/

CREATE OR REPLACE PROCEDURE user_get (
    p_id    IN users.user_id%TYPE,
    p_name  OUT users.name%TYPE,
    p_email OUT users.email%TYPE
)
IS
BEGIN
    SELECT name, email
      INTO p_name, p_email
      FROM users
     WHERE user_id = p_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        raise_application_error(-20001, 'El usuario ' || p_id || ' no existe.');
END;
/

CREATE OR REPLACE FUNCTION fn_existe_email (
    p_email IN users.email%TYPE
) RETURN NUMBER
IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
      FROM users
     WHERE LOWER(email) = LOWER(p_email);
    RETURN v_count;
END;
/

-- =====================================================================
-- 3. ARTÍCULOS
-- =====================================================================

CREATE OR REPLACE PROCEDURE article_insert (
    p_user_id IN articles.user_id%TYPE,
    p_title   IN articles.title%TYPE,
    p_text    IN articles.article_text%TYPE,
    p_id      OUT articles.article_id%TYPE
)
IS
BEGIN
    SELECT NVL(MAX(article_id), 0) + 1 INTO p_id FROM articles;

    INSERT INTO articles (article_id, user_id, title, article_date, article_text)
    VALUES (p_id, p_user_id, p_title, sysdate, p_text);
END;
/

CREATE OR REPLACE PROCEDURE article_update (
    p_id    IN articles.article_id%TYPE,
    p_title IN articles.title%TYPE,
    p_text  IN articles.article_text%TYPE
)
IS
    no_articulo EXCEPTION;
BEGIN
    UPDATE articles
       SET title = p_title,
           article_text = p_text
     WHERE article_id = p_id;
     
    IF SQL%ROWCOUNT = 0 THEN
        RAISE no_articulo;
    END IF;
EXCEPTION
    WHEN no_articulo THEN
        raise_application_error(-20002, 'El artículo ' || p_id || ' no existe.');
END;
/

CREATE OR REPLACE PROCEDURE article_delete (
    p_id IN articles.article_id%TYPE
)
IS
    no_articulo EXCEPTION;
BEGIN
    -- Borrado manual de hijos para evitar violación de llave foránea sin usar CASCADE
    DELETE FROM comments WHERE article_id = p_id;
    DELETE FROM article_tags WHERE article_id = p_id;
    DELETE FROM article_categories WHERE article_id = p_id;

    DELETE FROM articles WHERE article_id = p_id;
    IF SQL%ROWCOUNT = 0 THEN
        RAISE no_articulo;
    END IF;
EXCEPTION
    WHEN no_articulo THEN
        raise_application_error(-20002, 'El artículo ' || p_id || ' no existe.');
END;
/

CREATE OR REPLACE PROCEDURE article_get (
    p_id       IN  articles.article_id%TYPE,
    p_title    OUT articles.title%TYPE,
    p_date     OUT articles.article_date%TYPE,
    p_text     OUT articles.article_text%TYPE,
    p_user_id  OUT articles.user_id%TYPE
)
IS
BEGIN
    SELECT title, article_date, article_text, user_id
      INTO p_title, p_date, p_text, p_user_id
      FROM articles
     WHERE article_id = p_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        raise_application_error(-20002, 'El artículo ' || p_id || ' no existe.');
END;
/

CREATE OR REPLACE PROCEDURE article_all (
    p_cursor OUT SYS_REFCURSOR
)
IS
    opsql VARCHAR2(255);
BEGIN
    opsql := 'SELECT article_id, title, article_date, user_id FROM articles ORDER BY article_id';
    OPEN p_cursor FOR opsql;
END;
/

CREATE OR REPLACE PROCEDURE article_all_ordenado (
    p_atributo IN VARCHAR2,
    p_tipo     IN VARCHAR2,
    p_cursor   OUT SYS_REFCURSOR
)
IS
    v_col VARCHAR2(20);
    v_dir VARCHAR2(4);
    opsql VARCHAR2(500);
BEGIN
    IF UPPER(p_atributo) = 'TITLE' THEN
        v_col := 'title';
    ELSIF UPPER(p_atributo) = 'ARTICLE_DATE' THEN
        v_col := 'article_date';
    ELSE
        v_col := NULL;
    END IF;

    IF p_tipo = '1' THEN
        v_dir := 'ASC';
    ELSIF p_tipo = '2' THEN
        v_dir := 'DESC';
    ELSE
        v_dir := NULL;
    END IF;

    IF v_col IS NULL OR v_dir IS NULL THEN
        raise_application_error(-20003, 'Atributo o tipo de orden inválido.');
    END IF;

    opsql := 'SELECT article_id, title, article_date, user_id FROM articles ORDER BY ' || v_col || ' ' || v_dir;
    OPEN p_cursor FOR opsql;
END;
/

-- =====================================================================
-- 4. COMENTARIOS
-- =====================================================================

CREATE OR REPLACE PROCEDURE comment_insert (
    p_article_id IN comments.article_id%TYPE,
    p_name       IN comments.name%TYPE,
    p_url        IN comments.url%TYPE,
    p_id         OUT comments.comment_id%TYPE
)
IS
BEGIN
    SELECT NVL(MAX(comment_id), 0) + 1 INTO p_id FROM comments;

    INSERT INTO comments (comment_id, article_id, name, url, comment_date)
    VALUES (p_id, p_article_id, p_name, p_url, sysdate);
END;
/

CREATE OR REPLACE PROCEDURE comment_all (
    p_article_id IN comments.article_id%TYPE,
    p_cursor     OUT SYS_REFCURSOR
)
IS
    opsql VARCHAR2(255);
BEGIN
    opsql := 'SELECT comment_id, name, url, comment_date FROM comments WHERE article_id = :aid ORDER BY comment_date';
    OPEN p_cursor FOR opsql USING p_article_id;
END;
/

CREATE OR REPLACE FUNCTION fn_contar_comentarios (
    p_article_id IN comments.article_id%TYPE
) RETURN NUMBER
IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count 
      FROM comments 
     WHERE article_id = p_article_id;
    RETURN v_count;
END;
/

-- =====================================================================
-- 5. TAGS
-- =====================================================================

CREATE OR REPLACE PROCEDURE tag_insert (
    p_name IN tags.name%TYPE,
    p_url  IN tags.url%TYPE,
    p_id   OUT tags.tag_id%TYPE
)
IS
BEGIN
    SELECT NVL(MAX(tag_id), 0) + 1 INTO p_id FROM tags;
    INSERT INTO tags (tag_id, name, url) VALUES (p_id, p_name, p_url);
END;
/

CREATE OR REPLACE PROCEDURE tag_associate (
    p_article_id IN article_tags.article_id%TYPE,
    p_tag_id     IN article_tags.tag_id%TYPE
)
IS
    ellave_primaria EXCEPTION;
    PRAGMA exception_init(ellave_primaria, -00001);
BEGIN
    INSERT INTO article_tags (article_id, tag_id) VALUES (p_article_id, p_tag_id);
EXCEPTION
    WHEN ellave_primaria THEN
        raise_application_error(-20004, 'Ese tag ya está asociado al artículo.');
END;
/

CREATE OR REPLACE PROCEDURE tags_by_article (
    p_article_id IN tags.tag_id%TYPE,
    p_cursor     OUT SYS_REFCURSOR
)
IS
    opsql VARCHAR2(500);
BEGIN
    opsql := 'SELECT t.tag_id, t.name, t.url FROM tags t JOIN article_tags atg ON atg.tag_id = t.tag_id WHERE atg.article_id = :aid ORDER BY t.name';
    OPEN p_cursor FOR opsql USING p_article_id;
END;
/

CREATE OR REPLACE PROCEDURE articles_by_tag (
    p_tag_name IN tags.name%TYPE,
    p_cursor   OUT SYS_REFCURSOR
)
IS
    opsql VARCHAR2(500);
BEGIN
    -- Se aprovecha concatenación dinámica simulando uso de cursores dinámicos
    opsql := 'SELECT a.article_id, a.title, a.article_date FROM articles a ' ||
             'JOIN article_tags atg ON atg.article_id = a.article_id ' ||
             'JOIN tags t ON t.tag_id = atg.tag_id ' ||
             'WHERE LOWER(t.name) = LOWER(:tname) ORDER BY a.article_date DESC';
    OPEN p_cursor FOR opsql USING p_tag_name;
END;
/

-- =====================================================================
-- 6. CATEGORÍAS
-- =====================================================================

CREATE OR REPLACE PROCEDURE category_insert (
    p_name IN categories.name%TYPE,
    p_url  IN categories.url%TYPE,
    p_id   OUT categories.category_id%TYPE
)
IS
BEGIN
    SELECT NVL(MAX(category_id), 0) + 1 INTO p_id FROM categories;
    INSERT INTO categories (category_id, name, url) VALUES (p_id, p_name, p_url);
END;
/

CREATE OR REPLACE PROCEDURE category_associate (
    p_article_id  IN article_categories.article_id%TYPE,
    p_category_id IN article_categories.category_id%TYPE
)
IS
    ellave_primaria EXCEPTION;
    PRAGMA exception_init(ellave_primaria, -00001);
BEGIN
    INSERT INTO article_categories (article_id, category_id)
    VALUES (p_article_id, p_category_id);
EXCEPTION
    WHEN ellave_primaria THEN
        raise_application_error(-20005, 'Esa categoría ya está asociada al artículo.');
END;
/

CREATE OR REPLACE PROCEDURE categories_by_article (
    p_article_id IN article_categories.article_id%TYPE,
    p_cursor     OUT SYS_REFCURSOR
)
IS
    opsql VARCHAR2(500);
BEGIN
    opsql := 'SELECT c.category_id, c.name, c.url FROM categories c ' ||
             'JOIN article_categories ac ON ac.category_id = c.category_id ' ||
             'WHERE ac.article_id = :aid ORDER BY c.name';
    OPEN p_cursor FOR opsql USING p_article_id;
END;
/
