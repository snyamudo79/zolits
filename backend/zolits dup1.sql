--
-- PostgreSQL database dump
--

\restrict j8qhafmeNJJr9CQTihkvbRbrT572JPN7lnq9sAJQwvmXsYqThEaSacLBsgV5iJt

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-03-23 08:49:51

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5275 (class 0 OID 16425)
-- Dependencies: 226
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 5277 (class 0 OID 16435)
-- Dependencies: 228
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5273 (class 0 OID 16415)
-- Dependencies: 224
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add Token	8	add_tokenproxy
30	Can change Token	8	change_tokenproxy
31	Can delete Token	8	delete_tokenproxy
32	Can view Token	8	view_tokenproxy
33	Can add role	9	add_role
34	Can change role	9	change_role
35	Can delete role	9	delete_role
36	Can view role	9	view_role
37	Can add region	10	add_region
38	Can change region	10	change_region
39	Can delete region	10	delete_region
40	Can view region	10	view_region
41	Can add depot	11	add_depot
42	Can change depot	11	change_depot
43	Can delete depot	11	delete_depot
44	Can view depot	11	view_depot
45	Can add module	12	add_module
46	Can change module	12	change_module
47	Can delete module	12	delete_module
48	Can view module	12	view_module
49	Can add issue severity	13	add_issueseverity
50	Can change issue severity	13	change_issueseverity
51	Can delete issue severity	13	delete_issueseverity
52	Can view issue severity	13	view_issueseverity
53	Can add issue status	14	add_issuestatus
54	Can change issue status	14	change_issuestatus
55	Can delete issue status	14	delete_issuestatus
56	Can view issue status	14	view_issuestatus
57	Can add user profile	15	add_userprofile
58	Can change user profile	15	change_userprofile
59	Can delete user profile	15	delete_userprofile
60	Can view user profile	15	view_userprofile
61	Can add issue	16	add_issue
62	Can change issue	16	change_issue
63	Can delete issue	16	delete_issue
64	Can view issue	16	view_issue
65	Can add attachment	17	add_attachment
66	Can change attachment	17	change_attachment
67	Can delete attachment	17	delete_attachment
68	Can view attachment	17	view_attachment
69	Can add issue history	18	add_issuehistory
70	Can change issue history	18	change_issuehistory
71	Can delete issue history	18	delete_issuehistory
72	Can view issue history	18	view_issuehistory
73	Can add system	19	add_system
74	Can change system	19	change_system
75	Can delete system	19	delete_system
76	Can view system	19	view_system
77	Can add submodule	20	add_submodule
78	Can change submodule	20	change_submodule
79	Can delete submodule	20	delete_submodule
80	Can view submodule	20	view_submodule
\.


