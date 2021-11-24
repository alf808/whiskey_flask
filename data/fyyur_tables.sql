--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: nemo
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO nemo;

--
-- Name: artists; Type: TABLE; Schema: public; Owner: nemo
--

CREATE TABLE public.artists (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    phone character varying(120),
    genres character varying[],
    image_link character varying(500),
    facebook_link character varying(120),
    website character varying(120),
    seeking_venue boolean,
    seeking_description character varying(200)
);


ALTER TABLE public.artists OWNER TO nemo;

--
-- Name: artists_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE public.artists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artists_id_seq OWNER TO nemo;

--
-- Name: artists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE public.artists_id_seq OWNED BY public.artists.id;


--
-- Name: shows; Type: TABLE; Schema: public; Owner: nemo
--

CREATE TABLE public.shows (
    id integer NOT NULL,
    artist_id integer NOT NULL,
    venue_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL
);


ALTER TABLE public.shows OWNER TO nemo;

--
-- Name: shows_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE public.shows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shows_id_seq OWNER TO nemo;

--
-- Name: shows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE public.shows_id_seq OWNED BY public.shows.id;


--
-- Name: venues; Type: TABLE; Schema: public; Owner: nemo
--

CREATE TABLE public.venues (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    address character varying(120),
    phone character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    genres character varying[],
    website character varying(120),
    seeking_talent boolean,
    seeking_description character varying(200)
);


ALTER TABLE public.venues OWNER TO nemo;

--
-- Name: venues_id_seq; Type: SEQUENCE; Schema: public; Owner: nemo
--

CREATE SEQUENCE public.venues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venues_id_seq OWNER TO nemo;

--
-- Name: venues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nemo
--

ALTER SEQUENCE public.venues_id_seq OWNED BY public.venues.id;


--
-- Name: artists id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.artists ALTER COLUMN id SET DEFAULT nextval('public.artists_id_seq'::regclass);


--
-- Name: shows id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.shows ALTER COLUMN id SET DEFAULT nextval('public.shows_id_seq'::regclass);


--
-- Name: venues id; Type: DEFAULT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.venues ALTER COLUMN id SET DEFAULT nextval('public.venues_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: nemo
--

COPY public.alembic_version (version_num) FROM stdin;
fea1b43595c4
\.


--
-- Data for Name: artists; Type: TABLE DATA; Schema: public; Owner: nemo
--

COPY public.artists (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) FROM stdin;
\.


--
-- Data for Name: shows; Type: TABLE DATA; Schema: public; Owner: nemo
--

COPY public.shows (id, artist_id, venue_id, start_time) FROM stdin;
\.


--
-- Data for Name: venues; Type: TABLE DATA; Schema: public; Owner: nemo
--

COPY public.venues (id, name, city, state, address, phone, image_link, facebook_link, genres, website, seeking_talent, seeking_description) FROM stdin;
\.


--
-- Name: artists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nemo
--

SELECT pg_catalog.setval('public.artists_id_seq', 1, false);


--
-- Name: shows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nemo
--

SELECT pg_catalog.setval('public.shows_id_seq', 1, false);


--
-- Name: venues_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nemo
--

SELECT pg_catalog.setval('public.venues_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: artists artists_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.artists
    ADD CONSTRAINT artists_pkey PRIMARY KEY (id);


--
-- Name: shows shows_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_pkey PRIMARY KEY (id);


--
-- Name: venues venues_pkey; Type: CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.venues
    ADD CONSTRAINT venues_pkey PRIMARY KEY (id);


--
-- Name: shows shows_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artists(id);


--
-- Name: shows shows_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nemo
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- PostgreSQL database dump complete
--

