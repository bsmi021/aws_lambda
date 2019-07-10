-- #Table: public.payment_methods

-- DROP TABLE public.payment_methods;

CREATE TABLE public.payment_methods
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id bigint NOT NULL DEFAULT nextval('payment_methods_id_seq'::regclass),
    buyer_id bigint,
    card_type_id integer,
    cardholder_name character varying COLLATE pg_catalog."default",
    alias character varying COLLATE pg_catalog."default",
    card_number character varying COLLATE pg_catalog."default",
    expiration character varying COLLATE pg_catalog."default",
    security_number character varying COLLATE pg_catalog."default",
    CONSTRAINT payment_methods_pkey PRIMARY KEY (id),
    CONSTRAINT fk_payment_methods_buyers FOREIGN KEY (buyer_id)
        REFERENCES public.buyers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