--
-- TOC entry 5279 (class 0 OID 16444)
-- Dependencies: 230
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$1000000$NW672LZSrSn3e3yjipWe7H$MEGnJqu5Y6slbxluQICXSLssFPUNrSbeCVevFEOc0YA=	\N	f	zenyamudo				f	t	2026-03-10 09:57:10+02
3	pbkdf2_sha256$1000000$ueR5oZy2iTwvOTUX7ouc3o$G25NoMH8rTuV3F1iC5EakQtbpGgc1QwK3iR1J13tdr8=	\N	f	l.simoyi	L.	SIMOYI	l.simoyi@example.com	f	t	2026-03-10 12:55:40.952821+02
4	pbkdf2_sha256$1000000$itMAOiKMpEVkfctPp5hJKi$wlGrGg6VqLjtFPf1RWo7KwtxcTUcMX0GYmMFA8SIOmw=	\N	f	expert1	Expert	One	expert1@example.com	f	t	2026-03-12 17:44:33.504252+02
5	pbkdf2_sha256$1000000$eqESZvqTdARnzkrojupjsH$k/SMjj4NU3YtlaVFxD7IHnwrlgb+/FU9asIibgXcRcM=	\N	f	rm_southern	Regional	Manager	rm_southern@example.com	f	t	2026-03-12 17:44:36.645612+02
6	pbkdf2_sha256$1000000$TKZIGbYzyhujkbLVm2iABJ$I+cMVtKCXqvwOJS5sMX18PC/DGB4PWDjaj5a1j+/7ho=	\N	f	zetdc	nyamudods		snyamudo79@gmail.com	f	t	2026-03-12 18:18:57+02
8	pbkdf2_sha256$1000000$Rl4knF0N7mgJ756kSw7d8r$KmTzxnPL/lsBuXm3gKqvDB2ScS6oz4/yYqiNTsiEl60=	\N	f	testuser	Test	User	test@example.com	f	t	2026-03-13 13:09:56.78069+02
9	pbkdf2_sha256$1000000$GQsltS63KrPbNwh3dwoxtD$fAgo6OJ2EcN3dKPTwtOXpl8VNA85nfsz6+X960EdxtQ=	\N	f	ewfe3	dedewfref	feef	zw@zedtc.com	f	t	2026-03-13 14:01:01.959078+02
10	pbkdf2_sha256$1000000$9MOu6dkSbXacIsSEHifPDQ$WIusTkVrGkodpBsvwQYnm16/MjnDTyvGe+0tUp4uTKk=	\N	f	se123	ttttd	dvbfdbf	zwe@zedtc.com	f	t	2026-03-13 14:08:07.235484+02
11	pbkdf2_sha256$1000000$RFA3NUZTqO4Ed2v1KbulTU$C4mleJOSP1d9a2iZLWMfjN3hRNUZy6NH+pn/ORVqgg8=	\N	f	ze12345	ttv	ttv1	zwy@zedtc.com	f	t	2026-03-13 14:13:12.597972+02
12	pbkdf2_sha256$1000000$S20IOAxeEC5FcN2azkkmex$kimwW0wMtupMXjFbLN7C4busmx7VIy76WJKw93O/5yg=	\N	f	ze280127	violet	Mehlomnakulu	vmehlomakulu@zetdc.co.zw	f	t	2026-03-13 14:27:47.841556+02
13	pbkdf2_sha256$1000000$GdJIFkaONOy0pIZnuHiusF$9mySsAd0YxOk/glu7cCaoMQE/doJdye3ch5Nvf8jRvI=	\N	f	ze28012	dfegtrhgtrgtr	vfvgfbgbgfv	vmehlomakulu@zetdc.co.zw	f	t	2026-03-13 14:30:39.13968+02
14	pbkdf2_sha256$1000000$mowubBNTiJldng6DwaVxEq$jIsA28HxSM38hn37NU1NfEbIxG4BXHLcb1x5KVO8XeU=	\N	f	ze123456	tt3	tt4	zw@zedtc.com	f	t	2026-03-13 16:06:41.231351+02
15	pbkdf2_sha256$1000000$c3wyYwwFDhdpUIJnUgtDMD$/VxCE061DluSQm73iIXQsfc7n+7TmIWUtQrH9qeUWLc=	\N	f	bfbfr32	rewfergthgtrh	rtbhnbrnr	zw@zedtc.com	f	t	2026-03-13 16:09:58.513612+02
1	pbkdf2_sha256$1000000$Tqct07RLKrLediLK7oc4Om$1hXLTMNQIxVaq5GoKs8V/7F1Aeo2NLpXmIczmSPaw/Y=	2026-03-19 08:09:18.512191+02	t	ze9172535			snyamudo@zetdc.co.zw	t	t	2026-03-09 16:52:23+02
16	pbkdf2_sha256$1000000$Smfe42ab3jXm2J1KVHrGtC$P2mwlQqFOQ/5UbIv6+MxAxmNndN/pNSEnueLJ6ix5XQ=	\N	f	ze91221111	Shabnance	Nyamudo	snyamudo79@zetdc.co.zw	f	t	2026-03-20 12:29:23.371598+02
17	pbkdf2_sha256$1000000$1RJTlxh7M0ocmDsIKqGxnU$nK8G80ywGkTgWs9phmBVJQOgk/4yLmthAcKWjMyPW7M=	\N	f	ze328960	Lenard	Simoyi	lsimoyi@zetdc.co.zw	f	t	2026-03-20 12:48:43.662816+02
\.


--
-- TOC entry 5281 (class 0 OID 16463)
-- Dependencies: 232
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 5283 (class 0 OID 16472)
-- Dependencies: 234
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
1	6	1
2	6	3
3	6	4
\.


--
-- TOC entry 5286 (class 0 OID 16573)
-- Dependencies: 237
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
b24e7eb8246f73dc87f30f17c8d6817d7a799e44	2026-03-10 09:28:02.847364+02	1
e118fce0f3d415963fdf4b5f8f239e5da81f253b	2026-03-10 09:58:13.093863+02	2
dab5c1585c7103bf01f4cdba74e626091193efe9	2026-03-12 18:19:02.451185+02	6
6f600e8e54e277665ba87d6822ff562dfaa94f8c	2026-03-13 13:09:57.709695+02	8
8eb242cf8dc4a3771ae96f6473f30b04e1e366ff	2026-03-13 14:01:06.811504+02	9
84ac054fca4a62a17ec644582055cbd30bd3d5b1	2026-03-13 14:08:08.384556+02	10
e4147da3b7ec36eea0e94741a636a395acfa2b28	2026-03-13 14:13:18.640381+02	11
6ddf0c266ed84cd3aea3b3affb269287fd06f5b6	2026-03-13 14:27:49.863151+02	12
ae2dcbeb49d03484eaa30f88c53068a821233538	2026-03-13 14:30:39.921752+02	13
3edec0e9827b1e1d531b3b5d4d2f8540afb248fa	2026-03-13 16:06:42.085162+02	14
b4efc5a40acf4e64ce57507f09928c675ce9c071	2026-03-13 16:09:59.360677+02	15
2bf2355c549fe7f5cb102838763e5aa975569c1e	2026-03-20 12:29:25.365352+02	16
932f3003b75458384b26be07db1fc43f84a2a755	2026-03-20 12:48:44.816774+02	17
\.


