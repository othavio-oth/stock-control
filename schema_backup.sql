--
-- PostgreSQL database dump
--

-- Dumped from database version 15.10 (Debian 15.10-1.pgdg120+1)
-- Dumped by pg_dump version 15.10 (Debian 15.10-1.pgdg120+1)

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO strategy_db;

--
-- Name: cost_centers; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.cost_centers (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


ALTER TABLE public.cost_centers OWNER TO strategy_db;

--
-- Name: cost_centers_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.cost_centers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cost_centers_id_seq OWNER TO strategy_db;

--
-- Name: cost_centers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.cost_centers_id_seq OWNED BY public.cost_centers.id;


--
-- Name: cost_fabrication; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.cost_fabrication (
    id integer NOT NULL,
    fabrication_id integer NOT NULL,
    unit_cost numeric(15,4) NOT NULL,
    total_cost numeric(15,4) NOT NULL,
    cost_corrections numeric(15,4) NOT NULL
);


ALTER TABLE public.cost_fabrication OWNER TO strategy_db;

--
-- Name: cost_fabrication_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.cost_fabrication_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cost_fabrication_id_seq OWNER TO strategy_db;

--
-- Name: cost_fabrication_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.cost_fabrication_id_seq OWNED BY public.cost_fabrication.id;


--
-- Name: cost_taxation; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.cost_taxation (
    id integer NOT NULL,
    taxation numeric(15,4) NOT NULL,
    logistic numeric(15,4) NOT NULL,
    mld_taxation numeric(15,4) NOT NULL,
    prejudice numeric(15,4) NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE public.cost_taxation OWNER TO strategy_db;

--
-- Name: cost_taxation_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.cost_taxation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cost_taxation_id_seq OWNER TO strategy_db;

--
-- Name: cost_taxation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.cost_taxation_id_seq OWNED BY public.cost_taxation.id;


--
-- Name: fabrication_products; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.fabrication_products (
    id integer NOT NULL,
    fabrication_id integer NOT NULL,
    product_id integer,
    revenue_id integer,
    quantity double precision NOT NULL,
    correction_factor double precision NOT NULL
);


ALTER TABLE public.fabrication_products OWNER TO strategy_db;

--
-- Name: fabrication_products_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.fabrication_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fabrication_products_id_seq OWNER TO strategy_db;

--
-- Name: fabrication_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.fabrication_products_id_seq OWNED BY public.fabrication_products.id;


--
-- Name: fabrications; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.fabrications (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


ALTER TABLE public.fabrications OWNER TO strategy_db;

--
-- Name: fabrications_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.fabrications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fabrications_id_seq OWNER TO strategy_db;

--
-- Name: fabrications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.fabrications_id_seq OWNED BY public.fabrications.id;


--
-- Name: group; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public."group" (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying(500),
    status boolean
);


ALTER TABLE public."group" OWNER TO strategy_db;

--
-- Name: group_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_id_seq OWNER TO strategy_db;

--
-- Name: group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.group_id_seq OWNED BY public."group".id;


--
-- Name: order_production; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.order_production (
    id integer NOT NULL,
    init date,
    "end" date,
    status character varying(200),
    sale numeric(15,4),
    cost numeric(15,4),
    gain numeric(15,4),
    stock_location_id integer,
    cost_center_id integer,
    production_id integer
);


ALTER TABLE public.order_production OWNER TO strategy_db;

--
-- Name: order_production_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.order_production_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_production_id_seq OWNER TO strategy_db;

--
-- Name: order_production_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.order_production_id_seq OWNED BY public.order_production.id;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying,
    description character varying
);


ALTER TABLE public.permissions OWNER TO strategy_db;

--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_id_seq OWNER TO strategy_db;

--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: production; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.production (
    id integer NOT NULL,
    description character varying
);


ALTER TABLE public.production OWNER TO strategy_db;

--
-- Name: production_fabrication; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.production_fabrication (
    id integer NOT NULL,
    production_id integer NOT NULL,
    fabrication_id integer NOT NULL,
    quantity double precision NOT NULL
);


ALTER TABLE public.production_fabrication OWNER TO strategy_db;

--
-- Name: production_fabrication_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.production_fabrication_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.production_fabrication_id_seq OWNER TO strategy_db;

--
-- Name: production_fabrication_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.production_fabrication_id_seq OWNED BY public.production_fabrication.id;


--
-- Name: production_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.production_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.production_id_seq OWNER TO strategy_db;

--
-- Name: production_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.production_id_seq OWNED BY public.production.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.products (
    id integer NOT NULL,
    custom_id integer,
    description character varying NOT NULL,
    status boolean,
    type_registration_id integer NOT NULL,
    group_id integer NOT NULL,
    sub_group_id integer NOT NULL,
    date_cost date NOT NULL,
    cost_inside double precision NOT NULL,
    conversion_id integer,
    cost_output double precision NOT NULL,
    un_inside_id integer NOT NULL,
    un_output_stock_id integer NOT NULL,
    cost_taxation_id integer
);


ALTER TABLE public.products OWNER TO strategy_db;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO strategy_db;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: revenues; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.revenues (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


ALTER TABLE public.revenues OWNER TO strategy_db;

--
-- Name: revenues_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.revenues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.revenues_id_seq OWNER TO strategy_db;

--
-- Name: revenues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.revenues_id_seq OWNED BY public.revenues.id;


--
-- Name: revenues_products; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.revenues_products (
    id integer NOT NULL,
    revenue_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity double precision NOT NULL,
    correction_factor double precision NOT NULL
);


ALTER TABLE public.revenues_products OWNER TO strategy_db;

--
-- Name: revenues_products_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.revenues_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.revenues_products_id_seq OWNER TO strategy_db;

--
-- Name: revenues_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.revenues_products_id_seq OWNED BY public.revenues_products.id;


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.role_permissions (
    id integer NOT NULL,
    role_id integer,
    permission_id integer
);


ALTER TABLE public.role_permissions OWNER TO strategy_db;

--
-- Name: role_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.role_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_permissions_id_seq OWNER TO strategy_db;

--
-- Name: role_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.role_permissions_id_seq OWNED BY public.role_permissions.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying,
    description character varying
);


ALTER TABLE public.roles OWNER TO strategy_db;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO strategy_db;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: stock_location; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.stock_location (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


ALTER TABLE public.stock_location OWNER TO strategy_db;

--
-- Name: stock_location_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.stock_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stock_location_id_seq OWNER TO strategy_db;

--
-- Name: stock_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.stock_location_id_seq OWNED BY public.stock_location.id;


--
-- Name: subgroup; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.subgroup (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying(500),
    status boolean
);


ALTER TABLE public.subgroup OWNER TO strategy_db;

--
-- Name: subgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.subgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subgroup_id_seq OWNER TO strategy_db;

--
-- Name: subgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.subgroup_id_seq OWNED BY public.subgroup.id;


--
-- Name: type_registration; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.type_registration (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


ALTER TABLE public.type_registration OWNER TO strategy_db;

--
-- Name: type_registration_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.type_registration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_registration_id_seq OWNER TO strategy_db;

--
-- Name: type_registration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.type_registration_id_seq OWNED BY public.type_registration.id;


--
-- Name: unit_conversion; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.unit_conversion (
    id integer NOT NULL,
    unit_from integer NOT NULL,
    unit_to integer NOT NULL,
    conversion double precision NOT NULL,
    status boolean
);


ALTER TABLE public.unit_conversion OWNER TO strategy_db;

--
-- Name: unit_conversion_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.unit_conversion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.unit_conversion_id_seq OWNER TO strategy_db;

--
-- Name: unit_conversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.unit_conversion_id_seq OWNED BY public.unit_conversion.id;


--
-- Name: unit_measurement; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.unit_measurement (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    description character varying,
    status boolean
);


ALTER TABLE public.unit_measurement OWNER TO strategy_db;

--
-- Name: unit_measurement_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.unit_measurement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.unit_measurement_id_seq OWNER TO strategy_db;

--
-- Name: unit_measurement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.unit_measurement_id_seq OWNED BY public.unit_measurement.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: strategy_db
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);


ALTER TABLE public.user_roles OWNER TO strategy_db;

--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_roles_id_seq OWNER TO strategy_db;

--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: strategy_db
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


ALTER TABLE public.users OWNER TO strategy_db;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: strategy_db
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO strategy_db;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: strategy_db
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: cost_centers id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_centers ALTER COLUMN id SET DEFAULT nextval('public.cost_centers_id_seq'::regclass);


--
-- Name: cost_fabrication id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_fabrication ALTER COLUMN id SET DEFAULT nextval('public.cost_fabrication_id_seq'::regclass);


--
-- Name: cost_taxation id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_taxation ALTER COLUMN id SET DEFAULT nextval('public.cost_taxation_id_seq'::regclass);


--
-- Name: fabrication_products id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrication_products ALTER COLUMN id SET DEFAULT nextval('public.fabrication_products_id_seq'::regclass);


--
-- Name: fabrications id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrications ALTER COLUMN id SET DEFAULT nextval('public.fabrications_id_seq'::regclass);


--
-- Name: group id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public."group" ALTER COLUMN id SET DEFAULT nextval('public.group_id_seq'::regclass);


--
-- Name: order_production id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.order_production ALTER COLUMN id SET DEFAULT nextval('public.order_production_id_seq'::regclass);


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: production id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.production ALTER COLUMN id SET DEFAULT nextval('public.production_id_seq'::regclass);


--
-- Name: production_fabrication id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.production_fabrication ALTER COLUMN id SET DEFAULT nextval('public.production_fabrication_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: revenues id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues ALTER COLUMN id SET DEFAULT nextval('public.revenues_id_seq'::regclass);


--
-- Name: revenues_products id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues_products ALTER COLUMN id SET DEFAULT nextval('public.revenues_products_id_seq'::regclass);


--
-- Name: role_permissions id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.role_permissions ALTER COLUMN id SET DEFAULT nextval('public.role_permissions_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: stock_location id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.stock_location ALTER COLUMN id SET DEFAULT nextval('public.stock_location_id_seq'::regclass);


--
-- Name: subgroup id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.subgroup ALTER COLUMN id SET DEFAULT nextval('public.subgroup_id_seq'::regclass);


--
-- Name: type_registration id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.type_registration ALTER COLUMN id SET DEFAULT nextval('public.type_registration_id_seq'::regclass);


--
-- Name: unit_conversion id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_conversion ALTER COLUMN id SET DEFAULT nextval('public.unit_conversion_id_seq'::regclass);


--
-- Name: unit_measurement id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_measurement ALTER COLUMN id SET DEFAULT nextval('public.unit_measurement_id_seq'::regclass);


--
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cost_centers cost_centers_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_centers
    ADD CONSTRAINT cost_centers_name_key UNIQUE (name);


--
-- Name: cost_centers cost_centers_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_centers
    ADD CONSTRAINT cost_centers_pkey PRIMARY KEY (id);


--
-- Name: cost_fabrication cost_fabrication_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_fabrication
    ADD CONSTRAINT cost_fabrication_pkey PRIMARY KEY (id);


--
-- Name: cost_taxation cost_taxation_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_taxation
    ADD CONSTRAINT cost_taxation_pkey PRIMARY KEY (id);


--
-- Name: fabrication_products fabrication_products_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrication_products
    ADD CONSTRAINT fabrication_products_pkey PRIMARY KEY (id);


--
-- Name: fabrications fabrications_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrications
    ADD CONSTRAINT fabrications_name_key UNIQUE (name);


--
-- Name: fabrications fabrications_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrications
    ADD CONSTRAINT fabrications_pkey PRIMARY KEY (id);


--
-- Name: group group_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_name_key UNIQUE (name);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: order_production order_production_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.order_production
    ADD CONSTRAINT order_production_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: production_fabrication production_fabrication_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.production_fabrication
    ADD CONSTRAINT production_fabrication_pkey PRIMARY KEY (id);


--
-- Name: production production_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.production
    ADD CONSTRAINT production_pkey PRIMARY KEY (id);


--
-- Name: products products_custom_id_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_custom_id_key UNIQUE (custom_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: revenues revenues_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues
    ADD CONSTRAINT revenues_name_key UNIQUE (name);


--
-- Name: revenues revenues_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues
    ADD CONSTRAINT revenues_pkey PRIMARY KEY (id);


--
-- Name: revenues_products revenues_products_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues_products
    ADD CONSTRAINT revenues_products_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: stock_location stock_location_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT stock_location_name_key UNIQUE (name);


--
-- Name: stock_location stock_location_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT stock_location_pkey PRIMARY KEY (id);


--
-- Name: subgroup subgroup_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.subgroup
    ADD CONSTRAINT subgroup_name_key UNIQUE (name);


--
-- Name: subgroup subgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.subgroup
    ADD CONSTRAINT subgroup_pkey PRIMARY KEY (id);


--
-- Name: type_registration type_registration_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.type_registration
    ADD CONSTRAINT type_registration_name_key UNIQUE (name);


--
-- Name: type_registration type_registration_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.type_registration
    ADD CONSTRAINT type_registration_pkey PRIMARY KEY (id);


--
-- Name: unit_conversion unit_conversion_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_conversion
    ADD CONSTRAINT unit_conversion_pkey PRIMARY KEY (id);


--
-- Name: unit_measurement unit_measurement_name_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_measurement
    ADD CONSTRAINT unit_measurement_name_key UNIQUE (name);


--
-- Name: unit_measurement unit_measurement_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_measurement
    ADD CONSTRAINT unit_measurement_pkey PRIMARY KEY (id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_cost_centers_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_cost_centers_id ON public.cost_centers USING btree (id);


--
-- Name: ix_cost_fabrication_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_cost_fabrication_id ON public.cost_fabrication USING btree (id);


--
-- Name: ix_cost_taxation_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_cost_taxation_id ON public.cost_taxation USING btree (id);


--
-- Name: ix_fabrication_products_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_fabrication_products_id ON public.fabrication_products USING btree (id);


--
-- Name: ix_fabrications_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_fabrications_id ON public.fabrications USING btree (id);


--
-- Name: ix_group_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_group_id ON public."group" USING btree (id);


--
-- Name: ix_order_production_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_order_production_id ON public.order_production USING btree (id);


--
-- Name: ix_permissions_description; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE UNIQUE INDEX ix_permissions_description ON public.permissions USING btree (description);


--
-- Name: ix_permissions_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);


--
-- Name: ix_permissions_name; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE UNIQUE INDEX ix_permissions_name ON public.permissions USING btree (name);


--
-- Name: ix_production_fabrication_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_production_fabrication_id ON public.production_fabrication USING btree (id);


--
-- Name: ix_production_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_production_id ON public.production USING btree (id);


--
-- Name: ix_products_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_products_id ON public.products USING btree (id);


--
-- Name: ix_revenues_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_revenues_id ON public.revenues USING btree (id);


--
-- Name: ix_revenues_products_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_revenues_products_id ON public.revenues_products USING btree (id);


--
-- Name: ix_role_permissions_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_role_permissions_id ON public.role_permissions USING btree (id);


--
-- Name: ix_roles_description; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE UNIQUE INDEX ix_roles_description ON public.roles USING btree (description);


--
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- Name: ix_stock_location_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_stock_location_id ON public.stock_location USING btree (id);


--
-- Name: ix_subgroup_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_subgroup_id ON public.subgroup USING btree (id);


--
-- Name: ix_type_registration_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_type_registration_id ON public.type_registration USING btree (id);


--
-- Name: ix_unit_conversion_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_unit_conversion_id ON public.unit_conversion USING btree (id);


--
-- Name: ix_unit_measurement_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_unit_measurement_id ON public.unit_measurement USING btree (id);


--
-- Name: ix_user_roles_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_user_roles_id ON public.user_roles USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: strategy_db
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: cost_fabrication cost_fabrication_fabrication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.cost_fabrication
    ADD CONSTRAINT cost_fabrication_fabrication_id_fkey FOREIGN KEY (fabrication_id) REFERENCES public.fabrications(id);


--
-- Name: fabrication_products fabrication_products_fabrication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrication_products
    ADD CONSTRAINT fabrication_products_fabrication_id_fkey FOREIGN KEY (fabrication_id) REFERENCES public.fabrications(id);


--
-- Name: fabrication_products fabrication_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrication_products
    ADD CONSTRAINT fabrication_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: fabrication_products fabrication_products_revenue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.fabrication_products
    ADD CONSTRAINT fabrication_products_revenue_id_fkey FOREIGN KEY (revenue_id) REFERENCES public.revenues(id);


--
-- Name: order_production order_production_cost_center_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.order_production
    ADD CONSTRAINT order_production_cost_center_id_fkey FOREIGN KEY (cost_center_id) REFERENCES public.cost_centers(id);


--
-- Name: order_production order_production_production_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.order_production
    ADD CONSTRAINT order_production_production_id_fkey FOREIGN KEY (production_id) REFERENCES public.production(id);


--
-- Name: order_production order_production_stock_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.order_production
    ADD CONSTRAINT order_production_stock_location_id_fkey FOREIGN KEY (stock_location_id) REFERENCES public.stock_location(id);


--
-- Name: production_fabrication production_fabrication_fabrication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.production_fabrication
    ADD CONSTRAINT production_fabrication_fabrication_id_fkey FOREIGN KEY (fabrication_id) REFERENCES public.fabrications(id);


--
-- Name: production_fabrication production_fabrication_production_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.production_fabrication
    ADD CONSTRAINT production_fabrication_production_id_fkey FOREIGN KEY (production_id) REFERENCES public.production(id);


--
-- Name: products products_conversion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_conversion_id_fkey FOREIGN KEY (conversion_id) REFERENCES public.unit_conversion(id);


--
-- Name: products products_cost_taxation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_cost_taxation_id_fkey FOREIGN KEY (cost_taxation_id) REFERENCES public.cost_taxation(id);


--
-- Name: products products_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."group"(id);


--
-- Name: products products_sub_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_sub_group_id_fkey FOREIGN KEY (sub_group_id) REFERENCES public.subgroup(id);


--
-- Name: products products_type_registration_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_type_registration_id_fkey FOREIGN KEY (type_registration_id) REFERENCES public.type_registration(id);


--
-- Name: products products_un_inside_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_un_inside_id_fkey FOREIGN KEY (un_inside_id) REFERENCES public.unit_measurement(id);


--
-- Name: products products_un_output_stock_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_un_output_stock_id_fkey FOREIGN KEY (un_output_stock_id) REFERENCES public.unit_measurement(id);


--
-- Name: revenues_products revenues_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues_products
    ADD CONSTRAINT revenues_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: revenues_products revenues_products_revenue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.revenues_products
    ADD CONSTRAINT revenues_products_revenue_id_fkey FOREIGN KEY (revenue_id) REFERENCES public.revenues(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: unit_conversion unit_conversion_unit_from_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_conversion
    ADD CONSTRAINT unit_conversion_unit_from_fkey FOREIGN KEY (unit_from) REFERENCES public.unit_measurement(id);


--
-- Name: unit_conversion unit_conversion_unit_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.unit_conversion
    ADD CONSTRAINT unit_conversion_unit_to_fkey FOREIGN KEY (unit_to) REFERENCES public.unit_measurement(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: strategy_db
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

