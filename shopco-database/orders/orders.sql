--  #Table: public.orders

-- DROP TABLE public.orders;

CREATE TABLE public.orders
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id bigint NOT NULL DEFAULT nextval('orders_id_seq1'::regclass),
    order_id varchar(36),	
    customer_id character varying COLLATE pg_catalog."default" NOT NULL,
    address_id bigint NOT NULL,
    buyer_id integer,
    payment_method_id integer,
    order_status_id integer,
    order_date timestamp without time zone,
    is_draft boolean,
    description character varying COLLATE pg_catalog."default",
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT fk_order_address FOREIGN KEY (address_id)
        REFERENCES public.addresses (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_order_buyers FOREIGN KEY (buyer_id)
        REFERENCES public.buyers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_order_payment_methods FOREIGN KEY (payment_method_id)
        REFERENCES public.payment_methods (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

create unique index ux_order_id on public.orders(order_id);