--
-- TOC entry 5301 (class 0 OID 16696)
-- Dependencies: 252
-- Data for Name: core_attachment; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_attachment (id, file, uploaded_at, uploaded_by_id, issue_id) FROM stdin;
\.


--
-- TOC entry 5289 (class 0 OID 16602)
-- Dependencies: 240
-- Data for Name: core_depot; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_depot (id, name, region_id) FROM stdin;
1	GWERU	1
2	KWEKWE	1
3	ZVISHAVANE	1
10	KUWADZANA	6
11	MALBELREIGN	6
12	WORKINGTON/WARREN PARK	6
13	GLENVIEW	6
14	WATERFALLS	6
15	SOUTHERTON	6
16	CBD	6
17	BORROWDALE	6
18	MABVUKU	6
19	RUWA	6
20	KARIBA	4
21	KAROI	4
22	MHANGURA	4
23	CHINHOYI	4
24	MUTORASHANGA	4
25	KADOMA	4
26	CHEGUTU	4
27	NORTON	4
28	BEATRICE	4
29	CENTENARY	4
30	MVURWI	4
31	MT DARWIN	4
32	CONCESSION	4
33	BINDURA	4
34	MUTOKO/MUREWA	4
35	MARONDERA	4
36	BROMLEY	4
37	JURU	4
38	GWERU URBAN	1
39	GWERU RURAL	1
40	MVUMA	1
41	SHURUGWI	1
42	CHIVHU	1
43	REDCLIFF	1
44	GOKWE	1
45	NKAYI	1
46	NEMBUDZIYA	1
47	MATAGA	1
48	MUTARE URBAN	3
49	MUTARE ENVIRONS	3
50	NYANGA	3
51	CHIPINGE	3
53	CHIMANIMANI	3
54	MIDDLE SABI	3
55	RUSAPE	3
56	MASVINGO	3
57	GUTU	3
58	MASHAVA	3
59	RUTENGA	3
60	CHIREDZI	3
61	NKETA	2
62	ENTUMBANE	2
63	BULAWAYO EAST	2
64	PLUMTREE	2
65	TURK-MINE	2
66	BEITBRIDGE	2
67	VICTORIA FALLS	2
68	HWANGE	2
69	BINGA	2
70	LUPANE	2
71	GWANDA	2
72	MAPHISA	2
73	ESIGODINI	2
74	FILABUSI	2
75	BULAWAYO ENVIRONS	2
76	TSHOLOTSHO	2
\.


--
-- TOC entry 5307 (class 0 OID 41420)
-- Dependencies: 258
-- Data for Name: core_issue; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_issue (id, issue_number, region_id, depot_id, system_id, module_id, submodule_id, description, raised_by_name, contact_phone, issue_logged_by_id, assigned_to_id, severity_id, status_id, date_issue_raised, resolution_notes, zetdc_comments, longshine_comments, resolved_by_id, date_issue_resolved, screenshot) FROM stdin;
\.


--
-- TOC entry 5303 (class 0 OID 16706)
-- Dependencies: 254
-- Data for Name: core_issuehistory; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_issuehistory (id, changed_at, field_name, old_value, new_value, changed_by_id, issue_id) FROM stdin;
\.


--
-- TOC entry 5291 (class 0 OID 16610)
-- Dependencies: 242
-- Data for Name: core_issueseverity; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_issueseverity (id, name, priority_order) FROM stdin;
1	CRITICAL	1
2	HIGH	2
3	MEDIUM	3
4	LOW	4
\.


--
-- TOC entry 5293 (class 0 OID 16622)
-- Dependencies: 244
-- Data for Name: core_issuestatus; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_issuestatus (id, name, is_resolved_state) FROM stdin;
1	PENDING	f
6	RESOLVED	t
3	WORKINPROGRESS	f
8	WORK IN PROGRESS	f
\.


--
-- TOC entry 5295 (class 0 OID 16633)
-- Dependencies: 246
-- Data for Name: core_module; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_module (id, name, system_id) FROM stdin;
1	CRM	1
2	Assets	1
3	NDPM	1
\.


--
-- TOC entry 5297 (class 0 OID 16643)
-- Dependencies: 248
-- Data for Name: core_region; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_region (id, name, code) FROM stdin;
1	SOUTHERN	SU
2	WESTERN	WE
3	EASTERN	EA
4	NORTHERN	NO
5	HEAD OFFICE	HO
6	HARARE	HA
\.


--
-- TOC entry 5299 (class 0 OID 16656)
-- Dependencies: 250
-- Data for Name: core_role; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_role (id, name) FROM stdin;
1	ADMIN
2	END USER
3	ISSUE SOLVERS
4	REGIONAL_MANAGER
5	EXPERT
6	ENDUSER
\.


