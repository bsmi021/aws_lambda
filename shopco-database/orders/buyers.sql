--  #Table: public.buyers

-- DROP TABLE public.buyers;

CREATE TABLE public.buyers
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id bigint NOT NULL DEFAULT nextval('buyers_id_seq'::regclass),
    user_id bigint NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT buyers_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

