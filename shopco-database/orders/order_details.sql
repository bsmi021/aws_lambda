--# Table: public.order_details

-- DROP TABLE public.order_details;
 
CREATE TABLE public.order_details
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id bigint NOT NULL DEFAULT nextval('order_details_id_seq'::regclass),
    order_id bigint,
    product_id integer,
    product_name character varying COLLATE pg_catalog."default",
    unit_price double precision,
    discount double precision,
    units integer,
    CONSTRAINT order_details_pkey PRIMARY KEY (id),
    CONSTRAINT fk_order_details_order FOREIGN KEY (order_id)
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