--
-- TOC entry 5311 (class 0 OID 41521)
-- Dependencies: 262
-- Data for Name: core_submodule; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_submodule (id, name, module_id) FROM stdin;
1	security deposit review	1
2	Se enrollment	1
3	fraud management	1
4	planned outage	1
5	customer material purchase	1
6	new connection	1
7	fault outage	1
8	annual budget	1
9	change tariff	1
10	net metering connection	1
11	budget adjustment	1
12	standard connection	1
13	basic info change test 1	1
14	ownership transfer	1
15	temporary connection	1
16	change capacity	1
17	budget management	1
18	inbound delivery	2
19	outbound delivery	2
20	scrap management	2
21	overtime	3
22	internal project	3
\.


--
-- TOC entry 5309 (class 0 OID 41506)
-- Dependencies: 260
-- Data for Name: core_system; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_system (id, name) FROM stdin;
1	ZUMS
\.


--
-- TOC entry 5305 (class 0 OID 16726)
-- Dependencies: 256
-- Data for Name: core_userprofile; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.core_userprofile (id, slack_user_id, region_id, role_id, user_id, phone_number) FROM stdin;
1		\N	1	1	
2		\N	3	2	
3		\N	3	3	
4		\N	3	4	
5		1	2	5	
6		5	2	6	
8		\N	6	8	
9		\N	6	9	
10		\N	6	10	
11		\N	6	11	
12		\N	6	12	
13		\N	6	13	
14		\N	6	14	
15		\N	6	15	
16		\N	6	16	
17		\N	6	17	
\.


