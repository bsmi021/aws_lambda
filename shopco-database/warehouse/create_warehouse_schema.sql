--  SEQUENCE: public.sites_id_seq

-- DROP SEQUENCE public.sites_id_seq;
CREATE DATABASE warehouse;

USE warehouse;

CREATE SEQUENCE public.sites_id_seq;

-- DROP SEQUENCE public.inventory_items_id_seq;

CREATE SEQUENCE public.inventory_items_id_seq;

-- DROP TABLE public.sites;

CREATE TABLE public.sites
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id bigint NOT NULL DEFAULT nextval('sites_id_seq'::regclass),
    site_id varchar(36) not null,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    zip_code character varying(12) COLLATE pg_catalog."default" NOT NULL,
    type_id integer NOT NULL,
    is_deleted boolean not null default (FALSE),
    CONSTRAINT sites_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


CREATE INDEX ux_site_id
    ON public.sites USING btree
    (site_id)
    TABLESPACE pg_default;

-- DROP TABLE public.inventory_items;

CREATE TABLE public.inventory_items
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id bigint NOT NULL,
    version bigint NOT NULL,
    product_id varchar(36) NOT NULL,
    site_id bigint NOT NULL,
    on_reorder boolean,
    restock_threshold integer NOT NULL,
    max_stock_threshold integer NOT NULL,
    available_stock integer NOT NULL,
    committed_stock integer NOT NULL,
    CONSTRAINT inventory_items_pkey PRIMARY KEY (id, version, product_id, site_id),
    CONSTRAINT fk_inventory_items_site FOREIGN KEY (site_id)
        REFERENCES public.sites (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


-- Index: index

-- DROP INDEX public.index;

CREATE INDEX index
    ON public.inventory_items USING btree
    (id, version)
    TABLESPACE pg_default;

CREATE INDEX ux_product_version
	ON public.inventory_items using btree
	(product_id, version)
	TABLESPACE pg_default;