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
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: strategy_db
--

COPY public.alembic_version (version_num) FROM stdin;
4f7482d43e6b
\.


--
-- Data for Name: cost_centers; Type: TABLE DATA; Schema: public; Owner: strategy_db
--

COPY public.cost_centers (id, name, description, status) FROM stdin;
2	Matriz Norte	Matriz Norte de distribuição rua z	t
1	Núcleo A	Núcleo de distribuição	t
\.



COPY public.permissions (id, name, description) FROM stdin;
5	list_permissions	Lista as permissões de classes de usuários
2	update_users	Edita os usuários disponíveis
4	delete_users	Deleta usuários
6	update_permissions	Edita as permissões
3	create_users	Pode criar usuários teste
8	delete_permissions	Deleta Permissão
7	create_permissions	Cria as devidas permissões
1	list_users	Lista os usuários disponíveis
9	list_roles	Lista todas as Classes de usuário
10	create_roles	Cria classes de usuário
11	update_roles	Edita classes de usuário
12	delete_roles	Deleta classes de usuário
13	list_cost_taxation	Lista todos os Impostos de Custo
14	create_cost_taxation	Cria Impostos de Custo
15	update_cost_taxation	Edita Impostos de Custo
16	delete_cost_taxation	Deleta Impostos de Custo
17	list_groups	Lista todos os Grupos
18	create_groups	Cria Grupos
19	update_groups	Edita Grupos
20	delete_groups	Deleta Grupos
21	list_products	Lista todos os Produtos
22	create_products	Cria Produtos
23	update_products	Edita Produtos
24	delete_products	Deleta Produtos
25	list_subgroups	Lista todos os Subgrupos
26	create_subgroups	Cria Subgrupos
27	update_subgroups	Edita Subgrupos
28	delete_subgroups	Deleta Subgrupos
29	list_type_registration	Lista todos os Tipos de Registro
30	create_type_registration	Cria Tipos de Registro
31	update_type_registration	Edita Tipos de Registro
32	delete_type_registration	Deleta Tipos de Registro
33	list_unit_conversion	Lista todas as Conversões de Unidade
34	create_unit_conversion	Cria Conversões de Unidade
35	update_unit_conversion	Edita Conversões de Unidade
36	delete_unit_conversion	Deleta Conversões de Unidade
37	list_unit_measurement	Lista todas as Unidades de Medida
38	create_unit_measurement	Cria Unidades de Medida
39	update_unit_measurement	Edita Unidades de Medida
40	delete_unit_measurement	Deleta Unidades de Medida
41	list_cost_center	Lista todos os Centros de Custo
42	create_cost_center	Cria Centros de Custo
43	update_cost_center	Edita Centros de Custo
44	delete_cost_center	Deleta Centros de Custo
45	list_fabrication	Lista todas as Fabricações
46	create_fabrication	Cria Fabricações
47	update_fabrication	Edita Fabricações
48	delete_fabrication	Deleta Fabricações
49	list_order_production	Lista todas as Ordens de Produção
50	create_order_production	Cria Ordens de Produção
51	update_order_production	Edita Ordens de Produção
52	delete_order_production	Deleta Ordens de Produção
53	list_production	Lista todas as Produções
54	create_production	Cria Produções
55	update_production	Edita Produções
56	delete_production	Deleta Produções
57	list_revenue	Lista todas as Receitas
58	create_revenue	Cria Receitas
59	update_revenue	Edita Receitas
60	delete_revenue	Deleta Receitas
61	list_stock_locations	Lista todos os Locais de Estoque
62	create_stock_locations	Cria Locais de Estoque
63	update_stock_locations	Edita Locais de Estoque
64	delete_stock_locations	Deleta Locais de Estoque
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: strategy_db
--

COPY public.roles (id, name, description) FROM stdin;
1	Entregador	Apenas visualiza os pedidos realizados pelos mercantis
2	Administrador	Acesso total
3	Padeiro	Pode visualizar itens, e editar inventário.
4	Gerente	Acesso Intermediário
5	Test	T
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: strategy_db
--

COPY public.role_permissions (id, role_id, permission_id) FROM stdin;
1	1	1
2	2	3
3	2	1
4	2	2
5	4	3
6	2	3
7	4	3
8	2	3
9	2	5
10	2	6
11	4	2
12	2	2
13	2	1
14	4	1
15	4	1
16	2	1
17	2	4
18	2	7
19	2	8
20	2	9
21	2	10
22	2	12
23	2	13
24	2	14
25	2	15
26	2	16
27	2	17
28	2	18
29	2	19
30	2	20
31	2	21
32	2	22
33	2	23
34	2	24
35	2	25
36	2	26
37	2	27
38	2	28
39	2	29
40	2	30
41	2	31
42	2	32
43	2	33
44	2	34
45	2	35
46	2	36
47	2	37
48	2	38
49	2	39
50	2	40
51	2	41
52	2	42
53	2	43
54	2	44
55	2	45
56	2	46
57	2	47
58	2	48
59	2	49
60	2	50
61	2	51
62	2	52
63	2	53
64	2	54
65	2	55
66	2	56
67	2	57
68	2	58
69	2	59
70	2	60
71	2	61
72	2	62
73	2	63
74	2	64
\.