--
-- TOC entry 5285 (class 0 OID 16533)
-- Dependencies: 236
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-03-10 07:39:06.048846+02	1	ADMIN	1	[{"added": {}}]	9	1
2	2026-03-10 07:39:29.457326+02	2	REGIONAL_MANAGER	1	[{"added": {}}]	9	1
3	2026-03-10 07:39:49.222124+02	3	EXPERT	1	[{"added": {}}]	9	1
4	2026-03-10 07:40:41.030132+02	1	SOUTHERN	1	[{"added": {}}]	10	1
5	2026-03-10 07:41:03.96372+02	2	WESTERN	1	[{"added": {}}]	10	1
6	2026-03-10 07:41:39.249229+02	3	EASTERN	1	[{"added": {}}]	10	1
7	2026-03-10 07:42:35.05674+02	1	GWERU (SU)	1	[{"added": {}}]	11	1
8	2026-03-10 07:42:59.627696+02	2	KWEKWE (SU)	1	[{"added": {}}]	11	1
9	2026-03-10 07:43:32.442747+02	3	ZVISHAVANE (SU)	1	[{"added": {}}]	11	1
10	2026-03-10 07:44:02.434979+02	1	CRM	1	[{"added": {}}]	12	1
11	2026-03-10 07:44:08.708055+02	2	SMART VEND	1	[{"added": {}}]	12	1
12	2026-03-10 07:44:15.706823+02	3	ZUMS	1	[{"added": {}}]	12	1
13	2026-03-10 07:44:25.053692+02	4	CONTACTING	1	[{"added": {}}]	12	1
14	2026-03-10 07:44:37.865587+02	5	TARIFF CHANGE	1	[{"added": {}}]	12	1
15	2026-03-10 07:44:44.786293+02	6	ALL	1	[{"added": {}}]	12	1
16	2026-03-10 07:45:20.484575+02	1	CRITICAL	1	[{"added": {}}]	13	1
17	2026-03-10 07:45:31.126722+02	2	HIGH	1	[{"added": {}}]	13	1
18	2026-03-10 07:45:43.116717+02	3	MEDIUM	1	[{"added": {}}]	13	1
19	2026-03-10 07:45:55.488075+02	4	LOW	1	[{"added": {}}]	13	1
20	2026-03-10 07:46:43.362581+02	1	PENDING	1	[{"added": {}}]	14	1
21	2026-03-10 07:46:59.667962+02	2	ISSUE RECEIVED	1	[{"added": {}}]	14	1
22	2026-03-10 07:47:10.354675+02	3	WORK IN PROGRESS	1	[{"added": {}}]	14	1
23	2026-03-10 07:47:35.921139+02	4	NEEDS CLARIFICATION	1	[{"added": {}}]	14	1
24	2026-03-10 07:47:58.986946+02	5	NEW REQUIREMENTS	1	[{"added": {}}]	14	1
25	2026-03-10 07:48:08.618828+02	6	RESOLVED	1	[{"added": {}}]	14	1
26	2026-03-10 08:02:16.543046+02	1	ze9172535	2	[{"added": {"name": "user profile", "object": " (ADMIN)"}}]	4	1
27	2026-03-10 09:57:12.095736+02	2	zenyamudo	1	[{"added": {}}, {"added": {"name": "user profile", "object": " (EXPERT)"}}]	4	1
28	2026-03-10 09:57:34.511847+02	2	zenyamudo	2	[]	4	1
29	2026-03-12 18:48:21.418251+02	6	zetdc	2	[{"changed": {"fields": ["User permissions"]}}]	4	1
30	2026-03-12 18:49:04.581582+02	2	REGIONAL_MANAGER	2	[]	9	1
31	2026-03-13 10:24:08.802975+02	5	NEWREQUIREMENTS	2	[{"changed": {"fields": ["Name"]}}]	14	1
32	2026-03-13 10:24:47.699255+02	3	WORKINPROGRESS	2	[{"changed": {"fields": ["Name"]}}]	14	1
33	2026-03-13 10:25:11.074348+02	2	ISSUERECEIVED	2	[{"changed": {"fields": ["Name"]}}]	14	1
34	2026-03-13 10:25:26.950613+02	4	NEEDSCLARIFICATION	2	[{"changed": {"fields": ["Name"]}}]	14	1
35	2026-03-13 10:57:12.16358+02	14	SUPPLY CHAIN SCHEME	1	[{"added": {}}]	12	1
36	2026-03-13 10:57:32.247582+02	15	MOBILE	1	[{"added": {}}]	12	1
37	2026-03-13 10:58:37.322427+02	16	PROJECT COSTING	1	[{"added": {}}]	12	1
38	2026-03-13 10:58:58.417303+02	17	NDM AND ICS JOBS	1	[{"added": {}}]	12	1
39	2026-03-13 11:57:03.557084+02	2	END USER	2	[{"changed": {"fields": ["Name"]}}]	9	1
40	2026-03-13 11:57:37.002357+02	3	ISSUE SOLVERS	2	[{"changed": {"fields": ["Name"]}}]	9	1
41	2026-03-13 15:50:44.095127+02	1454	SU230	2	[{"changed": {"fields": ["Assigned to"]}}]	16	1
42	2026-03-16 11:49:59.733344+02	1457	SU232	2	[{"changed": {"fields": ["Raised by name"]}}]	16	1
43	2026-03-19 08:12:32.967016+02	10	KUWADZANA (HA)	1	[{"added": {}}]	11	1
44	2026-03-19 08:13:15.715226+02	11	MALBELREIGN (HA)	1	[{"added": {}}]	11	1
45	2026-03-19 08:13:18.939032+02	11	MALBELREIGN (HA)	2	[]	11	1
46	2026-03-19 08:14:10.900989+02	12	WORKINGTON/WARREN PARK (HA)	1	[{"added": {}}]	11	1
47	2026-03-19 08:14:33.090974+02	13	GLENVIEW (HA)	1	[{"added": {}}]	11	1
48	2026-03-19 08:14:46.297806+02	14	WATERFALLS (HA)	1	[{"added": {}}]	11	1
49	2026-03-19 08:15:04.093197+02	15	SOUTHERTON (HA)	1	[{"added": {}}]	11	1
50	2026-03-19 08:15:25.243824+02	16	CBD (HA)	1	[{"added": {}}]	11	1
51	2026-03-19 08:15:47.229741+02	17	BORROWDALE (HA)	1	[{"added": {}}]	11	1
52	2026-03-19 08:16:07.618735+02	18	MABVUKU (HA)	1	[{"added": {}}]	11	1
53	2026-03-19 08:16:18.333001+02	19	RUWA (HA)	1	[{"added": {}}]	11	1
54	2026-03-19 08:23:01.180056+02	20	KARIBA (NO)	1	[{"added": {}}]	11	1
55	2026-03-19 08:23:12.555727+02	21	KAROI (NO)	1	[{"added": {}}]	11	1
56	2026-03-19 08:23:33.524637+02	22	MHANGURA (NO)	1	[{"added": {}}]	11	1
57	2026-03-19 08:23:42.922018+02	23	CHINHOYI (NO)	1	[{"added": {}}]	11	1
58	2026-03-19 08:23:56.935728+02	24	MUTORASHANGA (NO)	1	[{"added": {}}]	11	1
59	2026-03-19 08:24:08.780625+02	25	KADOMA (NO)	1	[{"added": {}}]	11	1
60	2026-03-19 08:24:21.666318+02	26	CHEGUTU (NO)	1	[{"added": {}}]	11	1
61	2026-03-19 08:24:34.995609+02	27	NORTON (NO)	1	[{"added": {}}]	11	1
62	2026-03-19 08:24:56.166433+02	28	BEATRICE (NO)	1	[{"added": {}}]	11	1
63	2026-03-19 08:25:09.870164+02	29	CENTENARY (NO)	1	[{"added": {}}]	11	1
64	2026-03-19 08:25:23.150779+02	30	MVURWI (NO)	1	[{"added": {}}]	11	1
65	2026-03-19 08:25:35.730004+02	31	MT DARWIN (NO)	1	[{"added": {}}]	11	1
66	2026-03-19 08:26:17.499376+02	32	CONCESSION (NO)	1	[{"added": {}}]	11	1
67	2026-03-19 08:26:26.666412+02	33	BINDURA (NO)	1	[{"added": {}}]	11	1
68	2026-03-19 08:26:55.145828+02	34	MUTOKO/MUREWA (NO)	1	[{"added": {}}]	11	1
69	2026-03-19 08:27:09.9763+02	35	MARONDERA (NO)	1	[{"added": {}}]	11	1
70	2026-03-19 08:27:41.839586+02	36	BROMLEY (NO)	1	[{"added": {}}]	11	1
71	2026-03-19 08:27:54.005241+02	37	JURU (NO)	1	[{"added": {}}]	11	1
72	2026-03-19 08:28:42.807916+02	38	GWERU URBAN (SU)	1	[{"added": {}}]	11	1
73	2026-03-19 08:28:58.66413+02	39	GWERU RURAL (SU)	1	[{"added": {}}]	11	1
74	2026-03-19 08:29:16.817244+02	40	MVUMA (SU)	1	[{"added": {}}]	11	1
75	2026-03-19 08:29:25.307519+02	41	SHURUGWI (SU)	1	[{"added": {}}]	11	1
76	2026-03-19 08:29:37.899588+02	42	CHIVHU (SU)	1	[{"added": {}}]	11	1
77	2026-03-19 08:30:07.788135+02	43	REDCLIFF (SU)	1	[{"added": {}}]	11	1
78	2026-03-19 08:30:53.960422+02	44	GOKWE (SU)	1	[{"added": {}}]	11	1
79	2026-03-19 08:31:03.987582+02	45	NKAYI (SU)	1	[{"added": {}}]	11	1
80	2026-03-19 08:31:15.719471+02	46	NEMBUDZIYA (SU)	1	[{"added": {}}]	11	1
81	2026-03-19 08:31:33.555076+02	47	MATAGA (SU)	1	[{"added": {}}]	11	1
82	2026-03-19 08:34:44.726453+02	1340	SU77	2	[{"changed": {"fields": ["Depot", "Module", "Raised by name"]}}]	16	1
83	2026-03-19 08:36:38.654441+02	9	NEEDS CLARIFICATION	3		14	1
84	2026-03-19 08:36:45.231182+02	7	ISSUE RECEIVED	3		14	1
85	2026-03-19 08:36:51.332113+02	5	NEWREQUIREMENTS	3		14	1
86	2026-03-19 08:37:00.905026+02	4	NEEDSCLARIFICATION	3		14	1
87	2026-03-19 08:37:22.497177+02	2	ISSUERECEIVED	3		14	1
88	2026-03-19 09:11:02.997884+02	48	MUTARE (EA)	1	[{"added": {}}]	11	1
89	2026-03-19 09:11:41.908082+02	48	MUTARE URBAN (EA)	2	[{"changed": {"fields": ["Name"]}}]	11	1
90	2026-03-19 09:12:11.596569+02	49	MUTARE ENVIRONS (EA)	1	[{"added": {}}]	11	1
91	2026-03-19 09:25:27.907068+02	50	NYANGA (EA)	1	[{"added": {}}]	11	1
92	2026-03-19 09:25:41.543657+02	51	CHIPINGE (EA)	1	[{"added": {}}]	11	1
93	2026-03-19 09:26:00.307367+02	52	CHIMANIMANI (WE)	1	[{"added": {}}]	11	1
94	2026-03-19 09:26:15.203841+02	53	CHIMANIMANI (EA)	1	[{"added": {}}]	11	1
95	2026-03-19 09:26:31.01351+02	54	MIDDLE SABI (EA)	1	[{"added": {}}]	11	1
96	2026-03-19 09:26:47.073322+02	55	RUSAPE (EA)	1	[{"added": {}}]	11	1
97	2026-03-19 09:27:02.041008+02	56	MASVINGO (EA)	1	[{"added": {}}]	11	1
98	2026-03-19 09:27:10.986413+02	57	GUTU (EA)	1	[{"added": {}}]	11	1
99	2026-03-19 09:27:21.930993+02	58	MASHAVA (EA)	1	[{"added": {}}]	11	1
100	2026-03-19 09:27:36.395402+02	59	RUTENGA (EA)	1	[{"added": {}}]	11	1
101	2026-03-19 09:27:56.638059+02	60	CHIREDZI (EA)	1	[{"added": {}}]	11	1
102	2026-03-19 09:28:16.553806+02	61	NKETA (WE)	1	[{"added": {}}]	11	1
103	2026-03-19 09:28:30.871694+02	62	ENTUMBANE (WE)	1	[{"added": {}}]	11	1
104	2026-03-19 09:28:58.759285+02	63	BULAWAYO EAST (WE)	1	[{"added": {}}]	11	1
105	2026-03-19 09:29:16.628488+02	64	PLUMTREE (WE)	1	[{"added": {}}]	11	1
106	2026-03-19 09:29:32.56335+02	65	TURK-MINE (WE)	1	[{"added": {}}]	11	1
107	2026-03-19 09:29:46.641754+02	66	BEITBRIDGE (WE)	1	[{"added": {}}]	11	1
108	2026-03-19 09:30:05.438649+02	67	VICTORIA FALLS (WE)	1	[{"added": {}}]	11	1
109	2026-03-19 09:30:20.032169+02	68	HWANGE (WE)	1	[{"added": {}}]	11	1
110	2026-03-19 09:30:30.627651+02	69	BINGA (WE)	1	[{"added": {}}]	11	1
111	2026-03-19 09:30:49.843147+02	70	LUPANE (WE)	1	[{"added": {}}]	11	1
112	2026-03-19 09:31:05.271574+02	71	GWANDA (WE)	1	[{"added": {}}]	11	1
113	2026-03-19 09:31:26.188265+02	72	MAPHISA (WE)	1	[{"added": {}}]	11	1
114	2026-03-19 09:32:06.945393+02	73	ESIGODINI (WE)	1	[{"added": {}}]	11	1
115	2026-03-19 09:32:20.320893+02	74	FILABUSI (WE)	1	[{"added": {}}]	11	1
116	2026-03-19 09:32:43.536066+02	75	BULAWAYO ENVIRONS (WE)	1	[{"added": {}}]	11	1
117	2026-03-19 09:33:13.650532+02	76	TSHOLOTSHO (WE)	1	[{"added": {}}]	11	1
118	2026-03-19 09:34:18.453145+02	52	CHIMANIMANI (WE)	3		11	1
\.


