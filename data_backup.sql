--
-- PostgreSQL database dump
--

\restrict CBYHHJQeVQGmlhlixVFIJwdaD3Ess6oWIhJ2EEqbv0KeeGC5bw9cf4k4vazV6Ob

-- Dumped from database version 15.15 (Debian 15.15-1.pgdg13+1)
-- Dumped by pg_dump version 15.15 (Debian 15.15-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: movement_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.movement_type AS ENUM (
    'supplier_purchase',
    'to_client',
    'client_sale',
    'client_loss',
    'supplier_loss'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: client_loss_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.client_loss_history (
    id integer NOT NULL,
    cost_center_id integer NOT NULL,
    product_id integer NOT NULL,
    date date NOT NULL,
    lost_quantity integer NOT NULL,
    reason character varying,
    observed_at timestamp with time zone
);


--
-- Name: client_loss_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.client_loss_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: client_loss_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.client_loss_history_id_seq OWNED BY public.client_loss_history.id;


--
-- Name: client_sales_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.client_sales_history (
    id integer NOT NULL,
    cost_center_id integer NOT NULL,
    product_id integer NOT NULL,
    date date NOT NULL,
    sold_quantity integer NOT NULL,
    observed_at timestamp with time zone
);


--
-- Name: client_sales_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.client_sales_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: client_sales_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.client_sales_history_id_seq OWNED BY public.client_sales_history.id;


--
-- Name: client_stock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.client_stock (
    id integer NOT NULL,
    cost_center_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    last_observed_at timestamp with time zone,
    last_zeroed_at timestamp with time zone
);


--
-- Name: client_stock_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.client_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: client_stock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.client_stock_id_seq OWNED BY public.client_stock.id;


--
-- Name: cost_centers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cost_centers (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    retail_chain_id integer,
    is_active boolean,
    deleted_at timestamp without time zone
);


--
-- Name: cost_centers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cost_centers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cost_centers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cost_centers_id_seq OWNED BY public.cost_centers.id;


--
-- Name: inventory_stock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventory_stock (
    id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL
);


--
-- Name: inventory_stock_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventory_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventory_stock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventory_stock_id_seq OWNED BY public.inventory_stock.id;


--
-- Name: inventory_visit_products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventory_visit_products (
    id integer NOT NULL,
    inventory_visit_id integer NOT NULL,
    product_id integer NOT NULL,
    stock_quantity integer NOT NULL,
    sales_quantity integer DEFAULT 0 NOT NULL,
    loss_quantity integer DEFAULT 0 NOT NULL,
    next_quantity integer,
    shelf_price numeric(10,2),
    previous_client_stock integer,
    requested_quantity integer
);


--
-- Name: inventory_visit_products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventory_visit_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventory_visit_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventory_visit_products_id_seq OWNED BY public.inventory_visit_products.id;


--
-- Name: inventory_visits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventory_visits (
    id integer NOT NULL,
    cost_center_id integer NOT NULL,
    ticket_id integer,
    recorded_by integer,
    visited_at timestamp with time zone DEFAULT now() NOT NULL,
    total_stock_quantity integer,
    notes text
);


--
-- Name: inventory_visits_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inventory_visits_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inventory_visits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inventory_visits_id_seq OWNED BY public.inventory_visits.id;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying,
    description character varying
);


--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: product_cost_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.product_cost_history (
    id integer NOT NULL,
    product_id integer NOT NULL,
    cost numeric(10,2) NOT NULL,
    start_date timestamp without time zone DEFAULT now() NOT NULL,
    end_date timestamp without time zone
);


--
-- Name: product_cost_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.product_cost_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: product_cost_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.product_cost_history_id_seq OWNED BY public.product_cost_history.id;


--
-- Name: product_price_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.product_price_history (
    id integer NOT NULL,
    product_id integer NOT NULL,
    retail_chain_id integer,
    cost_center_id integer,
    price numeric(10,2) NOT NULL,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    CONSTRAINT check_price_hierarchy CHECK ((((retail_chain_id IS NOT NULL) AND (cost_center_id IS NULL)) OR ((retail_chain_id IS NULL) AND (cost_center_id IS NOT NULL))))
);


--
-- Name: product_price_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.product_price_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: product_price_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.product_price_history_id_seq OWNED BY public.product_price_history.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id integer NOT NULL,
    custom_id character varying,
    name character varying NOT NULL,
    category_id integer,
    is_active boolean,
    deleted_at timestamp without time zone
);


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: replenishment_recommendations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.replenishment_recommendations (
    id integer NOT NULL,
    cost_center_id integer NOT NULL,
    product_id integer NOT NULL,
    recommendation_date timestamp without time zone,
    recommendation character varying NOT NULL,
    reason character varying
);


--
-- Name: replenishment_recommendations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.replenishment_recommendations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: replenishment_recommendations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.replenishment_recommendations_id_seq OWNED BY public.replenishment_recommendations.id;


--
-- Name: retail_chains; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.retail_chains (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying(500),
    status boolean
);


--
-- Name: retail_chains_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.retail_chains_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: retail_chains_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.retail_chains_id_seq OWNED BY public.retail_chains.id;


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_permissions (
    id integer NOT NULL,
    role_id integer,
    permission_id integer
);


--
-- Name: role_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.role_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: role_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.role_permissions_id_seq OWNED BY public.role_permissions.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying,
    description character varying
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: sellers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sellers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    cost_center_id integer NOT NULL
);


--
-- Name: sellers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sellers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sellers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sellers_id_seq OWNED BY public.sellers.id;


--
-- Name: shelf_prices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shelf_prices (
    id integer NOT NULL,
    product_id integer NOT NULL,
    retail_chain_id integer,
    cost_center_id integer,
    percentage_rate numeric(10,4) NOT NULL,
    start_date timestamp without time zone DEFAULT now(),
    end_date timestamp without time zone,
    CONSTRAINT check_shelf_price_scope CHECK ((((retail_chain_id IS NOT NULL) AND (cost_center_id IS NULL)) OR ((retail_chain_id IS NULL) AND (cost_center_id IS NOT NULL))))
);


--
-- Name: shelf_prices_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.shelf_prices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: shelf_prices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.shelf_prices_id_seq OWNED BY public.shelf_prices.id;


--
-- Name: stock_movements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_movements (
    id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    movement_type public.movement_type NOT NULL,
    supplier_id integer,
    cost_center_id integer,
    product_unit_cost numeric(10,2),
    created_at timestamp with time zone DEFAULT now(),
    inventory_visit_id integer
);


--
-- Name: stock_movements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stock_movements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: stock_movements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stock_movements_id_seq OWNED BY public.stock_movements.id;


--
-- Name: suppliers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.suppliers (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    contact_email character varying(150),
    contact_phone character varying(50),
    address character varying(250),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


--
-- Name: suppliers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.suppliers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: suppliers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.suppliers_id_seq OWNED BY public.suppliers.id;


--
-- Name: ticket_products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ticket_products (
    id integer NOT NULL,
    ticket_id integer NOT NULL,
    product_id integer NOT NULL,
    sent_quantity integer NOT NULL,
    unit_price numeric(10,2),
    entry_price numeric(10,2)
);


--
-- Name: tickets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status character varying,
    cost_center_id integer NOT NULL,
    order_date date NOT NULL,
    approved_at timestamp without time zone,
    sales_start_date date,
    created_by integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: ticket_product_visit_summary; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.ticket_product_visit_summary AS
 WITH cutoff AS (
         SELECT t.id AS ticket_id,
            t.cost_center_id,
            COALESCE(t.created_at, (t.approved_at)::timestamp with time zone, ((((t.order_date)::timestamp without time zone + '1 day'::interval) - '00:00:01'::interval))::timestamp with time zone) AS cutoff_at
           FROM public.tickets t
        ), ranked AS (
         SELECT c.ticket_id,
            ivp.product_id,
            iv.visited_at,
            ivp.stock_quantity,
            ivp.loss_quantity,
            ivp.sales_quantity,
            tp.sent_quantity,
            row_number() OVER (PARTITION BY c.ticket_id, ivp.product_id ORDER BY iv.visited_at DESC, iv.id DESC) AS rn
           FROM (((cutoff c
             JOIN public.inventory_visits iv ON (((iv.cost_center_id = c.cost_center_id) AND (iv.visited_at < c.cutoff_at))))
             JOIN public.inventory_visit_products ivp ON ((ivp.inventory_visit_id = iv.id)))
             LEFT JOIN public.ticket_products tp ON (((tp.ticket_id = iv.ticket_id) AND (tp.product_id = ivp.product_id))))
        )
 SELECT ranked.ticket_id,
    ranked.product_id,
    max(
        CASE
            WHEN (ranked.rn = 1) THEN ranked.loss_quantity
            ELSE NULL::integer
        END) AS loss_last,
    max(
        CASE
            WHEN (ranked.rn = 2) THEN ranked.loss_quantity
            ELSE NULL::integer
        END) AS loss_prev,
    max(
        CASE
            WHEN (ranked.rn = 1) THEN ranked.sales_quantity
            ELSE NULL::integer
        END) AS sales_last,
    max(
        CASE
            WHEN (ranked.rn = 2) THEN ranked.sales_quantity
            ELSE NULL::integer
        END) AS sales_prev,
    max(
        CASE
            WHEN (ranked.rn = 1) THEN ranked.stock_quantity
            ELSE NULL::integer
        END) AS stock_last,
    max(
        CASE
            WHEN (ranked.rn = 2) THEN ranked.stock_quantity
            ELSE NULL::integer
        END) AS stock_prev,
    max(
        CASE
            WHEN (ranked.rn = 1) THEN ranked.sent_quantity
            ELSE NULL::integer
        END) AS order_last,
    max(
        CASE
            WHEN (ranked.rn = 2) THEN ranked.sent_quantity
            ELSE NULL::integer
        END) AS order_prev,
    max(
        CASE
            WHEN (ranked.rn = 2) THEN ranked.visited_at
            ELSE NULL::timestamp with time zone
        END) AS order_prev_date
   FROM ranked
  WHERE (ranked.rn <= 2)
  GROUP BY ranked.ticket_id, ranked.product_id;


--
-- Name: ticket_products_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ticket_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ticket_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ticket_products_id_seq OWNED BY public.ticket_products.id;


--
-- Name: tickets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_id_seq OWNED BY public.tickets.id;


--
-- Name: unit_conversion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.unit_conversion (
    id integer NOT NULL,
    unit_from integer NOT NULL,
    unit_to integer NOT NULL,
    conversion double precision NOT NULL,
    status boolean
);


--
-- Name: unit_conversion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.unit_conversion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: unit_conversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.unit_conversion_id_seq OWNED BY public.unit_conversion.id;


--
-- Name: unit_measurement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.unit_measurement (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


--
-- Name: unit_measurement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.unit_measurement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: unit_measurement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.unit_measurement_id_seq OWNED BY public.unit_measurement.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);


--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(250) NOT NULL,
    email character varying(200) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    full_name character varying(250),
    nickname character varying(250),
    is_active boolean,
    is_superuser boolean,
    last_login timestamp without time zone,
    date_joined timestamp without time zone
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: client_loss_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_loss_history ALTER COLUMN id SET DEFAULT nextval('public.client_loss_history_id_seq'::regclass);


--
-- Name: client_sales_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_sales_history ALTER COLUMN id SET DEFAULT nextval('public.client_sales_history_id_seq'::regclass);


--
-- Name: client_stock id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_stock ALTER COLUMN id SET DEFAULT nextval('public.client_stock_id_seq'::regclass);


--
-- Name: cost_centers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_centers ALTER COLUMN id SET DEFAULT nextval('public.cost_centers_id_seq'::regclass);


--
-- Name: inventory_stock id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_stock ALTER COLUMN id SET DEFAULT nextval('public.inventory_stock_id_seq'::regclass);


--
-- Name: inventory_visit_products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visit_products ALTER COLUMN id SET DEFAULT nextval('public.inventory_visit_products_id_seq'::regclass);


--
-- Name: inventory_visits id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visits ALTER COLUMN id SET DEFAULT nextval('public.inventory_visits_id_seq'::regclass);


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: product_cost_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_cost_history ALTER COLUMN id SET DEFAULT nextval('public.product_cost_history_id_seq'::regclass);


--
-- Name: product_price_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history ALTER COLUMN id SET DEFAULT nextval('public.product_price_history_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: replenishment_recommendations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.replenishment_recommendations ALTER COLUMN id SET DEFAULT nextval('public.replenishment_recommendations_id_seq'::regclass);


--
-- Name: retail_chains id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.retail_chains ALTER COLUMN id SET DEFAULT nextval('public.retail_chains_id_seq'::regclass);


--
-- Name: role_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions ALTER COLUMN id SET DEFAULT nextval('public.role_permissions_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: sellers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers ALTER COLUMN id SET DEFAULT nextval('public.sellers_id_seq'::regclass);


--
-- Name: shelf_prices id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices ALTER COLUMN id SET DEFAULT nextval('public.shelf_prices_id_seq'::regclass);


--
-- Name: stock_movements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements ALTER COLUMN id SET DEFAULT nextval('public.stock_movements_id_seq'::regclass);


--
-- Name: suppliers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suppliers ALTER COLUMN id SET DEFAULT nextval('public.suppliers_id_seq'::regclass);


--
-- Name: ticket_products id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_products ALTER COLUMN id SET DEFAULT nextval('public.ticket_products_id_seq'::regclass);


--
-- Name: tickets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets ALTER COLUMN id SET DEFAULT nextval('public.tickets_id_seq'::regclass);


--
-- Name: unit_conversion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_conversion ALTER COLUMN id SET DEFAULT nextval('public.unit_conversion_id_seq'::regclass);


--
-- Name: unit_measurement id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_measurement ALTER COLUMN id SET DEFAULT nextval('public.unit_measurement_id_seq'::regclass);


--
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
8c3f1d2a4b56
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categories (id, name, description, status) FROM stdin;
2	FRUTAS	FRUTAS	t
3	FOLHAGEM	SALADAS E COUVE-PICADA	t
1	VERDURAS 	BRÓCOLIS, COUVE-FLOR, MISTO ETC	t
4	LEGUMES	MANDIOQUINHA, ABOBRINHA, TOMATE, VAGEM	t
5	SEMENTE	PINHÃO	t
\.


--
-- Data for Name: client_loss_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.client_loss_history (id, cost_center_id, product_id, date, lost_quantity, reason, observed_at) FROM stdin;
1	1	44	2025-10-13	3	Perda registrada	\N
2	1	4	2025-11-17	3	Perda registrada	\N
3	1	44	2025-11-17	10	Perda registrada	\N
4	1	15	2025-11-17	3	Perda registrada	\N
5	1	14	2025-11-17	4	Perda registrada	\N
6	1	13	2025-11-17	4	Perda registrada	\N
7	1	16	2025-11-17	4	Perda registrada	\N
8	1	21	2025-11-17	5	Perda registrada	\N
9	1	35	2025-11-17	3	Perda registrada	\N
10	1	19	2025-11-17	3	Perda registrada	\N
11	1	4	2025-11-24	0	\N	2025-11-24 12:00:00-03
12	1	13	2025-11-24	0	\N	2025-11-24 12:00:00-03
13	1	14	2025-11-24	0	\N	2025-11-24 12:00:00-03
14	1	15	2025-11-24	0	\N	2025-11-24 12:00:00-03
15	1	16	2025-11-24	0	\N	2025-11-24 12:00:00-03
16	1	17	2025-11-24	0	\N	2025-11-24 12:00:00-03
17	1	18	2025-11-24	0	\N	2025-11-24 12:00:00-03
18	1	19	2025-11-24	0	\N	2025-11-24 12:00:00-03
19	1	20	2025-11-24	0	\N	2025-11-24 12:00:00-03
20	1	21	2025-11-24	0	\N	2025-11-24 12:00:00-03
21	1	23	2025-11-24	0	\N	2025-11-24 12:00:00-03
22	1	24	2025-11-24	0	\N	2025-11-24 12:00:00-03
23	1	26	2025-11-24	0	\N	2025-11-24 12:00:00-03
24	1	27	2025-11-24	0	\N	2025-11-24 12:00:00-03
25	1	28	2025-11-24	0	\N	2025-11-24 12:00:00-03
26	1	35	2025-11-24	0	\N	2025-11-24 12:00:00-03
27	1	36	2025-11-24	0	\N	2025-11-24 12:00:00-03
28	1	37	2025-11-24	0	\N	2025-11-24 12:00:00-03
29	1	39	2025-11-24	0	\N	2025-11-24 12:00:00-03
30	1	44	2025-11-24	0	\N	2025-11-24 12:00:00-03
31	1	4	2025-11-27	0	\N	2025-11-27 12:00:00-03
32	1	13	2025-11-27	0	\N	2025-11-27 12:00:00-03
33	1	14	2025-11-27	0	\N	2025-11-27 12:00:00-03
34	1	15	2025-11-27	0	\N	2025-11-27 12:00:00-03
35	1	16	2025-11-27	0	\N	2025-11-27 12:00:00-03
36	1	17	2025-11-27	0	\N	2025-11-27 12:00:00-03
37	1	18	2025-11-27	0	\N	2025-11-27 12:00:00-03
38	1	19	2025-11-27	0	\N	2025-11-27 12:00:00-03
39	1	20	2025-11-27	0	\N	2025-11-27 12:00:00-03
40	1	21	2025-11-27	0	\N	2025-11-27 12:00:00-03
41	1	23	2025-11-27	0	\N	2025-11-27 12:00:00-03
42	1	24	2025-11-27	0	\N	2025-11-27 12:00:00-03
43	1	27	2025-11-27	0	\N	2025-11-27 12:00:00-03
44	1	28	2025-11-27	0	\N	2025-11-27 12:00:00-03
45	1	35	2025-11-27	0	\N	2025-11-27 12:00:00-03
46	1	36	2025-11-27	0	\N	2025-11-27 12:00:00-03
47	1	37	2025-11-27	0	\N	2025-11-27 12:00:00-03
48	1	39	2025-11-27	0	\N	2025-11-27 12:00:00-03
49	1	40	2025-11-27	0	\N	2025-11-27 12:00:00-03
50	1	44	2025-11-27	0	\N	2025-11-27 12:00:00-03
51	1	4	2025-12-01	0	\N	2025-12-01 12:00:00-03
52	1	13	2025-12-01	1	\N	2025-12-01 12:00:00-03
53	1	14	2025-12-01	0	\N	2025-12-01 12:00:00-03
54	1	15	2025-12-01	4	\N	2025-12-01 12:00:00-03
55	1	16	2025-12-01	2	\N	2025-12-01 12:00:00-03
56	1	17	2025-12-01	3	\N	2025-12-01 12:00:00-03
57	1	18	2025-12-01	3	\N	2025-12-01 12:00:00-03
58	1	19	2025-12-01	7	\N	2025-12-01 12:00:00-03
59	1	20	2025-12-01	0	\N	2025-12-01 12:00:00-03
60	1	21	2025-12-01	4	\N	2025-12-01 12:00:00-03
61	1	23	2025-12-01	1	\N	2025-12-01 12:00:00-03
62	1	24	2025-12-01	4	\N	2025-12-01 12:00:00-03
63	1	25	2025-12-01	0	\N	2025-12-01 12:00:00-03
64	1	26	2025-12-01	0	\N	2025-12-01 12:00:00-03
65	1	27	2025-12-01	0	\N	2025-12-01 12:00:00-03
66	1	28	2025-12-01	11	\N	2025-12-01 12:00:00-03
67	1	35	2025-12-01	0	\N	2025-12-01 12:00:00-03
68	1	36	2025-12-01	0	\N	2025-12-01 12:00:00-03
69	1	37	2025-12-01	0	\N	2025-12-01 12:00:00-03
70	1	39	2025-12-01	0	\N	2025-12-01 12:00:00-03
71	1	40	2025-12-01	2	\N	2025-12-01 12:00:00-03
72	1	44	2025-12-01	22	\N	2025-12-01 12:00:00-03
73	1	4	2025-12-04	0	\N	2025-12-04 12:00:00-03
74	1	13	2025-12-04	0	\N	2025-12-04 12:00:00-03
75	1	14	2025-12-04	0	\N	2025-12-04 12:00:00-03
76	1	15	2025-12-04	0	\N	2025-12-04 12:00:00-03
77	1	16	2025-12-04	0	\N	2025-12-04 12:00:00-03
78	1	17	2025-12-04	0	\N	2025-12-04 12:00:00-03
79	1	18	2025-12-04	0	\N	2025-12-04 12:00:00-03
80	1	19	2025-12-04	0	\N	2025-12-04 12:00:00-03
81	1	20	2025-12-04	0	\N	2025-12-04 12:00:00-03
82	1	21	2025-12-04	0	\N	2025-12-04 12:00:00-03
83	1	22	2025-12-04	0	\N	2025-12-04 12:00:00-03
84	1	23	2025-12-04	0	\N	2025-12-04 12:00:00-03
85	1	24	2025-12-04	0	\N	2025-12-04 12:00:00-03
86	1	25	2025-12-04	0	\N	2025-12-04 12:00:00-03
87	1	26	2025-12-04	0	\N	2025-12-04 12:00:00-03
88	1	27	2025-12-04	0	\N	2025-12-04 12:00:00-03
89	1	28	2025-12-04	0	\N	2025-12-04 12:00:00-03
90	1	35	2025-12-04	0	\N	2025-12-04 12:00:00-03
91	1	36	2025-12-04	0	\N	2025-12-04 12:00:00-03
92	1	37	2025-12-04	0	\N	2025-12-04 12:00:00-03
93	1	39	2025-12-04	0	\N	2025-12-04 12:00:00-03
94	1	40	2025-12-04	0	\N	2025-12-04 12:00:00-03
95	1	44	2025-12-04	0	\N	2025-12-04 12:00:00-03
96	1	4	2025-12-08	0	\N	2025-12-08 12:00:00-03
97	1	13	2025-12-08	0	\N	2025-12-08 12:00:00-03
98	1	14	2025-12-08	7	\N	2025-12-08 12:00:00-03
99	1	15	2025-12-08	4	\N	2025-12-08 12:00:00-03
100	1	16	2025-12-08	0	\N	2025-12-08 12:00:00-03
101	1	17	2025-12-08	3	\N	2025-12-08 12:00:00-03
102	1	18	2025-12-08	1	\N	2025-12-08 12:00:00-03
103	1	19	2025-12-08	2	\N	2025-12-08 12:00:00-03
104	1	20	2025-12-08	0	\N	2025-12-08 12:00:00-03
105	1	21	2025-12-08	4	\N	2025-12-08 12:00:00-03
106	1	23	2025-12-08	0	\N	2025-12-08 12:00:00-03
107	1	24	2025-12-08	0	\N	2025-12-08 12:00:00-03
108	1	25	2025-12-08	0	\N	2025-12-08 12:00:00-03
109	1	26	2025-12-08	0	\N	2025-12-08 12:00:00-03
110	1	27	2025-12-08	1	\N	2025-12-08 12:00:00-03
111	1	28	2025-12-08	0	\N	2025-12-08 12:00:00-03
112	1	35	2025-12-08	8	\N	2025-12-08 12:00:00-03
113	1	36	2025-12-08	1	\N	2025-12-08 12:00:00-03
114	1	37	2025-12-08	0	\N	2025-12-08 12:00:00-03
115	1	39	2025-12-08	4	\N	2025-12-08 12:00:00-03
116	1	44	2025-12-08	15	\N	2025-12-08 12:00:00-03
117	1	4	2025-12-11	0	\N	2025-12-11 12:00:00-03
118	1	13	2025-12-11	0	\N	2025-12-11 12:00:00-03
119	1	14	2025-12-11	0	\N	2025-12-11 12:00:00-03
120	1	15	2025-12-11	0	\N	2025-12-11 12:00:00-03
121	1	16	2025-12-11	0	\N	2025-12-11 12:00:00-03
122	1	17	2025-12-11	0	\N	2025-12-11 12:00:00-03
123	1	18	2025-12-11	0	\N	2025-12-11 12:00:00-03
124	1	19	2025-12-11	0	\N	2025-12-11 12:00:00-03
125	1	20	2025-12-11	0	\N	2025-12-11 12:00:00-03
126	1	21	2025-12-11	0	\N	2025-12-11 12:00:00-03
127	1	23	2025-12-11	0	\N	2025-12-11 12:00:00-03
128	1	24	2025-12-11	0	\N	2025-12-11 12:00:00-03
129	1	27	2025-12-11	0	\N	2025-12-11 12:00:00-03
130	1	28	2025-12-11	0	\N	2025-12-11 12:00:00-03
131	1	35	2025-12-11	0	\N	2025-12-11 12:00:00-03
132	1	36	2025-12-11	0	\N	2025-12-11 12:00:00-03
133	1	44	2025-12-11	0	\N	2025-12-11 12:00:00-03
134	1	4	2025-12-18	0	\N	2025-12-18 12:00:00-03
135	1	13	2025-12-18	0	\N	2025-12-18 12:00:00-03
136	1	14	2025-12-18	0	\N	2025-12-18 12:00:00-03
137	1	15	2025-12-18	0	\N	2025-12-18 12:00:00-03
138	1	16	2025-12-18	0	\N	2025-12-18 12:00:00-03
139	1	19	2025-12-18	0	\N	2025-12-18 12:00:00-03
140	1	20	2025-12-18	0	\N	2025-12-18 12:00:00-03
141	1	21	2025-12-18	0	\N	2025-12-18 12:00:00-03
142	1	24	2025-12-18	0	\N	2025-12-18 12:00:00-03
143	1	27	2025-12-18	0	\N	2025-12-18 12:00:00-03
144	1	28	2025-12-18	0	\N	2025-12-18 12:00:00-03
145	1	44	2025-12-18	0	\N	2025-12-18 12:00:00-03
146	1	4	2026-01-05	6	\N	2026-01-05 12:00:00-03
147	1	13	2026-01-05	4	\N	2026-01-05 12:00:00-03
148	1	14	2026-01-05	11	\N	2026-01-05 12:00:00-03
149	1	15	2026-01-05	3	\N	2026-01-05 12:00:00-03
150	1	16	2026-01-05	27	\N	2026-01-05 12:00:00-03
151	1	17	2026-01-05	6	\N	2026-01-05 12:00:00-03
152	1	18	2026-01-05	7	\N	2026-01-05 12:00:00-03
153	1	19	2026-01-05	0	\N	2026-01-05 12:00:00-03
154	1	20	2026-01-05	0	\N	2026-01-05 12:00:00-03
155	1	21	2026-01-05	4	\N	2026-01-05 12:00:00-03
156	1	23	2026-01-05	0	\N	2026-01-05 12:00:00-03
157	1	24	2026-01-05	3	\N	2026-01-05 12:00:00-03
158	1	25	2026-01-05	0	\N	2026-01-05 12:00:00-03
159	1	26	2026-01-05	4	\N	2026-01-05 12:00:00-03
160	1	27	2026-01-05	0	\N	2026-01-05 12:00:00-03
161	1	28	2026-01-05	6	\N	2026-01-05 12:00:00-03
162	1	35	2026-01-05	4	\N	2026-01-05 12:00:00-03
163	1	36	2026-01-05	1	\N	2026-01-05 12:00:00-03
164	1	38	2026-01-05	0	\N	2026-01-05 12:00:00-03
165	1	39	2026-01-05	0	\N	2026-01-05 12:00:00-03
166	1	40	2026-01-05	0	\N	2026-01-05 12:00:00-03
167	1	44	2026-01-05	8	\N	2026-01-05 12:00:00-03
168	22	4	2026-01-05	0	\N	2026-01-05 12:00:00-03
169	22	13	2026-01-05	0	\N	2026-01-05 12:00:00-03
170	22	14	2026-01-05	0	\N	2026-01-05 12:00:00-03
171	22	15	2026-01-05	0	\N	2026-01-05 12:00:00-03
172	22	16	2026-01-05	0	\N	2026-01-05 12:00:00-03
173	22	17	2026-01-05	0	\N	2026-01-05 12:00:00-03
174	22	18	2026-01-05	0	\N	2026-01-05 12:00:00-03
175	22	19	2026-01-05	0	\N	2026-01-05 12:00:00-03
176	22	20	2026-01-05	0	\N	2026-01-05 12:00:00-03
177	22	21	2026-01-05	0	\N	2026-01-05 12:00:00-03
178	22	22	2026-01-05	0	\N	2026-01-05 12:00:00-03
179	22	24	2026-01-05	0	\N	2026-01-05 12:00:00-03
180	22	25	2026-01-05	0	\N	2026-01-05 12:00:00-03
181	22	26	2026-01-05	0	\N	2026-01-05 12:00:00-03
182	22	27	2026-01-05	0	\N	2026-01-05 12:00:00-03
183	22	28	2026-01-05	0	\N	2026-01-05 12:00:00-03
184	22	35	2026-01-05	0	\N	2026-01-05 12:00:00-03
185	22	36	2026-01-05	0	\N	2026-01-05 12:00:00-03
186	22	37	2026-01-05	0	\N	2026-01-05 12:00:00-03
187	22	44	2026-01-05	0	\N	2026-01-05 12:00:00-03
188	1	4	2026-01-08	0	\N	2026-01-08 12:00:00-03
189	1	13	2026-01-08	0	\N	2026-01-08 12:00:00-03
190	1	14	2026-01-08	0	\N	2026-01-08 12:00:00-03
191	1	15	2026-01-08	0	\N	2026-01-08 12:00:00-03
192	1	16	2026-01-08	0	\N	2026-01-08 12:00:00-03
193	1	17	2026-01-08	0	\N	2026-01-08 12:00:00-03
194	1	18	2026-01-08	0	\N	2026-01-08 12:00:00-03
195	1	19	2026-01-08	0	\N	2026-01-08 12:00:00-03
196	1	20	2026-01-08	0	\N	2026-01-08 12:00:00-03
197	1	21	2026-01-08	0	\N	2026-01-08 12:00:00-03
198	1	24	2026-01-08	0	\N	2026-01-08 12:00:00-03
199	1	26	2026-01-08	0	\N	2026-01-08 12:00:00-03
200	1	27	2026-01-08	0	\N	2026-01-08 12:00:00-03
201	1	28	2026-01-08	0	\N	2026-01-08 12:00:00-03
202	1	35	2026-01-08	0	\N	2026-01-08 12:00:00-03
203	1	37	2026-01-08	0	\N	2026-01-08 12:00:00-03
204	1	39	2026-01-08	0	\N	2026-01-08 12:00:00-03
205	1	44	2026-01-08	0	\N	2026-01-08 12:00:00-03
206	22	4	2026-01-08	0	\N	2026-01-08 12:00:00-03
207	22	13	2026-01-08	0	\N	2026-01-08 12:00:00-03
208	22	14	2026-01-08	0	\N	2026-01-08 12:00:00-03
209	22	15	2026-01-08	0	\N	2026-01-08 12:00:00-03
210	22	16	2026-01-08	0	\N	2026-01-08 12:00:00-03
211	22	18	2026-01-08	0	\N	2026-01-08 12:00:00-03
212	22	19	2026-01-08	0	\N	2026-01-08 12:00:00-03
213	22	20	2026-01-08	0	\N	2026-01-08 12:00:00-03
214	22	21	2026-01-08	0	\N	2026-01-08 12:00:00-03
215	22	22	2026-01-08	0	\N	2026-01-08 12:00:00-03
216	22	24	2026-01-08	0	\N	2026-01-08 12:00:00-03
217	22	26	2026-01-08	0	\N	2026-01-08 12:00:00-03
218	22	27	2026-01-08	0	\N	2026-01-08 12:00:00-03
219	22	28	2026-01-08	0	\N	2026-01-08 12:00:00-03
220	22	35	2026-01-08	0	\N	2026-01-08 12:00:00-03
221	22	36	2026-01-08	0	\N	2026-01-08 12:00:00-03
222	22	37	2026-01-08	0	\N	2026-01-08 12:00:00-03
223	22	44	2026-01-08	0	\N	2026-01-08 12:00:00-03
224	17	4	2026-01-12	5	\N	2026-01-12 12:00:00-03
225	17	13	2026-01-12	0	\N	2026-01-12 12:00:00-03
226	17	14	2026-01-12	0	\N	2026-01-12 12:00:00-03
227	17	15	2026-01-12	0	\N	2026-01-12 12:00:00-03
228	17	16	2026-01-12	0	\N	2026-01-12 12:00:00-03
229	17	17	2026-01-12	0	\N	2026-01-12 12:00:00-03
230	17	18	2026-01-12	0	\N	2026-01-12 12:00:00-03
231	17	19	2026-01-12	0	\N	2026-01-12 12:00:00-03
232	17	20	2026-01-12	0	\N	2026-01-12 12:00:00-03
233	17	21	2026-01-12	0	\N	2026-01-12 12:00:00-03
234	17	22	2026-01-12	0	\N	2026-01-12 12:00:00-03
235	17	23	2026-01-12	0	\N	2026-01-12 12:00:00-03
236	17	24	2026-01-12	0	\N	2026-01-12 12:00:00-03
237	17	25	2026-01-12	0	\N	2026-01-12 12:00:00-03
238	17	26	2026-01-12	0	\N	2026-01-12 12:00:00-03
239	17	27	2026-01-12	0	\N	2026-01-12 12:00:00-03
240	17	28	2026-01-12	0	\N	2026-01-12 12:00:00-03
241	17	35	2026-01-12	0	\N	2026-01-12 12:00:00-03
242	17	36	2026-01-12	0	\N	2026-01-12 12:00:00-03
243	17	37	2026-01-12	0	\N	2026-01-12 12:00:00-03
244	17	38	2026-01-12	0	\N	2026-01-12 12:00:00-03
245	17	39	2026-01-12	0	\N	2026-01-12 12:00:00-03
246	17	40	2026-01-12	0	\N	2026-01-12 12:00:00-03
247	17	41	2026-01-12	0	\N	2026-01-12 12:00:00-03
248	17	42	2026-01-12	0	\N	2026-01-12 12:00:00-03
249	17	44	2026-01-12	0	\N	2026-01-12 12:00:00-03
250	38	4	2026-01-12	0	\N	2026-01-12 12:00:00-03
251	38	13	2026-01-12	0	\N	2026-01-12 12:00:00-03
252	38	14	2026-01-12	0	\N	2026-01-12 12:00:00-03
253	38	15	2026-01-12	0	\N	2026-01-12 12:00:00-03
254	38	16	2026-01-12	0	\N	2026-01-12 12:00:00-03
255	38	17	2026-01-12	0	\N	2026-01-12 12:00:00-03
256	38	18	2026-01-12	0	\N	2026-01-12 12:00:00-03
257	38	19	2026-01-12	0	\N	2026-01-12 12:00:00-03
258	38	20	2026-01-12	0	\N	2026-01-12 12:00:00-03
259	38	21	2026-01-12	0	\N	2026-01-12 12:00:00-03
260	38	22	2026-01-12	0	\N	2026-01-12 12:00:00-03
261	38	23	2026-01-12	0	\N	2026-01-12 12:00:00-03
262	38	24	2026-01-12	0	\N	2026-01-12 12:00:00-03
263	38	25	2026-01-12	0	\N	2026-01-12 12:00:00-03
264	38	26	2026-01-12	0	\N	2026-01-12 12:00:00-03
265	38	27	2026-01-12	0	\N	2026-01-12 12:00:00-03
266	38	28	2026-01-12	0	\N	2026-01-12 12:00:00-03
267	38	35	2026-01-12	0	\N	2026-01-12 12:00:00-03
268	38	36	2026-01-12	0	\N	2026-01-12 12:00:00-03
269	38	37	2026-01-12	0	\N	2026-01-12 12:00:00-03
270	38	38	2026-01-12	0	\N	2026-01-12 12:00:00-03
271	38	39	2026-01-12	0	\N	2026-01-12 12:00:00-03
272	38	40	2026-01-12	0	\N	2026-01-12 12:00:00-03
273	38	41	2026-01-12	0	\N	2026-01-12 12:00:00-03
274	38	42	2026-01-12	0	\N	2026-01-12 12:00:00-03
275	38	44	2026-01-12	0	\N	2026-01-12 12:00:00-03
276	22	4	2026-01-12	30	\N	2026-01-12 12:00:00-03
277	22	13	2026-01-12	0	\N	2026-01-12 12:00:00-03
278	22	14	2026-01-12	0	\N	2026-01-12 12:00:00-03
279	22	15	2026-01-12	10	\N	2026-01-12 12:00:00-03
280	22	16	2026-01-12	0	\N	2026-01-12 12:00:00-03
281	22	17	2026-01-12	0	\N	2026-01-12 12:00:00-03
282	22	18	2026-01-12	0	\N	2026-01-12 12:00:00-03
283	22	19	2026-01-12	0	\N	2026-01-12 12:00:00-03
284	22	20	2026-01-12	2	\N	2026-01-12 12:00:00-03
285	22	21	2026-01-12	0	\N	2026-01-12 12:00:00-03
286	22	22	2026-01-12	0	\N	2026-01-12 12:00:00-03
287	22	24	2026-01-12	0	\N	2026-01-12 12:00:00-03
288	22	26	2026-01-12	0	\N	2026-01-12 12:00:00-03
289	22	27	2026-01-12	1	\N	2026-01-12 12:00:00-03
290	22	28	2026-01-12	0	\N	2026-01-12 12:00:00-03
291	22	35	2026-01-12	0	\N	2026-01-12 12:00:00-03
292	22	36	2026-01-12	0	\N	2026-01-12 12:00:00-03
293	22	37	2026-01-12	0	\N	2026-01-12 12:00:00-03
294	22	39	2026-01-12	0	\N	2026-01-12 12:00:00-03
295	22	44	2026-01-12	6	\N	2026-01-12 12:00:00-03
296	1	4	2026-01-12	0	\N	2026-01-12 12:00:00-03
297	1	13	2026-01-12	0	\N	2026-01-12 12:00:00-03
298	1	14	2026-01-12	0	\N	2026-01-12 12:00:00-03
299	1	15	2026-01-12	0	\N	2026-01-12 12:00:00-03
300	1	16	2026-01-12	0	\N	2026-01-12 12:00:00-03
301	1	17	2026-01-12	0	\N	2026-01-12 12:00:00-03
302	1	18	2026-01-12	0	\N	2026-01-12 12:00:00-03
303	1	19	2026-01-12	0	\N	2026-01-12 12:00:00-03
304	1	20	2026-01-12	0	\N	2026-01-12 12:00:00-03
305	1	21	2026-01-12	0	\N	2026-01-12 12:00:00-03
306	1	24	2026-01-12	0	\N	2026-01-12 12:00:00-03
307	1	26	2026-01-12	0	\N	2026-01-12 12:00:00-03
308	1	27	2026-01-12	0	\N	2026-01-12 12:00:00-03
309	1	28	2026-01-12	0	\N	2026-01-12 12:00:00-03
310	1	35	2026-01-12	0	\N	2026-01-12 12:00:00-03
311	1	36	2026-01-12	0	\N	2026-01-12 12:00:00-03
312	1	37	2026-01-12	0	\N	2026-01-12 12:00:00-03
313	1	39	2026-01-12	0	\N	2026-01-12 12:00:00-03
314	1	44	2026-01-12	0	\N	2026-01-12 12:00:00-03
315	17	4	2026-01-15	0	\N	2026-01-15 12:00:00-03
316	17	14	2026-01-15	0	\N	2026-01-15 12:00:00-03
317	17	15	2026-01-15	0	\N	2026-01-15 12:00:00-03
318	17	16	2026-01-15	0	\N	2026-01-15 12:00:00-03
319	17	18	2026-01-15	0	\N	2026-01-15 12:00:00-03
320	17	20	2026-01-15	0	\N	2026-01-15 12:00:00-03
321	17	22	2026-01-15	0	\N	2026-01-15 12:00:00-03
322	17	28	2026-01-15	0	\N	2026-01-15 12:00:00-03
323	17	35	2026-01-15	0	\N	2026-01-15 12:00:00-03
324	17	36	2026-01-15	0	\N	2026-01-15 12:00:00-03
325	17	37	2026-01-15	0	\N	2026-01-15 12:00:00-03
326	17	38	2026-01-15	0	\N	2026-01-15 12:00:00-03
327	17	40	2026-01-15	0	\N	2026-01-15 12:00:00-03
328	17	44	2026-01-15	10	\N	2026-01-15 12:00:00-03
329	1	4	2026-01-15	0	\N	2026-01-15 12:00:00-03
330	1	13	2026-01-15	0	\N	2026-01-15 12:00:00-03
331	1	14	2026-01-15	0	\N	2026-01-15 12:00:00-03
332	1	15	2026-01-15	0	\N	2026-01-15 12:00:00-03
333	1	16	2026-01-15	0	\N	2026-01-15 12:00:00-03
334	1	17	2026-01-15	0	\N	2026-01-15 12:00:00-03
335	1	18	2026-01-15	0	\N	2026-01-15 12:00:00-03
336	1	19	2026-01-15	0	\N	2026-01-15 12:00:00-03
337	1	20	2026-01-15	0	\N	2026-01-15 12:00:00-03
338	1	21	2026-01-15	0	\N	2026-01-15 12:00:00-03
339	1	24	2026-01-15	0	\N	2026-01-15 12:00:00-03
340	1	26	2026-01-15	0	\N	2026-01-15 12:00:00-03
341	1	27	2026-01-15	0	\N	2026-01-15 12:00:00-03
342	1	28	2026-01-15	0	\N	2026-01-15 12:00:00-03
343	1	35	2026-01-15	0	\N	2026-01-15 12:00:00-03
344	1	37	2026-01-15	0	\N	2026-01-15 12:00:00-03
345	1	38	2026-01-15	0	\N	2026-01-15 12:00:00-03
346	1	39	2026-01-15	0	\N	2026-01-15 12:00:00-03
347	1	44	2026-01-15	0	\N	2026-01-15 12:00:00-03
348	38	4	2026-01-15	0	\N	2026-01-15 12:00:00-03
349	38	13	2026-01-15	0	\N	2026-01-15 12:00:00-03
350	38	14	2026-01-15	0	\N	2026-01-15 12:00:00-03
351	38	15	2026-01-15	0	\N	2026-01-15 12:00:00-03
352	38	16	2026-01-15	0	\N	2026-01-15 12:00:00-03
353	38	17	2026-01-15	0	\N	2026-01-15 12:00:00-03
354	38	18	2026-01-15	0	\N	2026-01-15 12:00:00-03
355	38	19	2026-01-15	0	\N	2026-01-15 12:00:00-03
356	38	20	2026-01-15	0	\N	2026-01-15 12:00:00-03
357	38	21	2026-01-15	0	\N	2026-01-15 12:00:00-03
358	38	22	2026-01-15	0	\N	2026-01-15 12:00:00-03
359	38	23	2026-01-15	0	\N	2026-01-15 12:00:00-03
360	38	24	2026-01-15	0	\N	2026-01-15 12:00:00-03
361	38	25	2026-01-15	0	\N	2026-01-15 12:00:00-03
362	38	26	2026-01-15	0	\N	2026-01-15 12:00:00-03
363	38	27	2026-01-15	0	\N	2026-01-15 12:00:00-03
364	38	28	2026-01-15	0	\N	2026-01-15 12:00:00-03
365	38	34	2026-01-15	0	\N	2026-01-15 12:00:00-03
366	38	35	2026-01-15	0	\N	2026-01-15 12:00:00-03
367	38	36	2026-01-15	0	\N	2026-01-15 12:00:00-03
368	38	37	2026-01-15	0	\N	2026-01-15 12:00:00-03
369	38	38	2026-01-15	0	\N	2026-01-15 12:00:00-03
370	38	39	2026-01-15	0	\N	2026-01-15 12:00:00-03
371	38	40	2026-01-15	0	\N	2026-01-15 12:00:00-03
372	38	41	2026-01-15	0	\N	2026-01-15 12:00:00-03
373	38	42	2026-01-15	0	\N	2026-01-15 12:00:00-03
374	38	44	2026-01-15	0	\N	2026-01-15 12:00:00-03
375	22	4	2026-01-15	0	\N	2026-01-15 12:00:00-03
376	22	13	2026-01-15	0	\N	2026-01-15 12:00:00-03
377	22	14	2026-01-15	0	\N	2026-01-15 12:00:00-03
378	22	15	2026-01-15	0	\N	2026-01-15 12:00:00-03
379	22	16	2026-01-15	0	\N	2026-01-15 12:00:00-03
380	22	18	2026-01-15	0	\N	2026-01-15 12:00:00-03
381	22	19	2026-01-15	0	\N	2026-01-15 12:00:00-03
382	22	20	2026-01-15	0	\N	2026-01-15 12:00:00-03
383	22	21	2026-01-15	0	\N	2026-01-15 12:00:00-03
384	22	24	2026-01-15	0	\N	2026-01-15 12:00:00-03
385	22	26	2026-01-15	0	\N	2026-01-15 12:00:00-03
386	22	27	2026-01-15	0	\N	2026-01-15 12:00:00-03
387	22	28	2026-01-15	0	\N	2026-01-15 12:00:00-03
388	22	35	2026-01-15	0	\N	2026-01-15 12:00:00-03
389	22	36	2026-01-15	0	\N	2026-01-15 12:00:00-03
390	22	37	2026-01-15	0	\N	2026-01-15 12:00:00-03
391	22	39	2026-01-15	0	\N	2026-01-15 12:00:00-03
392	22	40	2026-01-15	0	\N	2026-01-15 12:00:00-03
393	22	41	2026-01-15	0	\N	2026-01-15 12:00:00-03
394	22	42	2026-01-15	0	\N	2026-01-15 12:00:00-03
395	22	44	2026-01-15	0	\N	2026-01-15 12:00:00-03
396	38	4	2026-01-19	0	\N	2026-01-19 12:00:00-03
397	38	13	2026-01-19	0	\N	2026-01-19 12:00:00-03
398	38	14	2026-01-19	0	\N	2026-01-19 12:00:00-03
399	38	15	2026-01-19	0	\N	2026-01-19 12:00:00-03
400	38	16	2026-01-19	0	\N	2026-01-19 12:00:00-03
401	38	17	2026-01-19	0	\N	2026-01-19 12:00:00-03
402	38	18	2026-01-19	0	\N	2026-01-19 12:00:00-03
403	38	19	2026-01-19	0	\N	2026-01-19 12:00:00-03
404	38	20	2026-01-19	0	\N	2026-01-19 12:00:00-03
405	38	21	2026-01-19	0	\N	2026-01-19 12:00:00-03
406	38	22	2026-01-19	0	\N	2026-01-19 12:00:00-03
407	38	24	2026-01-19	0	\N	2026-01-19 12:00:00-03
408	38	26	2026-01-19	0	\N	2026-01-19 12:00:00-03
409	38	27	2026-01-19	0	\N	2026-01-19 12:00:00-03
410	38	28	2026-01-19	0	\N	2026-01-19 12:00:00-03
411	38	34	2026-01-19	0	\N	2026-01-19 12:00:00-03
412	38	36	2026-01-19	0	\N	2026-01-19 12:00:00-03
413	38	37	2026-01-19	0	\N	2026-01-19 12:00:00-03
414	38	38	2026-01-19	0	\N	2026-01-19 12:00:00-03
415	38	39	2026-01-19	0	\N	2026-01-19 12:00:00-03
416	38	40	2026-01-19	0	\N	2026-01-19 12:00:00-03
417	38	41	2026-01-19	0	\N	2026-01-19 12:00:00-03
418	38	44	2026-01-19	0	\N	2026-01-19 12:00:00-03
419	17	4	2026-01-19	0	\N	2026-01-19 12:00:00-03
420	17	13	2026-01-19	0	\N	2026-01-19 12:00:00-03
421	17	14	2026-01-19	0	\N	2026-01-19 12:00:00-03
422	17	15	2026-01-19	0	\N	2026-01-19 12:00:00-03
423	17	16	2026-01-19	0	\N	2026-01-19 12:00:00-03
424	17	17	2026-01-19	0	\N	2026-01-19 12:00:00-03
425	17	18	2026-01-19	0	\N	2026-01-19 12:00:00-03
426	17	19	2026-01-19	0	\N	2026-01-19 12:00:00-03
427	17	20	2026-01-19	0	\N	2026-01-19 12:00:00-03
428	17	21	2026-01-19	0	\N	2026-01-19 12:00:00-03
429	17	22	2026-01-19	0	\N	2026-01-19 12:00:00-03
430	17	23	2026-01-19	0	\N	2026-01-19 12:00:00-03
431	17	24	2026-01-19	0	\N	2026-01-19 12:00:00-03
432	17	25	2026-01-19	0	\N	2026-01-19 12:00:00-03
433	17	26	2026-01-19	0	\N	2026-01-19 12:00:00-03
434	17	27	2026-01-19	0	\N	2026-01-19 12:00:00-03
435	17	28	2026-01-19	0	\N	2026-01-19 12:00:00-03
436	17	35	2026-01-19	0	\N	2026-01-19 12:00:00-03
437	17	36	2026-01-19	0	\N	2026-01-19 12:00:00-03
438	17	37	2026-01-19	0	\N	2026-01-19 12:00:00-03
439	17	38	2026-01-19	0	\N	2026-01-19 12:00:00-03
440	17	39	2026-01-19	0	\N	2026-01-19 12:00:00-03
441	17	40	2026-01-19	0	\N	2026-01-19 12:00:00-03
442	17	41	2026-01-19	0	\N	2026-01-19 12:00:00-03
443	17	42	2026-01-19	0	\N	2026-01-19 12:00:00-03
444	17	44	2026-01-19	0	\N	2026-01-19 12:00:00-03
445	1	4	2026-01-21	0	\N	2026-01-21 12:00:00-03
446	1	13	2026-01-21	0	\N	2026-01-21 12:00:00-03
447	1	14	2026-01-21	0	\N	2026-01-21 12:00:00-03
448	1	15	2026-01-21	0	\N	2026-01-21 12:00:00-03
449	1	16	2026-01-21	0	\N	2026-01-21 12:00:00-03
450	1	18	2026-01-21	0	\N	2026-01-21 12:00:00-03
451	1	19	2026-01-21	0	\N	2026-01-21 12:00:00-03
452	1	20	2026-01-21	0	\N	2026-01-21 12:00:00-03
453	1	21	2026-01-21	0	\N	2026-01-21 12:00:00-03
454	1	24	2026-01-21	0	\N	2026-01-21 12:00:00-03
455	1	26	2026-01-21	0	\N	2026-01-21 12:00:00-03
456	1	27	2026-01-21	0	\N	2026-01-21 12:00:00-03
457	1	28	2026-01-21	0	\N	2026-01-21 12:00:00-03
458	1	35	2026-01-21	0	\N	2026-01-21 12:00:00-03
459	1	36	2026-01-21	0	\N	2026-01-21 12:00:00-03
460	1	37	2026-01-21	0	\N	2026-01-21 12:00:00-03
461	1	38	2026-01-21	0	\N	2026-01-21 12:00:00-03
462	1	39	2026-01-21	0	\N	2026-01-21 12:00:00-03
463	1	42	2026-01-21	0	\N	2026-01-21 12:00:00-03
464	1	44	2026-01-21	0	\N	2026-01-21 12:00:00-03
465	1	17	2026-01-21	0	\N	2026-01-21 12:00:00-03
466	17	4	2026-01-22	0	\N	2026-01-22 12:00:00-03
467	17	14	2026-01-22	0	\N	2026-01-22 12:00:00-03
468	17	15	2026-01-22	0	\N	2026-01-22 12:00:00-03
469	17	16	2026-01-22	0	\N	2026-01-22 12:00:00-03
470	17	17	2026-01-22	0	\N	2026-01-22 12:00:00-03
471	17	18	2026-01-22	0	\N	2026-01-22 12:00:00-03
472	17	19	2026-01-22	0	\N	2026-01-22 12:00:00-03
473	17	20	2026-01-22	0	\N	2026-01-22 12:00:00-03
474	17	21	2026-01-22	0	\N	2026-01-22 12:00:00-03
475	17	22	2026-01-22	0	\N	2026-01-22 12:00:00-03
476	17	23	2026-01-22	0	\N	2026-01-22 12:00:00-03
477	17	24	2026-01-22	0	\N	2026-01-22 12:00:00-03
478	17	25	2026-01-22	0	\N	2026-01-22 12:00:00-03
479	17	26	2026-01-22	0	\N	2026-01-22 12:00:00-03
480	17	27	2026-01-22	0	\N	2026-01-22 12:00:00-03
481	17	28	2026-01-22	0	\N	2026-01-22 12:00:00-03
482	17	35	2026-01-22	0	\N	2026-01-22 12:00:00-03
483	17	36	2026-01-22	0	\N	2026-01-22 12:00:00-03
484	17	37	2026-01-22	0	\N	2026-01-22 12:00:00-03
485	17	38	2026-01-22	0	\N	2026-01-22 12:00:00-03
486	17	39	2026-01-22	0	\N	2026-01-22 12:00:00-03
487	17	40	2026-01-22	0	\N	2026-01-22 12:00:00-03
488	17	41	2026-01-22	0	\N	2026-01-22 12:00:00-03
489	17	42	2026-01-22	0	\N	2026-01-22 12:00:00-03
490	17	44	2026-01-22	0	\N	2026-01-22 12:00:00-03
491	38	4	2026-01-22	0	\N	2026-01-22 12:00:00-03
492	38	13	2026-01-22	0	\N	2026-01-22 12:00:00-03
493	38	14	2026-01-22	0	\N	2026-01-22 12:00:00-03
494	38	15	2026-01-22	0	\N	2026-01-22 12:00:00-03
495	38	16	2026-01-22	0	\N	2026-01-22 12:00:00-03
496	38	17	2026-01-22	0	\N	2026-01-22 12:00:00-03
497	38	18	2026-01-22	0	\N	2026-01-22 12:00:00-03
498	38	19	2026-01-22	0	\N	2026-01-22 12:00:00-03
499	38	20	2026-01-22	0	\N	2026-01-22 12:00:00-03
500	38	21	2026-01-22	0	\N	2026-01-22 12:00:00-03
501	38	22	2026-01-22	0	\N	2026-01-22 12:00:00-03
502	38	23	2026-01-22	0	\N	2026-01-22 12:00:00-03
503	38	24	2026-01-22	0	\N	2026-01-22 12:00:00-03
504	38	25	2026-01-22	0	\N	2026-01-22 12:00:00-03
505	38	26	2026-01-22	0	\N	2026-01-22 12:00:00-03
506	38	27	2026-01-22	0	\N	2026-01-22 12:00:00-03
507	38	28	2026-01-22	0	\N	2026-01-22 12:00:00-03
508	38	34	2026-01-22	0	\N	2026-01-22 12:00:00-03
509	38	35	2026-01-22	0	\N	2026-01-22 12:00:00-03
510	38	36	2026-01-22	0	\N	2026-01-22 12:00:00-03
511	38	37	2026-01-22	0	\N	2026-01-22 12:00:00-03
512	38	38	2026-01-22	0	\N	2026-01-22 12:00:00-03
513	38	39	2026-01-22	0	\N	2026-01-22 12:00:00-03
514	38	40	2026-01-22	0	\N	2026-01-22 12:00:00-03
515	38	41	2026-01-22	0	\N	2026-01-22 12:00:00-03
516	38	44	2026-01-22	0	\N	2026-01-22 12:00:00-03
517	22	4	2026-01-22	0	\N	2026-01-22 12:00:00-03
518	22	13	2026-01-22	0	\N	2026-01-22 12:00:00-03
519	22	14	2026-01-22	0	\N	2026-01-22 12:00:00-03
520	22	15	2026-01-22	0	\N	2026-01-22 12:00:00-03
521	22	16	2026-01-22	0	\N	2026-01-22 12:00:00-03
522	22	17	2026-01-22	0	\N	2026-01-22 12:00:00-03
523	22	18	2026-01-22	0	\N	2026-01-22 12:00:00-03
524	22	19	2026-01-22	0	\N	2026-01-22 12:00:00-03
525	22	20	2026-01-22	0	\N	2026-01-22 12:00:00-03
526	22	21	2026-01-22	0	\N	2026-01-22 12:00:00-03
527	22	22	2026-01-22	0	\N	2026-01-22 12:00:00-03
528	22	23	2026-01-22	0	\N	2026-01-22 12:00:00-03
529	22	24	2026-01-22	0	\N	2026-01-22 12:00:00-03
530	22	26	2026-01-22	0	\N	2026-01-22 12:00:00-03
531	22	27	2026-01-22	0	\N	2026-01-22 12:00:00-03
532	22	28	2026-01-22	0	\N	2026-01-22 12:00:00-03
533	22	35	2026-01-22	0	\N	2026-01-22 12:00:00-03
534	22	36	2026-01-22	0	\N	2026-01-22 12:00:00-03
535	22	39	2026-01-22	0	\N	2026-01-22 12:00:00-03
536	22	40	2026-01-22	0	\N	2026-01-22 12:00:00-03
537	22	41	2026-01-22	0	\N	2026-01-22 12:00:00-03
538	22	42	2026-01-22	0	\N	2026-01-22 12:00:00-03
539	22	44	2026-01-22	0	\N	2026-01-22 12:00:00-03
540	1	4	2026-01-22	0	\N	2026-01-22 12:00:00-03
541	1	13	2026-01-22	0	\N	2026-01-22 12:00:00-03
542	1	14	2026-01-22	0	\N	2026-01-22 12:00:00-03
543	1	15	2026-01-22	0	\N	2026-01-22 12:00:00-03
544	1	16	2026-01-22	0	\N	2026-01-22 12:00:00-03
545	1	17	2026-01-22	0	\N	2026-01-22 12:00:00-03
546	1	18	2026-01-22	0	\N	2026-01-22 12:00:00-03
547	1	19	2026-01-22	0	\N	2026-01-22 12:00:00-03
548	1	20	2026-01-22	0	\N	2026-01-22 12:00:00-03
549	1	21	2026-01-22	0	\N	2026-01-22 12:00:00-03
550	1	24	2026-01-22	0	\N	2026-01-22 12:00:00-03
551	1	26	2026-01-22	0	\N	2026-01-22 12:00:00-03
552	1	27	2026-01-22	0	\N	2026-01-22 12:00:00-03
553	1	28	2026-01-22	0	\N	2026-01-22 12:00:00-03
554	1	35	2026-01-22	0	\N	2026-01-22 12:00:00-03
555	1	36	2026-01-22	0	\N	2026-01-22 12:00:00-03
556	1	37	2026-01-22	0	\N	2026-01-22 12:00:00-03
557	1	44	2026-01-22	0	\N	2026-01-22 12:00:00-03
558	38	4	2026-01-26	0	\N	2026-01-26 12:00:00-03
559	38	13	2026-01-26	0	\N	2026-01-26 12:00:00-03
560	38	14	2026-01-26	0	\N	2026-01-26 12:00:00-03
561	38	15	2026-01-26	0	\N	2026-01-26 12:00:00-03
562	38	16	2026-01-26	0	\N	2026-01-26 12:00:00-03
563	38	17	2026-01-26	0	\N	2026-01-26 12:00:00-03
564	38	18	2026-01-26	0	\N	2026-01-26 12:00:00-03
565	38	19	2026-01-26	0	\N	2026-01-26 12:00:00-03
566	38	20	2026-01-26	0	\N	2026-01-26 12:00:00-03
567	38	21	2026-01-26	0	\N	2026-01-26 12:00:00-03
568	38	22	2026-01-26	0	\N	2026-01-26 12:00:00-03
569	38	23	2026-01-26	0	\N	2026-01-26 12:00:00-03
570	38	25	2026-01-26	0	\N	2026-01-26 12:00:00-03
571	38	26	2026-01-26	0	\N	2026-01-26 12:00:00-03
572	38	27	2026-01-26	0	\N	2026-01-26 12:00:00-03
573	38	28	2026-01-26	0	\N	2026-01-26 12:00:00-03
574	38	35	2026-01-26	0	\N	2026-01-26 12:00:00-03
575	38	37	2026-01-26	0	\N	2026-01-26 12:00:00-03
576	38	38	2026-01-26	0	\N	2026-01-26 12:00:00-03
577	38	39	2026-01-26	0	\N	2026-01-26 12:00:00-03
578	38	40	2026-01-26	0	\N	2026-01-26 12:00:00-03
579	38	41	2026-01-26	0	\N	2026-01-26 12:00:00-03
580	38	44	2026-01-26	0	\N	2026-01-26 12:00:00-03
581	17	4	2026-01-26	0	\N	2026-01-26 12:00:00-03
582	17	13	2026-01-26	0	\N	2026-01-26 12:00:00-03
583	17	14	2026-01-26	0	\N	2026-01-26 12:00:00-03
584	17	15	2026-01-26	0	\N	2026-01-26 12:00:00-03
585	17	16	2026-01-26	0	\N	2026-01-26 12:00:00-03
586	17	17	2026-01-26	0	\N	2026-01-26 12:00:00-03
587	17	18	2026-01-26	0	\N	2026-01-26 12:00:00-03
588	17	19	2026-01-26	0	\N	2026-01-26 12:00:00-03
589	17	20	2026-01-26	0	\N	2026-01-26 12:00:00-03
590	17	21	2026-01-26	0	\N	2026-01-26 12:00:00-03
591	17	22	2026-01-26	0	\N	2026-01-26 12:00:00-03
592	17	23	2026-01-26	0	\N	2026-01-26 12:00:00-03
593	17	24	2026-01-26	0	\N	2026-01-26 12:00:00-03
594	17	25	2026-01-26	0	\N	2026-01-26 12:00:00-03
595	17	26	2026-01-26	0	\N	2026-01-26 12:00:00-03
596	17	27	2026-01-26	0	\N	2026-01-26 12:00:00-03
597	17	28	2026-01-26	0	\N	2026-01-26 12:00:00-03
598	17	35	2026-01-26	0	\N	2026-01-26 12:00:00-03
599	17	36	2026-01-26	0	\N	2026-01-26 12:00:00-03
600	17	37	2026-01-26	0	\N	2026-01-26 12:00:00-03
601	17	38	2026-01-26	0	\N	2026-01-26 12:00:00-03
602	17	39	2026-01-26	0	\N	2026-01-26 12:00:00-03
603	17	40	2026-01-26	0	\N	2026-01-26 12:00:00-03
604	17	41	2026-01-26	0	\N	2026-01-26 12:00:00-03
605	17	42	2026-01-26	0	\N	2026-01-26 12:00:00-03
606	17	44	2026-01-26	0	\N	2026-01-26 12:00:00-03
607	38	4	2026-01-29	0	\N	2026-01-29 12:00:00-03
608	38	13	2026-01-29	0	\N	2026-01-29 12:00:00-03
609	38	14	2026-01-29	0	\N	2026-01-29 12:00:00-03
610	38	15	2026-01-29	0	\N	2026-01-29 12:00:00-03
611	38	16	2026-01-29	0	\N	2026-01-29 12:00:00-03
612	38	17	2026-01-29	0	\N	2026-01-29 12:00:00-03
613	38	18	2026-01-29	0	\N	2026-01-29 12:00:00-03
614	38	19	2026-01-29	0	\N	2026-01-29 12:00:00-03
615	38	20	2026-01-29	0	\N	2026-01-29 12:00:00-03
616	38	21	2026-01-29	0	\N	2026-01-29 12:00:00-03
617	38	22	2026-01-29	0	\N	2026-01-29 12:00:00-03
618	38	23	2026-01-29	0	\N	2026-01-29 12:00:00-03
619	38	24	2026-01-29	0	\N	2026-01-29 12:00:00-03
620	38	25	2026-01-29	0	\N	2026-01-29 12:00:00-03
621	38	26	2026-01-29	0	\N	2026-01-29 12:00:00-03
622	38	27	2026-01-29	0	\N	2026-01-29 12:00:00-03
623	38	28	2026-01-29	0	\N	2026-01-29 12:00:00-03
624	38	34	2026-01-29	0	\N	2026-01-29 12:00:00-03
625	38	35	2026-01-29	0	\N	2026-01-29 12:00:00-03
626	38	36	2026-01-29	0	\N	2026-01-29 12:00:00-03
627	38	37	2026-01-29	0	\N	2026-01-29 12:00:00-03
628	38	38	2026-01-29	0	\N	2026-01-29 12:00:00-03
629	38	39	2026-01-29	0	\N	2026-01-29 12:00:00-03
630	38	40	2026-01-29	0	\N	2026-01-29 12:00:00-03
631	38	41	2026-01-29	0	\N	2026-01-29 12:00:00-03
632	38	42	2026-01-29	0	\N	2026-01-29 12:00:00-03
633	38	44	2026-01-29	0	\N	2026-01-29 12:00:00-03
634	17	4	2026-01-29	0	\N	2026-01-29 12:00:00-03
635	17	13	2026-01-29	0	\N	2026-01-29 12:00:00-03
636	17	15	2026-01-29	0	\N	2026-01-29 12:00:00-03
637	17	16	2026-01-29	0	\N	2026-01-29 12:00:00-03
638	17	19	2026-01-29	0	\N	2026-01-29 12:00:00-03
639	17	20	2026-01-29	0	\N	2026-01-29 12:00:00-03
640	17	21	2026-01-29	0	\N	2026-01-29 12:00:00-03
641	17	22	2026-01-29	0	\N	2026-01-29 12:00:00-03
642	17	23	2026-01-29	0	\N	2026-01-29 12:00:00-03
643	17	24	2026-01-29	0	\N	2026-01-29 12:00:00-03
644	17	26	2026-01-29	0	\N	2026-01-29 12:00:00-03
645	17	27	2026-01-29	0	\N	2026-01-29 12:00:00-03
646	17	28	2026-01-29	0	\N	2026-01-29 12:00:00-03
647	17	29	2026-01-29	0	\N	2026-01-29 12:00:00-03
648	17	35	2026-01-29	0	\N	2026-01-29 12:00:00-03
649	17	36	2026-01-29	0	\N	2026-01-29 12:00:00-03
650	17	37	2026-01-29	0	\N	2026-01-29 12:00:00-03
651	17	38	2026-01-29	0	\N	2026-01-29 12:00:00-03
652	17	39	2026-01-29	0	\N	2026-01-29 12:00:00-03
653	17	40	2026-01-29	0	\N	2026-01-29 12:00:00-03
654	17	41	2026-01-29	0	\N	2026-01-29 12:00:00-03
655	17	42	2026-01-29	0	\N	2026-01-29 12:00:00-03
656	17	44	2026-01-29	0	\N	2026-01-29 12:00:00-03
657	1	4	2026-01-29	0	\N	2026-01-29 12:00:00-03
658	1	13	2026-01-29	0	\N	2026-01-29 12:00:00-03
659	1	14	2026-01-29	0	\N	2026-01-29 12:00:00-03
660	1	15	2026-01-29	0	\N	2026-01-29 12:00:00-03
661	1	16	2026-01-29	0	\N	2026-01-29 12:00:00-03
662	1	17	2026-01-29	0	\N	2026-01-29 12:00:00-03
663	1	18	2026-01-29	0	\N	2026-01-29 12:00:00-03
664	1	19	2026-01-29	0	\N	2026-01-29 12:00:00-03
665	1	20	2026-01-29	0	\N	2026-01-29 12:00:00-03
666	1	21	2026-01-29	0	\N	2026-01-29 12:00:00-03
667	1	22	2026-01-29	0	\N	2026-01-29 12:00:00-03
668	1	23	2026-01-29	0	\N	2026-01-29 12:00:00-03
669	1	24	2026-01-29	0	\N	2026-01-29 12:00:00-03
670	1	26	2026-01-29	0	\N	2026-01-29 12:00:00-03
671	1	27	2026-01-29	0	\N	2026-01-29 12:00:00-03
672	1	28	2026-01-29	0	\N	2026-01-29 12:00:00-03
673	1	35	2026-01-29	0	\N	2026-01-29 12:00:00-03
674	1	36	2026-01-29	0	\N	2026-01-29 12:00:00-03
675	1	39	2026-01-29	0	\N	2026-01-29 12:00:00-03
676	1	44	2026-01-29	0	\N	2026-01-29 12:00:00-03
677	22	4	2026-01-29	0	\N	2026-01-29 12:00:00-03
678	22	13	2026-01-29	0	\N	2026-01-29 12:00:00-03
679	22	14	2026-01-29	0	\N	2026-01-29 12:00:00-03
680	22	15	2026-01-29	0	\N	2026-01-29 12:00:00-03
681	22	16	2026-01-29	0	\N	2026-01-29 12:00:00-03
682	22	18	2026-01-29	0	\N	2026-01-29 12:00:00-03
683	22	19	2026-01-29	0	\N	2026-01-29 12:00:00-03
684	22	20	2026-01-29	0	\N	2026-01-29 12:00:00-03
685	22	21	2026-01-29	0	\N	2026-01-29 12:00:00-03
686	22	22	2026-01-29	0	\N	2026-01-29 12:00:00-03
687	22	23	2026-01-29	0	\N	2026-01-29 12:00:00-03
688	22	24	2026-01-29	0	\N	2026-01-29 12:00:00-03
689	22	26	2026-01-29	0	\N	2026-01-29 12:00:00-03
690	22	28	2026-01-29	0	\N	2026-01-29 12:00:00-03
691	22	29	2026-01-29	0	\N	2026-01-29 12:00:00-03
692	22	30	2026-01-29	0	\N	2026-01-29 12:00:00-03
693	22	35	2026-01-29	0	\N	2026-01-29 12:00:00-03
694	22	39	2026-01-29	0	\N	2026-01-29 12:00:00-03
695	22	40	2026-01-29	0	\N	2026-01-29 12:00:00-03
696	22	44	2026-01-29	0	\N	2026-01-29 12:00:00-03
697	38	4	2026-02-02	0	\N	2026-02-02 12:00:00-03
698	38	13	2026-02-02	0	\N	2026-02-02 12:00:00-03
699	38	14	2026-02-02	0	\N	2026-02-02 12:00:00-03
700	38	15	2026-02-02	0	\N	2026-02-02 12:00:00-03
701	38	16	2026-02-02	0	\N	2026-02-02 12:00:00-03
702	38	17	2026-02-02	0	\N	2026-02-02 12:00:00-03
703	38	18	2026-02-02	0	\N	2026-02-02 12:00:00-03
704	38	19	2026-02-02	0	\N	2026-02-02 12:00:00-03
705	38	20	2026-02-02	0	\N	2026-02-02 12:00:00-03
706	38	21	2026-02-02	0	\N	2026-02-02 12:00:00-03
707	38	22	2026-02-02	0	\N	2026-02-02 12:00:00-03
708	38	23	2026-02-02	0	\N	2026-02-02 12:00:00-03
709	38	24	2026-02-02	0	\N	2026-02-02 12:00:00-03
710	38	25	2026-02-02	0	\N	2026-02-02 12:00:00-03
711	38	26	2026-02-02	0	\N	2026-02-02 12:00:00-03
712	38	27	2026-02-02	0	\N	2026-02-02 12:00:00-03
713	38	28	2026-02-02	0	\N	2026-02-02 12:00:00-03
714	38	34	2026-02-02	0	\N	2026-02-02 12:00:00-03
715	38	35	2026-02-02	0	\N	2026-02-02 12:00:00-03
716	38	36	2026-02-02	0	\N	2026-02-02 12:00:00-03
717	38	37	2026-02-02	0	\N	2026-02-02 12:00:00-03
718	38	38	2026-02-02	0	\N	2026-02-02 12:00:00-03
719	38	39	2026-02-02	0	\N	2026-02-02 12:00:00-03
720	38	40	2026-02-02	0	\N	2026-02-02 12:00:00-03
721	38	41	2026-02-02	0	\N	2026-02-02 12:00:00-03
722	38	44	2026-02-02	1	\N	2026-02-02 12:00:00-03
723	17	4	2026-02-02	0	\N	2026-02-02 12:00:00-03
724	17	13	2026-02-02	0	\N	2026-02-02 12:00:00-03
725	17	14	2026-02-02	0	\N	2026-02-02 12:00:00-03
726	17	15	2026-02-02	0	\N	2026-02-02 12:00:00-03
727	17	16	2026-02-02	0	\N	2026-02-02 12:00:00-03
728	17	17	2026-02-02	0	\N	2026-02-02 12:00:00-03
729	17	18	2026-02-02	0	\N	2026-02-02 12:00:00-03
730	17	19	2026-02-02	0	\N	2026-02-02 12:00:00-03
731	17	20	2026-02-02	0	\N	2026-02-02 12:00:00-03
732	17	21	2026-02-02	0	\N	2026-02-02 12:00:00-03
733	17	22	2026-02-02	0	\N	2026-02-02 12:00:00-03
734	17	23	2026-02-02	0	\N	2026-02-02 12:00:00-03
735	17	24	2026-02-02	0	\N	2026-02-02 12:00:00-03
736	17	25	2026-02-02	0	\N	2026-02-02 12:00:00-03
737	17	26	2026-02-02	0	\N	2026-02-02 12:00:00-03
738	17	27	2026-02-02	0	\N	2026-02-02 12:00:00-03
739	17	28	2026-02-02	0	\N	2026-02-02 12:00:00-03
740	17	29	2026-02-02	0	\N	2026-02-02 12:00:00-03
741	17	30	2026-02-02	0	\N	2026-02-02 12:00:00-03
742	17	35	2026-02-02	0	\N	2026-02-02 12:00:00-03
743	17	36	2026-02-02	0	\N	2026-02-02 12:00:00-03
744	17	37	2026-02-02	0	\N	2026-02-02 12:00:00-03
745	17	38	2026-02-02	0	\N	2026-02-02 12:00:00-03
746	17	39	2026-02-02	0	\N	2026-02-02 12:00:00-03
747	17	40	2026-02-02	0	\N	2026-02-02 12:00:00-03
748	17	41	2026-02-02	0	\N	2026-02-02 12:00:00-03
749	17	42	2026-02-02	0	\N	2026-02-02 12:00:00-03
750	17	44	2026-02-02	0	\N	2026-02-02 12:00:00-03
751	22	4	2026-02-04	0	\N	2026-02-04 12:00:00-03
752	22	13	2026-02-04	0	\N	2026-02-04 12:00:00-03
753	22	14	2026-02-04	0	\N	2026-02-04 12:00:00-03
754	22	15	2026-02-04	0	\N	2026-02-04 12:00:00-03
755	22	16	2026-02-04	0	\N	2026-02-04 12:00:00-03
756	22	18	2026-02-04	0	\N	2026-02-04 12:00:00-03
757	22	19	2026-02-04	0	\N	2026-02-04 12:00:00-03
758	22	20	2026-02-04	0	\N	2026-02-04 12:00:00-03
759	22	21	2026-02-04	0	\N	2026-02-04 12:00:00-03
760	22	22	2026-02-04	0	\N	2026-02-04 12:00:00-03
761	22	23	2026-02-04	0	\N	2026-02-04 12:00:00-03
762	22	24	2026-02-04	0	\N	2026-02-04 12:00:00-03
763	22	26	2026-02-04	0	\N	2026-02-04 12:00:00-03
764	22	28	2026-02-04	0	\N	2026-02-04 12:00:00-03
765	22	29	2026-02-04	0	\N	2026-02-04 12:00:00-03
766	22	30	2026-02-04	0	\N	2026-02-04 12:00:00-03
767	22	35	2026-02-04	0	\N	2026-02-04 12:00:00-03
768	22	36	2026-02-04	0	\N	2026-02-04 12:00:00-03
769	22	39	2026-02-04	0	\N	2026-02-04 12:00:00-03
770	22	44	2026-02-04	0	\N	2026-02-04 12:00:00-03
771	1	4	2026-02-04	0	\N	2026-02-04 12:00:00-03
772	1	13	2026-02-04	0	\N	2026-02-04 12:00:00-03
773	1	14	2026-02-04	0	\N	2026-02-04 12:00:00-03
774	1	15	2026-02-04	0	\N	2026-02-04 12:00:00-03
775	1	16	2026-02-04	0	\N	2026-02-04 12:00:00-03
776	1	18	2026-02-04	0	\N	2026-02-04 12:00:00-03
777	1	19	2026-02-04	0	\N	2026-02-04 12:00:00-03
778	1	20	2026-02-04	0	\N	2026-02-04 12:00:00-03
779	1	21	2026-02-04	0	\N	2026-02-04 12:00:00-03
780	1	22	2026-02-04	0	\N	2026-02-04 12:00:00-03
781	1	24	2026-02-04	0	\N	2026-02-04 12:00:00-03
782	1	26	2026-02-04	0	\N	2026-02-04 12:00:00-03
783	1	27	2026-02-04	0	\N	2026-02-04 12:00:00-03
784	1	28	2026-02-04	0	\N	2026-02-04 12:00:00-03
785	1	35	2026-02-04	0	\N	2026-02-04 12:00:00-03
786	1	36	2026-02-04	0	\N	2026-02-04 12:00:00-03
787	1	39	2026-02-04	0	\N	2026-02-04 12:00:00-03
788	1	44	2026-02-04	0	\N	2026-02-04 12:00:00-03
789	38	4	2026-02-05	0	\N	2026-02-05 12:00:00-03
790	38	13	2026-02-05	1	\N	2026-02-05 12:00:00-03
791	38	14	2026-02-05	0	\N	2026-02-05 12:00:00-03
792	38	15	2026-02-05	8	\N	2026-02-05 12:00:00-03
793	38	16	2026-02-05	0	\N	2026-02-05 12:00:00-03
794	38	17	2026-02-05	0	\N	2026-02-05 12:00:00-03
795	38	18	2026-02-05	0	\N	2026-02-05 12:00:00-03
796	38	19	2026-02-05	8	\N	2026-02-05 12:00:00-03
797	38	20	2026-02-05	0	\N	2026-02-05 12:00:00-03
798	38	21	2026-02-05	0	\N	2026-02-05 12:00:00-03
799	38	22	2026-02-05	2	\N	2026-02-05 12:00:00-03
800	38	23	2026-02-05	0	\N	2026-02-05 12:00:00-03
801	38	24	2026-02-05	2	\N	2026-02-05 12:00:00-03
802	38	25	2026-02-05	0	\N	2026-02-05 12:00:00-03
803	38	26	2026-02-05	3	\N	2026-02-05 12:00:00-03
804	38	27	2026-02-05	0	\N	2026-02-05 12:00:00-03
805	38	28	2026-02-05	0	\N	2026-02-05 12:00:00-03
806	38	30	2026-02-05	0	\N	2026-02-05 12:00:00-03
807	38	34	2026-02-05	0	\N	2026-02-05 12:00:00-03
808	38	35	2026-02-05	0	\N	2026-02-05 12:00:00-03
809	38	36	2026-02-05	0	\N	2026-02-05 12:00:00-03
810	38	37	2026-02-05	0	\N	2026-02-05 12:00:00-03
811	38	38	2026-02-05	0	\N	2026-02-05 12:00:00-03
812	38	39	2026-02-05	0	\N	2026-02-05 12:00:00-03
813	38	40	2026-02-05	0	\N	2026-02-05 12:00:00-03
814	38	41	2026-02-05	0	\N	2026-02-05 12:00:00-03
815	38	44	2026-02-05	5	\N	2026-02-05 12:00:00-03
816	17	4	2026-02-05	0	\N	2026-02-05 12:00:00-03
817	17	13	2026-02-05	0	\N	2026-02-05 12:00:00-03
818	17	14	2026-02-05	0	\N	2026-02-05 12:00:00-03
819	17	15	2026-02-05	0	\N	2026-02-05 12:00:00-03
820	17	16	2026-02-05	0	\N	2026-02-05 12:00:00-03
821	17	17	2026-02-05	0	\N	2026-02-05 12:00:00-03
822	17	18	2026-02-05	0	\N	2026-02-05 12:00:00-03
823	17	19	2026-02-05	0	\N	2026-02-05 12:00:00-03
824	17	20	2026-02-05	0	\N	2026-02-05 12:00:00-03
825	17	21	2026-02-05	0	\N	2026-02-05 12:00:00-03
826	17	22	2026-02-05	0	\N	2026-02-05 12:00:00-03
827	17	23	2026-02-05	0	\N	2026-02-05 12:00:00-03
828	17	24	2026-02-05	0	\N	2026-02-05 12:00:00-03
829	17	25	2026-02-05	0	\N	2026-02-05 12:00:00-03
830	17	26	2026-02-05	0	\N	2026-02-05 12:00:00-03
831	17	27	2026-02-05	0	\N	2026-02-05 12:00:00-03
832	17	28	2026-02-05	0	\N	2026-02-05 12:00:00-03
833	17	35	2026-02-05	0	\N	2026-02-05 12:00:00-03
834	17	36	2026-02-05	0	\N	2026-02-05 12:00:00-03
835	17	37	2026-02-05	0	\N	2026-02-05 12:00:00-03
836	17	38	2026-02-05	0	\N	2026-02-05 12:00:00-03
837	17	39	2026-02-05	0	\N	2026-02-05 12:00:00-03
838	17	40	2026-02-05	0	\N	2026-02-05 12:00:00-03
839	17	41	2026-02-05	0	\N	2026-02-05 12:00:00-03
840	17	42	2026-02-05	0	\N	2026-02-05 12:00:00-03
841	17	44	2026-02-05	0	\N	2026-02-05 12:00:00-03
842	17	29	2026-02-05	0	\N	2026-02-05 12:00:00-03
843	17	30	2026-02-05	0	\N	2026-02-05 12:00:00-03
844	1	4	2026-02-05	0	\N	2026-02-05 12:00:00-03
845	1	13	2026-02-05	0	\N	2026-02-05 12:00:00-03
846	1	14	2026-02-05	0	\N	2026-02-05 12:00:00-03
847	1	15	2026-02-05	0	\N	2026-02-05 12:00:00-03
848	1	16	2026-02-05	0	\N	2026-02-05 12:00:00-03
849	1	18	2026-02-05	0	\N	2026-02-05 12:00:00-03
850	1	19	2026-02-05	0	\N	2026-02-05 12:00:00-03
851	1	20	2026-02-05	0	\N	2026-02-05 12:00:00-03
852	1	21	2026-02-05	0	\N	2026-02-05 12:00:00-03
853	1	22	2026-02-05	0	\N	2026-02-05 12:00:00-03
854	1	24	2026-02-05	0	\N	2026-02-05 12:00:00-03
855	1	26	2026-02-05	0	\N	2026-02-05 12:00:00-03
856	1	27	2026-02-05	0	\N	2026-02-05 12:00:00-03
857	1	28	2026-02-05	0	\N	2026-02-05 12:00:00-03
858	1	30	2026-02-05	0	\N	2026-02-05 12:00:00-03
859	1	35	2026-02-05	0	\N	2026-02-05 12:00:00-03
860	1	36	2026-02-05	0	\N	2026-02-05 12:00:00-03
861	1	39	2026-02-05	0	\N	2026-02-05 12:00:00-03
862	1	42	2026-02-05	0	\N	2026-02-05 12:00:00-03
863	1	44	2026-02-05	0	\N	2026-02-05 12:00:00-03
864	22	4	2026-02-05	0	\N	2026-02-05 12:00:00-03
865	22	13	2026-02-05	0	\N	2026-02-05 12:00:00-03
866	22	14	2026-02-05	0	\N	2026-02-05 12:00:00-03
867	22	15	2026-02-05	0	\N	2026-02-05 12:00:00-03
868	22	16	2026-02-05	0	\N	2026-02-05 12:00:00-03
869	22	18	2026-02-05	0	\N	2026-02-05 12:00:00-03
870	22	19	2026-02-05	0	\N	2026-02-05 12:00:00-03
871	22	20	2026-02-05	0	\N	2026-02-05 12:00:00-03
872	22	21	2026-02-05	0	\N	2026-02-05 12:00:00-03
873	22	22	2026-02-05	0	\N	2026-02-05 12:00:00-03
874	22	23	2026-02-05	0	\N	2026-02-05 12:00:00-03
875	22	24	2026-02-05	0	\N	2026-02-05 12:00:00-03
876	22	26	2026-02-05	0	\N	2026-02-05 12:00:00-03
877	22	27	2026-02-05	0	\N	2026-02-05 12:00:00-03
878	22	28	2026-02-05	0	\N	2026-02-05 12:00:00-03
879	22	29	2026-02-05	0	\N	2026-02-05 12:00:00-03
880	22	30	2026-02-05	0	\N	2026-02-05 12:00:00-03
881	22	36	2026-02-05	0	\N	2026-02-05 12:00:00-03
882	22	39	2026-02-05	0	\N	2026-02-05 12:00:00-03
883	22	41	2026-02-05	0	\N	2026-02-05 12:00:00-03
884	22	42	2026-02-05	0	\N	2026-02-05 12:00:00-03
885	22	44	2026-02-05	0	\N	2026-02-05 12:00:00-03
\.


--
-- Data for Name: client_sales_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.client_sales_history (id, cost_center_id, product_id, date, sold_quantity, observed_at) FROM stdin;
1	3	34	2025-09-11	1	\N
2	1	37	2025-09-18	4	\N
3	1	44	2025-09-18	51	\N
4	1	14	2025-09-18	23	\N
5	1	16	2025-09-18	2	\N
6	1	20	2025-09-18	14	\N
7	1	24	2025-09-18	3	\N
8	1	19	2025-09-18	5	\N
9	1	18	2025-09-18	15	\N
10	1	28	2025-09-18	25	\N
11	1	35	2025-09-18	9	\N
12	1	4	2025-10-07	1175	\N
13	1	44	2025-10-07	108	\N
14	1	15	2025-10-07	205	\N
15	1	19	2025-10-07	29	\N
16	1	14	2025-10-07	23	\N
17	1	27	2025-10-07	5	\N
18	1	28	2025-10-07	95	\N
19	1	35	2025-10-07	17	\N
20	4	20	2025-10-07	8	\N
21	7	4	2025-10-08	80	\N
22	7	44	2025-10-08	87	\N
23	7	20	2025-10-08	13	\N
24	7	24	2025-10-08	6	\N
25	7	14	2025-10-08	14	\N
26	7	28	2025-10-08	4	\N
27	14	4	2025-10-08	15	\N
28	14	44	2025-10-08	8	\N
29	14	15	2025-10-08	4	\N
30	14	17	2025-10-08	4	\N
31	14	20	2025-10-08	2	\N
32	14	22	2025-10-08	1	\N
33	14	27	2025-10-08	4	\N
34	14	44	2025-10-09	5	\N
35	1	4	2025-10-13	30	\N
36	1	44	2025-10-13	17	\N
37	19	4	2025-10-13	62	\N
38	19	44	2025-10-13	25	\N
39	19	15	2025-10-13	5	\N
40	19	17	2025-10-13	2	\N
41	19	20	2025-10-13	8	\N
42	19	24	2025-10-13	2	\N
43	19	28	2025-10-13	25	\N
44	19	35	2025-10-13	10	\N
45	10	4	2025-10-16	35	\N
46	10	44	2025-10-16	18	\N
47	10	16	2025-10-16	10	\N
48	10	17	2025-10-16	3	\N
49	10	18	2025-10-16	6	\N
50	10	20	2025-10-16	15	\N
51	10	21	2025-10-16	2	\N
52	10	24	2025-10-16	1	\N
53	10	14	2025-10-16	7	\N
54	10	28	2025-10-16	7	\N
55	10	35	2025-10-16	3	\N
56	10	37	2025-10-16	1	\N
57	10	40	2025-10-16	3	\N
58	19	4	2025-10-16	21	\N
59	19	44	2025-10-16	5	\N
60	5	39	2025-10-16	16	\N
61	5	38	2025-10-16	8	\N
62	5	40	2025-10-16	3	\N
63	5	37	2025-10-16	3	\N
64	5	41	2025-10-16	9	\N
65	5	35	2025-10-16	7	\N
66	5	44	2025-10-16	50	\N
67	5	4	2025-10-16	47	\N
68	5	18	2025-10-16	5	\N
69	5	15	2025-10-16	59	\N
70	5	24	2025-10-16	6	\N
71	5	28	2025-10-16	31	\N
72	17	4	2025-10-16	60	\N
73	17	44	2025-10-16	17	\N
74	17	13	2025-10-16	8	\N
75	17	16	2025-10-16	1	\N
76	17	14	2025-10-16	2	\N
77	17	27	2025-10-16	3	\N
78	17	28	2025-10-16	8	\N
79	17	29	2025-10-16	4	\N
80	17	41	2025-10-16	3	\N
81	17	42	2025-10-16	4	\N
82	20	4	2025-10-16	58	\N
83	20	44	2025-10-16	10	\N
84	20	15	2025-10-16	6	\N
85	20	13	2025-10-16	1	\N
86	20	16	2025-10-16	3	\N
87	20	17	2025-10-16	5	\N
88	20	18	2025-10-16	2	\N
89	20	20	2025-10-16	2	\N
90	20	24	2025-10-16	4	\N
91	20	27	2025-10-16	3	\N
92	20	28	2025-10-16	7	\N
93	20	35	2025-10-16	1	\N
94	20	39	2025-10-16	2	\N
95	20	41	2025-10-16	1	\N
96	20	38	2025-10-16	2	\N
97	1	15	2025-10-16	13	\N
98	1	18	2025-10-16	6	\N
99	1	19	2025-10-16	3	\N
100	1	23	2025-10-16	4	\N
101	1	14	2025-10-16	4	\N
102	1	28	2025-10-16	2	\N
103	1	35	2025-10-16	1	\N
104	2	4	2025-10-16	28	\N
105	2	18	2025-10-16	2	\N
106	2	19	2025-10-16	3	\N
107	2	14	2025-10-16	1	\N
108	2	28	2025-10-16	6	\N
109	2	38	2025-10-16	1	\N
110	2	39	2025-10-16	2	\N
111	2	41	2025-10-16	2	\N
112	7	44	2025-10-16	11	\N
113	7	15	2025-10-16	5	\N
114	7	4	2025-10-16	2	\N
115	7	20	2025-10-16	1	\N
116	7	28	2025-10-16	2	\N
117	7	42	2025-10-16	3	\N
118	7	37	2025-10-16	4	\N
119	7	41	2025-10-16	3	\N
120	7	39	2025-10-16	1	\N
121	4	4	2025-10-20	38	\N
122	4	44	2025-10-20	45	\N
123	4	14	2025-10-20	4	\N
124	4	16	2025-10-20	2	\N
125	4	19	2025-10-20	5	\N
126	4	26	2025-10-20	3	\N
127	4	15	2025-10-20	20	\N
128	4	27	2025-10-20	7	\N
129	4	17	2025-10-20	2	\N
130	4	24	2025-10-20	1	\N
131	4	20	2025-10-20	8	\N
132	4	40	2025-10-20	1	\N
133	1	15	2025-10-20	16	\N
134	1	18	2025-10-20	4	\N
135	1	20	2025-10-20	4	\N
136	1	23	2025-10-20	1	\N
137	1	24	2025-10-20	2	\N
138	1	14	2025-10-20	2	\N
139	1	27	2025-10-20	2	\N
140	1	28	2025-10-20	5	\N
141	1	37	2025-10-20	2	\N
142	10	4	2025-10-20	38	\N
143	10	44	2025-10-20	29	\N
144	10	15	2025-10-20	9	\N
145	10	17	2025-10-20	1	\N
146	10	19	2025-10-20	2	\N
147	10	20	2025-10-20	8	\N
148	10	14	2025-10-20	10	\N
149	10	27	2025-10-20	4	\N
150	10	16	2025-10-20	10	\N
151	10	28	2025-10-20	16	\N
152	10	35	2025-10-20	3	\N
153	10	36	2025-10-20	3	\N
154	10	37	2025-10-20	3	\N
155	10	38	2025-10-20	3	\N
156	10	40	2025-10-20	3	\N
157	21	4	2025-10-23	68	\N
158	21	44	2025-10-23	55	\N
159	21	15	2025-10-23	99	\N
160	21	13	2025-10-23	32	\N
161	21	16	2025-10-23	9	\N
163	21	18	2025-10-23	9	\N
164	21	20	2025-10-23	10	\N
165	21	24	2025-10-23	5	\N
166	21	14	2025-10-23	9	\N
168	21	28	2025-10-23	23	\N
169	21	29	2025-10-23	1	\N
170	21	30	2025-10-23	1	\N
171	21	35	2025-10-23	12	\N
173	21	39	2025-10-23	2	\N
174	21	41	2025-10-23	2	\N
162	21	17	2025-10-23	4	\N
167	21	27	2025-10-23	11	\N
172	21	38	2025-10-23	5	\N
176	8	44	2025-10-23	12	\N
177	8	18	2025-10-23	3	\N
178	8	20	2025-10-23	7	\N
179	8	21	2025-10-23	1	\N
180	8	26	2025-10-23	1	\N
181	8	28	2025-10-23	20	\N
182	8	35	2025-10-23	1	\N
183	8	39	2025-10-23	3	\N
184	8	14	2025-10-23	13	\N
185	4	4	2025-10-23	33	\N
186	4	44	2025-10-23	16	\N
187	4	15	2025-10-23	9	\N
188	4	18	2025-10-23	11	\N
189	4	19	2025-10-23	4	\N
190	4	20	2025-10-23	14	\N
191	4	21	2025-10-23	2	\N
192	4	26	2025-10-23	2	\N
193	4	14	2025-10-23	10	\N
194	4	39	2025-10-23	6	\N
195	4	40	2025-10-23	3	\N
175	8	4	2025-10-23	38	\N
196	10	4	2025-11-03	2	\N
197	10	16	2025-11-03	2	\N
198	10	18	2025-11-03	12	\N
199	10	20	2025-11-03	3	\N
200	10	26	2025-11-03	5	\N
201	10	27	2025-11-03	6	\N
202	10	28	2025-11-03	4	\N
203	10	35	2025-11-03	5	\N
204	1	4	2025-11-10	45	\N
205	1	44	2025-11-10	72	\N
206	1	15	2025-11-10	89	\N
207	1	20	2025-11-10	57	\N
208	1	4	2025-11-17	1	\N
209	1	44	2025-11-17	23	\N
210	1	15	2025-11-17	30	\N
211	1	20	2025-11-17	9	\N
212	1	14	2025-11-17	7	\N
213	1	13	2025-11-17	2	\N
214	1	16	2025-11-17	3	\N
215	1	21	2025-11-17	3	\N
216	1	35	2025-11-17	1	\N
217	1	19	2025-11-17	9	\N
218	1	24	2025-11-17	3	\N
219	1	28	2025-11-17	8	\N
220	1	27	2025-11-17	3	\N
221	1	26	2025-11-17	3	\N
222	1	23	2025-11-17	1	\N
223	1	4	2025-11-20	11	\N
224	1	44	2025-11-20	26	\N
225	1	15	2025-11-20	20	\N
226	1	13	2025-11-20	7	\N
227	1	16	2025-11-20	12	\N
228	1	18	2025-11-20	9	\N
229	1	19	2025-11-20	8	\N
230	1	20	2025-11-20	12	\N
231	1	21	2025-11-20	5	\N
232	1	23	2025-11-20	1	\N
233	1	24	2025-11-20	4	\N
234	1	26	2025-11-20	1	\N
235	1	14	2025-11-20	8	\N
236	1	27	2025-11-20	5	\N
237	1	28	2025-11-20	8	\N
238	1	35	2025-11-20	2	\N
239	1	4	2025-11-24	19	2025-11-24 12:00:00-03
240	1	13	2025-11-24	1	2025-11-24 12:00:00-03
241	1	14	2025-11-24	8	2025-11-24 12:00:00-03
242	1	15	2025-11-24	27	2025-11-24 12:00:00-03
243	1	16	2025-11-24	4	2025-11-24 12:00:00-03
244	1	17	2025-11-24	5	2025-11-24 12:00:00-03
245	1	18	2025-11-24	5	2025-11-24 12:00:00-03
246	1	19	2025-11-24	9	2025-11-24 12:00:00-03
247	1	20	2025-11-24	10	2025-11-24 12:00:00-03
248	1	21	2025-11-24	2	2025-11-24 12:00:00-03
249	1	23	2025-11-24	0	2025-11-24 12:00:00-03
250	1	24	2025-11-24	13	2025-11-24 12:00:00-03
251	1	26	2025-11-24	1	2025-11-24 12:00:00-03
252	1	27	2025-11-24	1	2025-11-24 12:00:00-03
253	1	28	2025-11-24	17	2025-11-24 12:00:00-03
254	1	35	2025-11-24	5	2025-11-24 12:00:00-03
255	1	36	2025-11-24	2	2025-11-24 12:00:00-03
256	1	37	2025-11-24	2	2025-11-24 12:00:00-03
257	1	39	2025-11-24	0	2025-11-24 12:00:00-03
258	1	44	2025-11-24	32	2025-11-24 12:00:00-03
259	1	4	2025-11-27	7	2025-11-27 12:00:00-03
260	1	13	2025-11-27	2	2025-11-27 12:00:00-03
261	1	14	2025-11-27	4	2025-11-27 12:00:00-03
262	1	15	2025-11-27	29	2025-11-27 12:00:00-03
263	1	16	2025-11-27	5	2025-11-27 12:00:00-03
264	1	17	2025-11-27	7	2025-11-27 12:00:00-03
265	1	18	2025-11-27	5	2025-11-27 12:00:00-03
266	1	19	2025-11-27	9	2025-11-27 12:00:00-03
267	1	20	2025-11-27	7	2025-11-27 12:00:00-03
268	1	21	2025-11-27	3	2025-11-27 12:00:00-03
269	1	23	2025-11-27	0	2025-11-27 12:00:00-03
270	1	24	2025-11-27	4	2025-11-27 12:00:00-03
271	1	27	2025-11-27	0	2025-11-27 12:00:00-03
272	1	28	2025-11-27	12	2025-11-27 12:00:00-03
273	1	35	2025-11-27	0	2025-11-27 12:00:00-03
274	1	36	2025-11-27	0	2025-11-27 12:00:00-03
275	1	37	2025-11-27	8	2025-11-27 12:00:00-03
276	1	39	2025-11-27	0	2025-11-27 12:00:00-03
277	1	40	2025-11-27	0	2025-11-27 12:00:00-03
278	1	44	2025-11-27	20	2025-11-27 12:00:00-03
279	1	4	2025-12-01	19	2025-12-01 12:00:00-03
280	1	13	2025-12-01	7	2025-12-01 12:00:00-03
281	1	14	2025-12-01	8	2025-12-01 12:00:00-03
282	1	15	2025-12-01	38	2025-12-01 12:00:00-03
283	1	16	2025-12-01	6	2025-12-01 12:00:00-03
284	1	17	2025-12-01	0	2025-12-01 12:00:00-03
285	1	18	2025-12-01	5	2025-12-01 12:00:00-03
286	1	19	2025-12-01	0	2025-12-01 12:00:00-03
287	1	20	2025-12-01	16	2025-12-01 12:00:00-03
288	1	21	2025-12-01	3	2025-12-01 12:00:00-03
289	1	23	2025-12-01	1	2025-12-01 12:00:00-03
290	1	24	2025-12-01	5	2025-12-01 12:00:00-03
291	1	25	2025-12-01	0	2025-12-01 12:00:00-03
292	1	26	2025-12-01	0	2025-12-01 12:00:00-03
293	1	27	2025-12-01	3	2025-12-01 12:00:00-03
294	1	28	2025-12-01	1	2025-12-01 12:00:00-03
295	1	35	2025-12-01	8	2025-12-01 12:00:00-03
296	1	36	2025-12-01	0	2025-12-01 12:00:00-03
297	1	37	2025-12-01	4	2025-12-01 12:00:00-03
298	1	39	2025-12-01	4	2025-12-01 12:00:00-03
299	1	40	2025-12-01	2	2025-12-01 12:00:00-03
300	1	44	2025-12-01	26	2025-12-01 12:00:00-03
301	1	4	2025-12-04	17	2025-12-04 12:00:00-03
302	1	13	2025-12-04	6	2025-12-04 12:00:00-03
303	1	14	2025-12-04	7	2025-12-04 12:00:00-03
304	1	15	2025-12-04	38	2025-12-04 12:00:00-03
305	1	16	2025-12-04	4	2025-12-04 12:00:00-03
306	1	17	2025-12-04	4	2025-12-04 12:00:00-03
307	1	18	2025-12-04	6	2025-12-04 12:00:00-03
308	1	19	2025-12-04	7	2025-12-04 12:00:00-03
309	1	20	2025-12-04	15	2025-12-04 12:00:00-03
310	1	21	2025-12-04	0	2025-12-04 12:00:00-03
311	1	22	2025-12-04	0	2025-12-04 12:00:00-03
312	1	23	2025-12-04	0	2025-12-04 12:00:00-03
313	1	24	2025-12-04	6	2025-12-04 12:00:00-03
314	1	25	2025-12-04	0	2025-12-04 12:00:00-03
315	1	26	2025-12-04	0	2025-12-04 12:00:00-03
316	1	27	2025-12-04	5	2025-12-04 12:00:00-03
317	1	28	2025-12-04	7	2025-12-04 12:00:00-03
318	1	35	2025-12-04	2	2025-12-04 12:00:00-03
319	1	36	2025-12-04	4	2025-12-04 12:00:00-03
320	1	37	2025-12-04	0	2025-12-04 12:00:00-03
321	1	39	2025-12-04	4	2025-12-04 12:00:00-03
322	1	40	2025-12-04	0	2025-12-04 12:00:00-03
323	1	44	2025-12-04	9	2025-12-04 12:00:00-03
324	1	4	2025-12-08	21	2025-12-08 12:00:00-03
325	1	13	2025-12-08	9	2025-12-08 12:00:00-03
326	1	14	2025-12-08	18	2025-12-08 12:00:00-03
327	1	15	2025-12-08	55	2025-12-08 12:00:00-03
328	1	16	2025-12-08	7	2025-12-08 12:00:00-03
329	1	17	2025-12-08	0	2025-12-08 12:00:00-03
330	1	18	2025-12-08	0	2025-12-08 12:00:00-03
331	1	19	2025-12-08	7	2025-12-08 12:00:00-03
332	1	20	2025-12-08	23	2025-12-08 12:00:00-03
333	1	21	2025-12-08	4	2025-12-08 12:00:00-03
334	1	23	2025-12-08	2	2025-12-08 12:00:00-03
335	1	24	2025-12-08	5	2025-12-08 12:00:00-03
336	1	25	2025-12-08	0	2025-12-08 12:00:00-03
337	1	26	2025-12-08	0	2025-12-08 12:00:00-03
338	1	27	2025-12-08	7	2025-12-08 12:00:00-03
339	1	28	2025-12-08	13	2025-12-08 12:00:00-03
340	1	35	2025-12-08	0	2025-12-08 12:00:00-03
341	1	36	2025-12-08	0	2025-12-08 12:00:00-03
342	1	37	2025-12-08	4	2025-12-08 12:00:00-03
343	1	39	2025-12-08	0	2025-12-08 12:00:00-03
344	1	44	2025-12-08	33	2025-12-08 12:00:00-03
345	1	4	2025-12-11	1	2025-12-11 12:00:00-03
346	1	13	2025-12-11	0	2025-12-11 12:00:00-03
347	1	14	2025-12-11	0	2025-12-11 12:00:00-03
348	1	15	2025-12-11	0	2025-12-11 12:00:00-03
349	1	16	2025-12-11	0	2025-12-11 12:00:00-03
350	1	17	2025-12-11	4	2025-12-11 12:00:00-03
351	1	18	2025-12-11	3	2025-12-11 12:00:00-03
352	1	19	2025-12-11	0	2025-12-11 12:00:00-03
353	1	20	2025-12-11	0	2025-12-11 12:00:00-03
354	1	21	2025-12-11	0	2025-12-11 12:00:00-03
355	1	23	2025-12-11	2	2025-12-11 12:00:00-03
356	1	24	2025-12-11	0	2025-12-11 12:00:00-03
357	1	27	2025-12-11	0	2025-12-11 12:00:00-03
358	1	28	2025-12-11	0	2025-12-11 12:00:00-03
359	1	35	2025-12-11	6	2025-12-11 12:00:00-03
360	1	36	2025-12-11	0	2025-12-11 12:00:00-03
361	1	44	2025-12-11	0	2025-12-11 12:00:00-03
362	1	4	2025-12-18	0	2025-12-18 12:00:00-03
363	1	13	2025-12-18	0	2025-12-18 12:00:00-03
364	1	14	2025-12-18	6	2025-12-18 12:00:00-03
365	1	15	2025-12-18	14	2025-12-18 12:00:00-03
366	1	16	2025-12-18	0	2025-12-18 12:00:00-03
367	1	19	2025-12-18	7	2025-12-18 12:00:00-03
368	1	20	2025-12-18	13	2025-12-18 12:00:00-03
369	1	21	2025-12-18	3	2025-12-18 12:00:00-03
370	1	24	2025-12-18	0	2025-12-18 12:00:00-03
371	1	27	2025-12-18	6	2025-12-18 12:00:00-03
372	1	28	2025-12-18	0	2025-12-18 12:00:00-03
373	1	44	2025-12-18	0	2025-12-18 12:00:00-03
374	1	4	2026-01-05	121	2026-01-05 12:00:00-03
375	1	13	2026-01-05	21	2026-01-05 12:00:00-03
376	1	14	2026-01-05	14	2026-01-05 12:00:00-03
377	1	15	2026-01-05	101	2026-01-05 12:00:00-03
378	1	16	2026-01-05	15	2026-01-05 12:00:00-03
379	1	17	2026-01-05	0	2026-01-05 12:00:00-03
380	1	18	2026-01-05	7	2026-01-05 12:00:00-03
381	1	19	2026-01-05	26	2026-01-05 12:00:00-03
382	1	20	2026-01-05	37	2026-01-05 12:00:00-03
383	1	21	2026-01-05	15	2026-01-05 12:00:00-03
384	1	23	2026-01-05	0	2026-01-05 12:00:00-03
385	1	24	2026-01-05	9	2026-01-05 12:00:00-03
386	1	25	2026-01-05	0	2026-01-05 12:00:00-03
387	1	26	2026-01-05	0	2026-01-05 12:00:00-03
388	1	27	2026-01-05	8	2026-01-05 12:00:00-03
389	1	28	2026-01-05	38	2026-01-05 12:00:00-03
390	1	35	2026-01-05	2	2026-01-05 12:00:00-03
391	1	36	2026-01-05	5	2026-01-05 12:00:00-03
392	1	38	2026-01-05	4	2026-01-05 12:00:00-03
393	1	39	2026-01-05	0	2026-01-05 12:00:00-03
394	1	40	2026-01-05	0	2026-01-05 12:00:00-03
395	1	44	2026-01-05	94	2026-01-05 12:00:00-03
396	22	4	2026-01-05	208	2026-01-05 12:00:00-03
397	22	13	2026-01-05	10	2026-01-05 12:00:00-03
398	22	14	2026-01-05	60	2026-01-05 12:00:00-03
399	22	15	2026-01-05	880	2026-01-05 12:00:00-03
400	22	16	2026-01-05	54	2026-01-05 12:00:00-03
401	22	17	2026-01-05	0	2026-01-05 12:00:00-03
402	22	18	2026-01-05	18	2026-01-05 12:00:00-03
403	22	19	2026-01-05	30	2026-01-05 12:00:00-03
404	22	20	2026-01-05	108	2026-01-05 12:00:00-03
405	22	21	2026-01-05	24	2026-01-05 12:00:00-03
406	22	22	2026-01-05	10	2026-01-05 12:00:00-03
407	22	24	2026-01-05	20	2026-01-05 12:00:00-03
408	22	25	2026-01-05	0	2026-01-05 12:00:00-03
409	22	26	2026-01-05	8	2026-01-05 12:00:00-03
410	22	27	2026-01-05	0	2026-01-05 12:00:00-03
411	22	28	2026-01-05	35	2026-01-05 12:00:00-03
412	22	35	2026-01-05	0	2026-01-05 12:00:00-03
413	22	36	2026-01-05	0	2026-01-05 12:00:00-03
414	22	37	2026-01-05	0	2026-01-05 12:00:00-03
415	22	44	2026-01-05	128	2026-01-05 12:00:00-03
416	1	4	2026-01-08	60	2026-01-08 12:00:00-03
417	1	13	2026-01-08	7	2026-01-08 12:00:00-03
418	1	14	2026-01-08	6	2026-01-08 12:00:00-03
419	1	15	2026-01-08	41	2026-01-08 12:00:00-03
420	1	16	2026-01-08	4	2026-01-08 12:00:00-03
421	1	17	2026-01-08	0	2026-01-08 12:00:00-03
422	1	18	2026-01-08	9	2026-01-08 12:00:00-03
423	1	19	2026-01-08	10	2026-01-08 12:00:00-03
424	1	20	2026-01-08	14	2026-01-08 12:00:00-03
425	1	21	2026-01-08	4	2026-01-08 12:00:00-03
426	1	24	2026-01-08	6	2026-01-08 12:00:00-03
427	1	26	2026-01-08	4	2026-01-08 12:00:00-03
428	1	27	2026-01-08	4	2026-01-08 12:00:00-03
429	1	28	2026-01-08	13	2026-01-08 12:00:00-03
430	1	35	2026-01-08	5	2026-01-08 12:00:00-03
431	1	37	2026-01-08	4	2026-01-08 12:00:00-03
432	1	39	2026-01-08	3	2026-01-08 12:00:00-03
433	1	44	2026-01-08	25	2026-01-08 12:00:00-03
434	22	4	2026-01-08	240	2026-01-08 12:00:00-03
435	22	13	2026-01-08	14	2026-01-08 12:00:00-03
436	22	14	2026-01-08	10	2026-01-08 12:00:00-03
437	22	15	2026-01-08	154	2026-01-08 12:00:00-03
438	22	16	2026-01-08	17	2026-01-08 12:00:00-03
439	22	18	2026-01-08	3	2026-01-08 12:00:00-03
440	22	19	2026-01-08	12	2026-01-08 12:00:00-03
441	22	20	2026-01-08	53	2026-01-08 12:00:00-03
442	22	21	2026-01-08	6	2026-01-08 12:00:00-03
443	22	22	2026-01-08	2	2026-01-08 12:00:00-03
444	22	24	2026-01-08	9	2026-01-08 12:00:00-03
445	22	26	2026-01-08	1	2026-01-08 12:00:00-03
446	22	27	2026-01-08	7	2026-01-08 12:00:00-03
447	22	28	2026-01-08	11	2026-01-08 12:00:00-03
448	22	35	2026-01-08	5	2026-01-08 12:00:00-03
449	22	36	2026-01-08	2	2026-01-08 12:00:00-03
450	22	37	2026-01-08	2	2026-01-08 12:00:00-03
451	22	44	2026-01-08	108	2026-01-08 12:00:00-03
452	17	4	2026-01-12	75	2026-01-12 12:00:00-03
453	17	13	2026-01-12	12	2026-01-12 12:00:00-03
454	17	14	2026-01-12	0	2026-01-12 12:00:00-03
455	17	15	2026-01-12	165	2026-01-12 12:00:00-03
456	17	16	2026-01-12	24	2026-01-12 12:00:00-03
457	17	17	2026-01-12	9	2026-01-12 12:00:00-03
458	17	18	2026-01-12	2	2026-01-12 12:00:00-03
459	17	19	2026-01-12	7	2026-01-12 12:00:00-03
460	17	20	2026-01-12	42	2026-01-12 12:00:00-03
461	17	21	2026-01-12	0	2026-01-12 12:00:00-03
462	17	22	2026-01-12	12	2026-01-12 12:00:00-03
463	17	23	2026-01-12	5	2026-01-12 12:00:00-03
464	17	24	2026-01-12	15	2026-01-12 12:00:00-03
465	17	25	2026-01-12	0	2026-01-12 12:00:00-03
466	17	26	2026-01-12	14	2026-01-12 12:00:00-03
467	17	27	2026-01-12	9	2026-01-12 12:00:00-03
468	17	28	2026-01-12	18	2026-01-12 12:00:00-03
469	17	35	2026-01-12	6	2026-01-12 12:00:00-03
470	17	36	2026-01-12	0	2026-01-12 12:00:00-03
471	17	37	2026-01-12	0	2026-01-12 12:00:00-03
472	17	38	2026-01-12	4	2026-01-12 12:00:00-03
473	17	39	2026-01-12	4	2026-01-12 12:00:00-03
474	17	40	2026-01-12	0	2026-01-12 12:00:00-03
475	17	41	2026-01-12	0	2026-01-12 12:00:00-03
476	17	42	2026-01-12	0	2026-01-12 12:00:00-03
477	17	44	2026-01-12	71	2026-01-12 12:00:00-03
478	38	4	2026-01-12	60	2026-01-12 12:00:00-03
479	38	13	2026-01-12	28	2026-01-12 12:00:00-03
480	38	14	2026-01-12	39	2026-01-12 12:00:00-03
481	38	15	2026-01-12	168	2026-01-12 12:00:00-03
482	38	16	2026-01-12	14	2026-01-12 12:00:00-03
483	38	17	2026-01-12	24	2026-01-12 12:00:00-03
484	38	18	2026-01-12	52	2026-01-12 12:00:00-03
485	38	19	2026-01-12	37	2026-01-12 12:00:00-03
486	38	20	2026-01-12	69	2026-01-12 12:00:00-03
487	38	21	2026-01-12	31	2026-01-12 12:00:00-03
488	38	22	2026-01-12	3	2026-01-12 12:00:00-03
489	38	23	2026-01-12	14	2026-01-12 12:00:00-03
490	38	24	2026-01-12	22	2026-01-12 12:00:00-03
491	38	25	2026-01-12	2	2026-01-12 12:00:00-03
492	38	26	2026-01-12	0	2026-01-12 12:00:00-03
493	38	27	2026-01-12	0	2026-01-12 12:00:00-03
494	38	28	2026-01-12	45	2026-01-12 12:00:00-03
495	38	35	2026-01-12	47	2026-01-12 12:00:00-03
496	38	36	2026-01-12	0	2026-01-12 12:00:00-03
497	38	37	2026-01-12	0	2026-01-12 12:00:00-03
498	38	38	2026-01-12	30	2026-01-12 12:00:00-03
499	38	39	2026-01-12	27	2026-01-12 12:00:00-03
500	38	40	2026-01-12	6	2026-01-12 12:00:00-03
501	38	41	2026-01-12	0	2026-01-12 12:00:00-03
502	38	42	2026-01-12	0	2026-01-12 12:00:00-03
503	38	44	2026-01-12	111	2026-01-12 12:00:00-03
504	22	4	2026-01-12	90	2026-01-12 12:00:00-03
505	22	13	2026-01-12	11	2026-01-12 12:00:00-03
506	22	14	2026-01-12	20	2026-01-12 12:00:00-03
507	22	15	2026-01-12	344	2026-01-12 12:00:00-03
508	22	16	2026-01-12	17	2026-01-12 12:00:00-03
509	22	17	2026-01-12	6	2026-01-12 12:00:00-03
510	22	18	2026-01-12	19	2026-01-12 12:00:00-03
511	22	19	2026-01-12	24	2026-01-12 12:00:00-03
512	22	20	2026-01-12	57	2026-01-12 12:00:00-03
513	22	21	2026-01-12	6	2026-01-12 12:00:00-03
514	22	22	2026-01-12	0	2026-01-12 12:00:00-03
515	22	24	2026-01-12	9	2026-01-12 12:00:00-03
516	22	26	2026-01-12	13	2026-01-12 12:00:00-03
517	22	27	2026-01-12	11	2026-01-12 12:00:00-03
518	22	28	2026-01-12	21	2026-01-12 12:00:00-03
519	22	35	2026-01-12	12	2026-01-12 12:00:00-03
520	22	36	2026-01-12	2	2026-01-12 12:00:00-03
521	22	37	2026-01-12	7	2026-01-12 12:00:00-03
522	22	39	2026-01-12	4	2026-01-12 12:00:00-03
523	22	44	2026-01-12	132	2026-01-12 12:00:00-03
524	1	4	2026-01-12	60	2026-01-12 12:00:00-03
525	1	13	2026-01-12	11	2026-01-12 12:00:00-03
526	1	14	2026-01-12	5	2026-01-12 12:00:00-03
527	1	15	2026-01-12	54	2026-01-12 12:00:00-03
528	1	16	2026-01-12	8	2026-01-12 12:00:00-03
529	1	17	2026-01-12	56	2026-01-12 12:00:00-03
530	1	18	2026-01-12	13	2026-01-12 12:00:00-03
531	1	19	2026-01-12	13	2026-01-12 12:00:00-03
532	1	20	2026-01-12	18	2026-01-12 12:00:00-03
533	1	21	2026-01-12	8	2026-01-12 12:00:00-03
534	1	24	2026-01-12	3	2026-01-12 12:00:00-03
535	1	26	2026-01-12	3	2026-01-12 12:00:00-03
536	1	27	2026-01-12	6	2026-01-12 12:00:00-03
537	1	28	2026-01-12	15	2026-01-12 12:00:00-03
538	1	35	2026-01-12	4	2026-01-12 12:00:00-03
539	1	36	2026-01-12	0	2026-01-12 12:00:00-03
540	1	37	2026-01-12	4	2026-01-12 12:00:00-03
541	1	39	2026-01-12	4	2026-01-12 12:00:00-03
542	1	44	2026-01-12	29	2026-01-12 12:00:00-03
543	17	4	2026-01-15	52	2026-01-15 12:00:00-03
544	17	14	2026-01-15	23	2026-01-15 12:00:00-03
545	17	15	2026-01-15	32	2026-01-15 12:00:00-03
546	17	16	2026-01-15	9	2026-01-15 12:00:00-03
547	17	18	2026-01-15	58	2026-01-15 12:00:00-03
548	17	20	2026-01-15	23	2026-01-15 12:00:00-03
549	17	22	2026-01-15	5	2026-01-15 12:00:00-03
550	17	28	2026-01-15	2	2026-01-15 12:00:00-03
551	17	35	2026-01-15	5	2026-01-15 12:00:00-03
552	17	36	2026-01-15	1	2026-01-15 12:00:00-03
553	17	37	2026-01-15	3	2026-01-15 12:00:00-03
554	17	38	2026-01-15	4	2026-01-15 12:00:00-03
555	17	40	2026-01-15	0	2026-01-15 12:00:00-03
556	17	44	2026-01-15	47	2026-01-15 12:00:00-03
557	1	4	2026-01-15	27	2026-01-15 12:00:00-03
558	1	13	2026-01-15	3	2026-01-15 12:00:00-03
559	1	14	2026-01-15	10	2026-01-15 12:00:00-03
560	1	15	2026-01-15	52	2026-01-15 12:00:00-03
561	1	16	2026-01-15	8	2026-01-15 12:00:00-03
562	1	17	2026-01-15	4	2026-01-15 12:00:00-03
563	1	18	2026-01-15	13	2026-01-15 12:00:00-03
564	1	19	2026-01-15	4	2026-01-15 12:00:00-03
565	1	20	2026-01-15	18	2026-01-15 12:00:00-03
566	1	21	2026-01-15	5	2026-01-15 12:00:00-03
567	1	24	2026-01-15	7	2026-01-15 12:00:00-03
568	1	26	2026-01-15	1	2026-01-15 12:00:00-03
569	1	27	2026-01-15	4	2026-01-15 12:00:00-03
570	1	28	2026-01-15	15	2026-01-15 12:00:00-03
571	1	35	2026-01-15	6	2026-01-15 12:00:00-03
572	1	37	2026-01-15	3	2026-01-15 12:00:00-03
573	1	38	2026-01-15	2	2026-01-15 12:00:00-03
574	1	39	2026-01-15	4	2026-01-15 12:00:00-03
575	1	44	2026-01-15	21	2026-01-15 12:00:00-03
585	38	21	2026-01-15	0	2026-01-15 12:00:00-03
589	38	25	2026-01-15	0	2026-01-15 12:00:00-03
601	38	42	2026-01-15	0	2026-01-15 12:00:00-03
576	38	4	2026-01-15	0	2026-01-15 12:00:00-03
577	38	13	2026-01-15	0	2026-01-15 12:00:00-03
578	38	14	2026-01-15	0	2026-01-15 12:00:00-03
579	38	15	2026-01-15	0	2026-01-15 12:00:00-03
580	38	16	2026-01-15	0	2026-01-15 12:00:00-03
581	38	17	2026-01-15	0	2026-01-15 12:00:00-03
582	38	18	2026-01-15	0	2026-01-15 12:00:00-03
583	38	19	2026-01-15	3	2026-01-15 12:00:00-03
584	38	20	2026-01-15	0	2026-01-15 12:00:00-03
586	38	22	2026-01-15	6	2026-01-15 12:00:00-03
587	38	23	2026-01-15	0	2026-01-15 12:00:00-03
588	38	24	2026-01-15	0	2026-01-15 12:00:00-03
590	38	26	2026-01-15	0	2026-01-15 12:00:00-03
591	38	27	2026-01-15	0	2026-01-15 12:00:00-03
592	38	28	2026-01-15	2	2026-01-15 12:00:00-03
593	38	34	2026-01-15	0	2026-01-15 12:00:00-03
594	38	35	2026-01-15	0	2026-01-15 12:00:00-03
595	38	36	2026-01-15	0	2026-01-15 12:00:00-03
596	38	37	2026-01-15	0	2026-01-15 12:00:00-03
597	38	38	2026-01-15	0	2026-01-15 12:00:00-03
598	38	39	2026-01-15	0	2026-01-15 12:00:00-03
599	38	40	2026-01-15	0	2026-01-15 12:00:00-03
600	38	41	2026-01-15	0	2026-01-15 12:00:00-03
602	38	44	2026-01-15	0	2026-01-15 12:00:00-03
603	22	4	2026-01-15	60	2026-01-15 12:00:00-03
604	22	13	2026-01-15	0	2026-01-15 12:00:00-03
605	22	14	2026-01-15	20	2026-01-15 12:00:00-03
606	22	15	2026-01-15	140	2026-01-15 12:00:00-03
607	22	16	2026-01-15	2	2026-01-15 12:00:00-03
608	22	18	2026-01-15	6	2026-01-15 12:00:00-03
609	22	19	2026-01-15	12	2026-01-15 12:00:00-03
610	22	20	2026-01-15	44	2026-01-15 12:00:00-03
611	22	21	2026-01-15	2	2026-01-15 12:00:00-03
612	22	24	2026-01-15	6	2026-01-15 12:00:00-03
613	22	26	2026-01-15	3	2026-01-15 12:00:00-03
614	22	27	2026-01-15	0	2026-01-15 12:00:00-03
615	22	28	2026-01-15	23	2026-01-15 12:00:00-03
616	22	35	2026-01-15	8	2026-01-15 12:00:00-03
617	22	36	2026-01-15	5	2026-01-15 12:00:00-03
618	22	37	2026-01-15	0	2026-01-15 12:00:00-03
619	22	39	2026-01-15	0	2026-01-15 12:00:00-03
620	22	40	2026-01-15	0	2026-01-15 12:00:00-03
621	22	41	2026-01-15	0	2026-01-15 12:00:00-03
622	22	42	2026-01-15	0	2026-01-15 12:00:00-03
623	22	44	2026-01-15	86	2026-01-15 12:00:00-03
624	38	4	2026-01-19	40	2026-01-19 12:00:00-03
625	38	13	2026-01-19	15	2026-01-19 12:00:00-03
626	38	14	2026-01-19	42	2026-01-19 12:00:00-03
627	38	15	2026-01-19	0	2026-01-19 12:00:00-03
628	38	16	2026-01-19	14	2026-01-19 12:00:00-03
629	38	17	2026-01-19	0	2026-01-19 12:00:00-03
630	38	18	2026-01-19	42	2026-01-19 12:00:00-03
631	38	19	2026-01-19	3	2026-01-19 12:00:00-03
632	38	20	2026-01-19	24	2026-01-19 12:00:00-03
633	38	21	2026-01-19	22	2026-01-19 12:00:00-03
634	38	22	2026-01-19	0	2026-01-19 12:00:00-03
635	38	24	2026-01-19	7	2026-01-19 12:00:00-03
636	38	26	2026-01-19	20	2026-01-19 12:00:00-03
637	38	27	2026-01-19	0	2026-01-19 12:00:00-03
638	38	28	2026-01-19	8	2026-01-19 12:00:00-03
639	38	34	2026-01-19	0	2026-01-19 12:00:00-03
640	38	36	2026-01-19	10	2026-01-19 12:00:00-03
641	38	37	2026-01-19	0	2026-01-19 12:00:00-03
642	38	38	2026-01-19	16	2026-01-19 12:00:00-03
643	38	39	2026-01-19	4	2026-01-19 12:00:00-03
644	38	40	2026-01-19	19	2026-01-19 12:00:00-03
645	38	41	2026-01-19	6	2026-01-19 12:00:00-03
646	38	44	2026-01-19	0	2026-01-19 12:00:00-03
647	17	4	2026-01-19	26	2026-01-19 12:00:00-03
648	17	13	2026-01-19	10	2026-01-19 12:00:00-03
649	17	14	2026-01-19	13	2026-01-19 12:00:00-03
650	17	15	2026-01-19	72	2026-01-19 12:00:00-03
651	17	16	2026-01-19	10	2026-01-19 12:00:00-03
652	17	17	2026-01-19	0	2026-01-19 12:00:00-03
653	17	18	2026-01-19	8	2026-01-19 12:00:00-03
654	17	19	2026-01-19	20	2026-01-19 12:00:00-03
655	17	20	2026-01-19	37	2026-01-19 12:00:00-03
656	17	21	2026-01-19	5	2026-01-19 12:00:00-03
657	17	22	2026-01-19	10	2026-01-19 12:00:00-03
658	17	23	2026-01-19	5	2026-01-19 12:00:00-03
659	17	24	2026-01-19	9	2026-01-19 12:00:00-03
660	17	25	2026-01-19	0	2026-01-19 12:00:00-03
661	17	26	2026-01-19	5	2026-01-19 12:00:00-03
662	17	27	2026-01-19	0	2026-01-19 12:00:00-03
663	17	28	2026-01-19	18	2026-01-19 12:00:00-03
664	17	35	2026-01-19	8	2026-01-19 12:00:00-03
665	17	36	2026-01-19	2	2026-01-19 12:00:00-03
666	17	37	2026-01-19	2	2026-01-19 12:00:00-03
667	17	38	2026-01-19	5	2026-01-19 12:00:00-03
668	17	39	2026-01-19	0	2026-01-19 12:00:00-03
669	17	40	2026-01-19	9	2026-01-19 12:00:00-03
670	17	41	2026-01-19	0	2026-01-19 12:00:00-03
671	17	42	2026-01-19	0	2026-01-19 12:00:00-03
672	17	44	2026-01-19	31	2026-01-19 12:00:00-03
675	1	14	2026-01-21	17	2026-01-21 12:00:00-03
677	1	16	2026-01-21	16	2026-01-21 12:00:00-03
678	1	18	2026-01-21	18	2026-01-21 12:00:00-03
679	1	19	2026-01-21	35	2026-01-21 12:00:00-03
680	1	20	2026-01-21	38	2026-01-21 12:00:00-03
681	1	21	2026-01-21	12	2026-01-21 12:00:00-03
682	1	24	2026-01-21	9	2026-01-21 12:00:00-03
683	1	26	2026-01-21	5	2026-01-21 12:00:00-03
685	1	28	2026-01-21	22	2026-01-21 12:00:00-03
686	1	35	2026-01-21	7	2026-01-21 12:00:00-03
687	1	36	2026-01-21	3	2026-01-21 12:00:00-03
688	1	37	2026-01-21	1	2026-01-21 12:00:00-03
689	1	38	2026-01-21	6	2026-01-21 12:00:00-03
690	1	39	2026-01-21	4	2026-01-21 12:00:00-03
692	1	44	2026-01-21	37	2026-01-21 12:00:00-03
673	1	4	2026-01-21	60	2026-01-21 12:00:00-03
674	1	13	2026-01-21	11	2026-01-21 12:00:00-03
676	1	15	2026-01-21	60	2026-01-21 12:00:00-03
684	1	27	2026-01-21	6	2026-01-21 12:00:00-03
691	1	42	2026-01-21	4	2026-01-21 12:00:00-03
693	1	17	2026-01-21	0	2026-01-21 12:00:00-03
694	17	4	2026-01-22	9	2026-01-22 12:00:00-03
695	17	14	2026-01-22	20	2026-01-22 12:00:00-03
696	17	15	2026-01-22	43	2026-01-22 12:00:00-03
697	17	16	2026-01-22	0	2026-01-22 12:00:00-03
698	17	17	2026-01-22	0	2026-01-22 12:00:00-03
699	17	18	2026-01-22	6	2026-01-22 12:00:00-03
700	17	19	2026-01-22	14	2026-01-22 12:00:00-03
701	17	20	2026-01-22	20	2026-01-22 12:00:00-03
702	17	21	2026-01-22	3	2026-01-22 12:00:00-03
703	17	22	2026-01-22	5	2026-01-22 12:00:00-03
704	17	23	2026-01-22	2	2026-01-22 12:00:00-03
705	17	24	2026-01-22	8	2026-01-22 12:00:00-03
706	17	25	2026-01-22	0	2026-01-22 12:00:00-03
707	17	26	2026-01-22	0	2026-01-22 12:00:00-03
708	17	27	2026-01-22	1	2026-01-22 12:00:00-03
709	17	28	2026-01-22	5	2026-01-22 12:00:00-03
710	17	35	2026-01-22	3	2026-01-22 12:00:00-03
711	17	36	2026-01-22	1	2026-01-22 12:00:00-03
712	17	37	2026-01-22	0	2026-01-22 12:00:00-03
713	17	38	2026-01-22	4	2026-01-22 12:00:00-03
714	17	39	2026-01-22	5	2026-01-22 12:00:00-03
715	17	40	2026-01-22	0	2026-01-22 12:00:00-03
716	17	41	2026-01-22	0	2026-01-22 12:00:00-03
717	17	42	2026-01-22	0	2026-01-22 12:00:00-03
718	17	44	2026-01-22	31	2026-01-22 12:00:00-03
719	38	4	2026-01-22	10	2026-01-22 12:00:00-03
720	38	13	2026-01-22	17	2026-01-22 12:00:00-03
721	38	14	2026-01-22	14	2026-01-22 12:00:00-03
722	38	15	2026-01-22	42	2026-01-22 12:00:00-03
723	38	16	2026-01-22	0	2026-01-22 12:00:00-03
724	38	17	2026-01-22	0	2026-01-22 12:00:00-03
725	38	18	2026-01-22	23	2026-01-22 12:00:00-03
726	38	19	2026-01-22	31	2026-01-22 12:00:00-03
727	38	20	2026-01-22	8	2026-01-22 12:00:00-03
728	38	21	2026-01-22	12	2026-01-22 12:00:00-03
729	38	22	2026-01-22	4	2026-01-22 12:00:00-03
730	38	23	2026-01-22	0	2026-01-22 12:00:00-03
731	38	24	2026-01-22	7	2026-01-22 12:00:00-03
732	38	25	2026-01-22	0	2026-01-22 12:00:00-03
733	38	26	2026-01-22	5	2026-01-22 12:00:00-03
734	38	27	2026-01-22	3	2026-01-22 12:00:00-03
735	38	28	2026-01-22	25	2026-01-22 12:00:00-03
736	38	34	2026-01-22	20	2026-01-22 12:00:00-03
737	38	35	2026-01-22	0	2026-01-22 12:00:00-03
738	38	36	2026-01-22	23	2026-01-22 12:00:00-03
739	38	37	2026-01-22	5	2026-01-22 12:00:00-03
740	38	38	2026-01-22	10	2026-01-22 12:00:00-03
741	38	39	2026-01-22	11	2026-01-22 12:00:00-03
742	38	40	2026-01-22	2	2026-01-22 12:00:00-03
743	38	41	2026-01-22	0	2026-01-22 12:00:00-03
744	38	44	2026-01-22	104	2026-01-22 12:00:00-03
745	22	4	2026-01-22	39	2026-01-22 12:00:00-03
746	22	13	2026-01-22	0	2026-01-22 12:00:00-03
747	22	14	2026-01-22	15	2026-01-22 12:00:00-03
748	22	15	2026-01-22	99	2026-01-22 12:00:00-03
749	22	16	2026-01-22	0	2026-01-22 12:00:00-03
750	22	17	2026-01-22	0	2026-01-22 12:00:00-03
751	22	18	2026-01-22	0	2026-01-22 12:00:00-03
752	22	19	2026-01-22	19	2026-01-22 12:00:00-03
753	22	20	2026-01-22	49	2026-01-22 12:00:00-03
754	22	21	2026-01-22	4	2026-01-22 12:00:00-03
755	22	22	2026-01-22	0	2026-01-22 12:00:00-03
756	22	23	2026-01-22	3	2026-01-22 12:00:00-03
757	22	24	2026-01-22	9	2026-01-22 12:00:00-03
758	22	26	2026-01-22	9	2026-01-22 12:00:00-03
759	22	27	2026-01-22	13	2026-01-22 12:00:00-03
760	22	28	2026-01-22	0	2026-01-22 12:00:00-03
761	22	35	2026-01-22	9	2026-01-22 12:00:00-03
762	22	36	2026-01-22	6	2026-01-22 12:00:00-03
763	22	39	2026-01-22	0	2026-01-22 12:00:00-03
764	22	40	2026-01-22	0	2026-01-22 12:00:00-03
765	22	41	2026-01-22	2	2026-01-22 12:00:00-03
766	22	42	2026-01-22	2	2026-01-22 12:00:00-03
767	22	44	2026-01-22	60	2026-01-22 12:00:00-03
768	1	4	2026-01-22	0	2026-01-22 12:00:00-03
769	1	13	2026-01-22	0	2026-01-22 12:00:00-03
770	1	14	2026-01-22	0	2026-01-22 12:00:00-03
771	1	15	2026-01-22	10	2026-01-22 12:00:00-03
772	1	16	2026-01-22	0	2026-01-22 12:00:00-03
773	1	17	2026-01-22	0	2026-01-22 12:00:00-03
774	1	18	2026-01-22	4	2026-01-22 12:00:00-03
775	1	19	2026-01-22	13	2026-01-22 12:00:00-03
776	1	20	2026-01-22	3	2026-01-22 12:00:00-03
777	1	21	2026-01-22	3	2026-01-22 12:00:00-03
778	1	24	2026-01-22	0	2026-01-22 12:00:00-03
779	1	26	2026-01-22	2	2026-01-22 12:00:00-03
780	1	27	2026-01-22	0	2026-01-22 12:00:00-03
781	1	28	2026-01-22	3	2026-01-22 12:00:00-03
782	1	35	2026-01-22	5	2026-01-22 12:00:00-03
783	1	36	2026-01-22	0	2026-01-22 12:00:00-03
784	1	37	2026-01-22	0	2026-01-22 12:00:00-03
785	1	44	2026-01-22	0	2026-01-22 12:00:00-03
786	38	4	2026-01-26	40	2026-01-26 12:00:00-03
787	38	13	2026-01-26	19	2026-01-26 12:00:00-03
788	38	14	2026-01-26	18	2026-01-26 12:00:00-03
789	38	15	2026-01-26	45	2026-01-26 12:00:00-03
790	38	16	2026-01-26	20	2026-01-26 12:00:00-03
791	38	17	2026-01-26	10	2026-01-26 12:00:00-03
792	38	18	2026-01-26	39	2026-01-26 12:00:00-03
793	38	19	2026-01-26	28	2026-01-26 12:00:00-03
794	38	20	2026-01-26	23	2026-01-26 12:00:00-03
795	38	21	2026-01-26	4	2026-01-26 12:00:00-03
796	38	22	2026-01-26	0	2026-01-26 12:00:00-03
797	38	23	2026-01-26	1	2026-01-26 12:00:00-03
798	38	25	2026-01-26	0	2026-01-26 12:00:00-03
799	38	26	2026-01-26	7	2026-01-26 12:00:00-03
800	38	27	2026-01-26	4	2026-01-26 12:00:00-03
801	38	28	2026-01-26	40	2026-01-26 12:00:00-03
802	38	35	2026-01-26	11	2026-01-26 12:00:00-03
803	38	37	2026-01-26	5	2026-01-26 12:00:00-03
804	38	38	2026-01-26	1	2026-01-26 12:00:00-03
805	38	39	2026-01-26	10	2026-01-26 12:00:00-03
806	38	40	2026-01-26	1	2026-01-26 12:00:00-03
807	38	41	2026-01-26	10	2026-01-26 12:00:00-03
808	38	44	2026-01-26	28	2026-01-26 12:00:00-03
809	17	4	2026-01-26	115	2026-01-26 12:00:00-03
810	17	13	2026-01-26	8	2026-01-26 12:00:00-03
811	17	14	2026-01-26	14	2026-01-26 12:00:00-03
812	17	15	2026-01-26	68	2026-01-26 12:00:00-03
813	17	16	2026-01-26	8	2026-01-26 12:00:00-03
814	17	17	2026-01-26	0	2026-01-26 12:00:00-03
815	17	18	2026-01-26	12	2026-01-26 12:00:00-03
816	17	19	2026-01-26	13	2026-01-26 12:00:00-03
817	17	20	2026-01-26	33	2026-01-26 12:00:00-03
818	17	21	2026-01-26	5	2026-01-26 12:00:00-03
819	17	22	2026-01-26	8	2026-01-26 12:00:00-03
820	17	23	2026-01-26	3	2026-01-26 12:00:00-03
821	17	24	2026-01-26	4	2026-01-26 12:00:00-03
822	17	25	2026-01-26	0	2026-01-26 12:00:00-03
823	17	26	2026-01-26	14	2026-01-26 12:00:00-03
824	17	27	2026-01-26	2	2026-01-26 12:00:00-03
825	17	28	2026-01-26	21	2026-01-26 12:00:00-03
826	17	35	2026-01-26	9	2026-01-26 12:00:00-03
827	17	36	2026-01-26	2	2026-01-26 12:00:00-03
828	17	37	2026-01-26	0	2026-01-26 12:00:00-03
829	17	38	2026-01-26	5	2026-01-26 12:00:00-03
830	17	39	2026-01-26	2	2026-01-26 12:00:00-03
831	17	40	2026-01-26	0	2026-01-26 12:00:00-03
832	17	41	2026-01-26	0	2026-01-26 12:00:00-03
833	17	42	2026-01-26	0	2026-01-26 12:00:00-03
834	17	44	2026-01-26	44	2026-01-26 12:00:00-03
835	38	4	2026-01-29	0	2026-01-29 12:00:00-03
836	38	13	2026-01-29	12	2026-01-29 12:00:00-03
837	38	14	2026-01-29	0	2026-01-29 12:00:00-03
838	38	15	2026-01-29	0	2026-01-29 12:00:00-03
839	38	16	2026-01-29	0	2026-01-29 12:00:00-03
840	38	17	2026-01-29	4	2026-01-29 12:00:00-03
841	38	18	2026-01-29	0	2026-01-29 12:00:00-03
842	38	19	2026-01-29	0	2026-01-29 12:00:00-03
843	38	20	2026-01-29	0	2026-01-29 12:00:00-03
844	38	21	2026-01-29	7	2026-01-29 12:00:00-03
845	38	22	2026-01-29	4	2026-01-29 12:00:00-03
846	38	23	2026-01-29	4	2026-01-29 12:00:00-03
847	38	24	2026-01-29	0	2026-01-29 12:00:00-03
848	38	25	2026-01-29	0	2026-01-29 12:00:00-03
849	38	26	2026-01-29	0	2026-01-29 12:00:00-03
850	38	27	2026-01-29	11	2026-01-29 12:00:00-03
851	38	28	2026-01-29	0	2026-01-29 12:00:00-03
852	38	34	2026-01-29	0	2026-01-29 12:00:00-03
853	38	35	2026-01-29	0	2026-01-29 12:00:00-03
854	38	36	2026-01-29	0	2026-01-29 12:00:00-03
855	38	37	2026-01-29	0	2026-01-29 12:00:00-03
856	38	38	2026-01-29	0	2026-01-29 12:00:00-03
857	38	39	2026-01-29	4	2026-01-29 12:00:00-03
858	38	40	2026-01-29	0	2026-01-29 12:00:00-03
859	38	41	2026-01-29	0	2026-01-29 12:00:00-03
860	38	42	2026-01-29	0	2026-01-29 12:00:00-03
861	38	44	2026-01-29	0	2026-01-29 12:00:00-03
862	17	4	2026-01-29	0	2026-01-29 12:00:00-03
863	17	13	2026-01-29	2	2026-01-29 12:00:00-03
864	17	15	2026-01-29	28	2026-01-29 12:00:00-03
865	17	16	2026-01-29	0	2026-01-29 12:00:00-03
866	17	19	2026-01-29	0	2026-01-29 12:00:00-03
867	17	20	2026-01-29	0	2026-01-29 12:00:00-03
868	17	21	2026-01-29	1	2026-01-29 12:00:00-03
869	17	22	2026-01-29	0	2026-01-29 12:00:00-03
870	17	23	2026-01-29	0	2026-01-29 12:00:00-03
871	17	24	2026-01-29	3	2026-01-29 12:00:00-03
872	17	26	2026-01-29	0	2026-01-29 12:00:00-03
873	17	27	2026-01-29	2	2026-01-29 12:00:00-03
874	17	28	2026-01-29	0	2026-01-29 12:00:00-03
875	17	29	2026-01-29	0	2026-01-29 12:00:00-03
876	17	35	2026-01-29	4	2026-01-29 12:00:00-03
877	17	36	2026-01-29	4	2026-01-29 12:00:00-03
878	17	37	2026-01-29	0	2026-01-29 12:00:00-03
879	17	38	2026-01-29	0	2026-01-29 12:00:00-03
880	17	39	2026-01-29	1	2026-01-29 12:00:00-03
881	17	40	2026-01-29	0	2026-01-29 12:00:00-03
882	17	41	2026-01-29	0	2026-01-29 12:00:00-03
883	17	42	2026-01-29	0	2026-01-29 12:00:00-03
884	17	44	2026-01-29	0	2026-01-29 12:00:00-03
885	1	4	2026-01-29	30	2026-01-29 12:00:00-03
886	1	13	2026-01-29	0	2026-01-29 12:00:00-03
887	1	14	2026-01-29	7	2026-01-29 12:00:00-03
888	1	15	2026-01-29	32	2026-01-29 12:00:00-03
889	1	16	2026-01-29	5	2026-01-29 12:00:00-03
890	1	17	2026-01-29	0	2026-01-29 12:00:00-03
891	1	18	2026-01-29	5	2026-01-29 12:00:00-03
892	1	19	2026-01-29	8	2026-01-29 12:00:00-03
893	1	20	2026-01-29	4	2026-01-29 12:00:00-03
894	1	21	2026-01-29	8	2026-01-29 12:00:00-03
895	1	22	2026-01-29	0	2026-01-29 12:00:00-03
896	1	23	2026-01-29	0	2026-01-29 12:00:00-03
897	1	24	2026-01-29	11	2026-01-29 12:00:00-03
898	1	26	2026-01-29	0	2026-01-29 12:00:00-03
899	1	27	2026-01-29	0	2026-01-29 12:00:00-03
900	1	28	2026-01-29	11	2026-01-29 12:00:00-03
901	1	35	2026-01-29	4	2026-01-29 12:00:00-03
902	1	36	2026-01-29	0	2026-01-29 12:00:00-03
903	1	39	2026-01-29	0	2026-01-29 12:00:00-03
904	1	44	2026-01-29	1	2026-01-29 12:00:00-03
905	22	4	2026-01-29	113	2026-01-29 12:00:00-03
906	22	13	2026-01-29	11	2026-01-29 12:00:00-03
907	22	14	2026-01-29	10	2026-01-29 12:00:00-03
908	22	15	2026-01-29	232	2026-01-29 12:00:00-03
909	22	16	2026-01-29	15	2026-01-29 12:00:00-03
910	22	18	2026-01-29	7	2026-01-29 12:00:00-03
911	22	19	2026-01-29	12	2026-01-29 12:00:00-03
912	22	20	2026-01-29	26	2026-01-29 12:00:00-03
913	22	21	2026-01-29	12	2026-01-29 12:00:00-03
914	22	22	2026-01-29	3	2026-01-29 12:00:00-03
915	22	23	2026-01-29	1	2026-01-29 12:00:00-03
916	22	24	2026-01-29	8	2026-01-29 12:00:00-03
917	22	26	2026-01-29	4	2026-01-29 12:00:00-03
918	22	28	2026-01-29	9	2026-01-29 12:00:00-03
919	22	29	2026-01-29	5	2026-01-29 12:00:00-03
920	22	30	2026-01-29	0	2026-01-29 12:00:00-03
921	22	35	2026-01-29	3	2026-01-29 12:00:00-03
922	22	39	2026-01-29	3	2026-01-29 12:00:00-03
923	22	40	2026-01-29	3	2026-01-29 12:00:00-03
924	22	44	2026-01-29	18	2026-01-29 12:00:00-03
925	38	4	2026-02-02	90	2026-02-02 12:00:00-03
926	38	13	2026-02-02	34	2026-02-02 12:00:00-03
927	38	14	2026-02-02	64	2026-02-02 12:00:00-03
928	38	15	2026-02-02	156	2026-02-02 12:00:00-03
929	38	16	2026-02-02	51	2026-02-02 12:00:00-03
930	38	17	2026-02-02	21	2026-02-02 12:00:00-03
931	38	18	2026-02-02	65	2026-02-02 12:00:00-03
932	38	19	2026-02-02	40	2026-02-02 12:00:00-03
933	38	20	2026-02-02	124	2026-02-02 12:00:00-03
934	38	21	2026-02-02	20	2026-02-02 12:00:00-03
935	38	22	2026-02-02	8	2026-02-02 12:00:00-03
936	38	23	2026-02-02	7	2026-02-02 12:00:00-03
937	38	24	2026-02-02	13	2026-02-02 12:00:00-03
938	38	25	2026-02-02	0	2026-02-02 12:00:00-03
939	38	26	2026-02-02	20	2026-02-02 12:00:00-03
940	38	27	2026-02-02	19	2026-02-02 12:00:00-03
941	38	28	2026-02-02	56	2026-02-02 12:00:00-03
942	38	34	2026-02-02	20	2026-02-02 12:00:00-03
943	38	35	2026-02-02	29	2026-02-02 12:00:00-03
944	38	36	2026-02-02	18	2026-02-02 12:00:00-03
945	38	37	2026-02-02	17	2026-02-02 12:00:00-03
946	38	38	2026-02-02	28	2026-02-02 12:00:00-03
947	38	39	2026-02-02	26	2026-02-02 12:00:00-03
948	38	40	2026-02-02	14	2026-02-02 12:00:00-03
949	38	41	2026-02-02	8	2026-02-02 12:00:00-03
950	38	44	2026-02-02	302	2026-02-02 12:00:00-03
951	17	4	2026-02-02	153	2026-02-02 12:00:00-03
952	17	13	2026-02-02	18	2026-02-02 12:00:00-03
953	17	14	2026-02-02	24	2026-02-02 12:00:00-03
954	17	15	2026-02-02	205	2026-02-02 12:00:00-03
955	17	16	2026-02-02	60	2026-02-02 12:00:00-03
956	17	17	2026-02-02	0	2026-02-02 12:00:00-03
957	17	18	2026-02-02	22	2026-02-02 12:00:00-03
958	17	19	2026-02-02	35	2026-02-02 12:00:00-03
959	17	20	2026-02-02	64	2026-02-02 12:00:00-03
960	17	21	2026-02-02	10	2026-02-02 12:00:00-03
961	17	22	2026-02-02	23	2026-02-02 12:00:00-03
962	17	23	2026-02-02	13	2026-02-02 12:00:00-03
963	17	24	2026-02-02	21	2026-02-02 12:00:00-03
964	17	25	2026-02-02	0	2026-02-02 12:00:00-03
965	17	26	2026-02-02	14	2026-02-02 12:00:00-03
966	17	27	2026-02-02	11	2026-02-02 12:00:00-03
967	17	28	2026-02-02	47	2026-02-02 12:00:00-03
968	17	29	2026-02-02	3	2026-02-02 12:00:00-03
969	17	30	2026-02-02	0	2026-02-02 12:00:00-03
970	17	35	2026-02-02	7	2026-02-02 12:00:00-03
971	17	36	2026-02-02	1	2026-02-02 12:00:00-03
972	17	37	2026-02-02	0	2026-02-02 12:00:00-03
973	17	38	2026-02-02	10	2026-02-02 12:00:00-03
974	17	39	2026-02-02	6	2026-02-02 12:00:00-03
975	17	40	2026-02-02	2	2026-02-02 12:00:00-03
976	17	41	2026-02-02	3	2026-02-02 12:00:00-03
977	17	42	2026-02-02	0	2026-02-02 12:00:00-03
978	17	44	2026-02-02	100	2026-02-02 12:00:00-03
979	22	4	2026-02-04	52	2026-02-04 12:00:00-03
980	22	13	2026-02-04	12	2026-02-04 12:00:00-03
981	22	14	2026-02-04	21	2026-02-04 12:00:00-03
982	22	15	2026-02-04	226	2026-02-04 12:00:00-03
983	22	16	2026-02-04	27	2026-02-04 12:00:00-03
984	22	18	2026-02-04	12	2026-02-04 12:00:00-03
985	22	19	2026-02-04	35	2026-02-04 12:00:00-03
986	22	20	2026-02-04	15	2026-02-04 12:00:00-03
987	22	21	2026-02-04	3	2026-02-04 12:00:00-03
988	22	22	2026-02-04	3	2026-02-04 12:00:00-03
989	22	23	2026-02-04	6	2026-02-04 12:00:00-03
990	22	24	2026-02-04	11	2026-02-04 12:00:00-03
991	22	26	2026-02-04	9	2026-02-04 12:00:00-03
992	22	28	2026-02-04	18	2026-02-04 12:00:00-03
993	22	29	2026-02-04	0	2026-02-04 12:00:00-03
994	22	30	2026-02-04	1	2026-02-04 12:00:00-03
995	22	35	2026-02-04	6	2026-02-04 12:00:00-03
996	22	36	2026-02-04	5	2026-02-04 12:00:00-03
997	22	39	2026-02-04	4	2026-02-04 12:00:00-03
998	22	44	2026-02-04	26	2026-02-04 12:00:00-03
999	1	4	2026-02-04	50	2026-02-04 12:00:00-03
1000	1	13	2026-02-04	6	2026-02-04 12:00:00-03
1001	1	14	2026-02-04	15	2026-02-04 12:00:00-03
1002	1	15	2026-02-04	76	2026-02-04 12:00:00-03
1003	1	16	2026-02-04	15	2026-02-04 12:00:00-03
1004	1	18	2026-02-04	7	2026-02-04 12:00:00-03
1005	1	19	2026-02-04	14	2026-02-04 12:00:00-03
1006	1	20	2026-02-04	20	2026-02-04 12:00:00-03
1007	1	21	2026-02-04	1	2026-02-04 12:00:00-03
1008	1	22	2026-02-04	3	2026-02-04 12:00:00-03
1009	1	24	2026-02-04	3	2026-02-04 12:00:00-03
1010	1	26	2026-02-04	4	2026-02-04 12:00:00-03
1011	1	27	2026-02-04	6	2026-02-04 12:00:00-03
1012	1	28	2026-02-04	22	2026-02-04 12:00:00-03
1013	1	35	2026-02-04	3	2026-02-04 12:00:00-03
1014	1	36	2026-02-04	4	2026-02-04 12:00:00-03
1015	1	39	2026-02-04	10	2026-02-04 12:00:00-03
1016	1	44	2026-02-04	28	2026-02-04 12:00:00-03
1017	38	4	2026-02-05	60	2026-02-05 12:00:00-03
1018	38	13	2026-02-05	28	2026-02-05 12:00:00-03
1019	38	14	2026-02-05	23	2026-02-05 12:00:00-03
1020	38	15	2026-02-05	64	2026-02-05 12:00:00-03
1021	38	16	2026-02-05	15	2026-02-05 12:00:00-03
1022	38	17	2026-02-05	6	2026-02-05 12:00:00-03
1023	38	18	2026-02-05	48	2026-02-05 12:00:00-03
1024	38	19	2026-02-05	22	2026-02-05 12:00:00-03
1025	38	20	2026-02-05	28	2026-02-05 12:00:00-03
1026	38	21	2026-02-05	6	2026-02-05 12:00:00-03
1027	38	22	2026-02-05	1	2026-02-05 12:00:00-03
1028	38	23	2026-02-05	3	2026-02-05 12:00:00-03
1029	38	24	2026-02-05	8	2026-02-05 12:00:00-03
1030	38	25	2026-02-05	0	2026-02-05 12:00:00-03
1031	38	26	2026-02-05	8	2026-02-05 12:00:00-03
1032	38	27	2026-02-05	20	2026-02-05 12:00:00-03
1033	38	28	2026-02-05	42	2026-02-05 12:00:00-03
1034	38	30	2026-02-05	1	2026-02-05 12:00:00-03
1035	38	34	2026-02-05	0	2026-02-05 12:00:00-03
1036	38	35	2026-02-05	0	2026-02-05 12:00:00-03
1037	38	36	2026-02-05	18	2026-02-05 12:00:00-03
1038	38	37	2026-02-05	8	2026-02-05 12:00:00-03
1039	38	38	2026-02-05	12	2026-02-05 12:00:00-03
1040	38	39	2026-02-05	17	2026-02-05 12:00:00-03
1041	38	40	2026-02-05	7	2026-02-05 12:00:00-03
1042	38	41	2026-02-05	7	2026-02-05 12:00:00-03
1043	38	44	2026-02-05	142	2026-02-05 12:00:00-03
1044	17	4	2026-02-05	0	2026-02-05 12:00:00-03
1049	17	17	2026-02-05	0	2026-02-05 12:00:00-03
1053	17	21	2026-02-05	0	2026-02-05 12:00:00-03
1057	17	25	2026-02-05	0	2026-02-05 12:00:00-03
1063	17	37	2026-02-05	0	2026-02-05 12:00:00-03
1069	17	44	2026-02-05	0	2026-02-05 12:00:00-03
1045	17	13	2026-02-05	7	2026-02-05 12:00:00-03
1046	17	14	2026-02-05	11	2026-02-05 12:00:00-03
1047	17	15	2026-02-05	44	2026-02-05 12:00:00-03
1048	17	16	2026-02-05	27	2026-02-05 12:00:00-03
1050	17	18	2026-02-05	14	2026-02-05 12:00:00-03
1051	17	19	2026-02-05	17	2026-02-05 12:00:00-03
1052	17	20	2026-02-05	27	2026-02-05 12:00:00-03
1054	17	22	2026-02-05	1	2026-02-05 12:00:00-03
1055	17	23	2026-02-05	3	2026-02-05 12:00:00-03
1056	17	24	2026-02-05	8	2026-02-05 12:00:00-03
1058	17	26	2026-02-05	5	2026-02-05 12:00:00-03
1059	17	27	2026-02-05	57	2026-02-05 12:00:00-03
1060	17	28	2026-02-05	30	2026-02-05 12:00:00-03
1061	17	35	2026-02-05	9	2026-02-05 12:00:00-03
1062	17	36	2026-02-05	3	2026-02-05 12:00:00-03
1064	17	38	2026-02-05	5	2026-02-05 12:00:00-03
1065	17	39	2026-02-05	5	2026-02-05 12:00:00-03
1066	17	40	2026-02-05	1	2026-02-05 12:00:00-03
1067	17	41	2026-02-05	1	2026-02-05 12:00:00-03
1068	17	42	2026-02-05	1	2026-02-05 12:00:00-03
1070	17	29	2026-02-05	0	2026-02-05 12:00:00-03
1071	17	30	2026-02-05	0	2026-02-05 12:00:00-03
1072	1	4	2026-02-05	34	2026-02-05 12:00:00-03
1073	1	13	2026-02-05	3	2026-02-05 12:00:00-03
1074	1	14	2026-02-05	11	2026-02-05 12:00:00-03
1075	1	15	2026-02-05	74	2026-02-05 12:00:00-03
1076	1	16	2026-02-05	7	2026-02-05 12:00:00-03
1077	1	18	2026-02-05	9	2026-02-05 12:00:00-03
1078	1	19	2026-02-05	7	2026-02-05 12:00:00-03
1079	1	20	2026-02-05	11	2026-02-05 12:00:00-03
1080	1	21	2026-02-05	1	2026-02-05 12:00:00-03
1081	1	22	2026-02-05	1	2026-02-05 12:00:00-03
1082	1	24	2026-02-05	4	2026-02-05 12:00:00-03
1083	1	26	2026-02-05	2	2026-02-05 12:00:00-03
1084	1	27	2026-02-05	2	2026-02-05 12:00:00-03
1085	1	28	2026-02-05	7	2026-02-05 12:00:00-03
1086	1	30	2026-02-05	0	2026-02-05 12:00:00-03
1087	1	35	2026-02-05	0	2026-02-05 12:00:00-03
1088	1	36	2026-02-05	3	2026-02-05 12:00:00-03
1089	1	39	2026-02-05	4	2026-02-05 12:00:00-03
1090	1	42	2026-02-05	4	2026-02-05 12:00:00-03
1091	1	44	2026-02-05	21	2026-02-05 12:00:00-03
1092	22	4	2026-02-05	46	2026-02-05 12:00:00-03
1093	22	13	2026-02-05	7	2026-02-05 12:00:00-03
1094	22	14	2026-02-05	12	2026-02-05 12:00:00-03
1095	22	15	2026-02-05	121	2026-02-05 12:00:00-03
1096	22	16	2026-02-05	12	2026-02-05 12:00:00-03
1097	22	18	2026-02-05	6	2026-02-05 12:00:00-03
1098	22	19	2026-02-05	18	2026-02-05 12:00:00-03
1099	22	20	2026-02-05	28	2026-02-05 12:00:00-03
1100	22	21	2026-02-05	3	2026-02-05 12:00:00-03
1101	22	22	2026-02-05	4	2026-02-05 12:00:00-03
1102	22	23	2026-02-05	5	2026-02-05 12:00:00-03
1103	22	24	2026-02-05	7	2026-02-05 12:00:00-03
1104	22	26	2026-02-05	5	2026-02-05 12:00:00-03
1105	22	27	2026-02-05	7	2026-02-05 12:00:00-03
1106	22	28	2026-02-05	17	2026-02-05 12:00:00-03
1107	22	29	2026-02-05	0	2026-02-05 12:00:00-03
1108	22	30	2026-02-05	2	2026-02-05 12:00:00-03
1109	22	36	2026-02-05	0	2026-02-05 12:00:00-03
1110	22	39	2026-02-05	0	2026-02-05 12:00:00-03
1111	22	41	2026-02-05	0	2026-02-05 12:00:00-03
1112	22	42	2026-02-05	0	2026-02-05 12:00:00-03
1113	22	44	2026-02-05	43	2026-02-05 12:00:00-03
\.


--
-- Data for Name: client_stock; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.client_stock (id, cost_center_id, product_id, quantity, last_observed_at, last_zeroed_at) FROM stdin;
110	19	4	11	\N	\N
96	5	38	1	\N	\N
92	5	28	9	\N	\N
88	5	19	12	\N	\N
112	19	13	0	\N	\N
121	20	4	22	\N	\N
122	20	44	30	\N	\N
89	5	20	53	\N	\N
53	10	35	0	\N	\N
307	22	18	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
83	5	44	258	\N	\N
327	17	36	1	2026-02-05 12:00:00-03	\N
12	10	37	2	\N	\N
315	38	4	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
99	5	41	9	\N	\N
309	22	24	7	2026-02-05 12:00:00-03	\N
93	5	35	9	\N	\N
338	22	30	6	2026-02-05 12:00:00-03	\N
100	5	42	8	\N	\N
113	19	16	0	\N	\N
329	17	40	2	2026-02-05 12:00:00-03	\N
98	5	40	6	\N	\N
94	5	36	0	\N	\N
35	3	34	1	\N	\N
16	1	4	9	2026-02-05 12:00:00-03	\N
87	5	18	19	\N	\N
31	7	26	0	\N	\N
328	17	37	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
49	7	24	0	\N	\N
337	17	30	6	2026-02-05 12:00:00-03	\N
140	14	15	8	\N	\N
34	7	39	4	\N	\N
339	1	30	10	2026-02-05 12:00:00-03	\N
90	5	14	27	\N	\N
85	5	16	60	\N	\N
47	7	20	9	\N	\N
114	19	18	0	\N	\N
115	19	19	0	\N	\N
48	7	22	6	\N	\N
84	5	15	141	\N	\N
124	20	13	14	\N	\N
91	5	27	18	\N	\N
141	14	17	0	\N	\N
118	19	28	28	\N	\N
95	5	37	13	\N	\N
120	19	35	4	\N	\N
132	20	14	2	\N	\N
127	20	18	4	\N	\N
13	10	39	6	\N	\N
129	20	20	8	\N	\N
59	2	16	21	\N	\N
119	19	29	5	\N	\N
33	7	38	0	\N	\N
46	7	19	0	\N	\N
143	14	20	3	\N	\N
142	14	18	6	\N	\N
293	1	25	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
317	38	34	20	2026-02-05 12:00:00-03	\N
325	17	21	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
3	10	16	12	\N	\N
294	22	13	2	2026-02-05 12:00:00-03	\N
61	2	18	6	\N	\N
80	4	39	0	\N	\N
56	2	4	32	\N	\N
299	22	4	18	2026-02-05 12:00:00-03	\N
77	4	35	4	\N	\N
134	20	28	23	\N	\N
111	19	44	11	\N	\N
102	7	28	0	\N	\N
101	7	15	25	\N	\N
44	7	17	0	\N	\N
67	2	38	3	\N	\N
68	2	39	2	\N	\N
60	2	17	0	\N	\N
63	2	20	18	\N	\N
9	10	14	2	\N	\N
58	2	15	27	\N	\N
66	2	37	6	\N	\N
64	2	22	14	\N	\N
14	10	40	2	\N	\N
57	2	44	48	\N	\N
79	4	38	4	\N	\N
15	10	41	2	\N	\N
104	8	44	28	\N	\N
81	4	40	1	\N	\N
2	10	44	29	\N	\N
72	4	18	0	\N	\N
76	4	28	3	\N	\N
86	5	17	6	\N	\N
74	4	24	4	\N	\N
326	17	25	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
105	8	20	7	\N	\N
106	8	21	2	\N	\N
275	21	26	10	\N	\N
107	8	28	0	\N	\N
108	8	35	3	\N	\N
109	8	39	0	\N	\N
69	4	4	7	\N	\N
52	10	24	16	\N	\N
117	19	27	4	\N	\N
43	7	16	6	\N	\N
11	10	28	0	\N	\N
71	4	17	3	\N	\N
8	10	23	4	\N	\N
45	7	18	6	\N	\N
70	4	44	16	\N	\N
73	4	20	4	\N	\N
75	4	14	0	\N	\N
78	4	36	0	\N	\N
30	7	44	32	\N	\N
7	10	20	7	\N	\N
5	10	18	0	\N	\N
54	10	36	2	\N	\N
50	10	15	181	\N	\N
135	20	35	3	\N	\N
136	20	39	1	\N	\N
304	22	21	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
6	10	19	54	\N	\N
128	20	19	0	\N	\N
137	20	40	5	\N	\N
130	20	21	0	\N	\N
131	20	22	0	\N	\N
4	10	17	9	\N	\N
51	10	22	6	\N	\N
82	5	4	433	\N	\N
10	10	27	0	\N	\N
125	20	16	15	\N	\N
126	20	17	1	\N	\N
133	20	27	5	\N	\N
97	5	39	2	\N	\N
144	14	22	5	\N	\N
62	2	19	3	\N	\N
332	22	40	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
139	14	44	3	\N	\N
145	14	14	6	\N	\N
123	20	15	44	\N	\N
1	10	4	0	\N	\N
32	7	14	6	\N	\N
55	10	38	4	\N	\N
116	19	20	6	\N	\N
138	14	4	5	\N	\N
65	2	14	11	\N	\N
150	11	4	40	\N	\N
155	11	20	18	\N	\N
160	11	27	5	\N	\N
165	11	41	3	\N	\N
146	14	27	1	\N	\N
276	21	30	4	\N	\N
285	21	25	5	\N	\N
234	6	19	6	\N	\N
239	6	39	5	\N	\N
209	5	24	6	\N	\N
246	5	25	2	\N	\N
273	2	21	6	\N	\N
282	8	19	7	\N	\N
211	7	37	4	\N	\N
290	10	13	27	\N	\N
17	1	44	5	2026-02-05 12:00:00-03	\N
18	1	16	8	2026-02-05 12:00:00-03	\N
19	1	18	3	2026-02-05 12:00:00-03	\N
20	1	20	20	2026-02-05 12:00:00-03	\N
21	1	26	2	2026-02-05 12:00:00-03	\N
22	1	14	11	2026-02-05 12:00:00-03	\N
23	1	28	13	2026-02-05 12:00:00-03	\N
24	1	35	7	2026-02-05 12:00:00-03	\N
26	1	39	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
36	1	15	32	2026-02-05 12:00:00-03	\N
38	1	24	5	2026-02-05 12:00:00-03	\N
39	1	27	10	2026-02-05 12:00:00-03	\N
40	1	36	3	2026-02-05 12:00:00-03	\N
42	1	19	9	2026-02-05 12:00:00-03	\N
292	1	13	11	2026-02-05 12:00:00-03	\N
25	1	38	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
27	1	40	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
28	1	41	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
37	1	17	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
41	1	37	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
295	22	27	2	2026-02-05 12:00:00-03	\N
300	22	44	1	2026-02-05 12:00:00-03	\N
305	22	14	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
308	22	22	2	2026-02-05 12:00:00-03	\N
311	22	29	5	2026-02-05 12:00:00-03	\N
333	22	41	3	2026-02-05 12:00:00-03	\N
334	22	42	3	2026-02-05 12:00:00-03	\N
335	22	23	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
251	38	17	11	2026-02-05 12:00:00-03	\N
256	38	23	7	2026-02-05 12:00:00-03	\N
261	38	28	12	2026-02-05 12:00:00-03	\N
266	38	39	8	2026-02-05 12:00:00-03	\N
316	38	19	15	2026-02-05 12:00:00-03	\N
318	38	36	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
330	38	27	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
340	38	30	9	2026-02-05 12:00:00-03	\N
331	38	42	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
217	17	15	15	2026-02-05 12:00:00-03	\N
219	17	16	4	2026-02-05 12:00:00-03	\N
222	17	26	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
224	17	27	2	2026-02-05 12:00:00-03	\N
227	17	38	3	2026-02-05 12:00:00-03	\N
229	17	42	2	2026-02-05 12:00:00-03	\N
323	17	39	1	2026-02-05 12:00:00-03	\N
147	14	28	10	\N	\N
151	11	44	32	\N	\N
156	11	21	5	\N	\N
161	11	28	15	\N	\N
210	5	26	8	\N	\N
280	21	40	5	\N	\N
277	21	35	4	\N	\N
230	6	4	40	\N	\N
235	6	20	18	\N	\N
240	6	40	5	\N	\N
242	19	30	2	\N	\N
336	1	42	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
296	22	28	15	2026-02-05 12:00:00-03	\N
286	8	15	22	\N	\N
274	4	22	10	\N	\N
291	10	42	1	\N	\N
29	7	4	24	\N	\N
213	7	41	3	\N	\N
301	22	15	19	2026-02-05 12:00:00-03	\N
306	22	19	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
310	22	26	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
247	38	44	13	2026-02-05 12:00:00-03	\N
252	38	18	2	2026-02-05 12:00:00-03	\N
257	38	24	24	2026-02-05 12:00:00-03	\N
262	38	35	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
267	38	40	9	2026-02-05 12:00:00-03	\N
215	17	4	84	2026-02-05 12:00:00-03	\N
269	17	17	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
220	17	20	13	2026-02-05 12:00:00-03	\N
225	17	28	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
319	17	19	6	2026-02-05 12:00:00-03	\N
148	14	39	3	\N	\N
152	11	15	25	\N	\N
157	11	22	6	\N	\N
162	11	35	6	\N	\N
278	21	36	5	\N	\N
231	6	44	16	\N	\N
236	6	14	8	\N	\N
241	6	42	3	\N	\N
302	22	16	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
314	22	36	1	2026-02-05 12:00:00-03	\N
324	22	39	4	2026-02-05 12:00:00-03	\N
212	7	40	0	\N	\N
281	8	18	2	\N	\N
287	8	16	2	\N	\N
243	5	21	55	\N	\N
297	22	35	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
312	22	17	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
313	22	25	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
248	38	15	59	2026-02-05 12:00:00-03	\N
253	38	20	41	2026-02-05 12:00:00-03	\N
258	38	26	12	2026-02-05 12:00:00-03	\N
268	38	41	4	2026-02-05 12:00:00-03	\N
263	38	29	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
218	17	13	5	2026-02-05 12:00:00-03	\N
223	17	14	1	2026-02-05 12:00:00-03	\N
228	17	41	2	2026-02-05 12:00:00-03	\N
270	17	18	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
320	17	22	3	2026-02-05 12:00:00-03	\N
149	14	40	3	\N	\N
153	11	16	12	\N	\N
158	11	24	6	\N	\N
163	11	37	3	\N	\N
232	6	15	17	\N	\N
237	6	28	20	\N	\N
244	5	22	5	\N	\N
271	20	30	9	\N	\N
279	21	37	4	\N	\N
214	7	42	4	\N	\N
283	8	26	1	\N	\N
288	8	24	4	\N	\N
103	8	4	2	\N	\N
303	22	20	6	2026-02-05 12:00:00-03	\N
298	22	37	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
249	38	13	2	2026-02-05 12:00:00-03	\N
254	38	21	26	2026-02-05 12:00:00-03	\N
259	38	25	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
264	38	37	1	2026-02-05 12:00:00-03	\N
321	17	23	3	2026-02-05 12:00:00-03	\N
154	11	18	6	\N	\N
159	11	14	12	\N	\N
164	11	39	3	\N	\N
172	1	21	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
272	1	22	6	2026-02-05 12:00:00-03	\N
171	1	23	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
250	38	16	27	2026-02-05 12:00:00-03	\N
207	19	17	6	\N	\N
174	4	16	12	\N	\N
255	38	22	11	2026-02-05 12:00:00-03	\N
260	38	14	26	2026-02-05 12:00:00-03	\N
265	38	38	7	2026-02-05 12:00:00-03	\N
216	17	44	49	2026-02-05 12:00:00-03	\N
221	17	24	10	2026-02-05 12:00:00-03	\N
226	17	29	2	2026-02-05 12:00:00-03	\N
322	17	35	0	2026-02-05 12:00:00-03	2026-02-05 12:00:00-03
201	21	42	3	\N	\N
205	20	42	2	\N	\N
184	21	4	12	\N	\N
185	21	44	17	\N	\N
186	21	15	51	\N	\N
233	6	18	6	\N	\N
187	21	13	8	\N	\N
188	21	16	15	\N	\N
238	6	38	4	\N	\N
189	21	17	2	\N	\N
190	21	18	4	\N	\N
206	19	15	30	\N	\N
208	19	24	6	\N	\N
245	5	23	4	\N	\N
191	21	20	9	\N	\N
193	21	24	1	\N	\N
194	21	14	3	\N	\N
195	21	27	4	\N	\N
196	21	28	22	\N	\N
197	21	29	4	\N	\N
198	21	38	5	\N	\N
202	20	24	2	\N	\N
204	20	41	2	\N	\N
203	20	38	0	\N	\N
199	21	39	5	\N	\N
200	21	41	1	\N	\N
169	2	28	9	\N	\N
170	2	41	1	\N	\N
166	2	23	8	\N	\N
167	2	26	14	\N	\N
168	2	27	10	\N	\N
192	21	23	20	\N	\N
289	8	25	2	\N	\N
284	8	14	0	\N	\N
173	4	15	16	\N	\N
175	4	19	8	\N	\N
176	4	21	10	\N	\N
178	4	26	1	\N	\N
177	4	23	7	\N	\N
179	4	27	7	\N	\N
180	4	41	4	\N	\N
181	4	42	1	\N	\N
183	10	26	1	\N	\N
182	10	21	2	\N	\N
\.


--
-- Data for Name: cost_centers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cost_centers (id, name, description, retail_chain_id, is_active, deleted_at) FROM stdin;
1	REX (1)	\N	1	t	\N
2	REX (2)	\N	1	t	\N
3	REX (3)	\N	1	t	\N
4	REX (4)	\N	1	t	\N
5	REX (5)	\N	1	t	\N
6	REX (6)	\N	1	t	\N
7	REX (7)	\N	1	t	\N
8	REX (14)	\N	1	t	\N
9	REX (15)	\N	1	t	\N
10	REX (17)	\N	1	t	\N
11	REX (18)	\N	1	t	\N
12	REX (25)	\N	1	t	\N
13	REX (30)	\N	1	t	\N
14	REX (31)	\N	1	t	\N
15	REX (13)	\N	1	t	\N
16	REX (21)	\N	1	t	\N
17	BH (189)	Lavras 	2	t	\N
18	BH (190)	LAVRAS	2	t	\N
19	BH (191)	FACULDADE - TRÊS CORAÇÕES	2	t	\N
20	BH (192)	TRÊS CORAÇÕES - RODOVIÁRIA 	2	t	\N
21	BH (194)	TRÊS CORAÇÕES - POLICIA CIVIL	2	t	\N
22	BH (343)	LAVRAS CENTRO	2	t	\N
23	BH (197)	VARGINHA - SHOPPING	2	t	\N
24	BH (291)	VARGINHA - ATACADO	2	t	\N
25	BH (239)	POUSO ALEGRE - SHOPPING	2	t	\N
26	BH (340)	POUSO ALEGRE - PERIMETRAL	2	t	\N
27	BH (195)	TRÊS PONTAS 	2	t	\N
28	BH (341)	POÇOS - ZONA LESTE	2	t	\N
29	BH (342)	POÇOS - CENTRO	2	t	\N
30	BH (376)	VARGINHA - REZENDE	2	t	\N
31	BH (377)	VARGINHA - CENTRO	2	t	\N
32	BH (263)	TRÊS CORAÇÕES - ATACADO PELÉZÃO	2	t	\N
33	ABC (23)	LAVRAS - DISTRITO	4	t	\N
34	ABC (78)	PERDÕES	4	t	\N
35	ABC (27)	VARGINHA	4	t	\N
36	ABC (73)	LAVRAS - RODOVIÁRIA	4	t	\N
37	ABC (54)	TRÊS CORAÇÕES - ATACADO	4	t	\N
38	VILLE FORTE (48)	LAVRAS	3	t	\N
39	VILLE FORTE (46)	POÇOS DE CALDAS	3	t	\N
40	MINEIRÃO (156)	VARGINHA	6	t	\N
\.


--
-- Data for Name: inventory_stock; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.inventory_stock (id, product_id, quantity) FROM stdin;
4	32	224
3	35	552
1	5	2912
7	31	1000
12	25	1000
15	29	960
17	17	689
23	21	622
22	26	749
32	34	8
30	36	818
29	37	816
28	38	705
10	30	3979
31	42	1956
5	4	9333
2	44	12083
6	15	176
9	13	472
14	16	13
21	18	84
19	19	70
24	20	2767
20	22	797
11	23	858
16	24	503
18	14	1962
8	28	9528
27	39	589
13	27	623
26	40	839
25	41	865
\.


--
-- Data for Name: inventory_visit_products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.inventory_visit_products (id, inventory_visit_id, product_id, stock_quantity, sales_quantity, loss_quantity, next_quantity, shelf_price, previous_client_stock, requested_quantity) FROM stdin;
721	30	4	0	0	0	\N	\N	0	10
722	30	44	15	0	0	\N	5.89	0	144
723	30	13	5	12	0	\N	8.98	17	40
724	30	15	62	0	0	\N	6.89	62	50
725	30	16	27	0	0	\N	9.98	17	12
726	30	17	14	4	0	\N	11.98	18	12
727	30	18	0	0	0	\N	\N	0	48
728	30	19	25	0	0	\N	8.98	13	24
729	30	20	67	0	0	\N	7.58	23	2
730	30	21	16	7	0	\N	8.98	23	1
731	30	22	16	4	0	\N	8.98	20	12
732	30	23	2	4	0	\N	8.48	6	10
733	30	24	23	0	0	\N	9.98	0	1
734	30	25	0	0	0	\N	\N	0	0
735	30	26	19	0	0	\N	12.89	17	8
736	30	14	17	0	0	\N	11.98	2	2
737	30	27	9	11	0	\N	8.49	20	10
738	30	28	20	0	0	\N	7.98	8	1
739	30	34	0	0	0	\N	\N	0	20
740	30	35	13	0	0	\N	11.99	7	8
741	30	36	7	0	0	\N	11.99	0	1
742	30	37	8	0	0	\N	6.98	0	2
743	30	38	2	0	0	\N	8.98	0	4
744	30	40	12	0	0	\N	8.98	8	1
745	30	41	1	0	0	\N	8.98	0	3
746	30	39	6	4	0	\N	8.98	10	3
747	30	42	0	0	0	\N	\N	0	0
771	32	4	21	30	0	\N	12.49	51	32
772	32	44	6	1	0	\N	\N	7	16
773	32	15	7	32	0	\N	\N	39	100
774	32	13	5	0	0	\N	\N	5	5
775	32	16	25	5	0	\N	\N	30	6
776	32	17	0	0	0	\N	\N	0	6
777	32	18	1	5	0	\N	\N	6	6
778	32	19	0	8	0	\N	\N	8	18
779	32	20	15	4	0	\N	\N	19	18
780	32	21	2	8	0	\N	\N	10	12
781	32	22	6	0	0	\N	\N	6	0
782	32	26	8	0	0	\N	\N	7	0
783	32	23	0	0	0	\N	\N	0	6
784	32	24	0	11	0	\N	\N	11	12
785	32	14	13	7	0	\N	\N	20	18
786	32	27	13	0	0	\N	\N	11	0
787	32	28	12	11	0	\N	\N	23	0
788	32	35	2	4	0	\N	\N	5	5
789	32	36	6	0	0	\N	\N	4	0
790	32	39	4	0	0	\N	\N	4	9
885	37	4	3	50	0	\N	\N	53	32
886	37	44	2	28	0	\N	\N	30	24
887	37	15	56	76	0	\N	\N	132	50
888	37	13	4	6	0	\N	\N	10	5
889	37	16	15	15	0	\N	\N	30	6
890	37	18	6	7	0	\N	\N	13	6
891	37	19	4	14	0	\N	\N	18	24
892	37	20	13	20	0	\N	\N	33	27
893	37	21	1	1	0	\N	\N	2	12
894	37	22	3	3	0	\N	\N	6	6
895	37	24	3	3	0	\N	\N	6	6
896	37	26	4	4	0	\N	\N	8	6
897	37	14	10	15	0	\N	\N	25	12
898	37	27	7	6	0	\N	\N	13	0
899	37	28	0	22	0	\N	\N	22	15
900	37	35	3	3	0	\N	\N	6	6
901	37	36	2	4	0	\N	\N	6	6
902	37	39	0	10	0	\N	\N	10	9
1003	42	4	18	46	0	\N	\N	64	40
1004	42	44	1	43	0	\N	\N	44	32
1005	42	15	19	121	0	\N	\N	140	100
1006	42	13	2	7	0	\N	\N	9	10
1007	42	16	0	12	0	\N	\N	12	12
1008	42	18	0	6	0	\N	\N	6	6
1009	42	19	0	18	0	\N	\N	18	18
1010	42	20	6	28	0	\N	\N	34	10
1011	42	21	0	3	0	\N	\N	3	6
1012	42	22	2	4	0	\N	\N	6	6
1013	42	23	0	5	0	\N	\N	5	0
1014	42	24	7	7	0	\N	\N	14	6
1015	42	26	0	5	0	\N	\N	5	0
1016	42	14	0	12	0	\N	\N	12	18
1017	42	27	2	7	0	\N	\N	9	0
1018	42	28	15	17	0	\N	\N	32	0
1019	42	29	5	0	0	\N	\N	5	0
1020	42	30	6	2	0	\N	\N	8	0
1021	42	36	1	0	0	\N	\N	1	0
1022	42	39	4	0	0	\N	\N	4	0
1023	42	41	3	0	0	\N	\N	3	0
1024	42	42	3	0	0	\N	\N	3	0
748	31	4	13	0	0	\N	12.90	11	0
749	31	44	8	0	0	\N	12.90	5	0
750	31	13	0	2	0	\N	\N	2	0
751	31	16	31	0	0	\N	10.90	16	0
752	31	19	4	0	0	\N	8.90	3	0
753	31	20	17	0	0	\N	8.90	16	0
754	31	22	15	0	0	\N	8.45	14	0
755	31	26	8	0	0	\N	14.90	2	0
756	31	27	5	2	0	\N	11.90	7	0
757	31	28	12	0	0	\N	7.45	4	0
758	31	35	0	4	0	\N	\N	4	0
759	31	36	0	4	0	\N	\N	4	0
760	31	38	3	0	0	\N	9.45	2	0
761	31	39	2	1	0	\N	8.45	3	0
762	31	24	6	3	0	\N	9.90	9	0
763	31	21	4	1	0	\N	8.45	5	0
764	31	15	89	28	0	\N	5.29	117	0
765	31	23	3	0	0	\N	6.90	0	0
766	31	29	3	0	0	\N	\N	0	0
767	31	40	0	0	0	\N	\N	0	0
768	31	37	0	0	0	\N	\N	0	0
769	31	41	0	0	0	\N	\N	0	0
770	31	42	0	0	0	\N	\N	0	0
903	38	20	41	28	0	\N	7.58	69	40
904	38	4	0	60	0	\N	\N	60	15
905	38	44	13	142	5	\N	5.89	160	160
906	38	15	59	64	8	\N	6.69	131	54
907	38	13	2	28	1	\N	8.98	31	30
908	38	16	27	15	0	\N	9.98	42	12
909	38	17	11	6	0	\N	11.98	17	12
910	38	18	2	48	0	\N	\N	50	72
911	38	19	15	22	8	\N	8.98	45	24
912	38	21	26	6	0	\N	8.98	32	0
913	38	22	11	1	2	\N	8.98	14	12
914	38	23	7	3	0	\N	8.98	10	10
915	38	24	24	8	2	\N	9.98	34	12
916	38	25	0	0	0	\N	\N	0	0
917	38	26	12	8	3	\N	12.89	23	9
918	38	14	26	23	0	\N	11.98	49	48
919	38	27	0	20	0	\N	8.49	20	20
920	38	28	12	42	0	\N	7.98	54	40
921	38	30	9	1	0	\N	7.98	10	10
922	38	34	20	0	0	\N	6.99	20	20
923	38	35	0	0	0	\N	11.99	0	0
924	38	36	0	18	0	\N	11.99	18	20
925	38	37	1	8	0	\N	6.98	9	20
926	38	38	7	12	0	\N	8.98	19	18
927	38	39	8	17	0	\N	8.98	25	18
928	38	40	9	7	0	\N	8.98	16	18
929	38	41	4	7	0	\N	8.98	11	18
791	33	4	12	113	0	\N	\N	125	80
792	33	44	22	18	0	\N	\N	40	48
793	33	15	91	232	0	\N	\N	323	150
794	33	13	2	11	0	\N	\N	13	10
795	33	16	3	15	0	\N	\N	18	18
796	33	18	6	7	0	\N	\N	13	0
797	33	19	11	12	0	\N	\N	23	18
798	33	20	12	26	0	\N	\N	38	27
799	33	21	0	12	0	\N	\N	12	6
800	33	22	3	3	0	\N	\N	6	0
801	33	23	1	1	0	\N	\N	2	6
802	33	24	1	8	0	\N	\N	9	6
803	33	26	6	4	0	\N	\N	10	0
804	33	14	3	10	0	\N	\N	13	18
805	33	28	10	9	0	\N	\N	19	0
806	33	29	0	5	0	\N	\N	5	6
807	33	35	0	3	0	\N	\N	3	6
808	33	39	0	3	0	\N	\N	3	4
809	33	40	0	3	0	\N	\N	3	0
810	33	30	1	0	0	\N	\N	0	8
930	39	4	84	0	0	\N	\N	84	0
931	39	44	49	0	0	\N	\N	49	0
932	39	15	59	0	0	\N	\N	59	0
933	39	13	12	0	0	\N	\N	12	0
934	39	16	31	0	0	\N	\N	31	0
935	39	17	0	0	0	\N	\N	0	0
936	39	18	14	0	0	\N	\N	14	0
937	39	19	23	0	0	\N	\N	23	0
938	39	20	40	0	0	\N	\N	40	0
939	39	21	0	0	0	\N	\N	0	0
940	39	22	4	0	0	\N	\N	4	0
941	39	23	6	0	0	\N	\N	6	0
942	39	24	18	0	0	\N	\N	18	0
943	39	25	0	0	0	\N	\N	0	0
944	39	26	5	0	0	\N	\N	5	0
945	39	14	12	0	0	\N	\N	12	0
946	39	27	59	0	0	\N	\N	4	0
947	39	28	30	0	0	\N	\N	30	0
948	39	35	9	0	0	\N	\N	9	0
949	39	36	4	0	0	\N	\N	4	0
950	39	37	0	0	0	\N	\N	0	0
951	39	38	8	0	0	\N	\N	8	0
952	39	39	6	0	0	\N	\N	6	0
953	39	40	3	0	0	\N	\N	3	0
954	39	41	3	0	0	\N	\N	3	0
955	39	42	3	0	0	\N	\N	3	0
811	34	4	0	90	0	\N	6.99	90	15
812	34	44	0	302	1	\N	\N	303	160
813	34	15	31	156	0	\N	6.89	187	100
814	34	36	9	18	0	\N	11.99	27	1
815	34	26	13	20	0	\N	12.89	33	16
816	34	35	0	29	0	\N	11.99	29	0
817	34	28	14	56	0	\N	7.98	70	2
818	34	22	14	8	0	\N	8.98	22	24
819	34	24	10	13	0	\N	9.98	23	24
820	34	21	8	20	0	\N	8.98	28	24
821	34	19	21	40	0	\N	8.98	61	48
822	34	16	18	51	0	\N	9.98	69	1
823	34	39	7	26	0	\N	8.98	33	3
824	34	41	2	8	0	\N	8.98	10	2
825	34	40	16	14	0	\N	8.98	30	0
826	34	38	1	28	0	\N	8.98	29	4
827	34	17	5	21	0	\N	11.98	26	24
828	34	20	51	124	0	\N	7.58	175	2
829	34	13	11	34	0	\N	8.98	45	2
830	34	18	0	65	0	\N	\N	65	60
831	34	34	0	20	0	\N	\N	20	20
832	34	37	0	17	0	\N	\N	17	3
833	34	23	0	7	0	\N	\N	7	20
834	34	14	1	64	0	\N	\N	65	4
835	34	27	0	19	0	\N	\N	19	1
836	34	25	0	0	0	\N	\N	0	0
837	35	4	0	153	0	\N	19.90	153	0
838	35	44	1	100	0	\N	12.90	101	0
839	35	15	59	205	0	\N	5.29	264	0
840	35	13	2	18	0	\N	14.90	20	0
841	35	16	19	60	0	\N	10.90	79	0
842	35	17	0	0	0	\N	\N	0	0
843	35	18	2	22	0	\N	\N	24	0
844	35	19	5	35	0	\N	8.90	40	0
845	35	20	7	64	0	\N	8.90	71	0
846	35	21	0	10	0	\N	\N	10	0
847	35	22	4	23	0	\N	8.45	27	0
848	35	24	6	21	0	\N	9.90	27	0
849	35	25	0	0	0	\N	\N	0	0
850	35	26	5	14	0	\N	14.90	19	0
851	35	14	0	24	0	\N	17.90	24	0
852	35	27	4	11	0	\N	11.90	15	0
853	35	28	10	47	0	\N	7.45	57	0
854	35	35	1	7	0	\N	\N	8	0
855	35	36	4	1	0	\N	12.90	5	0
856	35	37	0	0	0	\N	\N	0	0
857	35	38	4	10	0	\N	\N	14	0
858	35	39	1	6	0	\N	\N	7	0
859	35	40	3	2	0	\N	9.45	5	0
860	35	41	0	3	0	\N	9.45	3	0
861	35	42	3	0	0	\N	9.45	3	0
862	35	23	1	13	0	\N	6.90	14	0
863	35	29	5	3	0	\N	7.45	8	0
864	35	30	7	0	0	\N	9.90	5	0
956	40	4	84	0	0	\N	12.90	84	0
957	40	44	49	0	0	\N	12.90	49	0
958	40	15	15	44	0	\N	5.29	59	0
959	40	13	5	7	0	\N	14.90	12	0
960	40	20	13	27	0	\N	8.90	40	0
961	40	16	4	27	0	\N	10.90	31	0
962	40	19	6	17	0	\N	8.90	23	0
963	40	27	2	57	0	\N	11.90	59	0
964	40	29	2	0	0	\N	7.45	0	0
965	40	23	3	3	0	\N	6.90	6	0
966	40	24	10	8	0	\N	9.90	18	0
967	40	38	3	5	0	\N	9.45	8	0
968	40	39	1	5	0	\N	9.45	6	0
969	40	40	2	1	0	\N	9.45	3	0
970	40	41	2	1	0	\N	9.45	3	0
971	40	42	2	1	0	\N	9.45	3	0
972	40	22	3	1	0	\N	8.45	4	0
973	40	36	1	3	0	\N	12.90	4	0
974	40	30	6	0	0	\N	9.90	0	0
975	40	17	0	0	0	\N	13.90	0	0
976	40	18	0	14	0	\N	8.90	14	0
977	40	21	0	0	0	\N	8.45	0	0
978	40	25	0	0	0	\N	6.90	0	0
979	40	26	0	5	0	\N	14.90	5	0
980	40	14	1	11	0	\N	14.90	12	0
981	40	28	0	30	0	\N	7.45	30	0
982	40	35	0	9	0	\N	13.90	9	0
983	41	4	9	34	0	\N	\N	43	15
984	41	44	5	21	0	\N	\N	26	32
985	41	15	32	74	0	\N	\N	106	50
986	41	13	11	3	0	\N	\N	14	6
987	41	16	8	7	0	\N	\N	15	12
988	41	18	3	9	0	\N	\N	12	12
989	41	19	9	7	0	\N	\N	16	18
672	28	4	0	40	0	\N	6.99	40	10
673	28	44	0	28	0	\N	5.98	28	144
674	28	15	62	45	0	\N	6.89	107	50
675	28	13	17	19	0	\N	8.98	36	2
676	28	16	17	20	0	\N	9.98	37	24
677	28	17	18	10	0	\N	11.98	28	12
678	28	18	0	39	0	\N	4.89	39	3
679	28	19	13	28	0	\N	8.98	41	48
680	28	20	23	23	0	\N	5.00	46	5
681	28	21	23	4	0	\N	8.98	27	12
682	28	22	20	0	0	\N	8.98	20	0
683	28	23	6	1	0	\N	8.48	7	24
684	28	25	0	0	0	\N	\N	0	0
685	28	26	17	7	0	\N	12.89	24	8
686	28	14	2	18	0	\N	11.98	20	4
687	28	27	20	4	0	\N	8.49	24	0
688	28	28	8	40	0	\N	7.98	48	1
689	28	35	7	11	0	\N	11.99	18	1
690	28	37	0	5	0	\N	6.98	5	2
691	28	38	0	1	0	\N	8.98	1	2
692	28	39	10	10	0	\N	8.98	20	2
693	28	40	8	1	0	\N	8.98	9	2
694	28	41	0	10	0	\N	8.98	10	2
695	29	4	11	115	0	\N	\N	126	0
696	29	44	5	44	0	\N	\N	49	0
697	29	15	117	68	0	\N	\N	185	0
698	29	13	2	8	0	\N	\N	10	0
699	29	16	16	8	0	\N	\N	24	0
700	29	17	0	0	0	\N	\N	0	0
701	29	18	0	12	0	\N	\N	12	0
702	29	19	3	13	0	\N	\N	16	0
703	29	20	16	33	0	\N	\N	49	0
704	29	21	5	5	0	\N	\N	10	0
705	29	22	14	8	0	\N	\N	22	0
706	29	23	0	3	0	\N	\N	3	0
707	29	24	9	4	0	\N	\N	13	0
708	29	25	0	0	0	\N	\N	0	0
709	29	26	2	14	0	\N	\N	16	0
710	29	14	0	14	0	\N	\N	14	0
711	29	27	7	2	0	\N	\N	9	0
712	29	28	4	21	0	\N	\N	25	0
713	29	35	4	9	0	\N	\N	13	0
714	29	36	4	2	0	\N	\N	6	0
715	29	37	0	0	0	\N	\N	0	0
716	29	38	2	5	0	\N	\N	7	0
717	29	39	3	2	0	\N	\N	5	0
718	29	40	0	0	0	\N	\N	0	0
719	29	41	0	0	0	\N	\N	0	0
720	29	42	0	0	0	\N	\N	0	0
865	36	4	0	52	0	\N	\N	52	40
866	36	44	28	26	0	\N	\N	54	16
867	36	15	40	226	0	\N	\N	266	100
868	36	13	0	12	0	\N	\N	12	5
869	36	16	0	27	0	\N	\N	27	24
870	36	18	0	12	0	\N	\N	12	6
871	36	19	0	35	0	\N	\N	35	24
872	36	20	24	15	0	\N	\N	39	18
873	36	21	3	3	0	\N	\N	6	12
874	36	22	0	3	0	\N	\N	3	6
875	36	23	0	6	0	\N	\N	6	5
876	36	24	2	11	0	\N	\N	13	12
877	36	26	5	9	0	\N	\N	14	0
878	36	14	0	21	0	\N	\N	21	18
879	36	28	12	18	0	\N	\N	30	20
880	36	29	5	0	0	\N	\N	5	0
881	36	30	8	1	0	\N	\N	9	0
882	36	35	0	6	0	\N	\N	6	0
883	36	36	1	5	0	\N	\N	6	0
884	36	39	0	4	0	\N	\N	4	4
990	41	20	20	11	0	\N	\N	31	18
991	41	21	0	1	0	\N	\N	1	12
992	41	22	6	1	0	\N	\N	7	0
993	41	24	5	4	0	\N	\N	9	6
994	41	26	2	2	0	\N	\N	4	4
995	41	14	11	11	0	\N	\N	22	18
996	41	27	10	2	0	\N	\N	12	0
997	41	28	13	7	0	\N	\N	20	25
998	41	30	10	0	0	\N	\N	10	0
999	41	35	7	0	0	\N	\N	7	8
1000	41	36	3	3	0	\N	\N	6	8
1001	41	39	0	4	0	\N	\N	4	9
1002	41	42	0	4	0	\N	\N	4	4
\.


--
-- Data for Name: inventory_visits; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.inventory_visits (id, cost_center_id, ticket_id, recorded_by, visited_at, total_stock_quantity, notes) FROM stdin;
28	38	169	5	2026-01-26 12:00:00-03	271	Registro gerado automaticamente via formulario de vendas
29	17	168	5	2026-01-26 12:00:00-03	224	Registro gerado automaticamente via formulario de vendas
30	38	169	5	2026-01-29 12:00:00-03	386	Registro gerado automaticamente via formulario de vendas
31	17	168	5	2026-01-29 12:00:00-03	223	Registro gerado automaticamente via formulario de vendas
32	1	174	6	2026-01-29 12:00:00-03	146	Registro gerado automaticamente via formulario de vendas
33	22	176	6	2026-01-29 12:00:00-03	184	Registro gerado automaticamente via formulario de vendas
34	38	178	5	2026-02-02 12:00:00-03	232	Registro gerado automaticamente via formulario de vendas
35	17	179	5	2026-02-02 12:00:00-03	153	Registro gerado automaticamente via formulario de vendas
36	22	181	6	2026-02-04 12:00:00-03	128	Registro gerado automaticamente via formulario de vendas
37	1	180	6	2026-02-04 12:00:00-03	136	Registro gerado automaticamente via formulario de vendas
38	38	182	5	2026-02-05 12:00:00-03	346	Registro gerado automaticamente via formulario de vendas
39	17	183	5	2026-02-05 12:00:00-03	482	Registro gerado automaticamente via formulario de vendas
40	17	183	5	2026-02-05 12:00:00-03	214	Registro gerado automaticamente via formulario de vendas
41	1	185	6	2026-02-05 12:00:00-03	164	Registro gerado automaticamente via formulario de vendas
42	22	184	6	2026-02-05 12:00:00-03	94	Registro gerado automaticamente via formulario de vendas
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.permissions (id, name, description) FROM stdin;
\.


--
-- Data for Name: product_cost_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.product_cost_history (id, product_id, cost, start_date, end_date) FROM stdin;
1	5	2.50	2025-09-10 17:34:48.761338	2025-09-10 17:34:57.963505
2	5	2.50	2025-09-10 17:34:57.963527	2025-09-10 17:35:08.563558
5	35	6.00	2025-09-10 17:52:01.947313	\N
4	44	2.50	2025-09-10 17:44:38.003057	2025-09-10 17:55:49.94087
7	32	2.80	2025-09-10 17:57:11.267408	\N
6	44	2.68	2025-09-10 17:55:49.940887	2025-09-10 17:58:35.016388
10	15	3.00	2025-09-10 17:59:58.214319	2025-09-10 18:00:08.955931
11	15	3.00	2025-09-10 18:00:08.955944	2025-09-10 18:00:23.050373
3	5	2.50	2025-09-10 17:35:08.56358	2025-09-10 18:02:29.095535
13	5	2.55	2025-09-10 18:02:29.095559	2025-09-10 18:02:46.019473
14	5	2.58	2025-09-10 18:02:46.019495	\N
15	31	6.00	2025-09-11 08:35:17.30887	\N
17	13	4.50	2025-09-11 08:35:53.1567	\N
19	23	3.50	2025-09-11 08:36:53.495684	\N
20	25	3.50	2025-09-11 08:37:14.39447	\N
21	27	3.50	2025-09-11 08:37:33.582853	\N
22	16	3.50	2025-09-11 08:37:43.099711	\N
23	29	3.50	2025-09-11 08:38:10.500451	\N
24	24	3.50	2025-09-11 08:38:22.028126	\N
25	17	3.50	2025-09-11 08:38:32.593967	\N
26	14	3.50	2025-09-11 08:38:43.678538	\N
27	19	3.50	2025-09-11 08:38:57.520904	\N
28	22	3.50	2025-09-11 08:39:12.363633	\N
29	18	3.50	2025-09-11 08:39:21.001997	\N
30	26	3.50	2025-09-11 08:39:39.301606	\N
31	21	3.50	2025-09-11 08:39:49.133776	\N
33	41	3.80	2025-09-11 08:40:19.765578	\N
34	40	3.80	2025-09-11 08:40:33.978473	\N
35	39	3.80	2025-09-11 08:40:46.714498	\N
36	38	3.80	2025-09-11 08:40:57.181767	\N
37	37	2.80	2025-09-11 08:41:13.832391	\N
38	36	5.50	2025-09-11 08:41:28.418621	\N
39	42	2.80	2025-09-11 08:41:39.755313	2025-09-11 08:41:45.392377
40	42	3.30	2025-09-11 08:41:45.392403	\N
18	30	3.30	2025-09-11 08:36:05.764776	2025-09-25 19:29:26.426257
42	30	3.30	2025-09-25 19:29:26.426273	2025-09-25 19:29:28.057121
43	30	3.30	2025-09-25 19:29:28.057134	2025-09-25 19:29:30.607646
44	30	3.30	2025-09-25 19:29:30.607665	2025-09-25 19:29:32.627748
45	30	3.30	2025-09-25 19:29:32.627767	\N
32	20	3.50	2025-09-11 08:39:57.504405	2025-09-25 19:36:38.049405
46	20	3.15	2025-09-25 19:36:38.049423	2025-09-25 19:36:47.886667
47	20	3.09	2025-09-25 19:36:47.88668	2025-09-25 19:36:54.269281
48	20	3.06	2025-09-25 19:36:54.269293	2025-09-25 19:36:59.374958
49	20	3.05	2025-09-25 19:36:59.374971	\N
12	15	2.73	2025-09-10 18:00:23.050386	2025-10-15 16:33:38.150911
50	15	2.50	2025-10-15 16:33:38.150934	\N
8	44	2.70	2025-09-10 17:58:35.016403	2025-10-15 16:33:38.161933
9	4	12.00	2025-09-10 17:59:25.728493	2025-10-23 12:34:39.861974
41	34	8.00	2025-09-11 08:42:03.949862	2026-01-08 20:25:35.134259
53	34	8.00	2026-01-08 20:25:35.134293	\N
16	28	2.50	2025-09-11 08:35:30.016668	2026-01-08 20:34:24.870271
54	28	2.50	2026-01-08 20:34:24.870287	\N
51	44	3.00	2025-10-15 16:33:38.161947	2026-01-22 19:50:46.433772
55	44	4.16	2026-01-22 19:50:46.433791	\N
52	4	7.03	2025-10-23 12:34:39.861992	2026-01-22 19:51:53.993845
56	4	4.52	2026-01-22 19:51:53.993863	2026-01-22 19:52:45.782824
57	4	4.52	2026-01-22 19:52:45.782833	2026-01-27 18:39:16.402895
58	4	4.61	2026-01-27 18:39:16.402908	\N
\.


--
-- Data for Name: product_price_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.product_price_history (id, product_id, retail_chain_id, cost_center_id, price, start_date, end_date) FROM stdin;
2	4	1	\N	6.50	2025-09-10 10:56:51.053	\N
3	15	1	\N	4.55	2025-09-10 10:58:41.379	\N
4	16	1	\N	8.40	2025-09-10 10:59:58.655	\N
5	17	1	\N	8.70	2025-09-10 11:00:09.959	\N
6	14	1	\N	9.10	2025-09-10 11:01:56.547	\N
7	19	1	\N	7.70	2025-09-10 11:02:08.81	\N
8	20	1	\N	5.95	2025-09-10 11:02:27.65	\N
9	21	1	\N	7.70	2025-09-10 11:02:39.113	\N
10	22	1	\N	7.00	2025-09-10 11:03:53.693	\N
11	18	1	\N	7.70	2025-09-10 11:04:23.64	\N
12	23	1	\N	6.00	2025-09-10 11:04:38.597	\N
13	24	1	\N	8.40	2025-09-10 11:04:54.156	\N
14	25	1	\N	7.00	2025-09-10 11:05:06.886	\N
15	26	1	\N	10.50	2025-09-10 11:05:40.573	\N
16	27	1	\N	5.90	2025-09-10 11:06:26.732	\N
17	28	1	\N	4.90	2025-09-10 11:06:44.274	\N
18	29	1	\N	100000.00	2025-09-10 11:17:31.643	\N
19	30	1	\N	100000.00	2025-09-10 11:18:04.339	\N
20	31	1	\N	100000.00	2025-09-10 11:18:22.898	\N
21	32	1	\N	7.35	2025-09-10 11:18:47.06	\N
22	34	1	\N	100000.00	2025-09-10 11:19:16.38	\N
23	35	1	\N	9.80	2025-09-10 11:19:35.472	\N
24	36	1	\N	9.80	2025-09-10 11:29:24.311	\N
25	37	1	\N	5.60	2025-09-10 11:37:48.339	\N
26	38	1	\N	7.00	2025-09-10 11:38:31.583	\N
27	39	1	\N	7.00	2025-09-10 11:38:42.164	\N
28	40	1	\N	7.00	2025-09-10 11:38:54.645	\N
29	42	1	\N	7.00	2025-09-10 11:39:06.894	\N
30	41	1	\N	7.00	2025-09-10 11:39:28.205	\N
31	41	1	\N	7.10	2025-09-10 11:39:37.381	\N
33	13	2	\N	9.52	2025-09-10 13:11:55.507	\N
34	15	2	\N	5.52	2025-09-10 13:12:29.818	\N
35	4	2	\N	5.96	2025-09-11 08:10:46.605	\N
36	44	2	\N	7.56	2025-09-11 08:23:30.806	\N
37	15	2	\N	5.52	2025-09-11 08:23:58.8	\N
38	13	2	\N	9.52	2025-09-11 08:24:35.906	\N
39	16	2	\N	7.96	2025-09-11 08:25:41.818	\N
40	17	2	\N	10.32	2025-09-11 08:26:22.272	\N
41	18	2	\N	7.92	2025-09-11 08:27:55.729	\N
42	19	2	\N	7.12	2025-09-11 08:28:19.722	\N
43	20	2	\N	5.96	2025-09-11 08:29:02.906	\N
44	21	2	\N	7.92	2025-09-11 08:29:45.971	\N
45	22	2	\N	7.12	2025-09-11 08:30:02.518	\N
46	23	2	\N	5.56	2025-09-11 08:30:46.387	\N
47	24	2	\N	7.56	2025-09-11 08:31:13.327	\N
48	25	2	\N	5.52	2025-09-11 08:31:42.2	\N
49	26	2	\N	9.52	2025-09-11 08:32:08.866	\N
50	14	2	\N	9.52	2025-09-11 08:32:55.885	\N
51	27	2	\N	7.16	2025-09-11 08:33:27.305	\N
52	28	2	\N	5.96	2025-09-11 08:33:54.533	\N
53	29	2	\N	5.96	2025-09-11 08:34:13.749	\N
54	30	2	\N	6.76	2025-09-11 08:34:55.618	\N
55	31	2	\N	12.36	2025-09-11 08:35:14.113	\N
56	32	2	\N	8.36	2025-09-11 08:35:31.12	\N
57	35	2	\N	8.72	2025-09-11 08:35:56.957	\N
58	36	2	\N	9.52	2025-09-11 08:36:26.5	\N
59	37	2	\N	5.96	2025-09-11 08:36:42.102	\N
60	38	2	\N	7.56	2025-09-11 08:37:02.245	\N
61	39	2	\N	7.56	2025-09-11 08:37:23.468	\N
62	40	2	\N	7.56	2025-09-11 08:37:37.636	\N
63	41	2	\N	7.56	2025-09-11 08:37:54.613	\N
73	42	2	\N	7.56	2025-09-11 14:06:54.81	\N
75	4	3	\N	4.00	2025-09-11 14:11:56.105	\N
76	44	3	\N	6.00	2025-09-11 14:12:11.953	\N
77	15	3	\N	4.80	2025-09-11 14:12:28.097	\N
78	13	3	\N	6.50	2025-09-11 14:12:41.69	\N
79	16	3	\N	7.90	2025-09-11 14:12:58.017	\N
80	17	3	\N	9.20	2025-09-11 14:13:14.13	\N
81	18	3	\N	4.80	2025-09-11 14:13:58.697	\N
82	19	3	\N	6.80	2025-09-11 14:14:59.299	\N
83	20	3	\N	5.60	2025-09-11 14:15:24.985	\N
84	21	3	\N	6.80	2025-09-11 14:15:44.985	\N
85	22	3	\N	6.40	2025-09-11 14:16:12.776	\N
86	23	3	\N	6.00	2025-09-11 14:17:20.197	\N
87	24	3	\N	7.20	2025-09-11 14:17:34.597	\N
88	25	3	\N	5.60	2025-09-11 14:17:55.749	\N
89	26	3	\N	9.60	2025-09-11 14:18:10.468	\N
90	14	3	\N	8.80	2025-09-11 14:19:27.279	\N
91	27	3	\N	7.20	2025-09-11 14:19:40.061	\N
92	28	3	\N	5.20	2025-09-11 14:20:05.034	\N
93	29	3	\N	6.00	2025-09-11 14:20:30.496	\N
94	30	3	\N	5.95	2025-09-11 14:20:53.115	\N
95	31	3	\N	8.80	2025-09-11 14:21:13.481	\N
96	32	3	\N	6.30	2025-09-11 14:21:28.424	\N
97	34	3	\N	13.00	2025-09-11 14:21:44.913	\N
98	35	3	\N	9.20	2025-09-11 14:22:09.849	\N
99	36	3	\N	9.20	2025-09-11 14:23:45.254	\N
100	37	3	\N	5.20	2025-09-11 14:24:39.332	\N
101	38	3	\N	6.80	2025-09-11 14:25:13.868	\N
102	39	3	\N	6.80	2025-09-11 14:25:41.631	\N
103	40	3	\N	6.80	2025-09-11 14:26:32.021	\N
104	41	3	\N	6.80	2025-09-11 14:27:18.233	\N
105	42	3	\N	6.80	2025-09-11 14:27:48.385	\N
109	4	3	\N	6.68	2025-09-11 14:35:08.633	\N
110	4	4	\N	6.68	2025-09-11 14:37:48.417	\N
112	15	4	\N	5.21	2025-09-11 15:07:34.967	\N
113	13	4	\N	8.93	2025-09-11 15:07:50.285	\N
114	17	4	\N	8.93	2025-09-11 15:08:17.07	\N
115	18	4	\N	6.34	2025-09-11 15:08:39.397	\N
116	19	4	\N	6.37	2025-09-11 15:08:54.085	\N
117	20	4	\N	6.37	2025-09-11 15:09:09.428	\N
118	26	4	\N	9.68	2025-09-11 15:09:44.902	\N
119	14	4	\N	8.18	2025-09-11 15:10:00.182	\N
120	38	4	\N	7.73	2025-09-11 15:10:17.309	\N
121	39	4	\N	7.43	2025-09-11 15:10:50.181	\N
122	41	4	\N	7.43	2025-09-11 15:11:06.857	\N
123	42	4	\N	7.43	2025-09-11 15:11:18.313	\N
124	44	4	\N	5.93	2025-09-11 15:12:24.112	\N
125	4	1	\N	5.50	2025-09-15 07:50:13.918	\N
126	44	1	\N	6.50	2025-09-15 07:51:30.247	\N
127	4	1	\N	5.50	2025-09-15 10:43:36.794	\N
128	4	1	\N	5.50	2025-09-15 10:47:48.513	\N
129	4	1	\N	5.50	2025-09-15 10:48:23.139	\N
130	4	1	\N	5.50	2025-09-15 10:48:38.597	\N
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.products (id, custom_id, name, category_id, is_active, deleted_at) FROM stdin;
13	100400	COUVE-FLOR	1	t	\N
15	100300	TOMATINHO	4	t	\N
16	100500	VAGEM 	4	t	\N
17	100600	ERVILHA	4	t	\N
14	101600	MISTO (couve/broc)	1	t	\N
19	100800	QUIABO	4	t	\N
20	100900	MILHO	4	t	\N
21	101000	JILÓ	4	t	\N
22	101100	PIMENTA CAMBUCI	4	t	\N
18	100700	MANDIOQUINHA (BD)	4	t	\N
23	101200	ABOBRINHA	4	t	\N
24	101300	PEPINO	4	t	\N
25	101400	PIMENTÃO VERDE	4	t	\N
26	101500	PIMENTÃO COLOR	4	t	\N
27	101700	TOMATÃO 700G	4	t	\N
28	101800	COUVE PICADA	3	t	\N
29	101900	BERINJELA	4	t	\N
30	102000	PHYSALIS	2	t	\N
31	102100	MIRTILO	2	t	\N
32	102200	PINHÃO	4	t	\N
34	102300	MANDIOQUINHA KILO	4	t	\N
36	102500	ABÓBORA CABOTIÁ	4	t	\N
37	102600	ESPINAFRE SAQUINHO	3	t	\N
38	102700	ALFACE SALANOVA	3	t	\N
39	102800	RÚCULA BABY	3	t	\N
40	102900	AGRIÃO BABY	3	t	\N
41	103000	ESPINAFRE BABY	3	t	\N
42	103100	BETERRABA SALADA	3	t	\N
5	100200	BRÓCOLIS	1	f	2025-09-10 17:35:59.083237
44	100201	BRÓCOLIS	1	t	\N
4	100100	MORANGO (Bandeja)	2	t	\N
35	102400	MANDIOCA DESCASC	4	t	\N
\.


--
-- Data for Name: replenishment_recommendations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.replenishment_recommendations (id, cost_center_id, product_id, recommendation_date, recommendation, reason) FROM stdin;
\.


--
-- Data for Name: retail_chains; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.retail_chains (id, name, description, status) FROM stdin;
1	REX		t
2	BH		t
3	VILLE FORTE		t
4	ABC		t
5	MART MINAS		t
6	DMA (MINEIRÃO E EPA)		t
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.role_permissions (id, role_id, permission_id) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (id, name, description) FROM stdin;
1	admin	Administrador
2	employee	Funcionário
\.


--
-- Data for Name: sellers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sellers (id, user_id, cost_center_id) FROM stdin;
\.


--
-- Data for Name: shelf_prices; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.shelf_prices (id, product_id, retail_chain_id, cost_center_id, percentage_rate, start_date, end_date) FROM stdin;
\.


--
-- Data for Name: stock_movements; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.stock_movements (id, product_id, quantity, movement_type, supplier_id, cost_center_id, product_unit_cost, created_at, inventory_visit_id) FROM stdin;
1	5	704	supplier_purchase	1	\N	2.50	2025-09-10 17:34:48.714028-03	\N
2	5	704	supplier_purchase	1	\N	2.50	2025-09-10 17:34:57.953584-03	\N
3	5	704	supplier_purchase	1	\N	2.50	2025-09-10 17:35:08.551517-03	\N
4	44	704	supplier_purchase	1	\N	2.50	2025-09-10 17:44:37.999438-03	\N
6	44	400	supplier_purchase	3	\N	3.00	2025-09-10 17:55:49.936999-03	\N
7	32	224	supplier_purchase	2	\N	2.80	2025-09-10 17:57:11.264412-03	\N
8	44	224	supplier_purchase	2	\N	2.80	2025-09-10 17:58:35.013424-03	\N
9	4	3000	supplier_purchase	6	\N	12.00	2025-09-10 17:59:25.724697-03	\N
10	15	400	supplier_purchase	4	\N	3.00	2025-09-10 17:59:58.211589-03	\N
11	15	80	supplier_purchase	5	\N	3.00	2025-09-10 18:00:08.952922-03	\N
12	15	400	supplier_purchase	13	\N	2.40	2025-09-10 18:00:23.047249-03	\N
13	5	400	supplier_purchase	2	\N	2.80	2025-09-10 18:02:29.091653-03	\N
14	5	400	supplier_purchase	2	\N	2.80	2025-09-10 18:02:46.008963-03	\N
15	31	1000	supplier_purchase	2	\N	6.00	2025-09-11 08:35:17.295515-03	\N
16	28	1000	supplier_purchase	8	\N	2.50	2025-09-11 08:35:30.012335-03	\N
17	13	1000	supplier_purchase	2	\N	4.50	2025-09-11 08:35:53.153507-03	\N
18	30	25	supplier_purchase	4	\N	3.30	2025-09-11 08:36:05.760331-03	\N
19	23	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:36:53.492038-03	\N
20	25	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:37:14.389897-03	\N
21	27	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:37:33.579075-03	\N
22	16	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:37:43.095722-03	\N
23	29	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:38:10.496532-03	\N
24	24	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:38:22.024713-03	\N
25	17	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:38:32.589644-03	\N
27	19	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:38:57.51663-03	\N
28	22	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:39:12.356776-03	\N
29	18	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:39:20.998908-03	\N
30	26	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:39:39.29815-03	\N
31	21	1000	supplier_purchase	2	\N	3.50	2025-09-11 08:39:49.128629-03	\N
33	41	1000	supplier_purchase	2	\N	3.80	2025-09-11 08:40:19.762237-03	\N
34	40	1000	supplier_purchase	2	\N	3.80	2025-09-11 08:40:33.975714-03	\N
35	39	1000	supplier_purchase	2	\N	3.80	2025-09-11 08:40:46.710424-03	\N
36	38	1000	supplier_purchase	2	\N	3.80	2025-09-11 08:40:57.178039-03	\N
37	37	1000	supplier_purchase	2	\N	2.80	2025-09-11 08:41:13.828982-03	\N
38	36	1000	supplier_purchase	2	\N	5.50	2025-09-11 08:41:28.414196-03	\N
39	42	1000	supplier_purchase	2	\N	2.80	2025-09-11 08:41:39.750631-03	\N
40	42	1000	supplier_purchase	2	\N	3.80	2025-09-11 08:41:45.388285-03	\N
41	34	20	supplier_purchase	2	\N	8.00	2025-09-11 08:42:03.945701-03	\N
42	4	80	to_client	\N	10	12.00	2025-09-11 08:42:19.928025-03	\N
43	44	32	to_client	\N	10	2.70	2025-09-11 08:42:19.941089-03	\N
44	16	24	to_client	\N	10	3.50	2025-09-11 08:42:19.950277-03	\N
45	17	6	to_client	\N	10	3.50	2025-09-11 08:42:19.959518-03	\N
46	18	14	to_client	\N	10	3.50	2025-09-11 08:42:19.968576-03	\N
47	19	12	to_client	\N	10	3.50	2025-09-11 08:42:19.977775-03	\N
48	20	18	to_client	\N	10	3.50	2025-09-11 08:42:19.985624-03	\N
49	23	5	to_client	\N	10	3.50	2025-09-11 08:42:19.993395-03	\N
50	14	12	to_client	\N	10	3.50	2025-09-11 08:42:20.002269-03	\N
51	27	8	to_client	\N	10	3.50	2025-09-11 08:42:20.013444-03	\N
52	28	20	to_client	\N	10	2.50	2025-09-11 08:42:20.028056-03	\N
53	37	5	to_client	\N	10	2.80	2025-09-11 08:42:20.039905-03	\N
54	39	5	to_client	\N	10	3.80	2025-09-11 08:42:20.049406-03	\N
55	40	5	to_client	\N	10	3.80	2025-09-11 08:42:20.057171-03	\N
56	41	5	to_client	\N	10	3.80	2025-09-11 08:42:20.071738-03	\N
57	4	80	to_client	\N	1	12.00	2025-09-11 08:44:19.32766-03	\N
58	44	32	to_client	\N	1	2.70	2025-09-11 08:44:19.336892-03	\N
59	16	12	to_client	\N	1	3.50	2025-09-11 08:44:19.345095-03	\N
60	18	12	to_client	\N	1	3.50	2025-09-11 08:44:19.353749-03	\N
61	20	9	to_client	\N	1	3.50	2025-09-11 08:44:19.362563-03	\N
62	26	5	to_client	\N	1	3.50	2025-09-11 08:44:19.371173-03	\N
63	14	12	to_client	\N	1	3.50	2025-09-11 08:44:19.380631-03	\N
64	28	15	to_client	\N	1	2.50	2025-09-11 08:44:19.388437-03	\N
65	35	5	to_client	\N	1	6.00	2025-09-11 08:44:19.397933-03	\N
66	38	3	to_client	\N	1	3.80	2025-09-11 08:44:19.405429-03	\N
67	39	3	to_client	\N	1	3.80	2025-09-11 08:44:19.413022-03	\N
68	40	3	to_client	\N	1	3.80	2025-09-11 08:44:19.420708-03	\N
69	41	3	to_client	\N	1	3.80	2025-09-11 08:44:19.427992-03	\N
70	4	20	to_client	\N	7	12.00	2025-09-11 08:50:35.872657-03	\N
71	44	24	to_client	\N	7	2.70	2025-09-11 08:50:35.884451-03	\N
72	26	4	to_client	\N	7	3.50	2025-09-11 08:50:35.894054-03	\N
73	14	6	to_client	\N	7	3.50	2025-09-11 08:50:35.902601-03	\N
74	38	3	to_client	\N	7	3.80	2025-09-11 08:50:35.909693-03	\N
75	39	3	to_client	\N	7	3.80	2025-09-11 08:50:35.917233-03	\N
76	34	2	to_client	\N	3	8.00	2025-09-11 12:19:41.835935-03	\N
77	34	1	client_sale	\N	3	\N	2025-09-11 00:00:00-03	\N
78	4	120	to_client	\N	1	12.00	2025-09-15 08:01:34.474651-03	\N
79	44	32	to_client	\N	1	2.70	2025-09-15 08:01:34.493672-03	\N
80	15	25	to_client	\N	1	2.73	2025-09-15 08:01:34.505072-03	\N
81	17	6	to_client	\N	1	3.50	2025-09-15 08:01:34.515752-03	\N
82	18	6	to_client	\N	1	3.50	2025-09-15 08:01:34.523277-03	\N
83	20	10	to_client	\N	1	3.50	2025-09-15 08:01:34.531182-03	\N
84	24	6	to_client	\N	1	3.50	2025-09-15 08:01:34.538378-03	\N
85	14	12	to_client	\N	1	3.50	2025-09-15 08:01:34.545175-03	\N
86	27	10	to_client	\N	1	3.50	2025-09-15 08:01:34.552941-03	\N
87	28	15	to_client	\N	1	2.50	2025-09-15 08:01:34.561236-03	\N
88	35	5	to_client	\N	1	6.00	2025-09-15 08:01:34.568029-03	\N
89	36	3	to_client	\N	1	5.50	2025-09-15 08:01:34.575249-03	\N
90	37	5	to_client	\N	1	2.80	2025-09-15 08:01:34.582529-03	\N
91	38	5	to_client	\N	1	3.80	2025-09-15 08:01:34.589309-03	\N
92	39	5	to_client	\N	1	3.80	2025-09-15 08:01:34.596864-03	\N
93	41	3	to_client	\N	1	3.80	2025-09-15 08:01:34.604474-03	\N
94	19	6	to_client	\N	1	3.50	2025-09-15 08:01:34.611544-03	\N
95	4	60	to_client	\N	7	12.00	2025-09-15 10:30:51.142273-03	\N
96	44	32	to_client	\N	7	2.70	2025-09-15 10:30:51.177049-03	\N
97	16	6	to_client	\N	7	3.50	2025-09-15 10:30:51.187256-03	\N
98	17	6	to_client	\N	7	3.50	2025-09-15 10:30:51.21032-03	\N
99	18	6	to_client	\N	7	3.50	2025-09-15 10:30:51.226996-03	\N
100	19	6	to_client	\N	7	3.50	2025-09-15 10:30:51.240851-03	\N
101	20	9	to_client	\N	7	3.50	2025-09-15 10:30:51.253417-03	\N
102	22	6	to_client	\N	7	3.50	2025-09-15 10:30:51.262096-03	\N
103	24	6	to_client	\N	7	3.50	2025-09-15 10:30:51.271299-03	\N
104	14	6	to_client	\N	7	3.50	2025-09-15 10:30:51.279504-03	\N
105	4	100	to_client	\N	10	12.00	2025-09-15 10:40:37.611994-03	\N
106	44	40	to_client	\N	10	2.70	2025-09-15 10:40:37.622192-03	\N
107	15	25	to_client	\N	10	2.73	2025-09-15 10:40:37.629597-03	\N
108	16	24	to_client	\N	10	3.50	2025-09-15 10:40:37.638129-03	\N
109	18	12	to_client	\N	10	3.50	2025-09-15 10:40:37.647277-03	\N
110	20	18	to_client	\N	10	3.50	2025-09-15 10:40:37.656884-03	\N
111	22	8	to_client	\N	10	3.50	2025-09-15 10:40:37.663872-03	\N
112	24	12	to_client	\N	10	3.50	2025-09-15 10:40:37.674356-03	\N
113	14	12	to_client	\N	10	3.50	2025-09-15 10:40:37.684349-03	\N
114	27	10	to_client	\N	10	3.50	2025-09-15 10:40:37.695103-03	\N
115	35	8	to_client	\N	10	6.00	2025-09-15 10:40:37.704147-03	\N
116	36	5	to_client	\N	10	5.50	2025-09-15 10:40:37.713089-03	\N
117	37	5	to_client	\N	10	2.80	2025-09-15 10:40:37.71975-03	\N
118	38	9	to_client	\N	10	3.80	2025-09-15 10:40:37.725144-03	\N
119	39	9	to_client	\N	10	3.80	2025-09-15 10:40:37.734531-03	\N
120	40	5	to_client	\N	10	3.80	2025-09-15 10:40:37.742-03	\N
5	35	1000	supplier_purchase	17	\N	6.00	2025-09-10 17:52:01.938367-03	\N
121	41	5	to_client	\N	10	3.80	2025-09-15 10:40:37.748073-03	\N
122	44	68	to_client	\N	10	2.70	2025-09-15 20:38:06.877729-03	\N
123	16	24	to_client	\N	10	3.50	2025-09-15 20:38:06.961141-03	\N
124	18	19	to_client	\N	10	3.50	2025-09-15 20:38:06.986274-03	\N
125	19	7	to_client	\N	10	3.50	2025-09-15 20:38:07.007502-03	\N
126	20	5	to_client	\N	10	3.50	2025-09-15 20:38:07.029653-03	\N
127	14	14	to_client	\N	10	3.50	2025-09-15 20:38:07.049643-03	\N
128	27	11	to_client	\N	10	3.50	2025-09-15 20:38:07.056201-03	\N
129	28	10	to_client	\N	10	2.50	2025-09-15 20:38:07.062141-03	\N
130	37	10	to_client	\N	10	2.80	2025-09-15 20:38:07.068977-03	\N
131	38	8	to_client	\N	10	3.80	2025-09-15 20:38:07.077133-03	\N
132	39	15	to_client	\N	10	3.80	2025-09-15 20:38:07.084903-03	\N
133	40	8	to_client	\N	10	3.80	2025-09-15 20:38:07.090818-03	\N
134	41	8	to_client	\N	10	3.80	2025-09-15 20:38:07.096665-03	\N
135	44	31	to_client	\N	7	2.70	2025-09-15 20:38:26.908411-03	\N
136	14	8	to_client	\N	7	3.50	2025-09-15 20:38:26.913915-03	\N
137	38	3	to_client	\N	7	3.80	2025-09-15 20:38:26.919571-03	\N
138	39	3	to_client	\N	7	3.80	2025-09-15 20:38:26.926079-03	\N
139	37	4	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
140	44	51	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
141	14	23	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
142	16	2	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
143	20	14	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
144	24	3	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
145	19	5	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
146	18	15	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
147	28	25	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
148	35	9	client_sale	\N	1	\N	2025-09-18 00:00:00-03	\N
32	20	500	supplier_purchase	2	\N	3.50	2025-09-11 08:39:57.500196-03	\N
149	30	1000	supplier_purchase	2	\N	3.30	2025-09-25 19:29:26.42125-03	\N
150	30	1000	supplier_purchase	2	\N	3.30	2025-09-25 19:29:28.054664-03	\N
151	30	1000	supplier_purchase	2	\N	3.30	2025-09-25 19:29:30.60333-03	\N
152	30	1000	supplier_purchase	2	\N	3.30	2025-09-25 19:29:32.624365-03	\N
153	20	1000	supplier_purchase	2	\N	3.00	2025-09-25 19:36:38.045759-03	\N
154	20	1000	supplier_purchase	2	\N	3.00	2025-09-25 19:36:47.883317-03	\N
155	20	1000	supplier_purchase	2	\N	3.00	2025-09-25 19:36:54.266458-03	\N
156	20	1000	supplier_purchase	2	\N	3.00	2025-09-25 19:36:59.372314-03	\N
157	4	48	to_client	\N	1	12.00	2025-10-01 08:26:39.762356-03	\N
158	44	32	to_client	\N	1	2.70	2025-10-01 08:26:39.795397-03	\N
159	15	25	to_client	\N	1	2.73	2025-10-01 08:26:39.805849-03	\N
160	16	12	to_client	\N	1	3.50	2025-10-01 08:26:39.813663-03	\N
161	17	6	to_client	\N	1	3.50	2025-10-01 08:26:39.819669-03	\N
162	18	6	to_client	\N	1	3.50	2025-10-01 08:26:39.825627-03	\N
163	19	12	to_client	\N	1	3.50	2025-10-01 08:26:39.831781-03	\N
164	20	9	to_client	\N	1	3.05	2025-10-01 08:26:39.837954-03	\N
165	24	6	to_client	\N	1	3.50	2025-10-01 08:26:39.84493-03	\N
166	14	8	to_client	\N	1	3.50	2025-10-01 08:26:39.850533-03	\N
167	28	30	to_client	\N	1	2.50	2025-10-01 08:26:39.856879-03	\N
168	35	5	to_client	\N	1	6.00	2025-10-01 08:26:39.864228-03	\N
169	38	2	to_client	\N	1	3.80	2025-10-01 08:26:39.869955-03	\N
170	39	3	to_client	\N	1	3.80	2025-10-01 08:26:39.877411-03	\N
171	4	60	to_client	\N	2	12.00	2025-10-01 08:26:55.094003-03	\N
172	44	40	to_client	\N	2	2.70	2025-10-01 08:26:55.109147-03	\N
173	15	15	to_client	\N	2	2.73	2025-10-01 08:26:55.119431-03	\N
174	16	12	to_client	\N	2	3.50	2025-10-01 08:26:55.128947-03	\N
175	17	6	to_client	\N	2	3.50	2025-10-01 08:26:55.137151-03	\N
176	18	12	to_client	\N	2	3.50	2025-10-01 08:26:55.144671-03	\N
177	19	12	to_client	\N	2	3.50	2025-10-01 08:26:55.151759-03	\N
178	20	10	to_client	\N	2	3.05	2025-10-01 08:26:55.161103-03	\N
179	22	6	to_client	\N	2	3.50	2025-10-01 08:26:55.171407-03	\N
180	14	12	to_client	\N	2	3.50	2025-10-01 08:26:55.182521-03	\N
181	37	3	to_client	\N	2	2.80	2025-10-01 08:26:55.190378-03	\N
182	38	3	to_client	\N	2	3.80	2025-10-01 08:26:55.200697-03	\N
183	39	3	to_client	\N	2	3.80	2025-10-01 08:26:55.212479-03	\N
184	4	40	to_client	\N	4	12.00	2025-10-01 08:27:06.841552-03	\N
185	44	48	to_client	\N	4	2.70	2025-10-01 08:27:06.852165-03	\N
186	17	6	to_client	\N	4	3.50	2025-10-01 08:27:06.859562-03	\N
187	18	12	to_client	\N	4	3.50	2025-10-01 08:27:06.866636-03	\N
188	20	20	to_client	\N	4	3.05	2025-10-01 08:27:06.873712-03	\N
189	24	4	to_client	\N	4	3.50	2025-10-01 08:27:06.880946-03	\N
190	14	6	to_client	\N	4	3.50	2025-10-01 08:27:06.890273-03	\N
191	28	10	to_client	\N	4	2.50	2025-10-01 08:27:06.899267-03	\N
192	35	5	to_client	\N	4	6.00	2025-10-01 08:27:06.907731-03	\N
193	36	4	to_client	\N	4	5.50	2025-10-01 08:27:06.915717-03	\N
194	38	4	to_client	\N	4	3.80	2025-10-01 08:27:06.925577-03	\N
195	39	6	to_client	\N	4	3.80	2025-10-01 08:27:06.932978-03	\N
196	40	4	to_client	\N	4	3.80	2025-10-01 08:27:06.93945-03	\N
197	4	120	to_client	\N	5	12.00	2025-10-01 08:27:19.286897-03	\N
198	44	256	to_client	\N	5	2.70	2025-10-01 08:27:19.294291-03	\N
199	15	200	to_client	\N	5	2.73	2025-10-01 08:27:19.301871-03	\N
200	16	48	to_client	\N	5	3.50	2025-10-01 08:27:19.308294-03	\N
201	17	24	to_client	\N	5	3.50	2025-10-01 08:27:19.313959-03	\N
202	18	36	to_client	\N	5	3.50	2025-10-01 08:27:19.320231-03	\N
203	19	24	to_client	\N	5	3.50	2025-10-01 08:27:19.327863-03	\N
204	20	54	to_client	\N	5	3.05	2025-10-01 08:27:19.333438-03	\N
205	14	36	to_client	\N	5	3.50	2025-10-01 08:27:19.34126-03	\N
206	27	6	to_client	\N	5	3.50	2025-10-01 08:27:19.349041-03	\N
207	28	40	to_client	\N	5	2.50	2025-10-01 08:27:19.358265-03	\N
208	35	32	to_client	\N	5	6.00	2025-10-01 08:27:19.364305-03	\N
209	36	30	to_client	\N	5	5.50	2025-10-01 08:27:19.370129-03	\N
210	37	10	to_client	\N	5	2.80	2025-10-01 08:27:19.375417-03	\N
211	38	18	to_client	\N	5	3.80	2025-10-01 08:27:19.381029-03	\N
212	39	27	to_client	\N	5	3.80	2025-10-01 08:27:19.38675-03	\N
213	40	5	to_client	\N	5	3.80	2025-10-01 08:27:19.393272-03	\N
214	41	9	to_client	\N	5	3.80	2025-10-01 08:27:19.398969-03	\N
215	42	4	to_client	\N	5	3.30	2025-10-01 08:27:19.40482-03	\N
216	4	16	to_client	\N	7	12.00	2025-10-01 08:27:31.571101-03	\N
217	44	16	to_client	\N	7	2.70	2025-10-01 08:27:31.577655-03	\N
218	15	25	to_client	\N	7	2.73	2025-10-01 08:27:31.584968-03	\N
219	18	6	to_client	\N	7	3.50	2025-10-01 08:27:31.5922-03	\N
220	19	6	to_client	\N	7	3.50	2025-10-01 08:27:31.597329-03	\N
221	20	9	to_client	\N	7	3.05	2025-10-01 08:27:31.602661-03	\N
222	24	6	to_client	\N	7	3.50	2025-10-01 08:27:31.607952-03	\N
223	28	10	to_client	\N	7	2.50	2025-10-01 08:27:31.613719-03	\N
224	38	2	to_client	\N	7	3.80	2025-10-01 08:27:31.620629-03	\N
225	39	4	to_client	\N	7	3.80	2025-10-01 08:27:31.626923-03	\N
226	4	24	to_client	\N	8	12.00	2025-10-01 08:27:40.245728-03	\N
227	44	24	to_client	\N	8	2.70	2025-10-01 08:27:40.253257-03	\N
228	20	9	to_client	\N	8	3.05	2025-10-01 08:27:40.260893-03	\N
229	21	3	to_client	\N	8	3.50	2025-10-01 08:27:40.270251-03	\N
230	28	20	to_client	\N	8	2.50	2025-10-01 08:27:40.27827-03	\N
231	35	4	to_client	\N	8	6.00	2025-10-01 08:27:40.284714-03	\N
232	39	3	to_client	\N	8	3.80	2025-10-01 08:27:40.29404-03	\N
233	4	80	to_client	\N	10	12.00	2025-10-01 08:27:48.891726-03	\N
234	44	48	to_client	\N	10	2.70	2025-10-01 08:27:48.902255-03	\N
235	15	25	to_client	\N	10	2.73	2025-10-01 08:27:48.909397-03	\N
236	16	18	to_client	\N	10	3.50	2025-10-01 08:27:48.915594-03	\N
237	17	6	to_client	\N	10	3.50	2025-10-01 08:27:48.923721-03	\N
238	18	12	to_client	\N	10	3.50	2025-10-01 08:27:48.932265-03	\N
239	19	12	to_client	\N	10	3.50	2025-10-01 08:27:48.941093-03	\N
240	20	18	to_client	\N	10	3.05	2025-10-01 08:27:48.947668-03	\N
243	14	12	to_client	\N	10	3.50	2025-10-01 08:27:48.967944-03	\N
246	35	12	to_client	\N	10	6.00	2025-10-01 08:27:48.985979-03	\N
249	38	5	to_client	\N	10	3.80	2025-10-01 08:27:49.004262-03	\N
252	44	24	to_client	\N	19	2.70	2025-10-01 08:27:56.409786-03	\N
255	18	6	to_client	\N	19	3.50	2025-10-01 08:27:56.430752-03	\N
258	27	5	to_client	\N	19	3.50	2025-10-01 08:27:56.452556-03	\N
261	35	16	to_client	\N	19	6.00	2025-10-01 08:27:56.470602-03	\N
262	4	88	to_client	\N	20	12.00	2025-10-01 08:28:14.091348-03	\N
265	13	15	to_client	\N	20	4.50	2025-10-01 08:28:14.113591-03	\N
268	18	6	to_client	\N	20	3.50	2025-10-01 08:28:14.134254-03	\N
271	21	6	to_client	\N	20	3.50	2025-10-01 08:28:14.154741-03	\N
274	27	10	to_client	\N	20	3.50	2025-10-01 08:28:14.177698-03	\N
277	39	4	to_client	\N	20	3.80	2025-10-01 08:28:14.202517-03	\N
241	22	6	to_client	\N	10	3.50	2025-10-01 08:27:48.955283-03	\N
244	27	5	to_client	\N	10	3.50	2025-10-01 08:27:48.973507-03	\N
247	36	5	to_client	\N	10	5.50	2025-10-01 08:27:48.991695-03	\N
250	39	5	to_client	\N	10	3.80	2025-10-01 08:27:49.010954-03	\N
251	4	40	to_client	\N	19	12.00	2025-10-01 08:27:56.402532-03	\N
254	16	6	to_client	\N	19	3.50	2025-10-01 08:27:56.423943-03	\N
257	20	10	to_client	\N	19	3.05	2025-10-01 08:27:56.446239-03	\N
260	29	5	to_client	\N	19	3.50	2025-10-01 08:27:56.464871-03	\N
263	44	40	to_client	\N	20	2.70	2025-10-01 08:28:14.099189-03	\N
266	16	12	to_client	\N	20	3.50	2025-10-01 08:28:14.120489-03	\N
269	19	6	to_client	\N	20	3.50	2025-10-01 08:28:14.141368-03	\N
272	22	7	to_client	\N	20	3.50	2025-10-01 08:28:14.162516-03	\N
275	28	30	to_client	\N	20	2.50	2025-10-01 08:28:14.184383-03	\N
278	40	4	to_client	\N	20	3.80	2025-10-01 08:28:14.212315-03	\N
242	24	12	to_client	\N	10	3.50	2025-10-01 08:27:48.961305-03	\N
245	28	30	to_client	\N	10	2.50	2025-10-01 08:27:48.979749-03	\N
248	37	3	to_client	\N	10	2.80	2025-10-01 08:27:48.997301-03	\N
253	13	5	to_client	\N	19	4.50	2025-10-01 08:27:56.416957-03	\N
256	19	6	to_client	\N	19	3.50	2025-10-01 08:27:56.439275-03	\N
259	28	30	to_client	\N	19	2.50	2025-10-01 08:27:56.459271-03	\N
264	15	25	to_client	\N	20	2.73	2025-10-01 08:28:14.105585-03	\N
267	17	6	to_client	\N	20	3.50	2025-10-01 08:28:14.127481-03	\N
270	20	15	to_client	\N	20	3.05	2025-10-01 08:28:14.147961-03	\N
273	14	6	to_client	\N	20	3.50	2025-10-01 08:28:14.170244-03	\N
276	35	13	to_client	\N	20	6.00	2025-10-01 08:28:14.192964-03	\N
279	44	95	to_client	\N	1	2.70	2025-10-02 10:27:45.606766-03	\N
280	16	28	to_client	\N	1	3.50	2025-10-02 10:27:45.631668-03	\N
281	19	22	to_client	\N	1	3.50	2025-10-02 10:27:45.643214-03	\N
282	18	1	to_client	\N	1	3.50	2025-10-02 10:27:45.654909-03	\N
283	15	180	to_client	\N	1	2.73	2025-10-02 10:27:45.662608-03	\N
284	35	19	to_client	\N	1	6.00	2025-10-02 10:27:45.669557-03	\N
285	28	80	to_client	\N	1	2.50	2025-10-02 10:27:45.675361-03	\N
286	14	26	to_client	\N	1	3.50	2025-10-02 10:27:45.681385-03	\N
287	38	35	to_client	\N	1	3.80	2025-10-02 10:27:45.687544-03	\N
288	39	34	to_client	\N	1	3.80	2025-10-02 10:27:45.692934-03	\N
289	17	13	to_client	\N	1	3.50	2025-10-02 10:27:45.69805-03	\N
290	4	967	to_client	\N	1	12.00	2025-10-02 10:27:45.705125-03	\N
291	4	1175	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
292	44	108	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
293	15	205	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
294	19	29	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
295	14	23	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
296	27	5	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
297	28	95	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
298	35	17	client_sale	\N	1	\N	2025-10-07 00:00:00-03	\N
299	20	8	client_sale	\N	4	\N	2025-10-07 00:00:00-03	\N
300	4	80	client_sale	\N	7	\N	2025-10-08 00:00:00-03	\N
301	44	87	client_sale	\N	7	\N	2025-10-08 00:00:00-03	\N
302	20	13	client_sale	\N	7	\N	2025-10-08 00:00:00-03	\N
303	24	6	client_sale	\N	7	\N	2025-10-08 00:00:00-03	\N
304	14	14	client_sale	\N	7	\N	2025-10-08 00:00:00-03	\N
305	28	4	client_sale	\N	7	\N	2025-10-08 00:00:00-03	\N
306	4	20	to_client	\N	14	12.00	2025-10-08 11:54:30.219208-03	\N
307	44	16	to_client	\N	14	2.70	2025-10-08 11:54:30.237372-03	\N
308	15	12	to_client	\N	14	2.73	2025-10-08 11:54:30.24634-03	\N
309	17	4	to_client	\N	14	3.50	2025-10-08 11:54:30.254965-03	\N
310	18	6	to_client	\N	14	3.50	2025-10-08 11:54:30.26352-03	\N
311	20	5	to_client	\N	14	3.05	2025-10-08 11:54:30.271615-03	\N
312	22	6	to_client	\N	14	3.50	2025-10-08 11:54:30.278057-03	\N
313	14	6	to_client	\N	14	3.50	2025-10-08 11:54:30.284715-03	\N
314	27	5	to_client	\N	14	3.50	2025-10-08 11:54:30.29034-03	\N
315	28	10	to_client	\N	14	2.50	2025-10-08 11:54:30.296479-03	\N
316	39	3	to_client	\N	14	3.80	2025-10-08 11:54:30.302642-03	\N
317	40	3	to_client	\N	14	3.80	2025-10-08 11:54:30.308669-03	\N
318	4	40	to_client	\N	11	12.00	2025-10-08 11:54:54.751766-03	\N
319	44	32	to_client	\N	11	2.70	2025-10-08 11:54:54.758985-03	\N
320	15	25	to_client	\N	11	2.73	2025-10-08 11:54:54.766406-03	\N
321	16	12	to_client	\N	11	3.50	2025-10-08 11:54:54.772344-03	\N
322	18	6	to_client	\N	11	3.50	2025-10-08 11:54:54.778293-03	\N
323	20	18	to_client	\N	11	3.05	2025-10-08 11:54:54.784499-03	\N
324	21	5	to_client	\N	11	3.50	2025-10-08 11:54:54.790929-03	\N
325	22	6	to_client	\N	11	3.50	2025-10-08 11:54:54.796978-03	\N
326	24	6	to_client	\N	11	3.50	2025-10-08 11:54:54.804025-03	\N
327	14	12	to_client	\N	11	3.50	2025-10-08 11:54:54.810784-03	\N
328	27	5	to_client	\N	11	3.50	2025-10-08 11:54:54.819038-03	\N
329	28	15	to_client	\N	11	2.50	2025-10-08 11:54:54.826163-03	\N
330	35	6	to_client	\N	11	6.00	2025-10-08 11:54:54.832122-03	\N
331	37	3	to_client	\N	11	2.80	2025-10-08 11:54:54.837822-03	\N
332	39	3	to_client	\N	11	3.80	2025-10-08 11:54:54.843553-03	\N
333	41	3	to_client	\N	11	3.80	2025-10-08 11:54:54.849544-03	\N
334	4	16	to_client	\N	7	12.00	2025-10-08 11:55:22.188388-03	\N
335	44	16	to_client	\N	7	2.70	2025-10-08 11:55:22.198915-03	\N
336	15	25	to_client	\N	7	2.73	2025-10-08 11:55:22.206093-03	\N
337	20	5	to_client	\N	7	3.05	2025-10-08 11:55:22.213265-03	\N
338	24	6	to_client	\N	7	3.50	2025-10-08 11:55:22.220663-03	\N
339	14	6	to_client	\N	7	3.50	2025-10-08 11:55:22.227587-03	\N
340	28	6	to_client	\N	7	2.50	2025-10-08 11:55:22.233261-03	\N
341	4	15	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
342	44	8	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
343	15	4	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
344	17	4	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
345	20	2	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
346	22	1	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
347	27	4	client_sale	\N	14	\N	2025-10-08 00:00:00-03	\N
348	44	5	client_sale	\N	14	\N	2025-10-09 00:00:00-03	\N
349	4	60	to_client	\N	2	12.00	2025-10-13 20:56:47.154129-03	\N
350	44	48	to_client	\N	2	2.70	2025-10-13 20:56:47.167863-03	\N
351	15	25	to_client	\N	2	2.73	2025-10-13 20:56:47.175603-03	\N
352	16	12	to_client	\N	2	3.50	2025-10-13 20:56:47.181724-03	\N
353	18	8	to_client	\N	2	3.50	2025-10-13 20:56:47.18798-03	\N
354	19	6	to_client	\N	2	3.50	2025-10-13 20:56:47.195233-03	\N
355	20	18	to_client	\N	2	3.05	2025-10-13 20:56:47.202057-03	\N
356	22	6	to_client	\N	2	3.50	2025-10-13 20:56:47.207976-03	\N
357	23	4	to_client	\N	2	3.50	2025-10-13 20:56:47.213739-03	\N
358	26	4	to_client	\N	2	3.50	2025-10-13 20:56:47.225606-03	\N
359	14	12	to_client	\N	2	3.50	2025-10-13 20:56:47.233513-03	\N
360	27	6	to_client	\N	2	3.50	2025-10-13 20:56:47.239109-03	\N
361	28	15	to_client	\N	2	2.50	2025-10-13 20:56:47.245499-03	\N
362	37	6	to_client	\N	2	2.80	2025-10-13 20:56:47.253105-03	\N
363	38	4	to_client	\N	2	3.80	2025-10-13 20:56:47.259423-03	\N
364	39	4	to_client	\N	2	3.80	2025-10-13 20:56:47.266619-03	\N
365	41	3	to_client	\N	2	3.80	2025-10-13 20:56:47.273336-03	\N
366	44	32	to_client	\N	1	2.70	2025-10-13 20:56:54.864494-03	\N
367	15	15	to_client	\N	1	2.73	2025-10-13 20:56:54.872977-03	\N
368	18	12	to_client	\N	1	3.50	2025-10-13 20:56:54.880184-03	\N
369	19	6	to_client	\N	1	3.50	2025-10-13 20:56:54.886333-03	\N
370	23	4	to_client	\N	1	3.50	2025-10-13 20:56:54.893668-03	\N
371	24	4	to_client	\N	1	3.50	2025-10-13 20:56:54.90026-03	\N
372	14	6	to_client	\N	1	3.50	2025-10-13 20:56:54.907618-03	\N
373	28	15	to_client	\N	1	2.50	2025-10-13 20:56:54.913707-03	\N
374	35	5	to_client	\N	1	6.00	2025-10-13 20:56:54.920065-03	\N
375	37	3	to_client	\N	1	2.80	2025-10-13 20:56:54.925721-03	\N
376	21	8	to_client	\N	1	3.50	2025-10-13 20:56:54.932651-03	\N
377	4	40	to_client	\N	4	12.00	2025-10-13 20:57:03.153952-03	\N
378	44	64	to_client	\N	4	2.70	2025-10-13 20:57:03.16333-03	\N
379	15	25	to_client	\N	4	2.73	2025-10-13 20:57:03.172222-03	\N
380	16	12	to_client	\N	4	3.50	2025-10-13 20:57:03.182162-03	\N
381	17	12	to_client	\N	4	3.50	2025-10-13 20:57:03.193411-03	\N
382	18	12	to_client	\N	4	3.50	2025-10-13 20:57:03.201609-03	\N
383	19	12	to_client	\N	4	3.50	2025-10-13 20:57:03.210147-03	\N
384	20	20	to_client	\N	4	3.05	2025-10-13 20:57:03.219066-03	\N
385	21	6	to_client	\N	4	3.50	2025-10-13 20:57:03.2295-03	\N
386	23	4	to_client	\N	4	3.50	2025-10-13 20:57:03.239928-03	\N
387	24	5	to_client	\N	4	3.50	2025-10-13 20:57:03.249782-03	\N
388	26	4	to_client	\N	4	3.50	2025-10-13 20:57:03.258426-03	\N
389	14	12	to_client	\N	4	3.50	2025-10-13 20:57:03.268299-03	\N
390	27	10	to_client	\N	4	3.50	2025-10-13 20:57:03.277087-03	\N
395	40	4	to_client	\N	4	3.80	2025-10-13 20:57:03.330308-03	\N
391	28	10	to_client	\N	4	2.50	2025-10-13 20:57:03.289385-03	\N
396	41	4	to_client	\N	4	3.80	2025-10-13 20:57:03.339537-03	\N
392	35	5	to_client	\N	4	6.00	2025-10-13 20:57:03.300861-03	\N
397	42	2	to_client	\N	4	3.30	2025-10-13 20:57:03.348399-03	\N
393	38	4	to_client	\N	4	3.80	2025-10-13 20:57:03.311411-03	\N
394	39	4	to_client	\N	4	3.80	2025-10-13 20:57:03.321035-03	\N
398	44	32	to_client	\N	10	2.70	2025-10-13 20:58:24.70276-03	\N
399	4	48	to_client	\N	10	12.00	2025-10-13 20:58:24.710454-03	\N
400	15	25	to_client	\N	10	2.73	2025-10-13 20:58:24.717217-03	\N
401	16	12	to_client	\N	10	3.50	2025-10-13 20:58:24.725963-03	\N
402	17	6	to_client	\N	10	3.50	2025-10-13 20:58:24.732248-03	\N
403	18	12	to_client	\N	10	3.50	2025-10-13 20:58:24.742444-03	\N
404	19	6	to_client	\N	10	3.50	2025-10-13 20:58:24.749498-03	\N
405	20	18	to_client	\N	10	3.05	2025-10-13 20:58:24.755197-03	\N
406	21	6	to_client	\N	10	3.50	2025-10-13 20:58:24.761101-03	\N
407	22	6	to_client	\N	10	3.50	2025-10-13 20:58:24.767146-03	\N
408	24	6	to_client	\N	10	3.50	2025-10-13 20:58:24.77407-03	\N
409	26	5	to_client	\N	10	3.50	2025-10-13 20:58:24.779021-03	\N
410	14	12	to_client	\N	10	3.50	2025-10-13 20:58:24.784564-03	\N
411	27	8	to_client	\N	10	3.50	2025-10-13 20:58:24.790431-03	\N
412	28	20	to_client	\N	10	2.50	2025-10-13 20:58:24.795997-03	\N
413	35	8	to_client	\N	10	6.00	2025-10-13 20:58:24.801953-03	\N
414	37	3	to_client	\N	10	2.80	2025-10-13 20:58:24.807464-03	\N
415	38	3	to_client	\N	10	3.80	2025-10-13 20:58:24.813229-03	\N
416	39	5	to_client	\N	10	3.80	2025-10-13 20:58:24.819491-03	\N
417	40	5	to_client	\N	10	3.80	2025-10-13 20:58:24.82745-03	\N
418	41	3	to_client	\N	10	3.80	2025-10-13 20:58:24.834501-03	\N
419	4	40	to_client	\N	21	12.00	2025-10-13 20:58:34.905301-03	\N
420	44	40	to_client	\N	21	2.70	2025-10-13 20:58:34.913099-03	\N
421	15	75	to_client	\N	21	2.73	2025-10-13 20:58:34.919753-03	\N
422	13	20	to_client	\N	21	4.50	2025-10-13 20:58:34.926258-03	\N
423	16	18	to_client	\N	21	3.50	2025-10-13 20:58:34.934391-03	\N
424	17	6	to_client	\N	21	3.50	2025-10-13 20:58:34.941242-03	\N
425	18	6	to_client	\N	21	3.50	2025-10-13 20:58:34.94851-03	\N
426	20	9	to_client	\N	21	3.05	2025-10-13 20:58:34.955416-03	\N
427	23	4	to_client	\N	21	3.50	2025-10-13 20:58:34.961741-03	\N
428	24	6	to_client	\N	21	3.50	2025-10-13 20:58:34.968265-03	\N
429	14	6	to_client	\N	21	3.50	2025-10-13 20:58:34.975029-03	\N
430	27	8	to_client	\N	21	3.50	2025-10-13 20:58:34.981984-03	\N
431	28	25	to_client	\N	21	2.50	2025-10-13 20:58:34.988985-03	\N
432	29	5	to_client	\N	21	3.50	2025-10-13 20:58:34.996421-03	\N
433	38	5	to_client	\N	21	3.80	2025-10-13 20:58:35.003255-03	\N
434	39	4	to_client	\N	21	3.80	2025-10-13 20:58:35.010542-03	\N
435	41	3	to_client	\N	21	3.80	2025-10-13 20:58:35.017735-03	\N
436	42	3	to_client	\N	21	3.30	2025-10-13 20:58:35.023325-03	\N
437	4	80	to_client	\N	20	12.00	2025-10-13 20:58:39.81154-03	\N
438	44	40	to_client	\N	20	2.70	2025-10-13 20:58:39.817285-03	\N
439	15	50	to_client	\N	20	2.73	2025-10-13 20:58:39.824377-03	\N
440	13	15	to_client	\N	20	4.50	2025-10-13 20:58:39.831371-03	\N
441	16	18	to_client	\N	20	3.50	2025-10-13 20:58:39.837949-03	\N
442	17	6	to_client	\N	20	3.50	2025-10-13 20:58:39.845886-03	\N
443	18	6	to_client	\N	20	3.50	2025-10-13 20:58:39.852994-03	\N
444	20	10	to_client	\N	20	3.05	2025-10-13 20:58:39.860109-03	\N
445	24	6	to_client	\N	20	3.50	2025-10-13 20:58:39.868251-03	\N
446	27	8	to_client	\N	20	3.50	2025-10-13 20:58:39.874914-03	\N
447	28	30	to_client	\N	20	2.50	2025-10-13 20:58:39.882123-03	\N
448	35	4	to_client	\N	20	6.00	2025-10-13 20:58:39.890265-03	\N
449	38	2	to_client	\N	20	3.80	2025-10-13 20:58:39.897596-03	\N
450	39	3	to_client	\N	20	3.80	2025-10-13 20:58:39.904435-03	\N
451	40	5	to_client	\N	20	3.80	2025-10-13 20:58:39.910455-03	\N
452	41	3	to_client	\N	20	3.80	2025-10-13 20:58:39.91702-03	\N
453	42	2	to_client	\N	20	3.30	2025-10-13 20:58:39.924362-03	\N
454	4	32	to_client	\N	19	12.00	2025-10-13 21:20:13.897432-03	\N
455	44	16	to_client	\N	19	2.70	2025-10-13 21:20:13.906538-03	\N
456	15	25	to_client	\N	19	2.73	2025-10-13 21:20:13.913163-03	\N
457	17	6	to_client	\N	19	3.50	2025-10-13 21:20:13.921097-03	\N
458	20	6	to_client	\N	19	3.05	2025-10-13 21:20:13.9335-03	\N
459	24	4	to_client	\N	19	3.50	2025-10-13 21:20:13.939829-03	\N
460	28	20	to_client	\N	19	2.50	2025-10-13 21:20:13.948464-03	\N
461	35	4	to_client	\N	19	6.00	2025-10-13 21:20:13.955039-03	\N
462	4	30	client_sale	\N	1	\N	2025-10-13 00:00:00-03	\N
463	44	17	client_sale	\N	1	\N	2025-10-13 00:00:00-03	\N
464	44	3	client_loss	\N	1	\N	2025-10-13 10:00:00-03	\N
465	4	62	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
466	44	25	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
467	15	5	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
468	17	2	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
469	20	8	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
470	24	2	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
471	28	25	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
472	35	10	client_sale	\N	19	\N	2025-10-13 00:00:00-03	\N
473	4	60	to_client	\N	2	12.00	2025-10-15 16:28:06.261589-03	\N
474	44	48	to_client	\N	2	2.70	2025-10-15 16:28:06.276715-03	\N
475	15	25	to_client	\N	2	2.73	2025-10-15 16:28:06.284163-03	\N
476	16	12	to_client	\N	2	3.50	2025-10-15 16:28:06.294721-03	\N
477	18	8	to_client	\N	2	3.50	2025-10-15 16:28:06.307934-03	\N
478	19	6	to_client	\N	2	3.50	2025-10-15 16:28:06.317146-03	\N
479	20	18	to_client	\N	2	3.05	2025-10-15 16:28:06.323821-03	\N
480	22	6	to_client	\N	2	3.50	2025-10-15 16:28:06.330906-03	\N
481	23	4	to_client	\N	2	3.50	2025-10-15 16:28:06.337898-03	\N
482	26	4	to_client	\N	2	3.50	2025-10-15 16:28:06.344768-03	\N
483	14	12	to_client	\N	2	3.50	2025-10-15 16:28:06.352283-03	\N
484	27	6	to_client	\N	2	3.50	2025-10-15 16:28:06.361625-03	\N
485	28	15	to_client	\N	2	2.50	2025-10-15 16:28:06.368305-03	\N
486	37	6	to_client	\N	2	2.80	2025-10-15 16:28:06.377023-03	\N
487	38	4	to_client	\N	2	3.80	2025-10-15 16:28:06.383653-03	\N
488	39	4	to_client	\N	2	3.80	2025-10-15 16:28:06.390838-03	\N
489	41	3	to_client	\N	2	3.80	2025-10-15 16:28:06.399824-03	\N
490	15	5000	supplier_purchase	4	\N	2.50	2025-10-15 16:33:38.141483-03	\N
491	44	5000	supplier_purchase	1	\N	3.00	2025-10-15 16:33:38.154069-03	\N
492	44	32	to_client	\N	1	3.00	2025-10-15 16:33:57.971564-03	\N
493	15	15	to_client	\N	1	2.50	2025-10-15 16:33:57.97872-03	\N
494	18	12	to_client	\N	1	3.50	2025-10-15 16:33:57.984603-03	\N
495	19	6	to_client	\N	1	3.50	2025-10-15 16:33:57.990843-03	\N
496	21	8	to_client	\N	1	3.50	2025-10-15 16:33:57.996759-03	\N
497	23	4	to_client	\N	1	3.50	2025-10-15 16:33:58.002488-03	\N
498	24	4	to_client	\N	1	3.50	2025-10-15 16:33:58.008426-03	\N
499	14	6	to_client	\N	1	3.50	2025-10-15 16:33:58.01395-03	\N
500	28	15	to_client	\N	1	2.50	2025-10-15 16:33:58.019499-03	\N
501	35	5	to_client	\N	1	6.00	2025-10-15 16:33:58.025953-03	\N
502	37	3	to_client	\N	1	2.80	2025-10-15 16:33:58.031874-03	\N
503	4	40	to_client	\N	4	12.00	2025-10-15 16:36:36.969208-03	\N
504	44	64	to_client	\N	4	3.00	2025-10-15 16:36:36.976593-03	\N
505	15	25	to_client	\N	4	2.50	2025-10-15 16:36:36.98288-03	\N
506	16	12	to_client	\N	4	3.50	2025-10-15 16:36:36.990011-03	\N
507	17	12	to_client	\N	4	3.50	2025-10-15 16:36:36.998698-03	\N
508	18	12	to_client	\N	4	3.50	2025-10-15 16:36:37.008336-03	\N
509	19	12	to_client	\N	4	3.50	2025-10-15 16:36:37.017045-03	\N
510	20	20	to_client	\N	4	3.05	2025-10-15 16:36:37.024415-03	\N
511	21	6	to_client	\N	4	3.50	2025-10-15 16:36:37.031136-03	\N
512	23	4	to_client	\N	4	3.50	2025-10-15 16:36:37.039078-03	\N
513	24	5	to_client	\N	4	3.50	2025-10-15 16:36:37.052895-03	\N
514	26	4	to_client	\N	4	3.50	2025-10-15 16:36:37.059838-03	\N
515	14	12	to_client	\N	4	3.50	2025-10-15 16:36:37.066493-03	\N
516	27	10	to_client	\N	4	3.50	2025-10-15 16:36:37.074115-03	\N
517	28	10	to_client	\N	4	2.50	2025-10-15 16:36:37.080356-03	\N
518	35	5	to_client	\N	4	6.00	2025-10-15 16:36:37.087674-03	\N
523	42	2	to_client	\N	4	3.30	2025-10-15 16:36:37.132476-03	\N
524	4	180	to_client	\N	5	12.00	2025-10-15 16:39:24.350778-03	\N
529	18	24	to_client	\N	5	3.50	2025-10-15 16:39:24.390309-03	\N
534	14	24	to_client	\N	5	3.50	2025-10-15 16:39:24.432721-03	\N
539	38	9	to_client	\N	5	3.80	2025-10-15 16:39:24.471732-03	\N
546	19	6	to_client	\N	7	3.50	2025-10-15 16:41:03.367887-03	\N
551	39	4	to_client	\N	7	3.80	2025-10-15 16:41:03.412342-03	\N
557	15	25	to_client	\N	17	2.50	2025-10-15 16:42:02.047324-03	\N
562	26	4	to_client	\N	17	3.50	2025-10-15 16:42:02.100966-03	\N
567	38	2	to_client	\N	17	3.80	2025-10-15 16:42:02.152961-03	\N
571	44	32	to_client	\N	10	3.00	2025-10-15 16:43:53.779217-03	\N
576	19	6	to_client	\N	10	3.50	2025-10-15 16:43:53.816894-03	\N
581	26	5	to_client	\N	10	3.50	2025-10-15 16:43:53.85548-03	\N
586	37	3	to_client	\N	10	2.80	2025-10-15 16:43:53.891326-03	\N
519	38	4	to_client	\N	4	3.80	2025-10-15 16:36:37.0973-03	\N
527	16	48	to_client	\N	5	3.50	2025-10-15 16:39:24.375483-03	\N
532	24	12	to_client	\N	5	3.50	2025-10-15 16:39:24.414727-03	\N
537	35	16	to_client	\N	5	6.00	2025-10-15 16:39:24.457762-03	\N
542	41	18	to_client	\N	5	3.80	2025-10-15 16:39:24.490636-03	\N
545	15	25	to_client	\N	7	2.50	2025-10-15 16:41:03.358721-03	\N
550	37	4	to_client	\N	7	2.80	2025-10-15 16:41:03.402404-03	\N
559	16	8	to_client	\N	17	3.50	2025-10-15 16:42:02.071047-03	\N
564	27	8	to_client	\N	17	3.50	2025-10-15 16:42:02.121364-03	\N
569	42	4	to_client	\N	17	3.30	2025-10-15 16:42:02.177689-03	\N
572	15	25	to_client	\N	10	2.50	2025-10-15 16:43:53.786487-03	\N
577	20	18	to_client	\N	10	3.05	2025-10-15 16:43:53.8253-03	\N
582	14	12	to_client	\N	10	3.50	2025-10-15 16:43:53.862115-03	\N
587	38	3	to_client	\N	10	3.80	2025-10-15 16:43:53.898886-03	\N
520	39	4	to_client	\N	4	3.80	2025-10-15 16:36:37.106-03	\N
528	17	6	to_client	\N	5	3.50	2025-10-15 16:39:24.382887-03	\N
533	26	8	to_client	\N	5	3.50	2025-10-15 16:39:24.424071-03	\N
538	37	16	to_client	\N	5	2.80	2025-10-15 16:39:24.465825-03	\N
543	4	20	to_client	\N	7	12.00	2025-10-15 16:41:03.340065-03	\N
548	14	6	to_client	\N	7	3.50	2025-10-15 16:41:03.385483-03	\N
553	41	3	to_client	\N	7	3.80	2025-10-15 16:41:03.433985-03	\N
555	4	80	to_client	\N	17	12.00	2025-10-15 16:42:02.018147-03	\N
560	20	15	to_client	\N	17	3.05	2025-10-15 16:42:02.07961-03	\N
565	28	11	to_client	\N	17	2.50	2025-10-15 16:42:02.135167-03	\N
574	17	6	to_client	\N	10	3.50	2025-10-15 16:43:53.801472-03	\N
579	22	6	to_client	\N	10	3.50	2025-10-15 16:43:53.840833-03	\N
584	28	20	to_client	\N	10	2.50	2025-10-15 16:43:53.875454-03	\N
589	40	5	to_client	\N	10	3.80	2025-10-15 16:43:53.91061-03	\N
521	40	4	to_client	\N	4	3.80	2025-10-15 16:36:37.115378-03	\N
526	15	200	to_client	\N	5	2.50	2025-10-15 16:39:24.36774-03	\N
531	20	48	to_client	\N	5	3.05	2025-10-15 16:39:24.407481-03	\N
536	28	40	to_client	\N	5	2.50	2025-10-15 16:39:24.449482-03	\N
541	40	9	to_client	\N	5	3.80	2025-10-15 16:39:24.484711-03	\N
547	20	5	to_client	\N	7	3.05	2025-10-15 16:41:03.375489-03	\N
552	40	3	to_client	\N	7	3.80	2025-10-15 16:41:03.425228-03	\N
558	13	10	to_client	\N	17	4.50	2025-10-15 16:42:02.061222-03	\N
563	14	6	to_client	\N	17	3.50	2025-10-15 16:42:02.110322-03	\N
568	41	3	to_client	\N	17	3.80	2025-10-15 16:42:02.165883-03	\N
570	4	48	to_client	\N	10	12.00	2025-10-15 16:43:53.770421-03	\N
575	18	12	to_client	\N	10	3.50	2025-10-15 16:43:53.809857-03	\N
580	24	6	to_client	\N	10	3.50	2025-10-15 16:43:53.848271-03	\N
585	35	8	to_client	\N	10	6.00	2025-10-15 16:43:53.88173-03	\N
590	41	3	to_client	\N	10	3.80	2025-10-15 16:43:53.915909-03	\N
522	41	4	to_client	\N	4	3.80	2025-10-15 16:36:37.124084-03	\N
525	44	208	to_client	\N	5	3.00	2025-10-15 16:39:24.35991-03	\N
530	19	12	to_client	\N	5	3.50	2025-10-15 16:39:24.397327-03	\N
535	27	10	to_client	\N	5	3.50	2025-10-15 16:39:24.439782-03	\N
540	39	18	to_client	\N	5	3.80	2025-10-15 16:39:24.4782-03	\N
544	44	16	to_client	\N	7	3.00	2025-10-15 16:41:03.3496-03	\N
549	28	10	to_client	\N	7	2.50	2025-10-15 16:41:03.393099-03	\N
554	42	3	to_client	\N	7	3.30	2025-10-15 16:41:03.443303-03	\N
556	44	48	to_client	\N	17	3.00	2025-10-15 16:42:02.031572-03	\N
561	24	8	to_client	\N	17	3.50	2025-10-15 16:42:02.091219-03	\N
566	29	5	to_client	\N	17	3.50	2025-10-15 16:42:02.143647-03	\N
573	16	12	to_client	\N	10	3.50	2025-10-15 16:43:53.793128-03	\N
578	21	6	to_client	\N	10	3.50	2025-10-15 16:43:53.832917-03	\N
583	27	8	to_client	\N	10	3.50	2025-10-15 16:43:53.868308-03	\N
588	39	5	to_client	\N	10	3.80	2025-10-15 16:43:53.904761-03	\N
591	4	32	to_client	\N	19	12.00	2025-10-15 16:45:21.309296-03	\N
592	44	16	to_client	\N	19	3.00	2025-10-15 16:45:21.317833-03	\N
593	15	25	to_client	\N	19	2.50	2025-10-15 16:45:21.325954-03	\N
594	17	6	to_client	\N	19	3.50	2025-10-15 16:45:21.332971-03	\N
595	20	6	to_client	\N	19	3.05	2025-10-15 16:45:21.33947-03	\N
596	24	4	to_client	\N	19	3.50	2025-10-15 16:45:21.346604-03	\N
597	28	20	to_client	\N	19	2.50	2025-10-15 16:45:21.354536-03	\N
598	35	4	to_client	\N	19	6.00	2025-10-15 16:45:21.361312-03	\N
599	4	80	to_client	\N	20	12.00	2025-10-15 16:47:17.642508-03	\N
600	44	40	to_client	\N	20	3.00	2025-10-15 16:47:17.65046-03	\N
601	15	50	to_client	\N	20	2.50	2025-10-15 16:47:17.658369-03	\N
602	13	15	to_client	\N	20	4.50	2025-10-15 16:47:17.666252-03	\N
603	16	18	to_client	\N	20	3.50	2025-10-15 16:47:17.674481-03	\N
604	17	6	to_client	\N	20	3.50	2025-10-15 16:47:17.680416-03	\N
605	18	6	to_client	\N	20	3.50	2025-10-15 16:47:17.686546-03	\N
606	20	10	to_client	\N	20	3.05	2025-10-15 16:47:17.6937-03	\N
607	24	6	to_client	\N	20	3.50	2025-10-15 16:47:17.699497-03	\N
608	27	8	to_client	\N	20	3.50	2025-10-15 16:47:17.705642-03	\N
609	28	30	to_client	\N	20	2.50	2025-10-15 16:47:17.715206-03	\N
610	35	4	to_client	\N	20	6.00	2025-10-15 16:47:17.722234-03	\N
611	38	2	to_client	\N	20	3.80	2025-10-15 16:47:17.731467-03	\N
612	39	3	to_client	\N	20	3.80	2025-10-15 16:47:17.738469-03	\N
613	40	5	to_client	\N	20	3.80	2025-10-15 16:47:17.745452-03	\N
614	41	3	to_client	\N	20	3.80	2025-10-15 16:47:17.753769-03	\N
615	42	2	to_client	\N	20	3.30	2025-10-15 16:47:17.761433-03	\N
616	4	40	to_client	\N	6	12.00	2025-10-15 16:51:24.884659-03	\N
617	44	16	to_client	\N	6	3.00	2025-10-15 16:51:24.892283-03	\N
618	15	17	to_client	\N	6	2.50	2025-10-15 16:51:24.900836-03	\N
619	18	6	to_client	\N	6	3.50	2025-10-15 16:51:24.908021-03	\N
620	19	6	to_client	\N	6	3.50	2025-10-15 16:51:24.915598-03	\N
621	20	18	to_client	\N	6	3.05	2025-10-15 16:51:24.922427-03	\N
622	14	8	to_client	\N	6	3.50	2025-10-15 16:51:24.928278-03	\N
623	28	20	to_client	\N	6	2.50	2025-10-15 16:51:24.936913-03	\N
624	38	4	to_client	\N	6	3.80	2025-10-15 16:51:24.94443-03	\N
625	39	5	to_client	\N	6	3.80	2025-10-15 16:51:24.95072-03	\N
626	40	5	to_client	\N	6	3.80	2025-10-15 16:51:24.957533-03	\N
627	42	3	to_client	\N	6	3.30	2025-10-15 16:51:24.963609-03	\N
628	4	35	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
629	44	18	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
630	16	10	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
631	17	3	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
632	18	6	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
633	20	15	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
634	21	2	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
635	24	1	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
636	14	7	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
637	28	7	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
638	35	3	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
639	37	1	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
640	40	3	client_sale	\N	10	\N	2025-10-16 00:00:00-03	\N
641	4	21	client_sale	\N	19	\N	2025-10-16 00:00:00-03	\N
642	44	5	client_sale	\N	19	\N	2025-10-16 00:00:00-03	\N
643	39	16	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
644	38	8	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
645	40	3	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
646	37	3	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
647	41	9	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
648	35	7	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
649	44	50	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
650	4	47	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
651	18	5	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
652	15	59	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
653	24	6	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
654	28	31	client_sale	\N	5	\N	2025-10-16 00:00:00-03	\N
655	4	60	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
656	44	17	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
657	13	8	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
658	16	1	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
659	14	2	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
660	27	3	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
661	28	8	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
662	29	4	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
663	41	3	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
664	42	4	client_sale	\N	17	\N	2025-10-16 00:00:00-03	\N
665	4	58	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
666	44	10	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
667	15	6	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
668	13	1	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
669	16	3	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
670	17	5	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
671	18	2	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
672	20	2	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
673	24	4	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
674	27	3	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
675	28	7	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
676	35	1	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
677	39	2	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
678	41	1	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
679	38	2	client_sale	\N	20	\N	2025-10-16 00:00:00-03	\N
680	15	13	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
681	18	6	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
682	19	3	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
683	23	4	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
684	14	4	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
685	28	2	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
686	35	1	client_sale	\N	1	\N	2025-10-16 00:00:00-03	\N
687	4	28	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
688	18	2	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
689	19	3	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
690	14	1	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
691	28	6	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
692	38	1	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
693	39	2	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
694	41	2	client_sale	\N	2	\N	2025-10-16 00:00:00-03	\N
695	44	11	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
696	15	5	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
697	4	2	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
698	20	1	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
699	28	2	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
700	42	3	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
701	37	4	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
702	41	3	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
703	39	1	client_sale	\N	7	\N	2025-10-16 00:00:00-03	\N
704	4	38	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
705	44	45	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
706	14	4	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
707	16	2	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
708	19	5	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
710	15	20	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
711	27	7	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
712	17	2	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
713	24	1	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
715	40	1	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
716	4	40	to_client	\N	10	12.00	2025-10-20 10:46:36.21981-03	\N
717	44	32	to_client	\N	10	3.00	2025-10-20 10:46:36.233047-03	\N
719	16	24	to_client	\N	10	3.50	2025-10-20 10:46:36.251496-03	\N
720	17	6	to_client	\N	10	3.50	2025-10-20 10:46:36.260892-03	\N
721	18	12	to_client	\N	10	3.50	2025-10-20 10:46:36.269129-03	\N
722	19	6	to_client	\N	10	3.50	2025-10-20 10:46:36.275343-03	\N
724	14	12	to_client	\N	10	3.50	2025-10-20 10:46:36.287583-03	\N
725	27	10	to_client	\N	10	3.50	2025-10-20 10:46:36.293987-03	\N
726	28	20	to_client	\N	10	2.50	2025-10-20 10:46:36.300072-03	\N
727	35	8	to_client	\N	10	6.00	2025-10-20 10:46:36.307058-03	\N
729	37	5	to_client	\N	10	2.80	2025-10-20 10:46:36.31978-03	\N
730	38	5	to_client	\N	10	3.80	2025-10-20 10:46:36.325479-03	\N
731	39	5	to_client	\N	10	3.80	2025-10-20 10:46:36.330936-03	\N
732	40	5	to_client	\N	10	3.80	2025-10-20 10:46:36.336212-03	\N
733	4	24	to_client	\N	7	12.00	2025-10-20 10:46:42.87983-03	\N
734	44	32	to_client	\N	7	3.00	2025-10-20 10:46:42.887222-03	\N
735	15	25	to_client	\N	7	2.50	2025-10-20 10:46:42.895338-03	\N
736	16	6	to_client	\N	7	3.50	2025-10-20 10:46:42.904708-03	\N
738	20	9	to_client	\N	7	3.05	2025-10-20 10:46:42.917418-03	\N
739	22	6	to_client	\N	7	3.50	2025-10-20 10:46:42.925038-03	\N
740	14	6	to_client	\N	7	3.50	2025-10-20 10:46:42.931873-03	\N
741	37	4	to_client	\N	7	2.80	2025-10-20 10:46:42.938139-03	\N
743	41	3	to_client	\N	7	3.80	2025-10-20 10:46:42.950263-03	\N
744	42	4	to_client	\N	7	3.30	2025-10-20 10:46:42.957672-03	\N
745	4	24	to_client	\N	1	12.00	2025-10-20 10:46:48.934619-03	\N
747	15	25	to_client	\N	1	2.50	2025-10-20 10:46:48.949111-03	\N
748	16	12	to_client	\N	1	3.50	2025-10-20 10:46:48.956656-03	\N
749	18	8	to_client	\N	1	3.50	2025-10-20 10:46:48.96574-03	\N
750	19	4	to_client	\N	1	3.50	2025-10-20 10:46:48.972471-03	\N
752	23	5	to_client	\N	1	3.50	2025-10-20 10:46:48.989591-03	\N
753	24	4	to_client	\N	1	3.50	2025-10-20 10:46:48.997012-03	\N
754	14	4	to_client	\N	1	3.50	2025-10-20 10:46:49.002942-03	\N
755	27	4	to_client	\N	1	3.50	2025-10-20 10:46:49.009575-03	\N
757	36	4	to_client	\N	1	5.50	2025-10-20 10:46:49.028252-03	\N
758	37	3	to_client	\N	1	2.80	2025-10-20 10:46:49.036673-03	\N
761	20	4	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
766	28	5	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
709	26	3	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
714	20	8	client_sale	\N	4	\N	2025-10-20 00:00:00-03	\N
718	15	50	to_client	\N	10	2.50	2025-10-20 10:46:36.241741-03	\N
723	20	18	to_client	\N	10	3.05	2025-10-20 10:46:36.281491-03	\N
728	36	5	to_client	\N	10	5.50	2025-10-20 10:46:36.314052-03	\N
737	18	6	to_client	\N	7	3.50	2025-10-20 10:46:42.911427-03	\N
742	39	4	to_client	\N	7	3.80	2025-10-20 10:46:42.944487-03	\N
746	44	16	to_client	\N	1	3.00	2025-10-20 10:46:48.941631-03	\N
751	20	6	to_client	\N	1	3.05	2025-10-20 10:46:48.980472-03	\N
756	28	10	to_client	\N	1	2.50	2025-10-20 10:46:49.018592-03	\N
759	15	16	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
760	18	4	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
762	23	1	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
763	24	2	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
764	14	2	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
765	27	2	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
767	37	2	client_sale	\N	1	\N	2025-10-20 00:00:00-03	\N
768	4	38	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
769	44	29	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
770	15	9	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
771	17	1	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
772	19	2	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
773	20	8	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
774	14	10	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
775	27	4	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
776	16	10	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
777	28	16	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
778	35	3	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
779	36	3	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
780	37	3	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
781	38	3	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
782	40	3	client_sale	\N	10	\N	2025-10-20 00:00:00-03	\N
784	4	40	to_client	\N	4	7.06	2025-10-23 12:34:53.014727-03	\N
785	44	32	to_client	\N	4	3.00	2025-10-23 12:34:53.022927-03	\N
786	15	25	to_client	\N	4	2.50	2025-10-23 12:34:53.03246-03	\N
787	16	12	to_client	\N	4	3.50	2025-10-23 12:34:53.041377-03	\N
788	18	11	to_client	\N	4	3.50	2025-10-23 12:34:53.047452-03	\N
789	19	12	to_client	\N	4	3.50	2025-10-23 12:34:53.054589-03	\N
790	20	18	to_client	\N	4	3.05	2025-10-23 12:34:53.063717-03	\N
791	21	12	to_client	\N	4	3.50	2025-10-23 12:34:53.070639-03	\N
792	26	3	to_client	\N	4	3.50	2025-10-23 12:34:53.077165-03	\N
793	14	10	to_client	\N	4	3.50	2025-10-23 12:34:53.083196-03	\N
794	39	6	to_client	\N	4	3.80	2025-10-23 12:34:53.091046-03	\N
795	40	4	to_client	\N	4	3.80	2025-10-23 12:34:53.097583-03	\N
796	4	40	to_client	\N	21	7.06	2025-10-23 12:35:09.390708-03	\N
797	44	32	to_client	\N	21	3.00	2025-10-23 12:35:09.399436-03	\N
798	15	75	to_client	\N	21	2.50	2025-10-23 12:35:09.407719-03	\N
799	13	20	to_client	\N	21	4.50	2025-10-23 12:35:09.414853-03	\N
800	16	6	to_client	\N	21	3.50	2025-10-23 12:35:09.422255-03	\N
801	18	7	to_client	\N	21	3.50	2025-10-23 12:35:09.429645-03	\N
802	20	10	to_client	\N	21	3.05	2025-10-23 12:35:09.436775-03	\N
803	23	10	to_client	\N	21	3.50	2025-10-23 12:35:09.44422-03	\N
804	26	6	to_client	\N	21	3.50	2025-10-23 12:35:09.451917-03	\N
805	14	6	to_client	\N	21	3.50	2025-10-23 12:35:09.461064-03	\N
806	27	7	to_client	\N	21	3.50	2025-10-23 12:35:09.467032-03	\N
807	28	20	to_client	\N	21	2.50	2025-10-23 12:35:09.473532-03	\N
808	30	5	to_client	\N	21	3.30	2025-10-23 12:35:09.479913-03	\N
809	35	16	to_client	\N	21	6.00	2025-10-23 12:35:09.48654-03	\N
810	36	5	to_client	\N	21	5.50	2025-10-23 12:35:09.494137-03	\N
811	37	4	to_client	\N	21	2.80	2025-10-23 12:35:09.501893-03	\N
812	38	5	to_client	\N	21	3.80	2025-10-23 12:35:09.509511-03	\N
813	39	3	to_client	\N	21	3.80	2025-10-23 12:35:09.517355-03	\N
814	40	5	to_client	\N	21	3.80	2025-10-23 12:35:09.527827-03	\N
815	4	16	to_client	\N	8	7.06	2025-10-23 12:35:16.326081-03	\N
816	44	16	to_client	\N	8	3.00	2025-10-23 12:35:16.334906-03	\N
817	18	5	to_client	\N	8	3.50	2025-10-23 12:35:16.34231-03	\N
818	19	4	to_client	\N	8	3.50	2025-10-23 12:35:16.350435-03	\N
819	20	5	to_client	\N	8	3.05	2025-10-23 12:35:16.358335-03	\N
820	26	2	to_client	\N	8	3.50	2025-10-23 12:35:16.364081-03	\N
821	14	12	to_client	\N	8	3.50	2025-10-23 12:35:16.370573-03	\N
822	4	68	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
823	44	55	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
824	15	99	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
825	13	32	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
826	16	9	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
827	17	4	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
828	18	9	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
829	20	10	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
830	24	5	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
831	14	9	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
832	27	11	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
833	28	23	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
834	29	1	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
835	30	1	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
836	35	12	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
837	38	5	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
838	39	2	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
839	41	2	client_sale	\N	21	\N	2025-10-23 00:00:00-03	\N
840	4	4	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
841	44	12	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
842	18	3	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
843	20	7	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
844	21	1	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
845	26	1	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
846	28	20	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
847	35	1	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
848	39	3	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
849	14	13	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
850	4	33	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
851	44	16	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
852	15	9	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
853	18	11	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
854	19	4	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
855	20	14	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
856	21	2	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
857	26	2	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
858	14	10	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
859	39	6	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
860	40	3	client_sale	\N	4	\N	2025-10-23 00:00:00-03	\N
861	4	34	client_sale	\N	8	\N	2025-10-23 00:00:00-03	\N
862	4	2	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
863	16	2	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
864	18	12	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
865	20	3	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
866	26	5	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
867	27	6	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
868	28	4	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
869	35	5	client_sale	\N	10	\N	2025-11-03 00:00:00-03	\N
870	4	60	to_client	\N	1	7.06	2025-11-10 11:06:57.299371-03	\N
871	44	30	to_client	\N	1	3.00	2025-11-10 11:06:57.327049-03	\N
872	20	36	to_client	\N	1	3.05	2025-11-10 11:06:57.335328-03	\N
873	15	100	to_client	\N	10	2.50	2025-11-10 11:10:05.088416-03	\N
874	13	24	to_client	\N	10	4.50	2025-11-10 11:10:05.119689-03	\N
875	19	50	to_client	\N	10	3.50	2025-11-10 11:10:05.14458-03	\N
876	4	300	to_client	\N	5	7.06	2025-11-10 11:11:27.929268-03	\N
877	44	100	to_client	\N	5	3.00	2025-11-10 11:11:27.938976-03	\N
878	21	50	to_client	\N	5	3.50	2025-11-10 11:11:27.950555-03	\N
881	15	89	client_sale	\N	1	\N	2025-11-10 00:00:00-03	\N
885	15	25	to_client	\N	1	2.50	2025-11-16 15:52:58.729836-03	\N
890	23	4	to_client	\N	1	3.50	2025-11-16 15:52:58.774411-03	\N
895	35	4	to_client	\N	1	6.00	2025-11-16 15:52:58.809252-03	\N
899	4	3	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
902	15	30	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
906	14	4	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
909	16	3	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
916	19	3	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
920	26	3	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
923	44	24	to_client	\N	1	3.00	2025-11-19 23:18:41.457459-03	\N
928	19	12	to_client	\N	1	3.50	2025-11-19 23:18:41.561888-03	\N
933	28	10	to_client	\N	1	2.50	2025-11-19 23:18:41.61051-03	\N
935	44	26	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
940	19	8	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
945	26	1	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
879	4	45	client_sale	\N	1	\N	2025-11-10 00:00:00-03	\N
883	4	2	to_client	\N	1	7.06	2025-11-16 15:52:58.704596-03	\N
888	20	10	to_client	\N	1	3.05	2025-11-16 15:52:58.759283-03	\N
893	27	4	to_client	\N	1	3.50	2025-11-16 15:52:58.795087-03	\N
898	4	1	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
905	14	7	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
912	21	5	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
915	19	9	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
919	27	3	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
924	15	25	to_client	\N	1	2.50	2025-11-19 23:18:41.481631-03	\N
929	20	10	to_client	\N	1	3.05	2025-11-19 23:18:41.570938-03	\N
936	15	20	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
941	20	12	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
946	14	8	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
880	44	72	client_sale	\N	1	\N	2025-11-10 00:00:00-03	\N
886	18	6	to_client	\N	1	3.50	2025-11-16 15:52:58.73909-03	\N
891	24	6	to_client	\N	1	3.50	2025-11-16 15:52:58.780723-03	\N
896	37	4	to_client	\N	1	2.80	2025-11-16 15:52:58.818757-03	\N
900	44	23	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
907	13	2	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
914	35	3	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
917	24	3	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
925	13	10	to_client	\N	1	4.50	2025-11-19 23:18:41.506826-03	\N
930	24	12	to_client	\N	1	3.50	2025-11-19 23:18:41.580018-03	\N
937	13	7	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
942	21	5	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
947	27	5	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
882	20	57	client_sale	\N	1	\N	2025-11-10 00:00:00-03	\N
884	44	32	to_client	\N	1	3.00	2025-11-16 15:52:58.717764-03	\N
889	21	6	to_client	\N	1	3.50	2025-11-16 15:52:58.766508-03	\N
894	28	15	to_client	\N	1	2.50	2025-11-16 15:52:58.801657-03	\N
903	15	3	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
910	16	4	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
913	35	1	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
921	23	1	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
922	4	12	to_client	\N	1	7.06	2025-11-19 23:18:41.410058-03	\N
927	18	6	to_client	\N	1	3.50	2025-11-19 23:18:41.552548-03	\N
932	27	5	to_client	\N	1	3.50	2025-11-19 23:18:41.602371-03	\N
938	16	12	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
943	23	1	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
948	28	8	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
887	19	12	to_client	\N	1	3.50	2025-11-16 15:52:58.747733-03	\N
892	14	12	to_client	\N	1	3.50	2025-11-16 15:52:58.786942-03	\N
897	41	5	to_client	\N	1	3.80	2025-11-16 15:52:58.825489-03	\N
901	44	10	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
904	20	9	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
908	13	4	client_loss	\N	1	\N	2025-11-17 10:00:00-03	\N
911	21	3	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
918	28	8	client_sale	\N	1	\N	2025-11-17 00:00:00-03	\N
926	17	6	to_client	\N	1	3.50	2025-11-19 23:18:41.529707-03	\N
931	14	12	to_client	\N	1	3.50	2025-11-19 23:18:41.590108-03	\N
934	4	11	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
939	18	9	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
944	24	4	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
949	35	2	client_sale	\N	1	\N	2025-11-20 00:00:00-03	\N
950	4	12	to_client	\N	1	7.06	2025-11-24 11:25:13.780025-03	\N
951	44	32	to_client	\N	1	3.00	2025-11-24 11:25:13.824734-03	\N
952	15	50	to_client	\N	1	2.50	2025-11-24 11:25:13.834942-03	\N
953	13	5	to_client	\N	1	4.50	2025-11-24 11:25:13.843957-03	\N
954	16	6	to_client	\N	1	3.50	2025-11-24 11:25:13.855411-03	\N
955	17	6	to_client	\N	1	3.50	2025-11-24 11:25:13.866618-03	\N
956	18	12	to_client	\N	1	3.50	2025-11-24 11:25:13.875268-03	\N
957	19	12	to_client	\N	1	3.50	2025-11-24 11:25:13.884911-03	\N
958	20	10	to_client	\N	1	3.05	2025-11-24 11:25:13.894394-03	\N
959	21	6	to_client	\N	1	3.50	2025-11-24 11:25:13.901495-03	\N
960	24	6	to_client	\N	1	3.50	2025-11-24 11:25:13.908604-03	\N
961	14	12	to_client	\N	1	3.50	2025-11-24 11:25:13.914991-03	\N
962	28	15	to_client	\N	1	2.50	2025-11-24 11:25:13.920739-03	\N
963	35	5	to_client	\N	1	6.00	2025-11-24 11:25:13.927432-03	\N
964	37	5	to_client	\N	1	2.80	2025-11-24 11:25:13.93345-03	\N
965	4	12	to_client	\N	1	7.06	2025-11-27 10:35:00.823436-03	\N
966	44	32	to_client	\N	1	3.00	2025-11-27 10:35:00.90566-03	\N
967	15	25	to_client	\N	1	2.50	2025-11-27 10:35:00.93146-03	\N
968	16	6	to_client	\N	1	3.50	2025-11-27 10:35:00.947357-03	\N
969	18	12	to_client	\N	1	3.50	2025-11-27 10:35:00.968713-03	\N
970	20	10	to_client	\N	1	3.05	2025-11-27 10:35:00.982754-03	\N
971	24	6	to_client	\N	1	3.50	2025-11-27 10:35:00.992435-03	\N
972	14	6	to_client	\N	1	3.50	2025-11-27 10:35:01.006004-03	\N
973	28	10	to_client	\N	1	2.50	2025-11-27 10:35:01.018185-03	\N
974	37	5	to_client	\N	1	2.80	2025-11-27 10:35:01.029856-03	\N
975	4	16	to_client	\N	1	7.06	2025-12-01 09:56:35.680637-03	\N
976	44	40	to_client	\N	1	3.00	2025-12-01 09:56:35.714299-03	\N
977	15	50	to_client	\N	1	2.50	2025-12-01 09:56:35.724256-03	\N
978	16	4	to_client	\N	1	3.50	2025-12-01 09:56:35.738305-03	\N
979	17	6	to_client	\N	1	3.50	2025-12-01 09:56:35.761253-03	\N
980	19	6	to_client	\N	1	3.50	2025-12-01 09:56:35.777435-03	\N
981	20	18	to_client	\N	1	3.05	2025-12-01 09:56:35.786244-03	\N
982	21	4	to_client	\N	1	3.50	2025-12-01 09:56:35.797447-03	\N
983	24	6	to_client	\N	1	3.50	2025-12-01 09:56:35.806181-03	\N
984	27	6	to_client	\N	1	3.50	2025-12-01 09:56:35.813361-03	\N
985	28	10	to_client	\N	1	2.50	2025-12-01 09:56:35.820941-03	\N
986	35	4	to_client	\N	1	6.00	2025-12-01 09:56:35.827966-03	\N
987	37	4	to_client	\N	1	2.80	2025-12-01 09:56:35.837028-03	\N
988	39	4	to_client	\N	1	3.80	2025-12-01 09:56:35.848611-03	\N
989	40	4	to_client	\N	1	3.80	2025-12-01 09:56:35.857339-03	\N
990	4	20	to_client	\N	1	7.06	2025-12-04 10:39:41.620299-03	\N
991	44	40	to_client	\N	1	3.00	2025-12-04 10:39:41.638554-03	\N
992	15	25	to_client	\N	1	2.50	2025-12-04 10:39:41.649159-03	\N
993	13	10	to_client	\N	1	4.50	2025-12-04 10:39:41.659622-03	\N
994	16	6	to_client	\N	1	3.50	2025-12-04 10:39:41.671314-03	\N
995	19	4	to_client	\N	1	3.50	2025-12-04 10:39:41.683681-03	\N
996	20	18	to_client	\N	1	3.05	2025-12-04 10:39:41.692223-03	\N
997	21	6	to_client	\N	1	3.50	2025-12-04 10:39:41.699237-03	\N
998	14	12	to_client	\N	1	3.50	2025-12-04 10:39:41.70712-03	\N
999	27	6	to_client	\N	1	3.50	2025-12-04 10:39:41.717131-03	\N
1000	28	10	to_client	\N	1	2.50	2025-12-04 10:39:41.727365-03	\N
1001	35	6	to_client	\N	1	6.00	2025-12-04 10:39:41.735884-03	\N
1002	36	4	to_client	\N	1	5.50	2025-12-04 10:39:41.744412-03	\N
1003	39	4	to_client	\N	1	3.80	2025-12-04 10:39:41.75348-03	\N
1004	14	18	to_client	\N	1	3.50	2025-12-04 21:04:16.537177-03	\N
1005	24	6	to_client	\N	1	3.50	2025-12-04 21:04:16.559594-03	\N
1006	27	10	to_client	\N	1	3.50	2025-12-04 21:04:16.569367-03	\N
1007	28	10	to_client	\N	1	2.50	2025-12-04 21:04:16.578304-03	\N
1008	35	6	to_client	\N	1	6.00	2025-12-04 21:04:16.591941-03	\N
1009	39	4	to_client	\N	1	3.80	2025-12-04 21:04:16.59982-03	\N
1010	37	4	to_client	\N	1	2.80	2025-12-04 21:04:16.607322-03	\N
1011	23	4	to_client	\N	1	3.50	2025-12-04 21:04:16.613467-03	\N
1012	4	24	to_client	\N	1	7.06	2025-12-04 21:04:16.619478-03	\N
1013	15	50	to_client	\N	1	2.50	2025-12-04 21:04:16.625273-03	\N
1014	13	10	to_client	\N	1	4.50	2025-12-04 21:04:16.632228-03	\N
1015	16	12	to_client	\N	1	3.50	2025-12-04 21:04:16.639259-03	\N
1016	19	12	to_client	\N	1	3.50	2025-12-04 21:04:16.645885-03	\N
1017	20	27	to_client	\N	1	3.05	2025-12-04 21:04:16.653384-03	\N
1018	21	12	to_client	\N	1	3.50	2025-12-04 21:04:16.661288-03	\N
1019	4	0	to_client	\N	1	7.06	2025-12-11 09:57:38.311769-03	\N
1020	44	0	to_client	\N	1	3.00	2025-12-11 09:57:38.339518-03	\N
1021	15	0	to_client	\N	1	2.50	2025-12-11 09:57:38.34784-03	\N
1022	16	0	to_client	\N	1	3.50	2025-12-11 09:57:38.355892-03	\N
1023	17	0	to_client	\N	1	3.50	2025-12-11 09:57:38.363102-03	\N
1024	18	0	to_client	\N	1	3.50	2025-12-11 09:57:38.36933-03	\N
1025	19	0	to_client	\N	1	3.50	2025-12-11 09:57:38.374854-03	\N
1026	20	0	to_client	\N	1	3.05	2025-12-11 09:57:38.38101-03	\N
1027	24	0	to_client	\N	1	3.50	2025-12-11 09:57:38.391996-03	\N
1028	25	0	to_client	\N	1	3.50	2025-12-11 09:57:38.400558-03	\N
1029	14	0	to_client	\N	1	3.50	2025-12-11 09:57:38.406461-03	\N
1030	27	0	to_client	\N	1	3.50	2025-12-11 09:57:38.413933-03	\N
1031	28	0	to_client	\N	1	2.50	2025-12-11 09:57:38.421891-03	\N
1032	37	0	to_client	\N	1	2.80	2025-12-11 09:57:38.431306-03	\N
1033	13	0	to_client	\N	1	4.50	2025-12-11 09:57:38.439661-03	\N
1034	36	0	to_client	\N	1	5.50	2025-12-11 20:40:07.355776-03	\N
1035	13	0	to_client	\N	1	4.50	2025-12-11 20:40:07.371556-03	\N
1036	4	0	to_client	\N	1	7.06	2025-12-11 20:40:07.384711-03	\N
1037	44	0	to_client	\N	1	3.00	2025-12-11 20:40:07.39454-03	\N
1038	15	0	to_client	\N	1	2.50	2025-12-11 20:40:07.403352-03	\N
1039	18	0	to_client	\N	1	3.50	2025-12-11 20:40:07.412432-03	\N
1040	19	0	to_client	\N	1	3.50	2025-12-11 20:40:07.41886-03	\N
1041	20	0	to_client	\N	1	3.05	2025-12-11 20:40:07.425373-03	\N
1042	24	0	to_client	\N	1	3.50	2025-12-11 20:40:07.431141-03	\N
1043	14	0	to_client	\N	1	3.50	2025-12-11 20:40:07.438077-03	\N
1044	28	0	to_client	\N	1	2.50	2025-12-11 20:40:07.444037-03	\N
1050	37	0	to_client	\N	22	2.80	2025-12-15 20:46:04.568224-03	\N
1055	20	36	to_client	\N	22	3.05	2025-12-15 20:46:04.627417-03	\N
1045	35	0	to_client	\N	1	6.00	2025-12-11 20:40:07.450915-03	\N
1048	28	0	to_client	\N	22	2.50	2025-12-15 20:46:04.539429-03	\N
1053	15	300	to_client	\N	22	2.50	2025-12-15 20:46:04.608874-03	\N
1058	19	0	to_client	\N	22	3.50	2025-12-15 20:46:04.655669-03	\N
1046	13	0	to_client	\N	22	4.50	2025-12-15 20:46:04.48524-03	\N
1047	27	0	to_client	\N	22	3.50	2025-12-15 20:46:04.52375-03	\N
1051	4	48	to_client	\N	22	7.06	2025-12-15 20:46:04.581425-03	\N
1052	44	48	to_client	\N	22	3.00	2025-12-15 20:46:04.598281-03	\N
1056	21	12	to_client	\N	22	3.50	2025-12-15 20:46:04.635193-03	\N
1057	14	24	to_client	\N	22	3.50	2025-12-15 20:46:04.647458-03	\N
1049	35	0	to_client	\N	22	6.00	2025-12-15 20:46:04.554655-03	\N
1054	16	18	to_client	\N	22	3.50	2025-12-15 20:46:04.617718-03	\N
1059	4	80	to_client	\N	1	7.06	2026-01-04 20:02:23.822858-03	\N
1060	44	48	to_client	\N	1	3.00	2026-01-04 20:02:23.86912-03	\N
1061	15	50	to_client	\N	1	2.50	2026-01-04 20:02:23.877978-03	\N
1062	13	10	to_client	\N	1	4.50	2026-01-04 20:02:23.886882-03	\N
1063	16	24	to_client	\N	1	3.50	2026-01-04 20:02:23.894045-03	\N
1064	18	12	to_client	\N	1	3.50	2026-01-04 20:02:23.900417-03	\N
1065	19	24	to_client	\N	1	3.50	2026-01-04 20:02:23.905595-03	\N
1066	20	18	to_client	\N	1	3.05	2026-01-04 20:02:23.910901-03	\N
1067	21	12	to_client	\N	1	3.50	2026-01-04 20:02:23.91645-03	\N
1068	24	6	to_client	\N	1	3.50	2026-01-04 20:02:23.923599-03	\N
1069	26	6	to_client	\N	1	3.50	2026-01-04 20:02:23.928935-03	\N
1070	14	18	to_client	\N	1	3.50	2026-01-04 20:02:23.935639-03	\N
1071	27	5	to_client	\N	1	3.50	2026-01-04 20:02:23.940882-03	\N
1072	28	20	to_client	\N	1	2.50	2026-01-04 20:02:23.94684-03	\N
1073	35	6	to_client	\N	1	6.00	2026-01-04 20:02:23.953665-03	\N
1074	36	6	to_client	\N	1	5.50	2026-01-04 20:02:23.960288-03	\N
1075	38	4	to_client	\N	1	3.80	2026-01-04 20:02:23.968756-03	\N
1076	4	80	to_client	\N	22	7.06	2026-01-04 20:02:39.364956-03	\N
1077	44	40	to_client	\N	22	3.00	2026-01-04 20:02:39.373485-03	\N
1078	15	400	to_client	\N	22	2.50	2026-01-04 20:02:39.380124-03	\N
1079	16	24	to_client	\N	22	3.50	2026-01-04 20:02:39.385578-03	\N
1080	18	12	to_client	\N	22	3.50	2026-01-04 20:02:39.391072-03	\N
1081	19	24	to_client	\N	22	3.50	2026-01-04 20:02:39.40155-03	\N
1082	20	36	to_client	\N	22	3.05	2026-01-04 20:02:39.408203-03	\N
1083	21	12	to_client	\N	22	3.50	2026-01-04 20:02:39.415303-03	\N
1084	22	6	to_client	\N	22	3.50	2026-01-04 20:02:39.421829-03	\N
1085	24	12	to_client	\N	22	3.50	2026-01-04 20:02:39.43242-03	\N
1086	26	8	to_client	\N	22	3.50	2026-01-04 20:02:39.441266-03	\N
1087	14	18	to_client	\N	22	3.50	2026-01-04 20:02:39.447535-03	\N
1088	28	10	to_client	\N	22	2.50	2026-01-04 20:02:39.45348-03	\N
1089	29	5	to_client	\N	22	3.50	2026-01-04 20:02:39.45876-03	\N
1090	4	80	to_client	\N	22	7.06	2026-01-04 20:20:09.644383-03	\N
1091	44	40	to_client	\N	22	3.00	2026-01-04 20:20:09.653674-03	\N
1092	15	300	to_client	\N	22	2.50	2026-01-04 20:20:09.661617-03	\N
1093	13	10	to_client	\N	22	4.50	2026-01-04 20:20:09.670098-03	\N
1094	16	12	to_client	\N	22	3.50	2026-01-04 20:20:09.679273-03	\N
1095	18	6	to_client	\N	22	3.50	2026-01-04 20:20:09.688518-03	\N
1096	19	6	to_client	\N	22	3.50	2026-01-04 20:20:09.695396-03	\N
1097	20	36	to_client	\N	22	3.05	2026-01-04 20:20:09.703148-03	\N
1098	22	6	to_client	\N	22	3.50	2026-01-04 20:20:09.710146-03	\N
1099	24	8	to_client	\N	22	3.50	2026-01-04 20:20:09.719003-03	\N
1100	14	18	to_client	\N	22	3.50	2026-01-04 20:20:09.72828-03	\N
1101	28	25	to_client	\N	22	2.50	2026-01-04 20:20:09.73698-03	\N
1102	4	32	to_client	\N	1	7.06	2026-01-04 20:20:16.307126-03	\N
1103	44	32	to_client	\N	1	3.00	2026-01-04 20:20:16.317514-03	\N
1104	15	50	to_client	\N	1	2.50	2026-01-04 20:20:16.325333-03	\N
1105	13	10	to_client	\N	1	4.50	2026-01-04 20:20:16.332962-03	\N
1106	16	12	to_client	\N	1	3.50	2026-01-04 20:20:16.339844-03	\N
1107	17	6	to_client	\N	1	3.50	2026-01-04 20:20:16.346164-03	\N
1108	18	12	to_client	\N	1	3.50	2026-01-04 20:20:16.353288-03	\N
1109	20	18	to_client	\N	1	3.05	2026-01-04 20:20:16.361151-03	\N
1110	14	6	to_client	\N	1	3.50	2026-01-04 20:20:16.368275-03	\N
1111	28	15	to_client	\N	1	2.50	2026-01-04 20:20:16.377896-03	\N
1112	4	80	to_client	\N	1	7.06	2026-01-05 20:22:47.146409-03	\N
1113	44	48	to_client	\N	1	3.00	2026-01-05 20:22:47.17896-03	\N
1114	15	100	to_client	\N	1	2.50	2026-01-05 20:22:47.192176-03	\N
1115	16	12	to_client	\N	1	3.50	2026-01-05 20:22:47.208894-03	\N
1116	18	7	to_client	\N	1	3.50	2026-01-05 20:22:47.220592-03	\N
1117	19	12	to_client	\N	1	3.50	2026-01-05 20:22:47.232466-03	\N
1118	20	18	to_client	\N	1	3.05	2026-01-05 20:22:47.241308-03	\N
1119	21	12	to_client	\N	1	3.50	2026-01-05 20:22:47.248106-03	\N
1120	24	6	to_client	\N	1	3.50	2026-01-05 20:22:47.257537-03	\N
1121	14	6	to_client	\N	1	3.50	2026-01-05 20:22:47.26395-03	\N
1122	27	4	to_client	\N	1	3.50	2026-01-05 20:22:47.272037-03	\N
1123	28	15	to_client	\N	1	2.50	2026-01-05 20:22:47.280865-03	\N
1124	35	6	to_client	\N	1	6.00	2026-01-05 20:22:47.287909-03	\N
1125	39	3	to_client	\N	1	3.80	2026-01-05 20:22:47.294222-03	\N
1126	37	4	to_client	\N	1	2.80	2026-01-05 20:22:47.3017-03	\N
1127	13	10	to_client	\N	1	4.50	2026-01-05 20:22:47.308986-03	\N
783	4	2000	supplier_purchase	10	\N	7.00	2025-10-23 12:34:39.849353-03	\N
1128	18	12	to_client	\N	22	3.50	2026-01-05 21:08:22.787354-03	\N
1129	19	12	to_client	\N	22	3.50	2026-01-05 21:08:22.802315-03	\N
1130	20	54	to_client	\N	22	3.05	2026-01-05 21:08:22.814882-03	\N
1131	21	12	to_client	\N	22	3.50	2026-01-05 21:08:22.82663-03	\N
1132	24	12	to_client	\N	22	3.50	2026-01-05 21:08:22.834568-03	\N
1133	26	5	to_client	\N	22	3.50	2026-01-05 21:08:22.842758-03	\N
1134	14	12	to_client	\N	22	3.50	2026-01-05 21:08:22.851144-03	\N
1135	27	10	to_client	\N	22	3.50	2026-01-05 21:08:22.85808-03	\N
1136	28	15	to_client	\N	22	2.50	2026-01-05 21:08:22.866284-03	\N
1137	35	10	to_client	\N	22	6.00	2026-01-05 21:08:22.872638-03	\N
1138	36	4	to_client	\N	22	5.50	2026-01-05 21:08:22.878345-03	\N
1139	37	5	to_client	\N	22	2.80	2026-01-05 21:08:22.885318-03	\N
1140	4	240	to_client	\N	22	7.03	2026-01-05 21:08:22.89146-03	\N
1141	44	160	to_client	\N	22	3.00	2026-01-05 21:08:22.897106-03	\N
1142	15	250	to_client	\N	22	2.50	2026-01-05 21:08:22.903992-03	\N
1143	13	15	to_client	\N	22	4.50	2026-01-05 21:08:22.910489-03	\N
1144	16	24	to_client	\N	22	3.50	2026-01-05 21:08:22.915406-03	\N
1145	13	10	to_client	\N	1	4.50	2026-01-08 20:23:59.760279-03	\N
1146	4	40	to_client	\N	1	7.03	2026-01-08 20:23:59.793199-03	\N
1147	44	16	to_client	\N	1	3.00	2026-01-08 20:23:59.806292-03	\N
1148	16	12	to_client	\N	1	3.50	2026-01-08 20:23:59.820526-03	\N
1149	17	60	to_client	\N	1	3.50	2026-01-08 20:23:59.828106-03	\N
1150	18	12	to_client	\N	1	3.50	2026-01-08 20:23:59.83797-03	\N
1151	19	14	to_client	\N	1	3.50	2026-01-08 20:23:59.845047-03	\N
1152	20	20	to_client	\N	1	3.05	2026-01-08 20:23:59.852424-03	\N
1153	24	6	to_client	\N	1	3.50	2026-01-08 20:23:59.860151-03	\N
1154	26	5	to_client	\N	1	3.50	2026-01-08 20:23:59.868044-03	\N
1155	14	12	to_client	\N	1	3.50	2026-01-08 20:23:59.874139-03	\N
1156	27	7	to_client	\N	1	3.50	2026-01-08 20:23:59.881696-03	\N
1157	28	20	to_client	\N	1	2.50	2026-01-08 20:23:59.889084-03	\N
1158	35	7	to_client	\N	1	6.00	2026-01-08 20:23:59.896286-03	\N
1159	37	4	to_client	\N	1	2.80	2026-01-08 20:23:59.90295-03	\N
1160	39	4	to_client	\N	1	3.80	2026-01-08 20:23:59.909576-03	\N
1161	34	100	supplier_purchase	12	\N	8.00	2026-01-08 20:25:35.118351-03	\N
1162	4	60	to_client	\N	38	7.03	2026-01-08 20:25:54.81572-03	\N
1163	44	80	to_client	\N	38	3.00	2026-01-08 20:25:54.830234-03	\N
1168	18	50	to_client	\N	38	3.50	2026-01-08 20:25:54.885205-03	\N
1173	24	12	to_client	\N	38	3.50	2026-01-08 20:25:54.934368-03	\N
1178	35	16	to_client	\N	38	6.00	2026-01-08 20:25:54.986613-03	\N
1183	4	60	to_client	\N	17	7.03	2026-01-08 20:33:30.489436-03	\N
1188	17	6	to_client	\N	17	3.50	2026-01-08 20:33:30.553003-03	\N
1193	24	6	to_client	\N	17	3.50	2026-01-08 20:33:30.606108-03	\N
1198	35	6	to_client	\N	17	6.00	2026-01-08 20:33:30.668714-03	\N
1164	15	100	to_client	\N	38	2.50	2026-01-08 20:25:54.841721-03	\N
1169	19	48	to_client	\N	38	3.50	2026-01-08 20:25:54.895642-03	\N
1174	26	16	to_client	\N	38	3.50	2026-01-08 20:25:54.943463-03	\N
1179	36	16	to_client	\N	38	5.50	2026-01-08 20:25:54.996209-03	\N
1185	15	125	to_client	\N	17	2.50	2026-01-08 20:33:30.517393-03	\N
1190	20	27	to_client	\N	17	3.05	2026-01-08 20:33:30.571453-03	\N
1195	14	12	to_client	\N	17	3.50	2026-01-08 20:33:30.632242-03	\N
1200	39	5	to_client	\N	17	3.80	2026-01-08 20:33:30.692591-03	\N
1165	13	20	to_client	\N	38	4.50	2026-01-08 20:25:54.852284-03	\N
1166	16	12	to_client	\N	38	3.50	2026-01-08 20:25:54.863491-03	\N
1170	20	90	to_client	\N	38	3.05	2026-01-08 20:25:54.907567-03	\N
1171	21	48	to_client	\N	38	3.50	2026-01-08 20:25:54.917344-03	\N
1175	14	36	to_client	\N	38	3.50	2026-01-08 20:25:54.953549-03	\N
1176	28	25	to_client	\N	38	2.50	2026-01-08 20:25:54.963842-03	\N
1180	38	27	to_client	\N	38	3.80	2026-01-08 20:25:55.009313-03	\N
1181	39	27	to_client	\N	38	3.80	2026-01-08 20:25:55.018648-03	\N
1186	13	10	to_client	\N	17	4.50	2026-01-08 20:33:30.52693-03	\N
1187	16	24	to_client	\N	17	3.50	2026-01-08 20:33:30.540288-03	\N
1191	22	12	to_client	\N	17	3.50	2026-01-08 20:33:30.581879-03	\N
1192	23	5	to_client	\N	17	3.50	2026-01-08 20:33:30.591938-03	\N
1196	27	5	to_client	\N	17	3.50	2026-01-08 20:33:30.645121-03	\N
1197	28	15	to_client	\N	17	2.50	2026-01-08 20:33:30.65525-03	\N
1167	17	12	to_client	\N	38	3.50	2026-01-08 20:25:54.875904-03	\N
1172	23	10	to_client	\N	38	3.50	2026-01-08 20:25:54.925953-03	\N
1177	34	20	to_client	\N	38	8.00	2026-01-08 20:25:54.974636-03	\N
1182	40	18	to_client	\N	38	3.80	2026-01-08 20:25:55.027717-03	\N
1184	44	40	to_client	\N	17	3.00	2026-01-08 20:33:30.503089-03	\N
1189	19	7	to_client	\N	17	3.50	2026-01-08 20:33:30.561698-03	\N
1194	26	10	to_client	\N	17	3.50	2026-01-08 20:33:30.620075-03	\N
1199	38	5	to_client	\N	17	3.80	2026-01-08 20:33:30.682225-03	\N
1201	28	10000	supplier_purchase	8	\N	2.50	2026-01-08 20:34:24.865862-03	\N
1202	13	10	to_client	\N	22	4.50	2026-01-08 20:35:37.045883-03	\N
1203	4	120	to_client	\N	22	7.03	2026-01-08 20:35:37.054564-03	\N
1204	44	96	to_client	\N	22	3.00	2026-01-08 20:35:37.063209-03	\N
1205	15	250	to_client	\N	22	2.50	2026-01-08 20:35:37.072582-03	\N
1206	16	12	to_client	\N	22	3.50	2026-01-08 20:35:37.08321-03	\N
1207	18	10	to_client	\N	22	3.50	2026-01-08 20:35:37.093835-03	\N
1208	19	24	to_client	\N	22	3.50	2026-01-08 20:35:37.104173-03	\N
1209	20	108	to_client	\N	22	3.05	2026-01-08 20:35:37.112591-03	\N
1210	17	6	to_client	\N	22	3.50	2026-01-08 20:35:37.122115-03	\N
1211	24	6	to_client	\N	22	3.50	2026-01-08 20:35:37.130049-03	\N
1212	26	10	to_client	\N	22	3.50	2026-01-08 20:35:37.139073-03	\N
1213	14	18	to_client	\N	22	3.50	2026-01-08 20:35:37.146706-03	\N
1214	27	10	to_client	\N	22	3.50	2026-01-08 20:35:37.157993-03	\N
1215	28	25	to_client	\N	22	2.50	2026-01-08 20:35:37.171713-03	\N
1216	35	9	to_client	\N	22	6.00	2026-01-08 20:35:37.181984-03	\N
1217	37	4	to_client	\N	22	2.80	2026-01-08 20:35:37.195545-03	\N
1218	39	4	to_client	\N	22	3.80	2026-01-08 20:35:37.210825-03	\N
1219	4	72	to_client	\N	22	7.03	2026-01-12 20:34:01.056576-03	\N
1220	44	120	to_client	\N	22	3.00	2026-01-12 20:34:01.114385-03	\N
1221	15	100	to_client	\N	22	2.50	2026-01-12 20:34:01.13507-03	\N
1222	18	6	to_client	\N	22	3.50	2026-01-12 20:34:01.151213-03	\N
1223	19	12	to_client	\N	22	3.50	2026-01-12 20:34:01.168045-03	\N
1224	20	27	to_client	\N	22	3.05	2026-01-12 20:34:01.188912-03	\N
1225	21	6	to_client	\N	22	3.50	2026-01-12 20:34:01.202276-03	\N
1226	24	6	to_client	\N	22	3.50	2026-01-12 20:34:01.213743-03	\N
1227	26	5	to_client	\N	22	3.50	2026-01-12 20:34:01.220982-03	\N
1228	14	24	to_client	\N	22	3.50	2026-01-12 20:34:01.229495-03	\N
1229	28	15	to_client	\N	22	2.50	2026-01-12 20:34:01.2389-03	\N
1230	35	9	to_client	\N	22	6.00	2026-01-12 20:34:01.247556-03	\N
1231	36	5	to_client	\N	22	5.50	2026-01-12 20:34:01.256388-03	\N
1232	4	60	to_client	\N	17	7.03	2026-01-12 20:37:46.826451-03	\N
1233	44	72	to_client	\N	17	3.00	2026-01-12 20:37:46.836758-03	\N
1234	15	100	to_client	\N	17	2.50	2026-01-12 20:37:46.845402-03	\N
1235	13	5	to_client	\N	17	4.50	2026-01-12 20:37:46.853215-03	\N
1236	16	12	to_client	\N	17	3.50	2026-01-12 20:37:46.86212-03	\N
1237	18	6	to_client	\N	17	3.50	2026-01-12 20:37:46.868887-03	\N
1238	19	12	to_client	\N	17	3.50	2026-01-12 20:37:46.876066-03	\N
1239	20	30	to_client	\N	17	3.05	2026-01-12 20:37:46.88294-03	\N
1240	22	12	to_client	\N	17	3.50	2026-01-12 20:37:46.889919-03	\N
1241	23	5	to_client	\N	17	3.50	2026-01-12 20:37:46.898741-03	\N
1242	24	12	to_client	\N	17	3.50	2026-01-12 20:37:46.905676-03	\N
1243	26	6	to_client	\N	17	3.50	2026-01-12 20:37:46.911497-03	\N
1244	14	12	to_client	\N	17	3.50	2026-01-12 20:37:46.916858-03	\N
1245	28	20	to_client	\N	17	2.50	2026-01-12 20:37:46.923106-03	\N
1246	35	6	to_client	\N	17	6.00	2026-01-12 20:37:46.929968-03	\N
1247	36	4	to_client	\N	17	5.50	2026-01-12 20:37:46.936721-03	\N
1248	37	5	to_client	\N	17	2.80	2026-01-12 20:37:46.94435-03	\N
1249	38	6	to_client	\N	17	3.80	2026-01-12 20:37:46.950888-03	\N
1250	39	5	to_client	\N	17	3.80	2026-01-12 20:37:46.958396-03	\N
1251	40	4	to_client	\N	17	3.80	2026-01-12 20:37:46.966899-03	\N
1252	4	40	to_client	\N	1	7.03	2026-01-12 20:44:13.626908-03	\N
1253	44	32	to_client	\N	1	3.00	2026-01-12 20:44:13.634835-03	\N
1254	15	50	to_client	\N	1	2.50	2026-01-12 20:44:13.641938-03	\N
1255	16	6	to_client	\N	1	3.50	2026-01-12 20:44:13.648945-03	\N
1256	18	12	to_client	\N	1	3.50	2026-01-12 20:44:13.656325-03	\N
1257	19	24	to_client	\N	1	3.50	2026-01-12 20:44:13.663777-03	\N
1258	20	18	to_client	\N	1	3.05	2026-01-12 20:44:13.671139-03	\N
1259	21	12	to_client	\N	1	3.50	2026-01-12 20:44:13.677739-03	\N
1260	24	6	to_client	\N	1	3.50	2026-01-12 20:44:13.683874-03	\N
1261	14	12	to_client	\N	1	3.50	2026-01-12 20:44:13.689447-03	\N
1262	27	5	to_client	\N	1	3.50	2026-01-12 20:44:13.696013-03	\N
1263	28	15	to_client	\N	1	2.50	2026-01-12 20:44:13.703206-03	\N
1264	35	6	to_client	\N	1	6.00	2026-01-12 20:44:13.709288-03	\N
1265	37	4	to_client	\N	1	2.80	2026-01-12 20:44:13.715952-03	\N
1266	39	4	to_client	\N	1	3.80	2026-01-12 20:44:13.72294-03	\N
1267	38	4	to_client	\N	1	3.80	2026-01-12 20:44:13.729585-03	\N
1268	13	5	to_client	\N	1	4.50	2026-01-12 20:44:13.737104-03	\N
1269	4	60	to_client	\N	38	7.03	2026-01-12 20:48:13.790519-03	\N
1270	44	128	to_client	\N	38	3.00	2026-01-12 20:48:13.799339-03	\N
1271	15	100	to_client	\N	38	2.50	2026-01-12 20:48:13.808522-03	\N
1272	13	30	to_client	\N	38	4.50	2026-01-12 20:48:13.816468-03	\N
1273	16	12	to_client	\N	38	3.50	2026-01-12 20:48:13.825912-03	\N
1274	18	25	to_client	\N	38	3.50	2026-01-12 20:48:13.833736-03	\N
1275	19	48	to_client	\N	38	3.50	2026-01-12 20:48:13.841212-03	\N
1276	22	12	to_client	\N	38	3.50	2026-01-12 20:48:13.848124-03	\N
1277	23	10	to_client	\N	38	3.50	2026-01-12 20:48:13.858845-03	\N
1278	24	12	to_client	\N	38	3.50	2026-01-12 20:48:13.869503-03	\N
1279	14	24	to_client	\N	38	3.50	2026-01-12 20:48:13.878461-03	\N
1280	27	10	to_client	\N	38	3.50	2026-01-12 20:48:13.889807-03	\N
1281	28	35	to_client	\N	38	2.50	2026-01-12 20:48:13.897373-03	\N
1282	35	16	to_client	\N	38	6.00	2026-01-12 20:48:13.906645-03	\N
1283	37	10	to_client	\N	38	2.80	2026-01-12 20:48:13.916567-03	\N
1284	38	9	to_client	\N	38	3.80	2026-01-12 20:48:13.923438-03	\N
1285	39	9	to_client	\N	38	3.80	2026-01-12 20:48:13.933348-03	\N
1286	41	9	to_client	\N	38	3.80	2026-01-12 20:48:13.940677-03	\N
1287	34	20	to_client	\N	38	8.00	2026-01-12 20:48:13.951103-03	\N
1288	4	72	to_client	\N	22	7.03	2026-01-15 19:24:30.612125-03	\N
1289	44	16	to_client	\N	22	3.00	2026-01-15 19:24:30.647922-03	\N
1290	15	200	to_client	\N	22	2.50	2026-01-15 19:24:30.662315-03	\N
1291	18	6	to_client	\N	22	3.50	2026-01-15 19:24:30.677837-03	\N
1292	19	24	to_client	\N	22	3.50	2026-01-15 19:24:30.69357-03	\N
1293	20	36	to_client	\N	22	3.05	2026-01-15 19:24:30.704896-03	\N
1294	21	12	to_client	\N	22	3.50	2026-01-15 19:24:30.71226-03	\N
1295	35	9	to_client	\N	22	6.00	2026-01-15 19:24:30.719244-03	\N
1296	22	4	to_client	\N	22	3.50	2026-01-15 19:24:30.726892-03	\N
1297	23	5	to_client	\N	22	3.50	2026-01-15 19:24:30.73363-03	\N
1298	24	12	to_client	\N	22	3.50	2026-01-15 19:24:30.7464-03	\N
1299	36	6	to_client	\N	22	5.50	2026-01-15 19:24:30.757489-03	\N
1300	14	12	to_client	\N	22	3.50	2026-01-15 19:24:30.767661-03	\N
1305	40	2	to_client	\N	22	3.80	2026-01-15 19:24:30.820424-03	\N
1301	26	6	to_client	\N	22	3.50	2026-01-15 19:24:30.780838-03	\N
1306	41	2	to_client	\N	22	3.80	2026-01-15 19:24:30.830527-03	\N
1310	40	5	to_client	\N	17	3.80	2026-01-15 19:28:34.278456-03	\N
1315	19	20	to_client	\N	17	3.50	2026-01-15 19:28:34.321163-03	\N
1320	24	12	to_client	\N	17	3.50	2026-01-15 19:28:34.366885-03	\N
1328	19	12	to_client	\N	1	3.50	2026-01-15 19:48:55.175748-03	\N
1333	14	6	to_client	\N	1	3.50	2026-01-15 19:48:55.213936-03	\N
1338	38	4	to_client	\N	1	3.80	2026-01-15 19:48:55.253995-03	\N
1343	15	75	to_client	\N	38	2.50	2026-01-15 19:52:07.415054-03	\N
1348	22	12	to_client	\N	38	3.50	2026-01-15 19:52:07.449903-03	\N
1353	34	10	to_client	\N	38	8.00	2026-01-15 19:52:07.489479-03	\N
1357	44	32	to_client	\N	17	3.00	2026-01-19 20:42:55.254925-03	\N
1362	20	27	to_client	\N	17	3.05	2026-01-19 20:42:55.316858-03	\N
1367	26	10	to_client	\N	17	3.50	2026-01-19 20:42:55.356577-03	\N
1372	35	10	to_client	\N	17	6.00	2026-01-19 20:42:55.400164-03	\N
1302	27	10	to_client	\N	22	3.50	2026-01-15 19:24:30.790565-03	\N
1307	42	2	to_client	\N	22	3.30	2026-01-15 19:24:30.838215-03	\N
1311	4	18	to_client	\N	17	7.03	2026-01-15 19:28:34.286056-03	\N
1316	20	36	to_client	\N	17	3.05	2026-01-15 19:28:34.329775-03	\N
1321	26	6	to_client	\N	17	3.50	2026-01-15 19:28:34.373622-03	\N
1326	15	100	to_client	\N	1	2.50	2026-01-15 19:48:55.158846-03	\N
1331	24	6	to_client	\N	1	3.50	2026-01-15 19:48:55.19987-03	\N
1336	35	5	to_client	\N	1	6.00	2026-01-15 19:48:55.238508-03	\N
1341	4	40	to_client	\N	38	7.03	2026-01-15 19:52:07.399121-03	\N
1346	18	50	to_client	\N	38	3.50	2026-01-15 19:52:07.436294-03	\N
1351	26	16	to_client	\N	38	3.50	2026-01-15 19:52:07.473819-03	\N
1360	18	6	to_client	\N	17	3.50	2026-01-19 20:42:55.295473-03	\N
1365	23	5	to_client	\N	17	3.50	2026-01-19 20:42:55.340844-03	\N
1370	28	15	to_client	\N	17	2.50	2026-01-19 20:42:55.379847-03	\N
1303	28	15	to_client	\N	22	2.50	2026-01-15 19:24:30.80067-03	\N
1309	35	8	to_client	\N	17	6.00	2026-01-15 19:28:34.271209-03	\N
1314	13	10	to_client	\N	17	4.50	2026-01-15 19:28:34.312751-03	\N
1319	23	5	to_client	\N	17	3.50	2026-01-15 19:28:34.357844-03	\N
1327	18	12	to_client	\N	1	3.50	2026-01-15 19:48:55.168186-03	\N
1332	26	4	to_client	\N	1	3.50	2026-01-15 19:48:55.2074-03	\N
1337	36	3	to_client	\N	1	5.50	2026-01-15 19:48:55.245955-03	\N
1345	16	12	to_client	\N	38	3.50	2026-01-15 19:52:07.429198-03	\N
1350	27	20	to_client	\N	38	3.50	2026-01-15 19:52:07.466075-03	\N
1355	36	10	to_client	\N	38	5.50	2026-01-15 19:52:07.506768-03	\N
1359	13	10	to_client	\N	17	4.50	2026-01-19 20:42:55.282457-03	\N
1364	22	12	to_client	\N	17	3.50	2026-01-19 20:42:55.33213-03	\N
1369	27	5	to_client	\N	17	3.50	2026-01-19 20:42:55.371529-03	\N
1374	39	5	to_client	\N	17	3.80	2026-01-19 20:42:55.413785-03	\N
1304	39	2	to_client	\N	22	3.80	2026-01-15 19:24:30.812439-03	\N
1308	18	6	to_client	\N	17	3.50	2026-01-15 19:28:34.262356-03	\N
1312	44	16	to_client	\N	17	3.00	2026-01-15 19:28:34.293512-03	\N
1313	15	50	to_client	\N	17	2.50	2026-01-15 19:28:34.303049-03	\N
1317	21	6	to_client	\N	17	3.50	2026-01-15 19:28:34.34005-03	\N
1318	22	6	to_client	\N	17	3.50	2026-01-15 19:28:34.348256-03	\N
1322	14	12	to_client	\N	17	3.50	2026-01-15 19:28:34.380851-03	\N
1323	38	6	to_client	\N	17	3.80	2026-01-15 19:28:34.387356-03	\N
1324	4	60	to_client	\N	1	7.03	2026-01-15 19:48:55.140661-03	\N
1325	44	16	to_client	\N	1	3.00	2026-01-15 19:48:55.148992-03	\N
1329	20	27	to_client	\N	1	3.05	2026-01-15 19:48:55.182661-03	\N
1330	21	12	to_client	\N	1	3.50	2026-01-15 19:48:55.190736-03	\N
1334	27	5	to_client	\N	1	3.50	2026-01-15 19:48:55.223424-03	\N
1335	28	15	to_client	\N	1	2.50	2026-01-15 19:48:55.229923-03	\N
1339	39	4	to_client	\N	1	3.80	2026-01-15 19:48:55.262892-03	\N
1340	42	3	to_client	\N	1	3.30	2026-01-15 19:48:55.271158-03	\N
1342	44	64	to_client	\N	38	3.00	2026-01-15 19:52:07.408229-03	\N
1344	13	20	to_client	\N	38	4.50	2026-01-15 19:52:07.421946-03	\N
1347	14	24	to_client	\N	38	3.50	2026-01-15 19:52:07.443107-03	\N
1349	24	48	to_client	\N	38	3.50	2026-01-15 19:52:07.459186-03	\N
1352	28	50	to_client	\N	38	2.50	2026-01-15 19:52:07.481148-03	\N
1354	35	16	to_client	\N	38	6.00	2026-01-15 19:52:07.498985-03	\N
1356	4	15	to_client	\N	17	7.03	2026-01-19 20:42:55.213667-03	\N
1358	15	75	to_client	\N	17	2.50	2026-01-19 20:42:55.268971-03	\N
1361	19	18	to_client	\N	17	3.50	2026-01-19 20:42:55.309331-03	\N
1363	21	6	to_client	\N	17	3.50	2026-01-19 20:42:55.324095-03	\N
1366	24	6	to_client	\N	17	3.50	2026-01-19 20:42:55.350149-03	\N
1368	14	18	to_client	\N	17	3.50	2026-01-19 20:42:55.365094-03	\N
1371	30	8	to_client	\N	17	3.30	2026-01-19 20:42:55.387082-03	\N
1373	38	5	to_client	\N	17	3.80	2026-01-19 20:42:55.407191-03	\N
1375	4	10	to_client	\N	38	7.03	2026-01-19 20:54:56.225532-03	\N
1376	44	40	to_client	\N	38	3.00	2026-01-19 20:54:56.233741-03	\N
1377	18	25	to_client	\N	38	3.50	2026-01-19 20:54:56.242322-03	\N
1378	36	9	to_client	\N	38	5.50	2026-01-19 20:54:56.249929-03	\N
1379	38	9	to_client	\N	38	3.80	2026-01-19 20:54:56.257903-03	\N
1380	39	9	to_client	\N	38	3.80	2026-01-19 20:54:56.26594-03	\N
1381	40	9	to_client	\N	38	3.80	2026-01-19 20:54:56.272553-03	\N
1382	13	20	to_client	\N	38	4.50	2026-01-19 20:54:56.278578-03	\N
1383	14	12	to_client	\N	38	3.50	2026-01-19 20:54:56.28775-03	\N
1384	34	10	to_client	\N	38	8.00	2026-01-19 20:54:56.29529-03	\N
1385	37	4	to_client	\N	38	2.80	2026-01-19 20:54:56.30166-03	\N
1386	4	0	to_client	\N	1	7.03	2026-01-22 15:57:44.561334-03	\N
1387	44	0	to_client	\N	1	3.00	2026-01-22 15:57:44.57894-03	\N
1388	15	0	to_client	\N	1	2.50	2026-01-22 15:57:44.583761-03	\N
1389	13	0	to_client	\N	1	4.50	2026-01-22 15:57:44.588138-03	\N
1390	16	0	to_client	\N	1	3.50	2026-01-22 15:57:44.592392-03	\N
1391	18	0	to_client	\N	1	3.50	2026-01-22 15:57:44.596699-03	\N
1392	19	0	to_client	\N	1	3.50	2026-01-22 15:57:44.600961-03	\N
1393	20	0	to_client	\N	1	3.05	2026-01-22 15:57:44.605335-03	\N
1394	21	0	to_client	\N	1	3.50	2026-01-22 15:57:44.609661-03	\N
1395	24	0	to_client	\N	1	3.50	2026-01-22 15:57:44.614448-03	\N
1396	26	0	to_client	\N	1	3.50	2026-01-22 15:57:44.618953-03	\N
1397	14	0	to_client	\N	1	3.50	2026-01-22 15:57:44.623512-03	\N
1398	27	0	to_client	\N	1	3.50	2026-01-22 15:57:44.627711-03	\N
1399	28	0	to_client	\N	1	2.50	2026-01-22 15:57:44.632147-03	\N
1400	35	0	to_client	\N	1	6.00	2026-01-22 15:57:44.637412-03	\N
1401	36	0	to_client	\N	1	5.50	2026-01-22 15:57:44.641857-03	\N
1402	37	0	to_client	\N	1	2.80	2026-01-22 15:57:44.646053-03	\N
1403	38	0	to_client	\N	1	3.80	2026-01-22 15:57:44.650699-03	\N
1404	39	0	to_client	\N	1	3.80	2026-01-22 15:57:44.655443-03	\N
1405	42	0	to_client	\N	1	3.30	2026-01-22 15:57:44.660223-03	\N
1406	44	10000	supplier_purchase	2	\N	4.50	2026-01-22 19:50:46.420491-03	\N
1407	4	10000	supplier_purchase	6	\N	4.50	2026-01-22 19:51:53.989023-03	\N
1408	4	10	supplier_purchase	6	\N	4.50	2026-01-22 19:52:45.780082-03	\N
1409	4	120	to_client	\N	17	4.52	2026-01-22 19:53:01.774148-03	\N
1410	44	48	to_client	\N	17	4.16	2026-01-22 19:53:01.784075-03	\N
1411	15	100	to_client	\N	17	2.50	2026-01-22 19:53:01.792092-03	\N
1412	16	24	to_client	\N	17	3.50	2026-01-22 19:53:01.80369-03	\N
1413	18	12	to_client	\N	17	3.50	2026-01-22 19:53:01.81132-03	\N
1414	19	12	to_client	\N	17	3.50	2026-01-22 19:53:01.821028-03	\N
1415	20	36	to_client	\N	17	3.05	2026-01-22 19:53:01.831433-03	\N
1416	21	6	to_client	\N	17	3.50	2026-01-22 19:53:01.842013-03	\N
1417	22	12	to_client	\N	17	3.50	2026-01-22 19:53:01.853402-03	\N
1418	24	12	to_client	\N	17	3.50	2026-01-22 19:53:01.861021-03	\N
1419	26	5	to_client	\N	17	3.50	2026-01-22 19:53:01.870451-03	\N
1420	14	12	to_client	\N	17	3.50	2026-01-22 19:53:01.878757-03	\N
1421	27	5	to_client	\N	17	3.50	2026-01-22 19:53:01.889025-03	\N
1422	28	15	to_client	\N	17	2.50	2026-01-22 19:53:01.896367-03	\N
1423	35	5	to_client	\N	17	6.00	2026-01-22 19:53:01.904856-03	\N
1424	36	6	to_client	\N	17	5.50	2026-01-22 19:53:01.911581-03	\N
1425	39	4	to_client	\N	17	3.80	2026-01-22 19:53:01.918123-03	\N
1426	13	10	to_client	\N	17	4.50	2026-01-22 19:53:01.928418-03	\N
1427	29	5	to_client	\N	17	3.50	2026-01-22 19:53:01.936359-03	\N
1428	4	40	to_client	\N	38	4.52	2026-01-22 19:59:36.665116-03	\N
1429	44	28	to_client	\N	38	4.16	2026-01-22 19:59:36.674919-03	\N
1430	13	20	to_client	\N	38	4.50	2026-01-22 19:59:36.692897-03	\N
1431	16	24	to_client	\N	38	3.50	2026-01-22 19:59:36.706629-03	\N
1432	17	12	to_client	\N	38	3.50	2026-01-22 19:59:36.712742-03	\N
1433	18	25	to_client	\N	38	3.50	2026-01-22 19:59:36.723166-03	\N
1434	19	24	to_client	\N	38	3.50	2026-01-22 19:59:36.731871-03	\N
1435	20	18	to_client	\N	38	3.05	2026-01-22 19:59:36.738639-03	\N
1436	21	12	to_client	\N	38	3.50	2026-01-22 19:59:36.746635-03	\N
1437	26	16	to_client	\N	38	3.50	2026-01-22 19:59:36.75278-03	\N
1438	14	12	to_client	\N	38	3.50	2026-01-22 19:59:36.758129-03	\N
1439	28	25	to_client	\N	38	2.50	2026-01-22 19:59:36.763668-03	\N
1440	34	10	to_client	\N	38	8.00	2026-01-22 19:59:36.768708-03	\N
1441	39	18	to_client	\N	38	3.80	2026-01-22 19:59:36.773643-03	\N
1442	4	53	supplier_purchase	9	\N	21.00	2026-01-27 18:39:16.344981-03	\N
1443	4	80	to_client	\N	22	4.61	2026-01-29 17:12:40.542799-03	\N
1444	44	40	to_client	\N	22	4.16	2026-01-29 17:12:40.62555-03	\N
1445	15	150	to_client	\N	22	2.50	2026-01-29 17:12:40.637085-03	\N
1446	13	10	to_client	\N	22	4.50	2026-01-29 17:12:40.649194-03	\N
1447	16	12	to_client	\N	22	3.50	2026-01-29 17:12:40.656608-03	\N
1448	18	6	to_client	\N	22	3.50	2026-01-29 17:12:40.66436-03	\N
1449	19	18	to_client	\N	22	3.50	2026-01-29 17:12:40.671488-03	\N
1450	20	18	to_client	\N	22	3.05	2026-01-29 17:12:40.677611-03	\N
1451	24	6	to_client	\N	22	3.50	2026-01-29 17:12:40.683456-03	\N
1452	26	10	to_client	\N	22	3.50	2026-01-29 17:12:40.691821-03	\N
1453	14	12	to_client	\N	22	3.50	2026-01-29 17:12:40.700539-03	\N
1457	15	50	to_client	\N	38	2.50	2026-01-29 17:12:56.096901-03	\N
1462	26	8	to_client	\N	38	3.50	2026-01-29 17:12:56.12521-03	\N
1467	36	10	to_client	\N	38	5.50	2026-01-29 17:12:56.151496-03	\N
1472	4	80	to_client	\N	17	4.61	2026-01-29 17:13:11.702415-03	\N
1477	18	12	to_client	\N	17	3.50	2026-01-29 17:13:11.737182-03	\N
1482	23	5	to_client	\N	17	3.50	2026-01-29 17:13:11.776268-03	\N
1487	28	20	to_client	\N	17	2.50	2026-01-29 17:13:11.816065-03	\N
1490	16	18	to_client	\N	1	3.50	2026-01-29 17:13:25.424123-03	\N
1495	26	6	to_client	\N	1	3.50	2026-01-29 17:13:25.452188-03	\N
1500	36	4	to_client	\N	1	5.50	2026-01-29 17:13:25.479519-03	\N
1505	16	5	to_client	\N	1	3.50	2026-01-31 14:50:59.061385-03	\N
1510	14	12	to_client	\N	1	3.50	2026-01-31 14:50:59.098063-03	\N
1517	16	24	to_client	\N	17	3.50	2026-01-31 14:57:14.454276-03	\N
1522	23	6	to_client	\N	17	3.50	2026-01-31 14:57:14.486292-03	\N
1527	35	8	to_client	\N	17	6.00	2026-01-31 14:57:14.518156-03	\N
1532	41	3	to_client	\N	17	3.80	2026-01-31 14:57:14.546694-03	\N
1541	13	10	to_client	\N	22	4.50	2026-01-31 15:04:43.894456-03	\N
1546	21	6	to_client	\N	22	3.50	2026-01-31 15:04:43.930626-03	\N
1551	28	20	to_client	\N	22	2.50	2026-01-31 15:04:43.960489-03	\N
1557	44	144	to_client	\N	38	4.16	2026-01-31 15:08:24.60988-03	\N
1562	18	50	to_client	\N	38	3.50	2026-01-31 15:08:24.639035-03	\N
1567	23	5	to_client	\N	38	3.50	2026-01-31 15:08:24.670875-03	\N
1572	34	10	to_client	\N	38	8.00	2026-01-31 15:08:24.701955-03	\N
1577	41	9	to_client	\N	38	3.80	2026-01-31 15:08:24.730744-03	\N
1454	29	5	to_client	\N	22	3.50	2026-01-29 17:12:40.706918-03	\N
1455	4	80	to_client	\N	38	4.61	2026-01-29 17:12:56.083829-03	\N
1460	19	24	to_client	\N	38	3.50	2026-01-29 17:12:56.115497-03	\N
1465	34	10	to_client	\N	38	8.00	2026-01-29 17:12:56.140265-03	\N
1470	39	9	to_client	\N	38	3.80	2026-01-29 17:12:56.173825-03	\N
1474	15	75	to_client	\N	17	2.50	2026-01-29 17:13:11.716195-03	\N
1479	20	18	to_client	\N	17	3.05	2026-01-29 17:13:11.749183-03	\N
1484	26	6	to_client	\N	17	3.50	2026-01-29 17:13:11.792792-03	\N
1492	20	18	to_client	\N	1	3.05	2026-01-29 17:13:25.43564-03	\N
1497	27	5	to_client	\N	1	3.50	2026-01-29 17:13:25.463087-03	\N
1456	44	144	to_client	\N	38	4.16	2026-01-29 17:12:56.090431-03	\N
1461	20	72	to_client	\N	38	3.05	2026-01-29 17:12:56.120225-03	\N
1466	35	16	to_client	\N	38	6.00	2026-01-29 17:12:56.145412-03	\N
1471	40	9	to_client	\N	38	3.80	2026-01-29 17:12:56.182549-03	\N
1473	44	48	to_client	\N	17	4.16	2026-01-29 17:13:11.709062-03	\N
1478	19	12	to_client	\N	17	3.50	2026-01-29 17:13:11.743272-03	\N
1483	24	9	to_client	\N	17	3.50	2026-01-29 17:13:11.784169-03	\N
1488	38	5	to_client	\N	17	3.80	2026-01-29 17:13:11.825222-03	\N
1493	22	6	to_client	\N	1	3.50	2026-01-29 17:13:25.441402-03	\N
1498	28	15	to_client	\N	1	2.50	2026-01-29 17:13:25.468894-03	\N
1502	4	32	to_client	\N	1	4.61	2026-01-31 14:50:59.02263-03	\N
1507	19	18	to_client	\N	1	3.50	2026-01-31 14:50:59.080072-03	\N
1512	35	4	to_client	\N	1	6.00	2026-01-31 14:50:59.109651-03	\N
1516	15	100	to_client	\N	17	2.50	2026-01-31 14:57:14.447024-03	\N
1521	20	36	to_client	\N	17	3.05	2026-01-31 14:57:14.480199-03	\N
1526	29	5	to_client	\N	17	3.50	2026-01-31 14:57:14.511406-03	\N
1531	40	5	to_client	\N	17	3.80	2026-01-31 14:57:14.540929-03	\N
1536	30	5	to_client	\N	17	3.30	2026-01-31 14:57:14.569967-03	\N
1540	15	175	to_client	\N	22	2.50	2026-01-31 15:04:43.887996-03	\N
1545	20	27	to_client	\N	22	3.05	2026-01-31 15:04:43.922436-03	\N
1550	14	18	to_client	\N	22	3.50	2026-01-31 15:04:43.954327-03	\N
1555	39	4	to_client	\N	22	3.80	2026-01-31 15:04:43.986567-03	\N
1559	13	40	to_client	\N	38	4.50	2026-01-31 15:08:24.622118-03	\N
1564	20	36	to_client	\N	38	3.05	2026-01-31 15:08:24.6506-03	\N
1569	14	24	to_client	\N	38	3.50	2026-01-31 15:08:24.681415-03	\N
1574	38	18	to_client	\N	38	3.80	2026-01-31 15:08:24.714067-03	\N
1458	16	24	to_client	\N	38	3.50	2026-01-29 17:12:56.102554-03	\N
1459	18	15	to_client	\N	38	3.50	2026-01-29 17:12:56.109198-03	\N
1463	14	24	to_client	\N	38	3.50	2026-01-29 17:12:56.130467-03	\N
1464	28	25	to_client	\N	38	2.50	2026-01-29 17:12:56.135547-03	\N
1468	37	9	to_client	\N	38	2.80	2026-01-29 17:12:56.157707-03	\N
1469	38	9	to_client	\N	38	3.80	2026-01-29 17:12:56.166719-03	\N
1475	13	10	to_client	\N	17	4.50	2026-01-29 17:13:11.724301-03	\N
1476	16	24	to_client	\N	17	3.50	2026-01-29 17:13:11.729697-03	\N
1480	21	6	to_client	\N	17	3.50	2026-01-29 17:13:11.754969-03	\N
1481	22	12	to_client	\N	17	3.50	2026-01-29 17:13:11.764898-03	\N
1485	14	12	to_client	\N	17	3.50	2026-01-29 17:13:11.798574-03	\N
1486	27	10	to_client	\N	17	3.50	2026-01-29 17:13:11.806554-03	\N
1489	4	32	to_client	\N	1	4.61	2026-01-29 17:13:25.418378-03	\N
1491	18	6	to_client	\N	1	3.50	2026-01-29 17:13:25.429773-03	\N
1494	24	6	to_client	\N	1	3.50	2026-01-29 17:13:25.447109-03	\N
1496	14	12	to_client	\N	1	3.50	2026-01-29 17:13:25.457371-03	\N
1499	35	5	to_client	\N	1	6.00	2026-01-29 17:13:25.474507-03	\N
1501	39	4	to_client	\N	1	3.80	2026-01-29 17:13:25.484665-03	\N
1503	44	24	to_client	\N	1	4.16	2026-01-31 14:50:59.038636-03	\N
1504	15	125	to_client	\N	1	2.50	2026-01-31 14:50:59.049928-03	\N
1506	18	12	to_client	\N	1	3.50	2026-01-31 14:50:59.071277-03	\N
1508	20	18	to_client	\N	1	3.05	2026-01-31 14:50:59.086428-03	\N
1509	24	6	to_client	\N	1	3.50	2026-01-31 14:50:59.09259-03	\N
1511	28	10	to_client	\N	1	2.50	2026-01-31 14:50:59.103877-03	\N
1513	39	6	to_client	\N	1	3.80	2026-01-31 14:50:59.115258-03	\N
1514	13	5	to_client	\N	1	4.50	2026-01-31 14:50:59.121655-03	\N
1515	4	60	to_client	\N	17	4.61	2026-01-31 14:57:14.439372-03	\N
1518	13	10	to_client	\N	17	4.50	2026-01-31 14:57:14.460854-03	\N
1519	44	45	to_client	\N	17	4.16	2026-01-31 14:57:14.467346-03	\N
1520	19	24	to_client	\N	17	3.50	2026-01-31 14:57:14.47401-03	\N
1523	24	12	to_client	\N	17	3.50	2026-01-31 14:57:14.492553-03	\N
1524	26	5	to_client	\N	17	3.50	2026-01-31 14:57:14.498432-03	\N
1525	28	25	to_client	\N	17	2.50	2026-01-31 14:57:14.504133-03	\N
1528	36	5	to_client	\N	17	5.50	2026-01-31 14:57:14.524307-03	\N
1529	38	6	to_client	\N	17	3.80	2026-01-31 14:57:14.530127-03	\N
1530	39	5	to_client	\N	17	3.80	2026-01-31 14:57:14.535475-03	\N
1533	42	3	to_client	\N	17	3.30	2026-01-31 14:57:14.552958-03	\N
1534	18	12	to_client	\N	17	3.50	2026-01-31 14:57:14.558243-03	\N
1535	14	12	to_client	\N	17	3.50	2026-01-31 14:57:14.563144-03	\N
1537	36	6	to_client	\N	22	5.50	2026-01-31 15:04:43.864238-03	\N
1538	4	40	to_client	\N	22	4.61	2026-01-31 15:04:43.873986-03	\N
1539	44	32	to_client	\N	22	4.16	2026-01-31 15:04:43.881234-03	\N
1542	16	24	to_client	\N	22	3.50	2026-01-31 15:04:43.90059-03	\N
1543	18	6	to_client	\N	22	3.50	2026-01-31 15:04:43.906994-03	\N
1544	19	24	to_client	\N	22	3.50	2026-01-31 15:04:43.914174-03	\N
1547	23	5	to_client	\N	22	3.50	2026-01-31 15:04:43.936885-03	\N
1548	24	12	to_client	\N	22	3.50	2026-01-31 15:04:43.942618-03	\N
1549	26	8	to_client	\N	22	3.50	2026-01-31 15:04:43.948614-03	\N
1552	29	5	to_client	\N	22	3.50	2026-01-31 15:04:43.966635-03	\N
1553	30	8	to_client	\N	22	3.30	2026-01-31 15:04:43.972445-03	\N
1554	35	6	to_client	\N	22	6.00	2026-01-31 15:04:43.979362-03	\N
1556	4	10	to_client	\N	38	4.61	2026-01-31 15:08:24.601493-03	\N
1558	15	75	to_client	\N	38	2.50	2026-01-31 15:08:24.616284-03	\N
1560	16	18	to_client	\N	38	3.50	2026-01-31 15:08:24.627377-03	\N
1561	17	12	to_client	\N	38	3.50	2026-01-31 15:08:24.632938-03	\N
1563	19	12	to_client	\N	38	3.50	2026-01-31 15:08:24.644597-03	\N
1565	21	12	to_client	\N	38	3.50	2026-01-31 15:08:24.657015-03	\N
1566	22	6	to_client	\N	38	3.50	2026-01-31 15:08:24.663587-03	\N
1568	26	6	to_client	\N	38	3.50	2026-01-31 15:08:24.6762-03	\N
1570	27	10	to_client	\N	38	3.50	2026-01-31 15:08:24.687491-03	\N
1571	28	25	to_client	\N	38	2.50	2026-01-31 15:08:24.693976-03	\N
1573	36	10	to_client	\N	38	5.50	2026-01-31 15:08:24.708503-03	\N
1575	39	18	to_client	\N	38	3.80	2026-01-31 15:08:24.719681-03	\N
1576	40	9	to_client	\N	38	3.80	2026-01-31 15:08:24.725203-03	\N
1578	4	40	to_client	\N	1	4.61	2026-02-04 10:07:21.314095-03	\N
1579	13	10	to_client	\N	1	4.50	2026-02-04 10:07:21.346067-03	\N
1580	14	12	to_client	\N	1	3.50	2026-02-04 10:07:21.36333-03	\N
1581	15	50	to_client	\N	1	2.50	2026-02-04 10:07:21.374578-03	\N
1582	18	6	to_client	\N	1	3.50	2026-02-04 10:07:21.39141-03	\N
1583	19	12	to_client	\N	1	3.50	2026-02-04 10:07:21.410123-03	\N
1584	20	18	to_client	\N	1	3.05	2026-02-04 10:07:21.418571-03	\N
1585	22	4	to_client	\N	1	3.50	2026-02-04 10:07:21.425943-03	\N
1586	24	6	to_client	\N	1	3.50	2026-02-04 10:07:21.439537-03	\N
1587	27	5	to_client	\N	1	3.50	2026-02-04 10:07:21.4483-03	\N
1588	28	20	to_client	\N	1	2.50	2026-02-04 10:07:21.456962-03	\N
1589	30	10	to_client	\N	1	3.30	2026-02-04 10:07:21.465271-03	\N
1590	35	4	to_client	\N	1	6.00	2026-02-04 10:07:21.481938-03	\N
1591	36	4	to_client	\N	1	5.50	2026-02-04 10:07:21.489701-03	\N
1592	39	4	to_client	\N	1	3.80	2026-02-04 10:07:21.501431-03	\N
1593	42	4	to_client	\N	1	3.30	2026-02-04 10:07:21.515737-03	\N
1594	44	24	to_client	\N	1	4.16	2026-02-04 10:07:21.522713-03	\N
1595	4	84	to_client	\N	17	4.61	2026-02-04 10:11:34.620375-03	\N
1596	44	48	to_client	\N	17	4.16	2026-02-04 10:11:34.628077-03	\N
1597	13	10	to_client	\N	17	4.50	2026-02-04 10:11:34.634035-03	\N
1598	16	12	to_client	\N	17	3.50	2026-02-04 10:11:34.640499-03	\N
1599	18	12	to_client	\N	17	3.50	2026-02-04 10:11:34.647516-03	\N
1600	19	18	to_client	\N	17	3.50	2026-02-04 10:11:34.654203-03	\N
1601	20	33	to_client	\N	17	3.05	2026-02-04 10:11:34.65968-03	\N
1602	23	5	to_client	\N	17	3.50	2026-02-04 10:11:34.665632-03	\N
1603	24	12	to_client	\N	17	3.50	2026-02-04 10:11:34.671489-03	\N
1604	14	12	to_client	\N	17	3.50	2026-02-04 10:11:34.67794-03	\N
1605	28	20	to_client	\N	17	2.50	2026-02-04 10:11:34.683811-03	\N
1606	35	8	to_client	\N	17	6.00	2026-02-04 10:11:34.689281-03	\N
1607	38	4	to_client	\N	17	3.80	2026-02-04 10:11:34.694655-03	\N
1608	39	5	to_client	\N	17	3.80	2026-02-04 10:11:34.699759-03	\N
1609	41	3	to_client	\N	17	3.80	2026-02-04 10:11:34.705292-03	\N
26	14	3000	supplier_purchase	2	\N	3.50	2025-09-11 08:38:43.674646-03	\N
1610	4	60	to_client	\N	38	4.61	2026-02-04 10:18:30.634936-03	\N
1611	44	160	to_client	\N	38	4.16	2026-02-04 10:18:30.644962-03	\N
1612	15	100	to_client	\N	38	2.50	2026-02-04 10:18:30.654975-03	\N
1613	13	20	to_client	\N	38	4.50	2026-02-04 10:18:30.661512-03	\N
1614	16	24	to_client	\N	38	3.50	2026-02-04 10:18:30.667644-03	\N
1615	17	12	to_client	\N	38	3.50	2026-02-04 10:18:30.674443-03	\N
1616	18	50	to_client	\N	38	3.50	2026-02-04 10:18:30.68101-03	\N
1617	19	24	to_client	\N	38	3.50	2026-02-04 10:18:30.69106-03	\N
1618	20	18	to_client	\N	38	3.05	2026-02-04 10:18:30.697138-03	\N
1619	21	24	to_client	\N	38	3.50	2026-02-04 10:18:30.702421-03	\N
1620	23	10	to_client	\N	38	3.50	2026-02-04 10:18:30.708399-03	\N
1625	28	40	to_client	\N	38	2.50	2026-02-04 10:18:30.740688-03	\N
1630	39	18	to_client	\N	38	3.80	2026-02-04 10:18:30.770104-03	\N
1637	13	9	to_client	\N	22	4.50	2026-02-04 10:22:01.165239-03	\N
1642	22	6	to_client	\N	22	3.50	2026-02-04 10:22:01.209673-03	\N
1647	39	4	to_client	\N	22	3.80	2026-02-04 10:22:01.254276-03	\N
1621	24	24	to_client	\N	38	3.50	2026-02-04 10:18:30.714044-03	\N
1626	34	20	to_client	\N	38	8.00	2026-02-04 10:18:30.745984-03	\N
1631	41	9	to_client	\N	38	3.80	2026-02-04 10:18:30.776375-03	\N
1634	4	64	to_client	\N	22	4.61	2026-02-04 10:22:01.138495-03	\N
1639	18	6	to_client	\N	22	3.50	2026-02-04 10:22:01.182721-03	\N
1644	24	12	to_client	\N	22	3.50	2026-02-04 10:22:01.227019-03	\N
1649	41	3	to_client	\N	22	3.80	2026-02-04 10:22:01.270966-03	\N
1622	26	10	to_client	\N	38	3.50	2026-02-04 10:18:30.721694-03	\N
1627	36	9	to_client	\N	38	5.50	2026-02-04 10:18:30.751956-03	\N
1632	30	10	to_client	\N	38	3.30	2026-02-04 10:18:30.783781-03	\N
1635	44	16	to_client	\N	22	4.16	2026-02-04 10:22:01.146237-03	\N
1640	19	18	to_client	\N	22	3.50	2026-02-04 10:22:01.190246-03	\N
1645	14	12	to_client	\N	22	3.50	2026-02-04 10:22:01.233812-03	\N
1623	14	48	to_client	\N	38	3.50	2026-02-04 10:18:30.727936-03	\N
1628	37	9	to_client	\N	38	2.80	2026-02-04 10:18:30.757248-03	\N
1624	27	20	to_client	\N	38	3.50	2026-02-04 10:18:30.734542-03	\N
1629	38	18	to_client	\N	38	3.80	2026-02-04 10:18:30.763322-03	\N
1633	42	3	to_client	\N	22	3.30	2026-02-04 10:22:01.128183-03	\N
1636	15	100	to_client	\N	22	2.50	2026-02-04 10:22:01.154238-03	\N
1638	16	12	to_client	\N	22	3.50	2026-02-04 10:22:01.176664-03	\N
1641	20	10	to_client	\N	22	3.05	2026-02-04 10:22:01.200809-03	\N
1643	23	5	to_client	\N	22	3.50	2026-02-04 10:22:01.219335-03	\N
1646	28	20	to_client	\N	22	2.50	2026-02-04 10:22:01.244712-03	\N
1648	27	9	to_client	\N	22	3.50	2026-02-04 10:22:01.262957-03	\N
\.


--
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.suppliers (id, name, contact_email, contact_phone, address, created_at, updated_at) FROM stdin;
2	DOUGLAS	\N	\N	\N	2025-09-10 17:29:30.052239-03	\N
1	EDEVALDO (Di)	\N	\N	\N	2025-09-10 17:29:23.599393-03	2025-09-10 17:29:39.059414-03
3	MARCOS	\N	\N	\N	2025-09-10 17:29:52.706558-03	\N
4	LUCAS	\N	\N	\N	2025-09-10 17:30:04.138602-03	\N
5	HIDERALDO	\N	\N	\N	2025-09-10 17:31:15.763424-03	\N
6	CEASA (MORANGO)	\N	\N	\N	2025-09-10 17:31:38.364959-03	\N
7	ISMARIO	\N	\N	\N	2025-09-10 17:32:01.256213-03	\N
8	JAILSON	\N	\N	\N	2025-09-10 17:32:11.563888-03	\N
9	MÁRCIA	\N	\N	\N	2025-09-10 17:32:19.850077-03	\N
10	ALMEIDA	\N	\N	\N	2025-09-10 17:32:25.293233-03	\N
11	MIKHAIL	\N	\N	\N	2025-09-10 17:32:44.330924-03	\N
12	GIOVANNI	\N	\N	\N	2025-09-10 17:32:57.104699-03	\N
13	RODRIGO (TOMATINHO	\N	\N	\N	2025-09-10 17:33:09.352532-03	\N
14	VALTER (TOMATE)	\N	\N	\N	2025-09-10 17:33:20.759892-03	\N
15	GAMBÁ	\N	\N	\N	2025-09-10 17:33:33.619907-03	\N
16	MORINISHI	\N	\N	\N	2025-09-10 17:33:53.024929-03	\N
17	ERICA (MANDIOCA)	\N	\N	\N	2025-09-10 17:34:13.361228-03	\N
\.


--
-- Data for Name: ticket_products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ticket_products (id, ticket_id, product_id, sent_quantity, unit_price, entry_price) FROM stdin;
2210	174	4	32	6.50	\N
2211	174	16	18	8.40	\N
2212	174	18	6	7.70	\N
2213	174	20	18	5.95	\N
2214	174	22	6	7.00	\N
2215	174	24	6	8.40	\N
2216	174	26	6	10.50	\N
2217	174	14	12	9.10	\N
2218	174	27	5	5.90	\N
2219	174	28	15	4.90	\N
2220	174	35	5	9.80	\N
2221	174	36	4	9.80	\N
2222	174	39	4	7.00	\N
2362	181	36	6	9.52	5.50
2269	178	4	10	4.00	\N
2270	178	44	144	6.00	\N
2272	178	15	75	4.80	\N
2271	178	13	40	6.50	\N
2273	178	16	18	7.90	\N
2274	178	17	12	9.20	\N
2275	178	18	50	4.80	\N
2276	178	19	12	6.80	\N
2277	178	20	36	5.60	\N
2278	178	21	12	6.80	\N
2279	178	22	6	6.40	\N
2280	178	23	5	6.00	\N
2283	178	26	6	9.60	\N
2284	178	14	24	8.80	\N
2285	178	27	10	7.20	\N
2286	178	28	25	5.20	\N
2287	178	34	10	13.00	\N
2289	178	36	10	9.20	\N
2291	178	38	18	6.80	\N
2294	178	39	18	6.80	\N
2292	178	40	9	6.80	\N
2293	178	41	9	6.80	\N
2456	185	42	4	7.00	3.30
2389	183	4	84	5.96	\N
2390	183	44	48	7.56	\N
2392	183	13	10	9.52	\N
2393	183	16	12	7.96	\N
2395	183	18	12	7.92	\N
2396	183	19	18	7.12	\N
2397	183	20	33	5.96	\N
2414	183	23	5	5.56	\N
2400	183	24	12	7.56	\N
2403	183	14	12	9.52	\N
2405	183	28	20	5.96	\N
2406	183	35	8	8.72	\N
2409	183	38	4	7.56	\N
2410	183	39	5	7.56	\N
2412	183	41	3	7.56	\N
2363	182	4	60	4.00	\N
2364	182	44	160	6.00	\N
2365	182	15	100	4.80	\N
2381	182	13	20	6.50	\N
2374	182	16	24	7.90	\N
2379	182	17	12	9.20	\N
2382	182	18	50	4.80	\N
2373	182	19	24	6.80	\N
2380	182	20	18	5.60	\N
2372	182	21	24	6.80	\N
2385	182	23	10	6.00	\N
2371	182	24	24	7.20	\N
2367	182	26	10	9.60	\N
2386	182	14	48	8.80	\N
2387	182	27	20	7.20	\N
2369	182	28	40	5.20	\N
2383	182	34	20	13.00	\N
2366	182	36	9	9.20	\N
2384	182	37	9	5.20	\N
2378	182	38	18	6.80	\N
2375	182	39	18	6.80	\N
2376	182	41	9	6.80	\N
2460	184	42	3	7.56	3.30
2541	189	4	0	0.00	\N
2542	189	44	0	0.00	\N
2543	189	15	0	0.00	\N
2544	189	13	0	0.00	\N
2545	189	16	0	0.00	\N
2546	189	18	0	0.00	\N
2547	189	19	0	0.00	\N
2548	189	20	0	0.00	\N
2549	189	21	0	0.00	\N
2550	189	22	0	0.00	\N
2551	189	24	0	0.00	\N
2552	189	26	0	0.00	\N
2553	189	14	0	0.00	\N
2554	189	27	0	0.00	\N
2555	189	28	0	0.00	\N
2556	189	30	0	0.00	\N
2557	189	35	0	0.00	\N
2558	189	36	0	0.00	\N
2559	189	39	0	0.00	\N
2560	189	42	0	0.00	\N
2223	175	4	80	5.96	\N
2224	175	44	48	7.56	\N
2225	175	15	75	5.52	\N
2226	175	13	10	9.52	\N
2227	175	16	24	7.96	\N
2228	175	18	12	7.92	\N
2229	175	19	12	7.12	\N
2230	175	20	18	5.96	\N
2231	175	21	6	7.92	\N
2232	175	22	12	7.12	\N
2233	175	23	5	5.56	\N
2234	175	24	9	7.56	\N
2235	175	26	6	9.52	\N
2236	175	14	12	9.52	\N
2237	175	27	10	7.16	\N
2238	175	28	20	5.96	\N
2239	175	38	5	7.56	\N
2252	177	4	80	4.00	\N
2253	177	44	144	6.00	\N
2254	177	15	50	4.80	\N
2255	177	16	24	7.90	\N
2256	177	18	15	4.80	\N
2257	177	19	24	6.80	\N
2258	177	20	72	5.60	\N
2259	177	26	8	9.60	\N
2260	177	14	24	8.80	\N
2261	177	28	25	5.20	\N
2262	177	34	10	13.00	\N
2263	177	35	16	9.20	\N
2264	177	36	10	9.20	\N
2265	177	37	9	5.20	\N
2266	177	38	9	6.80	\N
2267	177	39	9	6.80	\N
2268	177	40	9	6.80	\N
2296	179	4	60	5.96	\N
2312	179	15	100	5.52	\N
2299	179	16	24	7.96	\N
2298	179	13	10	9.52	\N
2297	179	44	45	7.56	\N
2300	179	19	24	7.12	\N
2301	179	20	36	5.96	\N
2313	179	23	6	5.56	\N
2310	179	24	12	7.56	\N
2303	179	26	5	9.52	\N
2305	179	28	25	5.96	\N
2314	179	29	5	5.96	\N
2306	179	35	8	8.72	\N
2307	179	36	5	9.52	\N
2308	179	38	6	7.56	\N
2309	179	39	5	7.56	\N
2315	179	40	5	7.56	\N
2317	179	41	3	7.56	\N
2318	179	42	3	7.56	\N
2339	181	4	40	5.96	\N
2340	181	44	32	7.56	\N
2341	181	15	175	5.52	\N
2342	181	13	10	9.52	\N
2343	181	16	24	7.96	\N
2344	181	18	6	7.92	\N
2345	181	19	24	7.12	\N
2346	181	20	27	5.96	\N
2347	181	21	6	7.92	\N
2349	181	23	5	5.56	\N
2350	181	24	12	7.56	\N
2351	181	26	8	9.52	\N
2352	181	14	18	9.52	\N
2353	181	28	20	5.96	\N
2354	181	29	5	5.96	\N
2358	181	30	8	6.76	\N
2355	181	35	6	8.72	\N
2356	181	39	4	7.56	\N
2457	182	30	10	5.95	3.30
2417	184	4	64	5.96	\N
2418	184	44	16	7.56	\N
2419	184	15	100	5.52	\N
2420	184	13	9	9.52	\N
2421	184	16	12	7.96	\N
2422	184	18	6	7.92	\N
2423	184	19	18	7.12	\N
2424	184	20	10	5.96	\N
2426	184	22	6	7.12	\N
2427	184	23	5	5.56	\N
2428	184	24	12	7.56	\N
2430	184	14	12	9.52	\N
2431	184	28	20	5.96	\N
2436	184	39	4	7.56	\N
2461	186	20	0	0.00	\N
2462	186	4	0	0.00	\N
2463	186	44	0	0.00	\N
2464	186	15	0	0.00	\N
2465	186	13	0	0.00	\N
2466	186	16	0	0.00	\N
2467	186	17	0	0.00	\N
2468	186	18	0	0.00	\N
2469	186	19	0	0.00	\N
2470	186	21	0	0.00	\N
2471	186	22	0	0.00	\N
2472	186	23	0	0.00	\N
2473	186	24	0	0.00	\N
2474	186	25	0	0.00	\N
2475	186	26	0	0.00	\N
2476	186	14	0	0.00	\N
2477	186	27	0	0.00	\N
2478	186	28	0	0.00	\N
2479	186	30	0	0.00	\N
2480	186	34	0	0.00	\N
2481	186	35	0	0.00	\N
2482	186	36	0	0.00	\N
2483	186	37	0	0.00	\N
2484	186	38	0	0.00	\N
2485	186	39	0	0.00	\N
2486	186	40	0	0.00	\N
2487	186	41	0	0.00	\N
2488	187	4	0	0.00	\N
2489	187	44	0	0.00	\N
2490	187	15	0	0.00	\N
2491	187	13	0	0.00	\N
2492	187	16	0	0.00	\N
2493	187	17	0	0.00	\N
2494	187	18	0	0.00	\N
2495	187	19	0	0.00	\N
2496	187	20	0	0.00	\N
2497	187	21	0	0.00	\N
2498	187	22	0	0.00	\N
2499	187	23	0	0.00	\N
2500	187	24	0	0.00	\N
2501	187	25	0	0.00	\N
2502	187	26	0	0.00	\N
2503	187	14	0	0.00	\N
2504	187	27	0	0.00	\N
2505	187	28	0	0.00	\N
2240	176	4	80	5.96	\N
2241	176	44	40	7.56	\N
2242	176	15	150	5.52	\N
2243	176	13	10	9.52	\N
2244	176	16	12	7.96	\N
2245	176	18	6	7.92	\N
2246	176	19	18	7.12	\N
2247	176	20	18	5.96	\N
2248	176	24	6	7.56	\N
2249	176	26	10	9.52	\N
2250	176	14	12	9.52	\N
2251	176	29	5	5.96	\N
2319	180	4	32	6.50	\N
2320	180	44	24	6.50	\N
2321	180	15	125	4.55	\N
2323	180	16	5	8.40	\N
2325	180	18	12	7.70	\N
2326	180	19	18	7.70	\N
2327	180	20	18	5.95	\N
2332	180	24	6	8.40	\N
2333	180	14	12	9.10	\N
2335	180	28	10	4.90	\N
2336	180	35	4	9.80	\N
2338	180	39	6	7.00	\N
2322	180	13	5	10.10	\N
2437	185	4	40	6.50	\N
2438	185	44	24	6.50	\N
2439	185	15	50	4.55	\N
2506	187	35	0	0.00	\N
2442	185	18	6	7.70	\N
2443	185	19	12	7.70	\N
2444	185	20	18	5.95	\N
2446	185	22	4	7.00	\N
2447	185	24	6	8.40	\N
2449	185	14	12	9.10	\N
2450	185	27	5	5.90	\N
2451	185	28	20	4.90	\N
2452	185	35	4	9.80	\N
2453	185	36	4	9.80	\N
2454	185	39	4	7.00	\N
2440	185	13	10	10.10	\N
2458	184	27	9	7.16	3.50
2507	187	36	0	0.00	\N
2508	187	37	0	0.00	\N
2509	187	38	0	0.00	\N
2510	187	39	0	0.00	\N
2511	187	40	0	0.00	\N
2512	187	41	0	0.00	\N
2513	187	42	0	0.00	\N
2064	168	4	120	5.96	\N
2065	168	44	48	7.56	\N
2066	168	15	100	5.52	\N
2082	168	36	6	9.52	\N
2138	168	13	10	9.52	4.50
2067	168	16	24	7.96	\N
2069	168	18	12	7.92	\N
2070	168	19	12	7.12	\N
2071	168	20	36	5.96	\N
2072	168	21	6	7.92	\N
2073	168	22	12	7.12	\N
2075	168	24	12	7.56	\N
2077	168	26	5	9.52	\N
2078	168	14	12	9.52	\N
2079	168	27	5	7.16	\N
2080	168	28	15	5.96	\N
2139	168	29	5	5.96	3.50
2081	168	35	5	8.72	\N
2085	168	39	4	7.56	\N
2089	169	4	40	4.00	\N
2161	172	4	0	0.00	\N
2092	169	13	20	6.50	\N
2093	169	16	24	7.90	\N
2094	169	17	12	9.20	\N
2095	169	18	25	4.80	\N
2096	169	19	24	6.80	\N
2097	169	20	18	5.60	\N
2098	169	21	12	6.80	\N
2103	169	26	16	9.60	\N
2104	169	14	12	8.80	\N
2106	169	28	25	5.20	\N
2107	169	34	10	13.00	\N
2140	169	39	18	6.80	3.80
2090	169	44	128	6.00	\N
2141	171	4	0	0.00	\N
2142	171	44	0	0.00	\N
2143	171	15	0	0.00	\N
2144	171	16	0	0.00	\N
2145	171	18	0	0.00	\N
2146	171	19	0	0.00	\N
2147	171	20	0	0.00	\N
2148	171	21	0	0.00	\N
2149	171	26	0	0.00	\N
2150	171	14	0	0.00	\N
2151	171	27	0	0.00	\N
2152	171	28	0	0.00	\N
2153	171	35	0	0.00	\N
2154	171	16	0	0.00	\N
2155	171	17	0	0.00	\N
2156	171	13	0	0.00	\N
2162	172	44	0	0.00	\N
2163	172	15	0	0.00	\N
2164	172	13	0	0.00	\N
2165	172	16	0	0.00	\N
2166	172	17	0	0.00	\N
2167	172	18	0	0.00	\N
2168	172	19	0	0.00	\N
2169	172	20	0	0.00	\N
2170	172	21	0	0.00	\N
2171	172	22	0	0.00	\N
2172	172	23	0	0.00	\N
2173	172	25	0	0.00	\N
2174	172	26	0	0.00	\N
2175	172	14	0	0.00	\N
2176	172	27	0	0.00	\N
2177	172	28	0	0.00	\N
2178	172	35	0	0.00	\N
2179	172	37	0	0.00	\N
2180	172	38	0	0.00	\N
2181	172	39	0	0.00	\N
2182	172	40	0	0.00	\N
2183	172	41	0	0.00	\N
2157	171	19	0	0.00	\N
2158	171	24	0	0.00	\N
2159	171	36	0	0.00	\N
2160	171	37	0	0.00	\N
2184	173	4	0	0.00	\N
2185	173	44	0	0.00	\N
2186	173	15	0	0.00	\N
2187	173	13	0	0.00	\N
2188	173	16	0	0.00	\N
2189	173	17	0	0.00	\N
2190	173	18	0	0.00	\N
2191	173	19	0	0.00	\N
2192	173	20	0	0.00	\N
2193	173	21	0	0.00	\N
2194	173	22	0	0.00	\N
2195	173	23	0	0.00	\N
2196	173	24	0	0.00	\N
2197	173	25	0	0.00	\N
2198	173	26	0	0.00	\N
2199	173	14	0	0.00	\N
2200	173	27	0	0.00	\N
2201	173	28	0	0.00	\N
2202	173	35	0	0.00	\N
2203	173	36	0	0.00	\N
2204	173	37	0	0.00	\N
2205	173	38	0	0.00	\N
2206	173	39	0	0.00	\N
2207	173	40	0	0.00	\N
2208	173	41	0	0.00	\N
2209	173	42	0	0.00	\N
2359	179	18	12	7.92	3.50
2360	179	14	12	9.52	3.50
2361	179	30	5	6.76	3.30
2455	185	30	10	100000.00	3.30
2459	184	41	3	7.56	3.80
2514	188	4	0	0.00	\N
2515	188	44	0	0.00	\N
2516	188	15	0	0.00	\N
2517	188	13	0	0.00	\N
2518	188	20	0	0.00	\N
2519	188	16	0	0.00	\N
2520	188	19	0	0.00	\N
2521	188	27	0	0.00	\N
2522	188	29	0	0.00	\N
2523	188	23	0	0.00	\N
2524	188	24	0	0.00	\N
2525	188	38	0	0.00	\N
2526	188	39	0	0.00	\N
2527	188	40	0	0.00	\N
2528	188	41	0	0.00	\N
2529	188	42	0	0.00	\N
2530	188	22	0	0.00	\N
2531	188	36	0	0.00	\N
2532	188	30	0	0.00	\N
2533	188	17	0	0.00	\N
2534	188	18	0	0.00	\N
2535	188	21	0	0.00	\N
2536	188	25	0	0.00	\N
2537	188	26	0	0.00	\N
2538	188	14	0	0.00	\N
2539	188	28	0	0.00	\N
2540	188	35	0	0.00	\N
2561	190	4	0	0.00	\N
2562	190	44	0	0.00	\N
2563	190	15	0	0.00	\N
2564	190	13	0	0.00	\N
2565	190	16	0	0.00	\N
2566	190	18	0	0.00	\N
2567	190	19	0	0.00	\N
2568	190	20	0	0.00	\N
2569	190	21	0	0.00	\N
2570	190	22	0	0.00	\N
2571	190	23	0	0.00	\N
2572	190	24	0	0.00	\N
2573	190	26	0	0.00	\N
2574	190	14	0	0.00	\N
2575	190	27	0	0.00	\N
2576	190	28	0	0.00	\N
2577	190	29	0	0.00	\N
2578	190	30	0	0.00	\N
2579	190	36	0	0.00	\N
2580	190	39	0	0.00	\N
2581	190	41	0	0.00	\N
2582	190	42	0	0.00	\N
\.


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets (id, name, description, status, cost_center_id, order_date, approved_at, sales_start_date, created_by, created_at) FROM stdin;
182	VILLE FORTE (48) - 02/02/2026	Gerado a partir do diÃ¡logo de vendas	approved	38	2026-02-02	2026-02-04 10:18:30.789459	2026-02-05	5	2026-02-02 09:25:58.454811-03
184	BH (343) - 04/02/2026	Gerado a partir do diÃ¡logo de vendas	approved	22	2026-02-04	2026-02-04 10:22:01.275779	2026-02-05	6	2026-02-04 08:53:56.169751-03
186	VILLE FORTE (48) - 05/02/2026	Gerado a partir do diÃ¡logo de vendas	open	38	2026-02-05	\N	\N	5	2026-02-05 13:33:35.58722-03
187	BH (189) - 05/02/2026	Gerado a partir do diÃ¡logo de vendas	open	17	2026-02-05	\N	\N	5	2026-02-05 13:38:44.324643-03
188	BH (189) - 05/02/2026 - #1	Gerado a partir do diÃ¡logo de vendas	open	17	2026-02-05	\N	\N	5	2026-02-05 14:51:53.397299-03
189	REX (1) - 05/02/2026	Gerado a partir do diÃ¡logo de vendas	open	1	2026-02-05	\N	\N	6	2026-02-05 16:29:29.463875-03
190	BH (343) - 05/02/2026	Gerado a partir do diÃ¡logo de vendas	open	22	2026-02-05	\N	\N	6	2026-02-05 16:36:12.753303-03
168	BH (189) - 22/01/2026	Gerado a partir do diÃ¡logo de vendas	approved	17	2026-01-22	2026-01-22 19:53:01.940514	2026-01-23	5	2026-01-22 16:30:04.979725-03
169	VILLE FORTE (48) - 22/01/2026	Gerado a partir do diÃ¡logo de vendas	approved	38	2026-01-22	2026-01-22 19:59:36.776705	2026-01-23	5	2026-01-22 16:43:56.599905-03
171	REX (1) - 22/01/2026	Gerado a partir do diÃ¡logo de vendas	open	1	2026-01-22	\N	\N	6	2026-01-22 20:14:55.053301-03
172	VILLE FORTE (48) - 26/01/2026	Gerado a partir do diÃ¡logo de vendas	open	38	2026-01-26	\N	\N	5	2026-01-26 13:06:45.031755-03
173	BH (189) - 26/01/2026	Gerado a partir do diÃ¡logo de vendas	open	17	2026-01-26	\N	\N	5	2026-01-26 13:21:43.375036-03
176	BH (343) - 26/01/2026		approved	22	2026-01-26	2026-01-29 17:12:40.710398	2026-01-30	1	2026-01-26 20:07:51.230605-03
177	VILLE FORTE (48) - 26/01/2026 - #1		approved	38	2026-01-26	2026-01-29 17:12:56.186635	2026-01-30	1	2026-01-26 20:12:06.868391-03
175	BH (189) - 26/01/2026 - #1		approved	17	2026-01-26	2026-01-29 17:13:11.832549	2026-01-30	1	2026-01-26 20:03:55.697827-03
174	REX (1) - 26/01/2026		approved	1	2026-01-26	2026-01-29 17:13:25.487313	2026-01-30	1	2026-01-26 19:59:36.707174-03
180	REX (1) - 29/01/2026	Gerado a partir do diÃ¡logo de vendas	approved	1	2026-01-29	2026-01-31 14:50:59.12545	2026-02-01	6	2026-01-29 22:33:08.968049-03
179	BH (189) - 29/01/2026	Gerado a partir do diÃ¡logo de vendas	approved	17	2026-01-29	2026-01-31 14:57:14.57372	2026-02-01	5	2026-01-29 14:30:21.957279-03
181	BH (343) - 29/01/2026	Gerado a partir do diÃ¡logo de vendas	approved	22	2026-01-29	2026-01-31 15:04:43.989694	2026-02-01	6	2026-01-29 22:39:40.277587-03
178	VILLE FORTE (48) - 29/01/2026	Gerado a partir do diÃ¡logo de vendas	approved	38	2026-01-29	2026-01-31 15:08:24.733805	2026-02-01	5	2026-01-29 13:21:50.015056-03
185	REX (1) - 04/02/2026	Gerado a partir do diÃ¡logo de vendas	approved	1	2026-02-04	2026-02-04 10:07:21.526799	2026-02-05	6	2026-02-04 08:58:56.655266-03
183	BH (189) - 02/02/2026	Gerado a partir do diÃ¡logo de vendas	approved	17	2026-02-02	2026-02-04 10:11:34.708484	2026-02-05	5	2026-02-02 12:44:13.159335-03
\.


--
-- Data for Name: unit_conversion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.unit_conversion (id, unit_from, unit_to, conversion, status) FROM stdin;
\.


--
-- Data for Name: unit_measurement; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.unit_measurement (id, name, description, status) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_roles (id, user_id, role_id) FROM stdin;
1	1	1
2	2	1
3	3	1
4	4	2
5	5	2
6	6	2
7	7	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, username, email, hashed_password, full_name, nickname, is_active, is_superuser, last_login, date_joined) FROM stdin;
2	LUCIANA	luciana.santos@komerben.com.br	$2b$12$priVqyYrMri7P7umOJ99q.MCr1THZWUjg3ZjdrILudDnjHCkSL4Qi	Luciana	\N	t	f	\N	2025-09-08 20:27:15.639305
6	MARIA EDUARDA	eduardadiasdv23@icloud.com	$2b$12$VQ6PTb7KqnSAQ/t/5bWl3uL02IWiDjNphmq0ANXSoXCTPqpOFcjkS	MARIA EDUARDA	\N	t	f	\N	2025-09-10 12:56:42.688927
5	Jéssica Lavras	gsk.depaula@gmail.com	$2b$12$dMKMVsl.tcK57inFWExRVese1L9sWoeWeT8vZjHGaj0wznr5CAFfq	JESSICA 	\N	t	f	\N	2025-09-10 12:52:47.673831
3	J SANTOS	jessica.santos@komerben.com.br	$2b$12$6jrPwyd0hUesvikX1by26OYC4AR5MC/uCpUvLHBH13wpHdngRv1S2	JESSICA S	\N	t	f	\N	2025-09-10 12:44:16.136428
4	Ingrid	ingridlima.borges@hotmail.com	$2b$12$fE6F29dVFax46.ylYDyhieLwA.oXRntzPpTAqHMa.IHovJ.TnSZpm	Ingrid	\N	t	f	\N	2025-09-10 12:50:31.695892
7	Othávio	othaviodls@gmail.com	$2b$12$6NS2XajYQf0fz5fi4QXGM.DmVEk4MY9kbRRTCWDAQWVT4syi8G0hG	Othávio	\N	t	f	\N	2025-10-27 18:45:47.126461
1	Paulo.Santos	paulo.santos@komerben.com.br	$2b$12$CsL84v/9eOmCDgGHdpUIreNUqbsNVr4OUBqbIndN75p1O7.3gk1qa	Administrador do Sistema	\N	t	t	\N	2025-09-08 20:27:15.639305
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categories_id_seq', 5, true);


--
-- Name: client_loss_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.client_loss_history_id_seq', 885, true);


--
-- Name: client_sales_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.client_sales_history_id_seq', 1113, true);


--
-- Name: client_stock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.client_stock_id_seq', 340, true);


--
-- Name: cost_centers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cost_centers_id_seq', 40, true);


--
-- Name: inventory_stock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inventory_stock_id_seq', 32, true);


--
-- Name: inventory_visit_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inventory_visit_products_id_seq', 1024, true);


--
-- Name: inventory_visits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inventory_visits_id_seq', 42, true);


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.permissions_id_seq', 1, false);


--
-- Name: product_cost_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.product_cost_history_id_seq', 58, true);


--
-- Name: product_price_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.product_price_history_id_seq', 130, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.products_id_seq', 44, true);


--
-- Name: replenishment_recommendations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.replenishment_recommendations_id_seq', 1, false);


--
-- Name: retail_chains_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.retail_chains_id_seq', 6, true);


--
-- Name: role_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.role_permissions_id_seq', 1, false);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_id_seq', 2, true);


--
-- Name: sellers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sellers_id_seq', 1, false);


--
-- Name: shelf_prices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.shelf_prices_id_seq', 1, false);


--
-- Name: stock_movements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.stock_movements_id_seq', 1649, true);


--
-- Name: suppliers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.suppliers_id_seq', 17, true);


--
-- Name: ticket_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ticket_products_id_seq', 2582, true);


--
-- Name: tickets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_id_seq', 190, true);


--
-- Name: unit_conversion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.unit_conversion_id_seq', 1, false);


--
-- Name: unit_measurement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.unit_measurement_id_seq', 1, false);


--
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 7, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: client_loss_history client_loss_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_loss_history
    ADD CONSTRAINT client_loss_history_pkey PRIMARY KEY (id);


--
-- Name: client_sales_history client_sales_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_sales_history
    ADD CONSTRAINT client_sales_history_pkey PRIMARY KEY (id);


--
-- Name: client_stock client_stock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_stock
    ADD CONSTRAINT client_stock_pkey PRIMARY KEY (id);


--
-- Name: cost_centers cost_centers_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_centers
    ADD CONSTRAINT cost_centers_name_key UNIQUE (name);


--
-- Name: cost_centers cost_centers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_centers
    ADD CONSTRAINT cost_centers_pkey PRIMARY KEY (id);


--
-- Name: inventory_stock inventory_stock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_stock
    ADD CONSTRAINT inventory_stock_pkey PRIMARY KEY (id);


--
-- Name: inventory_visit_products inventory_visit_products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visit_products
    ADD CONSTRAINT inventory_visit_products_pkey PRIMARY KEY (id);


--
-- Name: inventory_visits inventory_visits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visits
    ADD CONSTRAINT inventory_visits_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: product_cost_history product_cost_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_cost_history
    ADD CONSTRAINT product_cost_history_pkey PRIMARY KEY (id);


--
-- Name: product_price_history product_price_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history
    ADD CONSTRAINT product_price_history_pkey PRIMARY KEY (id);


--
-- Name: products products_custom_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_custom_id_key UNIQUE (custom_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: replenishment_recommendations replenishment_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.replenishment_recommendations
    ADD CONSTRAINT replenishment_recommendations_pkey PRIMARY KEY (id);


--
-- Name: retail_chains retail_chains_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.retail_chains
    ADD CONSTRAINT retail_chains_name_key UNIQUE (name);


--
-- Name: retail_chains retail_chains_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.retail_chains
    ADD CONSTRAINT retail_chains_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: sellers sellers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_pkey PRIMARY KEY (id);


--
-- Name: sellers sellers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_user_id_key UNIQUE (user_id);


--
-- Name: shelf_prices shelf_prices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices
    ADD CONSTRAINT shelf_prices_pkey PRIMARY KEY (id);


--
-- Name: stock_movements stock_movements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_pkey PRIMARY KEY (id);


--
-- Name: suppliers suppliers_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_name_key UNIQUE (name);


--
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- Name: ticket_products ticket_products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_products
    ADD CONSTRAINT ticket_products_pkey PRIMARY KEY (id);


--
-- Name: tickets tickets_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_name_key UNIQUE (name);


--
-- Name: tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (id);


--
-- Name: product_price_history uix_product_chain_start; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history
    ADD CONSTRAINT uix_product_chain_start UNIQUE (product_id, retail_chain_id, start_date);


--
-- Name: product_price_history uix_product_cost_center_start; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history
    ADD CONSTRAINT uix_product_cost_center_start UNIQUE (product_id, cost_center_id, start_date);


--
-- Name: shelf_prices uix_shelf_price_chain_start; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices
    ADD CONSTRAINT uix_shelf_price_chain_start UNIQUE (product_id, retail_chain_id, start_date);


--
-- Name: shelf_prices uix_shelf_price_cost_center_start; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices
    ADD CONSTRAINT uix_shelf_price_cost_center_start UNIQUE (product_id, cost_center_id, start_date);


--
-- Name: unit_conversion unit_conversion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_conversion
    ADD CONSTRAINT unit_conversion_pkey PRIMARY KEY (id);


--
-- Name: unit_measurement unit_measurement_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_measurement
    ADD CONSTRAINT unit_measurement_name_key UNIQUE (name);


--
-- Name: unit_measurement unit_measurement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_measurement
    ADD CONSTRAINT unit_measurement_pkey PRIMARY KEY (id);


--
-- Name: client_sales_history uq_sales_day; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_sales_history
    ADD CONSTRAINT uq_sales_day UNIQUE (cost_center_id, product_id, date);


--
-- Name: inventory_visit_products uq_visit_product_visit_product; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visit_products
    ADD CONSTRAINT uq_visit_product_visit_product UNIQUE (inventory_visit_id, product_id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_client_loss_cc_product_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_client_loss_cc_product_date ON public.client_loss_history USING btree (cost_center_id, product_id, date);


--
-- Name: ix_client_stock_cc_product; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_client_stock_cc_product ON public.client_stock USING btree (cost_center_id, product_id);


--
-- Name: ix_cost_centers_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_cost_centers_id ON public.cost_centers USING btree (id);


--
-- Name: ix_permissions_description; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_permissions_description ON public.permissions USING btree (description);


--
-- Name: ix_permissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);


--
-- Name: ix_permissions_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_permissions_name ON public.permissions USING btree (name);


--
-- Name: ix_product_cost_history_end_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_product_cost_history_end_date ON public.product_cost_history USING btree (end_date);


--
-- Name: ix_product_cost_history_product_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_product_cost_history_product_id ON public.product_cost_history USING btree (product_id);


--
-- Name: ix_products_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_products_id ON public.products USING btree (id);


--
-- Name: ix_retail_chains_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_retail_chains_id ON public.retail_chains USING btree (id);


--
-- Name: ix_role_permissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_role_permissions_id ON public.role_permissions USING btree (id);


--
-- Name: ix_roles_description; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_roles_description ON public.roles USING btree (description);


--
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- Name: ix_stock_movements_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_stock_movements_id ON public.stock_movements USING btree (id);


--
-- Name: ix_stock_movements_inventory_visit_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_stock_movements_inventory_visit_id ON public.stock_movements USING btree (inventory_visit_id);


--
-- Name: ix_ticket_products_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ticket_products_id ON public.ticket_products USING btree (id);


--
-- Name: ix_ticket_products_product_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ticket_products_product_id ON public.ticket_products USING btree (product_id);


--
-- Name: ix_ticket_products_ticket_product; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ticket_products_ticket_product ON public.ticket_products USING btree (ticket_id, product_id);


--
-- Name: ix_tickets_cc_approved_orderdate; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_cc_approved_orderdate ON public.tickets USING btree (cost_center_id, order_date DESC) WHERE ((status)::text = 'approved'::text);


--
-- Name: ix_tickets_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_id ON public.tickets USING btree (id);


--
-- Name: ix_unit_conversion_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_unit_conversion_id ON public.unit_conversion USING btree (id);


--
-- Name: ix_unit_measurement_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_unit_measurement_id ON public.unit_measurement USING btree (id);


--
-- Name: ix_user_roles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_roles_id ON public.user_roles USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: client_loss_history client_loss_history_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_loss_history
    ADD CONSTRAINT client_loss_history_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: client_loss_history client_loss_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_loss_history
    ADD CONSTRAINT client_loss_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: client_sales_history client_sales_history_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_sales_history
    ADD CONSTRAINT client_sales_history_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: client_sales_history client_sales_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_sales_history
    ADD CONSTRAINT client_sales_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: client_stock client_stock_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_stock
    ADD CONSTRAINT client_stock_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: client_stock client_stock_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_stock
    ADD CONSTRAINT client_stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: cost_centers cost_centers_retail_chain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cost_centers
    ADD CONSTRAINT cost_centers_retail_chain_id_fkey FOREIGN KEY (retail_chain_id) REFERENCES public.retail_chains(id);


--
-- Name: inventory_visits fk_inventory_visit_cost_center; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visits
    ADD CONSTRAINT fk_inventory_visit_cost_center FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: inventory_visits fk_inventory_visit_ticket; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visits
    ADD CONSTRAINT fk_inventory_visit_ticket FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: inventory_visits fk_inventory_visit_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visits
    ADD CONSTRAINT fk_inventory_visit_user FOREIGN KEY (recorded_by) REFERENCES public.users(id);


--
-- Name: stock_movements fk_stock_movements_inventory_visit; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT fk_stock_movements_inventory_visit FOREIGN KEY (inventory_visit_id) REFERENCES public.inventory_visits(id) ON DELETE SET NULL;


--
-- Name: inventory_visit_products fk_visit_product_product; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visit_products
    ADD CONSTRAINT fk_visit_product_product FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: inventory_visit_products fk_visit_product_visit; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_visit_products
    ADD CONSTRAINT fk_visit_product_visit FOREIGN KEY (inventory_visit_id) REFERENCES public.inventory_visits(id) ON DELETE CASCADE;


--
-- Name: inventory_stock inventory_stock_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_stock
    ADD CONSTRAINT inventory_stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: product_cost_history product_cost_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_cost_history
    ADD CONSTRAINT product_cost_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: product_price_history product_price_history_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history
    ADD CONSTRAINT product_price_history_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: product_price_history product_price_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history
    ADD CONSTRAINT product_price_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: product_price_history product_price_history_retail_chain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_price_history
    ADD CONSTRAINT product_price_history_retail_chain_id_fkey FOREIGN KEY (retail_chain_id) REFERENCES public.retail_chains(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: replenishment_recommendations replenishment_recommendations_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.replenishment_recommendations
    ADD CONSTRAINT replenishment_recommendations_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: replenishment_recommendations replenishment_recommendations_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.replenishment_recommendations
    ADD CONSTRAINT replenishment_recommendations_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: sellers sellers_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: sellers sellers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: shelf_prices shelf_prices_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices
    ADD CONSTRAINT shelf_prices_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: shelf_prices shelf_prices_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices
    ADD CONSTRAINT shelf_prices_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: shelf_prices shelf_prices_retail_chain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shelf_prices
    ADD CONSTRAINT shelf_prices_retail_chain_id_fkey FOREIGN KEY (retail_chain_id) REFERENCES public.retail_chains(id);


--
-- Name: stock_movements stock_movements_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: stock_movements stock_movements_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: stock_movements stock_movements_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movements
    ADD CONSTRAINT stock_movements_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id);


--
-- Name: ticket_products ticket_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_products
    ADD CONSTRAINT ticket_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: ticket_products ticket_products_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_products
    ADD CONSTRAINT ticket_products_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: tickets tickets_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: tickets tickets_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: unit_conversion unit_conversion_unit_from_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_conversion
    ADD CONSTRAINT unit_conversion_unit_from_fkey FOREIGN KEY (unit_from) REFERENCES public.unit_measurement(id);


--
-- Name: unit_conversion unit_conversion_unit_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.unit_conversion
    ADD CONSTRAINT unit_conversion_unit_to_fkey FOREIGN KEY (unit_to) REFERENCES public.unit_measurement(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict CBYHHJQeVQGmlhlixVFIJwdaD3Ess6oWIhJ2EEqbv0KeeGC5bw9cf4k4vazV6Ob

