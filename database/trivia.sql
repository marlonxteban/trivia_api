--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1 (Debian 13.1-1.pgdg100+1)
-- Dumped by pg_dump version 13.1 (Debian 13.1-1.pgdg100+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: marlon
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO marlon;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: marlon
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    type character varying
);


ALTER TABLE public.categories OWNER TO marlon;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: marlon
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO marlon;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: marlon
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: questions; Type: TABLE; Schema: public; Owner: marlon
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    question character varying,
    answer character varying,
    category_id integer,
    difficulty integer
);


ALTER TABLE public.questions OWNER TO marlon;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: marlon
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.questions_id_seq OWNER TO marlon;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: marlon
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: marlon
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: marlon
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: marlon
--

COPY public.alembic_version (version_num) FROM stdin;
1fcf48a3b5c1
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: marlon
--

COPY public.categories (id, type) FROM stdin;
1       Science
2       Art
3       Geography
4       History
5       Entertainment
6       Sports
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: marlon
--

COPY public.questions (id, question, answer, category_id, difficulty) FROM stdin;
5       Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?      Maya Angelou    2       4
9       What boxer's original name is Cassius Clay?     Muhammad Ali    6       1
2       What movie earned Tom Hanks his third straight Oscar nomination, in 1996?       Apollo 13       5       4
4       What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?  Apollo 13
5       4
6       What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?
Edward Scissorhands     5       3
10      Which is the only team to play in every soccer World Cup tournament?    Brazil  6       3
11      Which country won the first ever soccer World Cup in 1930?      Uruguay 6       4
12      Who invented Peanut Butter?     George Washington Carver        4       2
13      What is the largest lake in Africa?     Lake Victoria   3       2
14      In which royal palace would you find the Hall of Mirrors?       The Palace of Versailles        3       3
15      The Taj Mahal is located in which Indian city?  Agra    3       2
16      Which Dutch graphic artist–initials M C was a creator of optical illusions?     Escher  2       1
17      La Giaconda is better known as what?    Mona Lisa       2       3
18      How many paintings did Van Gogh sell in his lifetime?   One     2       4
19      Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?
Jackson Pollock 2       2
20      What is the heaviest organ in the human body?   The Liver       1       4
21      Who discovered penicillin?      Alexander Fleming       3       1
22      Hematology is a branch of medicine involving the study of what? Blood   1       4
23      Which dung beetle was worshipped by the ancient Egyptians?      Scarab  4       4
3       Who is this?    me      5       1
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marlon
--

SELECT pg_catalog.setval('public.categories_id_seq', 1, false);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marlon
--

SELECT pg_catalog.setval('public.questions_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: marlon
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: marlon
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: marlon
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: questions questions_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marlon
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCA
DE;


--
-- PostgreSQL database dump complete
--