--
-- TOC entry 5271 (class 0 OID 16403)
-- Dependencies: 222
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	authtoken	token
8	authtoken	tokenproxy
9	core	role
10	core	region
11	core	depot
12	core	module
13	core	issueseverity
14	core	issuestatus
15	core	userprofile
16	core	issue
17	core	attachment
18	core	issuehistory
19	core	system
20	core	submodule
\.


--
-- TOC entry 5269 (class 0 OID 16391)
-- Dependencies: 220
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-03-09 16:44:35.935337+02
2	auth	0001_initial	2026-03-09 16:44:36.099271+02
3	admin	0001_initial	2026-03-09 16:44:36.147454+02
4	admin	0002_logentry_remove_auto_add	2026-03-09 16:44:36.154147+02
5	admin	0003_logentry_add_action_flag_choices	2026-03-09 16:44:36.161445+02
6	contenttypes	0002_remove_content_type_name	2026-03-09 16:44:36.181182+02
7	auth	0002_alter_permission_name_max_length	2026-03-09 16:44:36.188558+02
8	auth	0003_alter_user_email_max_length	2026-03-09 16:44:36.194682+02
9	auth	0004_alter_user_username_opts	2026-03-09 16:44:36.207805+02
10	auth	0005_alter_user_last_login_null	2026-03-09 16:44:36.220893+02
11	auth	0006_require_contenttypes_0002	2026-03-09 16:44:36.222405+02
12	auth	0007_alter_validators_add_error_messages	2026-03-09 16:44:36.228015+02
13	auth	0008_alter_user_username_max_length	2026-03-09 16:44:36.24479+02
14	auth	0009_alter_user_last_name_max_length	2026-03-09 16:44:36.259539+02
15	auth	0010_alter_group_name_max_length	2026-03-09 16:44:36.269732+02
16	auth	0011_update_proxy_permissions	2026-03-09 16:44:36.307286+02
17	auth	0012_alter_user_first_name_max_length	2026-03-09 16:44:36.33348+02
18	authtoken	0001_initial	2026-03-09 16:44:36.363453+02
19	authtoken	0002_auto_20160226_1747	2026-03-09 16:44:36.391597+02
20	authtoken	0003_tokenproxy	2026-03-09 16:44:36.393642+02
21	authtoken	0004_alter_tokenproxy_options	2026-03-09 16:44:36.397767+02
22	sessions	0001_initial	2026-03-09 16:44:36.416567+02
23	core	0001_initial	2026-03-10 07:29:01.020267+02
24	core	0002_userprofile_phone_number	2026-03-12 17:04:02.737005+02
25	core	0002_issue_screenshot	2026-03-13 08:54:21.879761+02
26	core	0003_userprofile_phone_number	2026-03-14 10:07:18.813959+02
27	core	0003_userprofile_phone_number	2026-03-14 10:07:48.395764+02
28	core	0004_issue_resolved_by	2026-03-14 10:08:09.770398+02
29	core	0005_remove_issue_issue_resolved_by_and_more	2026-03-14 12:13:33.899152+02
30	core	0006_userprofile_phone_number	2026-03-14 12:13:35.286517+02
31	core	0007_remove_issue_code_remove_issue_created_at_and_more	2026-03-18 07:27:10.372542+02
32	core	0008_alter_issue_functionality	2026-03-18 14:27:32.7001+02
33	core	0009_remove_issue_issue_number	2026-03-18 14:36:51.617234+02
34	core	0010_issue_issue_number_alter_issue_functionality	2026-03-18 15:41:26.265139+02
35	core	0011_alter_issue_issue_number	2026-03-18 15:43:00.876159+02
36	core	0012_remove_issue_functionality	2026-03-18 16:28:46.29983+02
37	core	0013_reorder_issue_columns	2026-03-18 16:34:31.903971+02
38	core	0014_issue_submodule_issue_system	2026-03-20 15:55:04.135634+02
39	core	0015_reorder_issue_columns_v2	2026-03-20 15:57:15.734057+02
40	core	0016_system_alter_issue_module_alter_module_name_and_more	2026-03-20 16:31:25.318024+02
\.


