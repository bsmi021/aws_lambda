--  Table: public.sites

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