--
-- TOC entry 5287 (class 0 OID 16589)
-- Dependencies: 238
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: zolits
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
3jyc04qzyc7fjbhmg1hchxu8de947pq5	.eJxVjDkOwjAQAP-yNbKytrFxSnreYO1h4wBKpBwV4u8oUgpoZ0bzhkzb2vK2lDkPCj0gnH4ZkzzLuAt90HifjEzjOg9s9sQcdjG3ScvrerR_g0ZLgx4Ek8UYhNX5S6woyWsKRIW5OrIWLbkuRNGiqesknFkSWmc9V4lYC3y-67g4Tw:1vzpgT:oJXYX5b98d6oXeM4NXjgLNz4-kBdFqomCLZBtRaqCKM	2026-03-24 07:31:09.907524+02
r20wllgt1h34c9znkhgw1q0gdvrz2m31	.eJxVjDkOwjAQAP-yNbKytrFxSnreYO1h4wBKpBwV4u8oUgpoZ0bzhkzb2vK2lDkPCj0gnH4ZkzzLuAt90HifjEzjOg9s9sQcdjG3ScvrerR_g0ZLgx4Ek8UYhNX5S6woyWsKRIW5OrIWLbkuRNGiqesknFkSWmc9V4lYC3y-67g4Tw:1w0ifa:PvgqcS4BjpRGBmg_zlxd830o0II46Z-RNW7p95iEvYg	2026-03-26 18:13:54.149196+02
ll2zca7dig80yne23fvszmt0pjjtkrcl	.eJxVjM0OgjAQBt9lz6ah9FeO3nmG5lu6FdRAQuFkfHdDwkGvM5N5U8K-jWmvsqYpU0eaLr-MMTxlPkR-YL4valjmbZ1YHYk6bVX9kuV1O9u_wYg6UkcNezHFILCGaX0AHMMYxOBbFOttjsLaDjG67EsrEYav1kI3zCE7T58v7qA4Iw:1w36ZK:Iwt80acbRjtv_5qYwauOiC29P5NjFO6tps9CeX0RsNc	2026-04-02 08:09:18.516516+02
\.


--
-- TOC entry 5318 (class 0 OID 0)
-- Dependencies: 225
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 5319 (class 0 OID 0)
-- Dependencies: 227
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 5320 (class 0 OID 0)
-- Dependencies: 223
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 80, true);


--
-- TOC entry 5321 (class 0 OID 0)
-- Dependencies: 231
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- TOC entry 5322 (class 0 OID 0)
-- Dependencies: 229
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 17, true);


--
-- TOC entry 5323 (class 0 OID 0)
-- Dependencies: 233
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 3, true);


--
-- TOC entry 5324 (class 0 OID 0)
-- Dependencies: 251
-- Name: core_attachment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_attachment_id_seq', 1, false);


--
-- TOC entry 5325 (class 0 OID 0)
-- Dependencies: 239
-- Name: core_depot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_depot_id_seq', 76, true);


--
-- TOC entry 5326 (class 0 OID 0)
-- Dependencies: 257
-- Name: core_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_issue_id_seq', 1, false);


--
-- TOC entry 5327 (class 0 OID 0)
-- Dependencies: 253
-- Name: core_issuehistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_issuehistory_id_seq', 1, false);


--
-- TOC entry 5328 (class 0 OID 0)
-- Dependencies: 241
-- Name: core_issueseverity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_issueseverity_id_seq', 4, true);


--
-- TOC entry 5329 (class 0 OID 0)
-- Dependencies: 243
-- Name: core_issuestatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_issuestatus_id_seq', 9, true);


--
-- TOC entry 5330 (class 0 OID 0)
-- Dependencies: 245
-- Name: core_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_module_id_seq', 3, true);


--
-- TOC entry 5331 (class 0 OID 0)
-- Dependencies: 247
-- Name: core_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_region_id_seq', 7, true);


--
-- TOC entry 5332 (class 0 OID 0)
-- Dependencies: 249
-- Name: core_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_role_id_seq', 6, true);


--
-- TOC entry 5333 (class 0 OID 0)
-- Dependencies: 261
-- Name: core_submodule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_submodule_id_seq', 22, true);


--
-- TOC entry 5334 (class 0 OID 0)
-- Dependencies: 259
-- Name: core_system_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_system_id_seq', 3, true);


--
-- TOC entry 5335 (class 0 OID 0)
-- Dependencies: 255
-- Name: core_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.core_userprofile_id_seq', 17, true);


--
-- TOC entry 5336 (class 0 OID 0)
-- Dependencies: 235
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 118, true);


--
-- TOC entry 5337 (class 0 OID 0)
-- Dependencies: 221
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 20, true);


--
-- TOC entry 5338 (class 0 OID 0)
-- Dependencies: 219
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zolits
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 40, true);


-- Completed on 2026-03-23 08:49:54

--
-- PostgreSQL database dump complete
--

\unrestrict j8qhafmeNJJr9CQTihkvbRbrT572JPN7lnq9sAJQwvmXsYqThEaSacLBsgV5iJt

