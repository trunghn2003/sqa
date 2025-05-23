PGDMP     *    	                }            SmartLib_DB    15.4    15.4 �    1           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            2           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            3           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            4           1262    26591    SmartLib_DB    DATABASE     �   CREATE DATABASE "SmartLib_DB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Arabic_Palestinian Authority.1252';
    DROP DATABASE "SmartLib_DB";
                postgres    false            �           1247    27101    status_enum    TYPE     Z   CREATE TYPE public.status_enum AS ENUM (
    'Pending',
    'Accepted',
    'Rejected'
);
    DROP TYPE public.status_enum;
       public          postgres    false            �            1259    26592    Book    TABLE     �  CREATE TABLE public."Book" (
    book_id integer NOT NULL,
    book_name character varying(255) NOT NULL,
    book_author character varying(255) NOT NULL,
    book_type character varying(255) NOT NULL,
    book_barcode character varying(255) NOT NULL,
    book_image character varying(255),
    book_reading_counter integer,
    book_rating_avg integer,
    book_uploaded_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    book_favourite_counter integer DEFAULT 0,
    category_id integer NOT NULL,
    status public.status_enum DEFAULT 'Pending'::public.status_enum NOT NULL,
    book_description character varying(2048) DEFAULT 'No Description'::character varying NOT NULL,
    book_file character varying(255)
);
    DROP TABLE public."Book";
       public         heap    postgres    false    965    965                       1259    26999    Book_Continue_Reading    TABLE     �   CREATE TABLE public."Book_Continue_Reading" (
    continue_reading_id integer NOT NULL,
    book_id integer NOT NULL,
    reader_id integer NOT NULL
);
 +   DROP TABLE public."Book_Continue_Reading";
       public         heap    postgres    false                       1259    26998 -   Book_Continue_Reading_continue_reading_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Book_Continue_Reading_continue_reading_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 F   DROP SEQUENCE public."Book_Continue_Reading_continue_reading_id_seq";
       public          postgres    false    262            5           0    0 -   Book_Continue_Reading_continue_reading_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."Book_Continue_Reading_continue_reading_id_seq" OWNED BY public."Book_Continue_Reading".continue_reading_id;
          public          postgres    false    261            �            1259    26597    Book_book_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Book_book_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."Book_book_id_seq";
       public          postgres    false    214            6           0    0    Book_book_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."Book_book_id_seq" OWNED BY public."Book".book_id;
          public          postgres    false    215                       1259    26946    Category    TABLE     x   CREATE TABLE public."Category" (
    category_id integer NOT NULL,
    category_name character varying(255) NOT NULL
);
    DROP TABLE public."Category";
       public         heap    postgres    false                       1259    26945    Category_category_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Category_category_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."Category_category_id_seq";
       public          postgres    false    258            7           0    0    Category_category_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."Category_category_id_seq" OWNED BY public."Category".category_id;
          public          postgres    false    257            �            1259    26598 	   Copy_Book    TABLE     �   CREATE TABLE public."Copy_Book" (
    copy_book_id integer NOT NULL,
    book_id integer NOT NULL,
    reader_id integer NOT NULL
);
    DROP TABLE public."Copy_Book";
       public         heap    postgres    false            �            1259    26601    Copy_Book_copy_book_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Copy_Book_copy_book_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public."Copy_Book_copy_book_id_seq";
       public          postgres    false    216            8           0    0    Copy_Book_copy_book_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public."Copy_Book_copy_book_id_seq" OWNED BY public."Copy_Book".copy_book_id;
          public          postgres    false    217            �            1259    26602    FeedBack    TABLE     �   CREATE TABLE public."FeedBack" (
    feedback_id integer NOT NULL,
    reader_id integer NOT NULL,
    feedback_description character varying(255) NOT NULL,
    feedback_time timestamp without time zone DEFAULT now()
);
    DROP TABLE public."FeedBack";
       public         heap    postgres    false            �            1259    26605    FeedBack_feedback_id_seq    SEQUENCE     �   CREATE SEQUENCE public."FeedBack_feedback_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."FeedBack_feedback_id_seq";
       public          postgres    false    218            9           0    0    FeedBack_feedback_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."FeedBack_feedback_id_seq" OWNED BY public."FeedBack".feedback_id;
          public          postgres    false    219            �            1259    26606    Gamification_Record    TABLE     $  CREATE TABLE public."Gamification_Record" (
    gamification_record_id integer NOT NULL,
    reader_id integer NOT NULL,
    gamification_description character varying(255) NOT NULL,
    achieved_point integer NOT NULL,
    date_and_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
 )   DROP TABLE public."Gamification_Record";
       public         heap    postgres    false            �            1259    26610 .   Gamification_Record_gamification_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Gamification_Record_gamification_record_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 G   DROP SEQUENCE public."Gamification_Record_gamification_record_id_seq";
       public          postgres    false    220            :           0    0 .   Gamification_Record_gamification_record_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public."Gamification_Record_gamification_record_id_seq" OWNED BY public."Gamification_Record".gamification_record_id;
          public          postgres    false    221            �            1259    26611    Manager    TABLE     a   CREATE TABLE public."Manager" (
    manager_id integer NOT NULL,
    user_id integer NOT NULL
);
    DROP TABLE public."Manager";
       public         heap    postgres    false            �            1259    26614    Manager_manager_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Manager_manager_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public."Manager_manager_id_seq";
       public          postgres    false    222            ;           0    0    Manager_manager_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public."Manager_manager_id_seq" OWNED BY public."Manager".manager_id;
          public          postgres    false    223            �            1259    26615    Note    TABLE     �   CREATE TABLE public."Note" (
    note_id integer NOT NULL,
    copy_book_id integer NOT NULL,
    note_record character varying(255) NOT NULL
);
    DROP TABLE public."Note";
       public         heap    postgres    false            �            1259    26618    Note_note_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Note_note_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."Note_note_id_seq";
       public          postgres    false    224            <           0    0    Note_note_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."Note_note_id_seq" OWNED BY public."Note".note_id;
          public          postgres    false    225            �            1259    26619    Notification    TABLE     �   CREATE TABLE public."Notification" (
    notification_id integer NOT NULL,
    reader_id integer NOT NULL,
    manager_id integer NOT NULL,
    notification_record character varying(255) NOT NULL,
    notification_title character varying(255)
);
 "   DROP TABLE public."Notification";
       public         heap    postgres    false            �            1259    26622     Notification_notification_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Notification_notification_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public."Notification_notification_id_seq";
       public          postgres    false    226            =           0    0     Notification_notification_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE public."Notification_notification_id_seq" OWNED BY public."Notification".notification_id;
          public          postgres    false    227                        1259    26929    Preferences    TABLE     {   CREATE TABLE public."Preferences" (
    preferences_id integer NOT NULL,
    reader_id integer,
    category_id integer
);
 !   DROP TABLE public."Preferences";
       public         heap    postgres    false            �            1259    26928    Preferences_preferences_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Preferences_preferences_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public."Preferences_preferences_id_seq";
       public          postgres    false    256            >           0    0    Preferences_preferences_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public."Preferences_preferences_id_seq" OWNED BY public."Preferences".preferences_id;
          public          postgres    false    255            �            1259    26623    Rating_And_Review    TABLE     �   CREATE TABLE public."Rating_And_Review" (
    rating_and_review_id integer NOT NULL,
    book_id integer NOT NULL,
    reader_id integer NOT NULL,
    rating integer NOT NULL,
    review character varying(255) NOT NULL
);
 '   DROP TABLE public."Rating_And_Review";
       public         heap    postgres    false            �            1259    26626 *   Rating_And_Review_rating_and_review_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Rating_And_Review_rating_and_review_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 C   DROP SEQUENCE public."Rating_And_Review_rating_and_review_id_seq";
       public          postgres    false    228            ?           0    0 *   Rating_And_Review_rating_and_review_id_seq    SEQUENCE OWNED BY     }   ALTER SEQUENCE public."Rating_And_Review_rating_and_review_id_seq" OWNED BY public."Rating_And_Review".rating_and_review_id;
          public          postgres    false    229            �            1259    26627    Reader    TABLE     �   CREATE TABLE public."Reader" (
    reader_id integer NOT NULL,
    user_id integer NOT NULL,
    reader_rank character varying(255) NOT NULL,
    reader_point integer NOT NULL,
    is_first_time boolean NOT NULL
);
    DROP TABLE public."Reader";
       public         heap    postgres    false            �            1259    26630    Reader_reader_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Reader_reader_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public."Reader_reader_id_seq";
       public          postgres    false    230            @           0    0    Reader_reader_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public."Reader_reader_id_seq" OWNED BY public."Reader".reader_id;
          public          postgres    false    231            �            1259    26631    Search    TABLE     �   CREATE TABLE public."Search" (
    search_id integer NOT NULL,
    reader_id integer NOT NULL,
    search_record character varying(255) NOT NULL
);
    DROP TABLE public."Search";
       public         heap    postgres    false            �            1259    26634    Search_search_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Search_search_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public."Search_search_id_seq";
       public          postgres    false    232            A           0    0    Search_search_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public."Search_search_id_seq" OWNED BY public."Search".search_id;
          public          postgres    false    233                       1259    27083    Uploaded_Book    TABLE     �   CREATE TABLE public."Uploaded_Book" (
    uploaded_book_id integer NOT NULL,
    book_id integer NOT NULL,
    reader_id integer NOT NULL
);
 #   DROP TABLE public."Uploaded_Book";
       public         heap    postgres    false                       1259    27082 "   Uploaded_Book_uploaded_book_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Uploaded_Book_uploaded_book_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public."Uploaded_Book_uploaded_book_id_seq";
       public          postgres    false    264            B           0    0 "   Uploaded_Book_uploaded_book_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public."Uploaded_Book_uploaded_book_id_seq" OWNED BY public."Uploaded_Book".uploaded_book_id;
          public          postgres    false    263            �            1259    26635    User    TABLE     O  CREATE TABLE public."User" (
    user_id integer NOT NULL,
    user_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    user_password character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    is_admin boolean NOT NULL,
    last_login timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public."User";
       public         heap    postgres    false            �            1259    26640    User_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public."User_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."User_user_id_seq";
       public          postgres    false    234            C           0    0    User_user_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."User_user_id_seq" OWNED BY public."User".user_id;
          public          postgres    false    235                       1259    26957 	   Wish_List    TABLE     �   CREATE TABLE public."Wish_List" (
    wish_list_id integer NOT NULL,
    book_id integer NOT NULL,
    reader_id integer NOT NULL
);
    DROP TABLE public."Wish_List";
       public         heap    postgres    false                       1259    26956    Wish_List_wish_list_id_seq    SEQUENCE     �   CREATE SEQUENCE public."Wish_List_wish_list_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public."Wish_List_wish_list_id_seq";
       public          postgres    false    260            D           0    0    Wish_List_wish_list_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public."Wish_List_wish_list_id_seq" OWNED BY public."Wish_List".wish_list_id;
          public          postgres    false    259            �            1259    26763 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap    postgres    false            �            1259    26762    auth_group_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    243            �            1259    26771    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap    postgres    false            �            1259    26770    auth_group_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    245            �            1259    26757    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap    postgres    false            �            1259    26756    auth_permission_id_seq    SEQUENCE     �   ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    241            �            1259    26777 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap    postgres    false            �            1259    26785    auth_user_groups    TABLE     ~   CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap    postgres    false            �            1259    26784    auth_user_groups_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    249            �            1259    26776    auth_user_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    247            �            1259    26791    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap    postgres    false            �            1259    26790 !   auth_user_user_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    251            �            1259    26849    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap    postgres    false            �            1259    26848    django_admin_log_id_seq    SEQUENCE     �   ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    253            �            1259    26749    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap    postgres    false            �            1259    26748    django_content_type_id_seq    SEQUENCE     �   ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    239            �            1259    26741    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap    postgres    false            �            1259    26740    django_migrations_id_seq    SEQUENCE     �   ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    237            �            1259    26877    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap    postgres    false            �           2604    26979    Book book_id    DEFAULT     p   ALTER TABLE ONLY public."Book" ALTER COLUMN book_id SET DEFAULT nextval('public."Book_book_id_seq"'::regclass);
 =   ALTER TABLE public."Book" ALTER COLUMN book_id DROP DEFAULT;
       public          postgres    false    215    214            �           2604    27002 )   Book_Continue_Reading continue_reading_id    DEFAULT     �   ALTER TABLE ONLY public."Book_Continue_Reading" ALTER COLUMN continue_reading_id SET DEFAULT nextval('public."Book_Continue_Reading_continue_reading_id_seq"'::regclass);
 Z   ALTER TABLE public."Book_Continue_Reading" ALTER COLUMN continue_reading_id DROP DEFAULT;
       public          postgres    false    262    261    262            �           2604    26980    Category category_id    DEFAULT     �   ALTER TABLE ONLY public."Category" ALTER COLUMN category_id SET DEFAULT nextval('public."Category_category_id_seq"'::regclass);
 E   ALTER TABLE public."Category" ALTER COLUMN category_id DROP DEFAULT;
       public          postgres    false    257    258    258            �           2604    26981    Copy_Book copy_book_id    DEFAULT     �   ALTER TABLE ONLY public."Copy_Book" ALTER COLUMN copy_book_id SET DEFAULT nextval('public."Copy_Book_copy_book_id_seq"'::regclass);
 G   ALTER TABLE public."Copy_Book" ALTER COLUMN copy_book_id DROP DEFAULT;
       public          postgres    false    217    216            �           2604    26982    FeedBack feedback_id    DEFAULT     �   ALTER TABLE ONLY public."FeedBack" ALTER COLUMN feedback_id SET DEFAULT nextval('public."FeedBack_feedback_id_seq"'::regclass);
 E   ALTER TABLE public."FeedBack" ALTER COLUMN feedback_id DROP DEFAULT;
       public          postgres    false    219    218            �           2604    26983 *   Gamification_Record gamification_record_id    DEFAULT     �   ALTER TABLE ONLY public."Gamification_Record" ALTER COLUMN gamification_record_id SET DEFAULT nextval('public."Gamification_Record_gamification_record_id_seq"'::regclass);
 [   ALTER TABLE public."Gamification_Record" ALTER COLUMN gamification_record_id DROP DEFAULT;
       public          postgres    false    221    220            �           2604    26984    Manager manager_id    DEFAULT     |   ALTER TABLE ONLY public."Manager" ALTER COLUMN manager_id SET DEFAULT nextval('public."Manager_manager_id_seq"'::regclass);
 C   ALTER TABLE public."Manager" ALTER COLUMN manager_id DROP DEFAULT;
       public          postgres    false    223    222            �           2604    26985    Note note_id    DEFAULT     p   ALTER TABLE ONLY public."Note" ALTER COLUMN note_id SET DEFAULT nextval('public."Note_note_id_seq"'::regclass);
 =   ALTER TABLE public."Note" ALTER COLUMN note_id DROP DEFAULT;
       public          postgres    false    225    224            �           2604    26986    Notification notification_id    DEFAULT     �   ALTER TABLE ONLY public."Notification" ALTER COLUMN notification_id SET DEFAULT nextval('public."Notification_notification_id_seq"'::regclass);
 M   ALTER TABLE public."Notification" ALTER COLUMN notification_id DROP DEFAULT;
       public          postgres    false    227    226            �           2604    26987    Preferences preferences_id    DEFAULT     �   ALTER TABLE ONLY public."Preferences" ALTER COLUMN preferences_id SET DEFAULT nextval('public."Preferences_preferences_id_seq"'::regclass);
 K   ALTER TABLE public."Preferences" ALTER COLUMN preferences_id DROP DEFAULT;
       public          postgres    false    255    256    256            �           2604    26988 &   Rating_And_Review rating_and_review_id    DEFAULT     �   ALTER TABLE ONLY public."Rating_And_Review" ALTER COLUMN rating_and_review_id SET DEFAULT nextval('public."Rating_And_Review_rating_and_review_id_seq"'::regclass);
 W   ALTER TABLE public."Rating_And_Review" ALTER COLUMN rating_and_review_id DROP DEFAULT;
       public          postgres    false    229    228            �           2604    26989    Reader reader_id    DEFAULT     x   ALTER TABLE ONLY public."Reader" ALTER COLUMN reader_id SET DEFAULT nextval('public."Reader_reader_id_seq"'::regclass);
 A   ALTER TABLE public."Reader" ALTER COLUMN reader_id DROP DEFAULT;
       public          postgres    false    231    230            �           2604    26990    Search search_id    DEFAULT     x   ALTER TABLE ONLY public."Search" ALTER COLUMN search_id SET DEFAULT nextval('public."Search_search_id_seq"'::regclass);
 A   ALTER TABLE public."Search" ALTER COLUMN search_id DROP DEFAULT;
       public          postgres    false    233    232            �           2604    27086    Uploaded_Book uploaded_book_id    DEFAULT     �   ALTER TABLE ONLY public."Uploaded_Book" ALTER COLUMN uploaded_book_id SET DEFAULT nextval('public."Uploaded_Book_uploaded_book_id_seq"'::regclass);
 O   ALTER TABLE public."Uploaded_Book" ALTER COLUMN uploaded_book_id DROP DEFAULT;
       public          postgres    false    264    263    264            �           2604    26991    User user_id    DEFAULT     p   ALTER TABLE ONLY public."User" ALTER COLUMN user_id SET DEFAULT nextval('public."User_user_id_seq"'::regclass);
 =   ALTER TABLE public."User" ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    235    234            �           2604    26992    Wish_List wish_list_id    DEFAULT     �   ALTER TABLE ONLY public."Wish_List" ALTER COLUMN wish_list_id SET DEFAULT nextval('public."Wish_List_wish_list_id_seq"'::regclass);
 G   ALTER TABLE public."Wish_List" ALTER COLUMN wish_list_id DROP DEFAULT;
       public          postgres    false    260    259    260            �          0    26592    Book 
   TABLE DATA           �   COPY public."Book" (book_id, book_name, book_author, book_type, book_barcode, book_image, book_reading_counter, book_rating_avg, book_uploaded_date, book_favourite_counter, category_id, status, book_description, book_file) FROM stdin;
    public          postgres    false    214   !      ,          0    26999    Book_Continue_Reading 
   TABLE DATA           Z   COPY public."Book_Continue_Reading" (continue_reading_id, book_id, reader_id) FROM stdin;
    public          postgres    false    262   9-      (          0    26946    Category 
   TABLE DATA           @   COPY public."Category" (category_id, category_name) FROM stdin;
    public          postgres    false    258   w-      �          0    26598 	   Copy_Book 
   TABLE DATA           G   COPY public."Copy_Book" (copy_book_id, book_id, reader_id) FROM stdin;
    public          postgres    false    216   �-                 0    26602    FeedBack 
   TABLE DATA           a   COPY public."FeedBack" (feedback_id, reader_id, feedback_description, feedback_time) FROM stdin;
    public          postgres    false    218   .                0    26606    Gamification_Record 
   TABLE DATA           �   COPY public."Gamification_Record" (gamification_record_id, reader_id, gamification_description, achieved_point, date_and_time) FROM stdin;
    public          postgres    false    220   �/                0    26611    Manager 
   TABLE DATA           8   COPY public."Manager" (manager_id, user_id) FROM stdin;
    public          postgres    false    222   �2                0    26615    Note 
   TABLE DATA           D   COPY public."Note" (note_id, copy_book_id, note_record) FROM stdin;
    public          postgres    false    224   �2                0    26619    Notification 
   TABLE DATA           y   COPY public."Notification" (notification_id, reader_id, manager_id, notification_record, notification_title) FROM stdin;
    public          postgres    false    226   �2      &          0    26929    Preferences 
   TABLE DATA           O   COPY public."Preferences" (preferences_id, reader_id, category_id) FROM stdin;
    public          postgres    false    256   �4      
          0    26623    Rating_And_Review 
   TABLE DATA           g   COPY public."Rating_And_Review" (rating_and_review_id, book_id, reader_id, rating, review) FROM stdin;
    public          postgres    false    228   5                0    26627    Reader 
   TABLE DATA           `   COPY public."Reader" (reader_id, user_id, reader_rank, reader_point, is_first_time) FROM stdin;
    public          postgres    false    230   �5                0    26631    Search 
   TABLE DATA           G   COPY public."Search" (search_id, reader_id, search_record) FROM stdin;
    public          postgres    false    232    6      .          0    27083    Uploaded_Book 
   TABLE DATA           O   COPY public."Uploaded_Book" (uploaded_book_id, book_id, reader_id) FROM stdin;
    public          postgres    false    264   6                0    26635    User 
   TABLE DATA           k   COPY public."User" (user_id, user_name, email, user_password, is_active, is_admin, last_login) FROM stdin;
    public          postgres    false    234   I6      *          0    26957 	   Wish_List 
   TABLE DATA           G   COPY public."Wish_List" (wish_list_id, book_id, reader_id) FROM stdin;
    public          postgres    false    260   L8                0    26763 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          postgres    false    243   �8                0    26771    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          postgres    false    245   �8                0    26757    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          postgres    false    241   �8                0    26777 	   auth_user 
   TABLE DATA           �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public          postgres    false    247   ]<                0    26785    auth_user_groups 
   TABLE DATA           A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public          postgres    false    249   �=      !          0    26791    auth_user_user_permissions 
   TABLE DATA           P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public          postgres    false    251   �=      #          0    26849    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          postgres    false    253   >                0    26749    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          postgres    false    239   8?                0    26741    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          postgres    false    237   @@      $          0    26877    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          postgres    false    254   �C      E           0    0 -   Book_Continue_Reading_continue_reading_id_seq    SEQUENCE SET     ^   SELECT pg_catalog.setval('public."Book_Continue_Reading_continue_reading_id_seq"', 33, true);
          public          postgres    false    261            F           0    0    Book_book_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."Book_book_id_seq"', 72, true);
          public          postgres    false    215            G           0    0    Category_category_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."Category_category_id_seq"', 17, true);
          public          postgres    false    257            H           0    0    Copy_Book_copy_book_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public."Copy_Book_copy_book_id_seq"', 1, true);
          public          postgres    false    217            I           0    0    FeedBack_feedback_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."FeedBack_feedback_id_seq"', 36, true);
          public          postgres    false    219            J           0    0 .   Gamification_Record_gamification_record_id_seq    SEQUENCE SET     _   SELECT pg_catalog.setval('public."Gamification_Record_gamification_record_id_seq"', 69, true);
          public          postgres    false    221            K           0    0    Manager_manager_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public."Manager_manager_id_seq"', 2, true);
          public          postgres    false    223            L           0    0    Note_note_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public."Note_note_id_seq"', 1, true);
          public          postgres    false    225            M           0    0     Notification_notification_id_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('public."Notification_notification_id_seq"', 89, true);
          public          postgres    false    227            N           0    0    Preferences_preferences_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public."Preferences_preferences_id_seq"', 617, true);
          public          postgres    false    255            O           0    0 *   Rating_And_Review_rating_and_review_id_seq    SEQUENCE SET     [   SELECT pg_catalog.setval('public."Rating_And_Review_rating_and_review_id_seq"', 59, true);
          public          postgres    false    229            P           0    0    Reader_reader_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public."Reader_reader_id_seq"', 80, true);
          public          postgres    false    231            Q           0    0    Search_search_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."Search_search_id_seq"', 2, true);
          public          postgres    false    233            R           0    0 "   Uploaded_Book_uploaded_book_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public."Uploaded_Book_uploaded_book_id_seq"', 55, true);
          public          postgres    false    263            S           0    0    User_user_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public."User_user_id_seq"', 115, true);
          public          postgres    false    235            T           0    0    Wish_List_wish_list_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public."Wish_List_wish_list_id_seq"', 137, true);
          public          postgres    false    259            U           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public          postgres    false    242            V           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public          postgres    false    244            W           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 88, true);
          public          postgres    false    240            X           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
          public          postgres    false    248            Y           0    0    auth_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.auth_user_id_seq', 3, true);
          public          postgres    false    246            Z           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
          public          postgres    false    250            [           0    0    django_admin_log_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 9, true);
          public          postgres    false    252            \           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 23, true);
          public          postgres    false    238            ]           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 38, true);
          public          postgres    false    236            N           2606    27004 0   Book_Continue_Reading Book_Continue_Reading_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."Book_Continue_Reading"
    ADD CONSTRAINT "Book_Continue_Reading_pkey" PRIMARY KEY (continue_reading_id);
 ^   ALTER TABLE ONLY public."Book_Continue_Reading" DROP CONSTRAINT "Book_Continue_Reading_pkey";
       public            postgres    false    262            �           2606    26653    Book Book_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_pkey" PRIMARY KEY (book_id);
 <   ALTER TABLE ONLY public."Book" DROP CONSTRAINT "Book_pkey";
       public            postgres    false    214            J           2606    26951    Category Category_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public."Category"
    ADD CONSTRAINT "Category_pkey" PRIMARY KEY (category_id);
 D   ALTER TABLE ONLY public."Category" DROP CONSTRAINT "Category_pkey";
       public            postgres    false    258            �           2606    26655    Copy_Book Copy_Book_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public."Copy_Book"
    ADD CONSTRAINT "Copy_Book_pkey" PRIMARY KEY (copy_book_id);
 F   ALTER TABLE ONLY public."Copy_Book" DROP CONSTRAINT "Copy_Book_pkey";
       public            postgres    false    216                       2606    26657    FeedBack FeedBack_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public."FeedBack"
    ADD CONSTRAINT "FeedBack_pkey" PRIMARY KEY (feedback_id);
 D   ALTER TABLE ONLY public."FeedBack" DROP CONSTRAINT "FeedBack_pkey";
       public            postgres    false    218                       2606    26659 ,   Gamification_Record Gamification_Record_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."Gamification_Record"
    ADD CONSTRAINT "Gamification_Record_pkey" PRIMARY KEY (gamification_record_id);
 Z   ALTER TABLE ONLY public."Gamification_Record" DROP CONSTRAINT "Gamification_Record_pkey";
       public            postgres    false    220                       2606    26661    Manager Manager_manager_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY public."Manager"
    ADD CONSTRAINT "Manager_manager_id_key" UNIQUE (manager_id);
 L   ALTER TABLE ONLY public."Manager" DROP CONSTRAINT "Manager_manager_id_key";
       public            postgres    false    222                       2606    26663    Manager Manager_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public."Manager"
    ADD CONSTRAINT "Manager_pkey" PRIMARY KEY (manager_id, user_id);
 B   ALTER TABLE ONLY public."Manager" DROP CONSTRAINT "Manager_pkey";
       public            postgres    false    222    222            	           2606    26665    Note Note_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."Note"
    ADD CONSTRAINT "Note_pkey" PRIMARY KEY (note_id);
 <   ALTER TABLE ONLY public."Note" DROP CONSTRAINT "Note_pkey";
       public            postgres    false    224                       2606    26667    Notification Notification_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public."Notification"
    ADD CONSTRAINT "Notification_pkey" PRIMARY KEY (notification_id);
 L   ALTER TABLE ONLY public."Notification" DROP CONSTRAINT "Notification_pkey";
       public            postgres    false    226            H           2606    26934    Preferences Preferences_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public."Preferences"
    ADD CONSTRAINT "Preferences_pkey" PRIMARY KEY (preferences_id);
 J   ALTER TABLE ONLY public."Preferences" DROP CONSTRAINT "Preferences_pkey";
       public            postgres    false    256                       2606    26669 (   Rating_And_Review Rating_And_Review_pkey 
   CONSTRAINT     |   ALTER TABLE ONLY public."Rating_And_Review"
    ADD CONSTRAINT "Rating_And_Review_pkey" PRIMARY KEY (rating_and_review_id);
 V   ALTER TABLE ONLY public."Rating_And_Review" DROP CONSTRAINT "Rating_And_Review_pkey";
       public            postgres    false    228                       2606    26671    Reader Reader_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public."Reader"
    ADD CONSTRAINT "Reader_pkey" PRIMARY KEY (reader_id, user_id);
 @   ALTER TABLE ONLY public."Reader" DROP CONSTRAINT "Reader_pkey";
       public            postgres    false    230    230                       2606    26673    Reader Reader_reader_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY public."Reader"
    ADD CONSTRAINT "Reader_reader_id_key" UNIQUE (reader_id);
 I   ALTER TABLE ONLY public."Reader" DROP CONSTRAINT "Reader_reader_id_key";
       public            postgres    false    230                       2606    26675    Search Search_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public."Search"
    ADD CONSTRAINT "Search_pkey" PRIMARY KEY (search_id);
 @   ALTER TABLE ONLY public."Search" DROP CONSTRAINT "Search_pkey";
       public            postgres    false    232            P           2606    27088     Uploaded_Book Uploaded_Book_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public."Uploaded_Book"
    ADD CONSTRAINT "Uploaded_Book_pkey" PRIMARY KEY (uploaded_book_id);
 N   ALTER TABLE ONLY public."Uploaded_Book" DROP CONSTRAINT "Uploaded_Book_pkey";
       public            postgres    false    264                       2606    26677    User User_email_key 
   CONSTRAINT     S   ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_email_key" UNIQUE (email);
 A   ALTER TABLE ONLY public."User" DROP CONSTRAINT "User_email_key";
       public            postgres    false    234                       2606    26679    User User_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);
 <   ALTER TABLE ONLY public."User" DROP CONSTRAINT "User_pkey";
       public            postgres    false    234            L           2606    26962    Wish_List Wish_List_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public."Wish_List"
    ADD CONSTRAINT "Wish_List_pkey" PRIMARY KEY (wish_list_id);
 F   ALTER TABLE ONLY public."Wish_List" DROP CONSTRAINT "Wish_List_pkey";
       public            postgres    false    260            %           2606    26875    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            postgres    false    243            *           2606    26806 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            postgres    false    245    245            -           2606    26775 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            postgres    false    245            '           2606    26767    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            postgres    false    243                        2606    26797 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            postgres    false    241    241            "           2606    26761 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            postgres    false    241            5           2606    26789 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public            postgres    false    249            8           2606    26821 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public            postgres    false    249    249            /           2606    26781    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public            postgres    false    247            ;           2606    26795 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public            postgres    false    251            >           2606    26835 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public            postgres    false    251    251            2           2606    26870     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public            postgres    false    247            A           2606    26856 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            postgres    false    253                       2606    26755 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            postgres    false    239    239                       2606    26753 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            postgres    false    239                       2606    26747 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            postgres    false    237            E           2606    26883 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public            postgres    false    254            #           1259    26876    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            postgres    false    243            (           1259    26817 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            postgres    false    245            +           1259    26818 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            postgres    false    245                       1259    26803 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            postgres    false    241            3           1259    26833 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public            postgres    false    249            6           1259    26832 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public            postgres    false    249            9           1259    26847 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public            postgres    false    251            <           1259    26846 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public            postgres    false    251            0           1259    26871     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public            postgres    false    247            ?           1259    26867 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            postgres    false    253            B           1259    26868 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            postgres    false    253            C           1259    26885 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public            postgres    false    254            F           1259    26884 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public            postgres    false    254            j           2606    27005 8   Book_Continue_Reading Book_Continue_Reading_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Book_Continue_Reading"
    ADD CONSTRAINT "Book_Continue_Reading_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(book_id) ON UPDATE CASCADE ON DELETE CASCADE;
 f   ALTER TABLE ONLY public."Book_Continue_Reading" DROP CONSTRAINT "Book_Continue_Reading_book_id_fkey";
       public          postgres    false    3325    262    214            k           2606    27010 :   Book_Continue_Reading Book_Continue_Reading_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Book_Continue_Reading"
    ADD CONSTRAINT "Book_Continue_Reading_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 h   ALTER TABLE ONLY public."Book_Continue_Reading" DROP CONSTRAINT "Book_Continue_Reading_reader_id_fkey";
       public          postgres    false    3345    230    262            Q           2606    26993    Book Book_category_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Book"
    ADD CONSTRAINT "Book_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public."Category"(category_id) ON UPDATE CASCADE ON DELETE CASCADE;
 H   ALTER TABLE ONLY public."Book" DROP CONSTRAINT "Book_category_id_fkey";
       public          postgres    false    258    3402    214            R           2606    26680     Copy_Book Copy_Book_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Copy_Book"
    ADD CONSTRAINT "Copy_Book_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(book_id) ON UPDATE CASCADE ON DELETE CASCADE;
 N   ALTER TABLE ONLY public."Copy_Book" DROP CONSTRAINT "Copy_Book_book_id_fkey";
       public          postgres    false    214    216    3325            S           2606    26685 "   Copy_Book Copy_Book_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Copy_Book"
    ADD CONSTRAINT "Copy_Book_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 P   ALTER TABLE ONLY public."Copy_Book" DROP CONSTRAINT "Copy_Book_reader_id_fkey";
       public          postgres    false    230    216    3345            T           2606    26690     FeedBack FeedBack_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."FeedBack"
    ADD CONSTRAINT "FeedBack_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 N   ALTER TABLE ONLY public."FeedBack" DROP CONSTRAINT "FeedBack_reader_id_fkey";
       public          postgres    false    230    3345    218            U           2606    26695 6   Gamification_Record Gamification_Record_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Gamification_Record"
    ADD CONSTRAINT "Gamification_Record_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 d   ALTER TABLE ONLY public."Gamification_Record" DROP CONSTRAINT "Gamification_Record_reader_id_fkey";
       public          postgres    false    3345    220    230            V           2606    26700    Manager Manager_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Manager"
    ADD CONSTRAINT "Manager_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 J   ALTER TABLE ONLY public."Manager" DROP CONSTRAINT "Manager_user_id_fkey";
       public          postgres    false    234    3351    222            W           2606    26705    Note Note_copy_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Note"
    ADD CONSTRAINT "Note_copy_book_id_fkey" FOREIGN KEY (copy_book_id) REFERENCES public."Copy_Book"(copy_book_id) ON UPDATE CASCADE ON DELETE CASCADE;
 I   ALTER TABLE ONLY public."Note" DROP CONSTRAINT "Note_copy_book_id_fkey";
       public          postgres    false    216    224    3327            X           2606    26710 )   Notification Notification_manager_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Notification"
    ADD CONSTRAINT "Notification_manager_id_fkey" FOREIGN KEY (manager_id) REFERENCES public."Manager"(manager_id) ON UPDATE CASCADE ON DELETE CASCADE;
 W   ALTER TABLE ONLY public."Notification" DROP CONSTRAINT "Notification_manager_id_fkey";
       public          postgres    false    222    226    3333            Y           2606    26715 (   Notification Notification_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Notification"
    ADD CONSTRAINT "Notification_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 V   ALTER TABLE ONLY public."Notification" DROP CONSTRAINT "Notification_reader_id_fkey";
       public          postgres    false    3345    230    226            g           2606    26935 &   Preferences Preferences_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Preferences"
    ADD CONSTRAINT "Preferences_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public."Preferences" DROP CONSTRAINT "Preferences_reader_id_fkey";
       public          postgres    false    230    256    3345            Z           2606    26720 0   Rating_And_Review Rating_And_Review_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Rating_And_Review"
    ADD CONSTRAINT "Rating_And_Review_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(book_id) ON UPDATE CASCADE ON DELETE CASCADE;
 ^   ALTER TABLE ONLY public."Rating_And_Review" DROP CONSTRAINT "Rating_And_Review_book_id_fkey";
       public          postgres    false    228    214    3325            [           2606    26725 2   Rating_And_Review Rating_And_Review_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Rating_And_Review"
    ADD CONSTRAINT "Rating_And_Review_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 `   ALTER TABLE ONLY public."Rating_And_Review" DROP CONSTRAINT "Rating_And_Review_reader_id_fkey";
       public          postgres    false    230    3345    228            \           2606    26730    Reader Reader_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Reader"
    ADD CONSTRAINT "Reader_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 H   ALTER TABLE ONLY public."Reader" DROP CONSTRAINT "Reader_user_id_fkey";
       public          postgres    false    230    234    3351            ]           2606    26735    Search Search_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Search"
    ADD CONSTRAINT "Search_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 J   ALTER TABLE ONLY public."Search" DROP CONSTRAINT "Search_reader_id_fkey";
       public          postgres    false    232    230    3345            l           2606    27089 (   Uploaded_Book Uploaded_Book_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Uploaded_Book"
    ADD CONSTRAINT "Uploaded_Book_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(book_id) ON UPDATE CASCADE ON DELETE CASCADE;
 V   ALTER TABLE ONLY public."Uploaded_Book" DROP CONSTRAINT "Uploaded_Book_book_id_fkey";
       public          postgres    false    264    214    3325            m           2606    27094 *   Uploaded_Book Uploaded_Book_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Uploaded_Book"
    ADD CONSTRAINT "Uploaded_Book_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 X   ALTER TABLE ONLY public."Uploaded_Book" DROP CONSTRAINT "Uploaded_Book_reader_id_fkey";
       public          postgres    false    3345    264    230            h           2606    26963     Wish_List Wish_List_book_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Wish_List"
    ADD CONSTRAINT "Wish_List_book_id_fkey" FOREIGN KEY (book_id) REFERENCES public."Book"(book_id) ON UPDATE CASCADE ON DELETE CASCADE;
 N   ALTER TABLE ONLY public."Wish_List" DROP CONSTRAINT "Wish_List_book_id_fkey";
       public          postgres    false    3325    260    214            i           2606    26968 "   Wish_List Wish_List_reader_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Wish_List"
    ADD CONSTRAINT "Wish_List_reader_id_fkey" FOREIGN KEY (reader_id) REFERENCES public."Reader"(reader_id) ON UPDATE CASCADE ON DELETE CASCADE;
 P   ALTER TABLE ONLY public."Wish_List" DROP CONSTRAINT "Wish_List_reader_id_fkey";
       public          postgres    false    3345    260    230            _           2606    26812 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          postgres    false    245    3362    241            `           2606    26807 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          postgres    false    245    243    3367            ^           2606    26798 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          postgres    false    3357    239    241            a           2606    26827 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public          postgres    false    243    3367    249            b           2606    26822 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public          postgres    false    249    247    3375            c           2606    26841 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public          postgres    false    241    3362    251            d           2606    26836 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public          postgres    false    3375    251    247            e           2606    26857 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          postgres    false    239    253    3357            f           2606    26862 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public          postgres    false    3375    253    247            �   '  x��X�r�8}f���yXI���o�-;N<����T�j"!c����i>b_���K�t��(U���qY���>}�4z�h�~&/OB,�^f��H|h=�_>���[�{��Q�[�-�yu?�\+�s��/����XGݨu��A��ivz�۹귯ڃְ۟�;�hw�~4��q�
��h�Z�ĳ��N��>Ub�mU�|�ke��pս���|�p����N�U336qB�tI[��,s¬��&W�֣���^f��H�٨Dx#�z�b�Ҿ�&�v"�>�0I���j�A�	-�	�ܥ�*�1OebvNdZ��i���-3~h#�iC�o�4�ѭ��KK����v̞��9�<�,��wUFW:	��"Y�u�V'ڛҩU4���cu�4�6~���H����UwԚ�'�1#���g���	Nn
D#Q.���ڜ�2�|�M�l��k��~/n���o2��]5�{�o鷽;��N�����^u���&�A��F�:t/]K��-Q��_)�.D����+`'�����Lo)�Rdd�6D���0��B9b-r]�M�J��(�����ń��Wh�o��R��'��\j��@w�f�_�ׅ��oVk�(3I�w��S;�SQ(�M�c���L���%�K�BK��Q!�1~����J�*�`�
��*W��7�-)c�\;%�V���Y�)mH �2CT[�޳�&e�u��]�:Q5�l��$ǋ��\�"/�մ[�:��b�Ǧ[�h��6����w�9��[��Y��y�w��p����.h�x���n�?&l��3l՜``���bKD`Ҭ>`A�!���R��ҧ�B)� �E�%~-��v�b2�;�F�e�7np���g� ��9Ѝ\�i!�+�4*�j��F�>d�[�s��]*viU�+H�q?���Jx��m9_܎�Y$�I�dw@��� �إ{���؝!>Q�>^�P�^a�.�s�"��`#����?�Zy��:a��OC0�.��x�e��bJ&����Jn���U��-�rzx'���\��j�Bq���������2".Qx%[��s�3 >sZn��Pe��2��]*Ax� _C�\	X��\�P��8�}z����<{�.f7��秛^/��}�h�9�e�6�}:�%�&���wd�G�w|,���qA���ՠ��G��ʣuڧ��5&�-?+����5����=?D���:���P�l�@
Ld��dR&[*�1k��u�%Ƶ���df���&�j��T���0����TɚZ�Ve�8_ ����>���ؒ�,���>�ȉ{����!.3ԍ݇m���@�j��g�	�M%E��Li� {�ʊ| ̻�1*(���ӧHж�h/g=ʕ~�hAD�1ç��Jud�c��a�� t�#u\C*D���i%V"�������~.���Ǩ���`ո�}!:W���`��&�a'Ȁ�9U�'��	�b�I&5��xh�@�>����ּ~�����b�d��"oLˠ�⊑P�
ƈJU�. E��%�A���pY���3�C�ԪU�~��.@v�N���O���F��ے@�XQ�o ߝY�v�c1�T}ė�Z�~$�
��9F��ذ��箃�DǺ�*��՘�IEs��n%�S%ѳ2�+ФS���A���!J.��XgѺzUfx|`�sO*�t:LhWd��(W �M[C���A��/��`=�l>{����w��Y���9�!7rԸ�/�ϱ=�.����v�5���g{2De+����X[�EQ���h��_s4�hm_C<��11k-u Ճ�ㆧB�%�ьA> ���J�.Y����� WVX_�"	e^�O�׸�T<���:���Ϥ/U5U��o��0��! C�>�f*�:3����5j�m*+�X��0^d~x�|����x�_�/������G1��}�ޕN�G8���Zۏ6�~��������&�0�a:�`�^xxI�����ßא���)�,���}P��,퉕���S���mG�T��a����(@K�%���kTԺ,�H��l0�㋬3LI"p����X�i!(�o�Zo�_���c+�2�啠FvP�*�[t��w&C���ƙz2�96���@�),1%�$�ʾ �)��Y��di�p�b�.$+(J�*Mx�'3�M���8�	ta<t�L�z(�a^:�,�t�l���Ј_���g���a6��s��<<�&H{g \��7�Y�=�t&� ��W�0�`���X|)�4gzq�Ra��G�s<�sh -uf�:r�7 T�C��jM#�N�d��N�m���+pº�A�-��z��6n�'M��������X&�ꎂ��30�4�4�*{�b�O_H��!l)����3f����5���Rz���VY��aT��?h+C�_f���@>8��-�@��3�g���C�"��i�@C�s��-���jq��k&�6�S/=D;�4'�^`�W�^��~��.�w�}t���A�j�e����_���4K%�e����d��r|���Mp�P��ѽ�:�OQ򇳼g#9�1�\`���_�7;>�h����k�EZ-7pc����d�}����[b���FLDFm쑚7KƁ@�7R��xW+HB*��(
�0L?Jky&��u�*���*g�po���Jna7���	� ͤ�.5ـ|�2���W����B�B7�'嫚y
��p͋���^u���r1���c�o$Ť�*���A�(��Ms��ި1���/�JW�Qk�wǃ�r�Q�vTz~FZ��6���Ãx������&��������)�"�C�-��YY�/�I�W�vk4w�P�󲸦�j�y�Cヌ�|=O���!��]�%�f��L�k@"�
��rt6H�Kyj�$t$���� �
����P����+���G`-�1���x.!���Br�C�{�v�}v��3�Lȅb��@љ)��gؼ:�!5�eO^��{�˧��O��`�T�Ѓ+е���)4���U�'�J����.���с��bx�t�AV��A;�Db����ye�O���z���� #��      ,   .   x�32�46�4��22�463�9�-Ac#Ns 2�A�H� �]m      (   t   x��=�0���)zD�g�F�Z"��Q�V��AOz+�+k�)�&���'鱥V��/���M�u,�=�X+���jeƑ����%]���Gt=��7�]sM�6��x, |�(%      �      x������ � �          �  x�m��N�0�����,���γp3�����!��$+k��o*U��߉A���q3&�aGyd��
��R�u�S,���R19<{ wp��������0+!])TY�Y�\[�2F����]I�������G�J���I�i�	���RU#i�# _)�5�[��lP�)�=K��&r�$���|��p�M2Xe�*(�'�����V�#�ā�o�3
�[F��ؗ�x�oyxLזZn��pUSI��@�+�G�w�ͣ��%�.䊓�����L��EM����@��Dn����6�t��7eVط�kƠQ�8� ��銴K��NFp�\���9��C����8>��������c�:���q�<=����,I.�h�pC?M��N         �  x����NAE�㯘=�U�~툢| Qv�<!`G�����R0�I�K�[�U�oZ��k@HN�7T�J0	d9Zq�/�Z;�H�����10���xi��kkЧ�`����ݼ�l�8���FV, #�	�*6xz�$G�����QZ���x{~�N^��DnW�����s8l=?�z�s��7����j�{���r#Q�P��Z9��;L!*�v�#��M��Bj��9D�J	�PJ��5���>t��U�� �GQ��u��T���Q��+%�ԋ��W�P ��#�(�]�\b�J�G�-�*b(DT|c����f�ތ��������vz�n����-�<� ���f���<~�/U%�$����l��L��b}y=����>��O�Ϥ����ަ"!�0�K�b)��ټ
���$˥�0�%`ߕ.��f"J���K����vw5��6������x۟)��\!�������Jv{���/��J��X^s���Y�zN�z�R�c0�!<W0��]�S�p�8�S@��
 d?:/��A
-%u��"���|l�Jѥ9ץЮfl�=�y6�
���T��F1Ve{��d���lm�a#D0Ċ8��UԽ���KJR:��N����*���8�Z���[h����y�M8Q
Ȅ�Ɗ2��k�fk�Q��R#�^\�ѱ'o/�����W16�wzǥmނ%i��ym!��Ӎ��l�+�M�*���l�t�}s���o�{X�V	㬊            x�3������� �&            x������ � �         �  x��V�n�0<�W��C�(~�9��z��*Qo�p�aG�$��7-NC�X��3�^3�:Kx���,�U$S�T�S5�خ��O7O֮R1���x�ޭ6}�=K�>���k����3�Z��F�
�y�ϛJ��ML��j�O̟$!	���]��b��D2�*�u7��ڏ�j���8 ��+,	�-�{d���ar��p��8�%1)��j�u����`֡�_�V��C��#�#@��ǁ��ˁ<���A��	���-ڝ���md�^u�ֺlds��)n�jۚ�6J��H뤩eS��tE�5�vښvr<={��k�´���RG��@ڗyQ�.e��}�[�6�Ѣ�XD-Q+<ah>\B� �Hl���,�iYDӲ��e��ˀ-�[na9p�	��g�X0�5��
G&�db������l`���i���{      &   b   x�̻D!���?������&���Y���k34��)8(�.xB��H_�K�W� � )$(�@���o+?�ٗ_PB�<��¾����o!      
   x   x�M�K1C��)zD�һ�)b�E��h!Ì7��,G���*)�MP����3T�15���/$����K%�o	Z�{v�LF'3,o��~"�+Ǹ��̅��.���{��_q> � �</         T   x�33�4�t��I�4640�,�0�444�t*�ϫJ����-��&�A��ٙ@A3�4.SKNS�V��P��1LH$F��� Z��            x������ � �      .      x�35�47�4��25�471b���� +Ue         �  x�u�Ɏ�@���s�m4���`@������V�Q�Ø�����8)�'U�RU]��~�!A����H�C�\a����ٓbq;��ࠌ�n�pÕ-n��/%D���2���L{K���=A(ߋ���$'L�'ڒ6-�����9I��/��h^���P��z�{�Ƈx}^�h�Q��n�DC�6�_S�6' l�}�� f��P&����#�8�s�ų��T�&�mo�	��bd{����^%�n5�ܕ?�N1����<�ǐ}kI�MH�?�càfPj'kS�V������e��+������پZY!pY/��)��Q�	q2/�X�����<ӆ���?���D����BG��[t�:[�<���5�Cg;�G�2K�؅�V�sM�T���jlf��V��9�B`Φ�����o=H��A��Y�g.偆ѧ#�����'3�[yu�[#��Uc�%��v����4z�w����q�g�Ic=x�d�<��C�g �e�9ؤ      *   D   x�%̱�0��)ƣ׃�zq�u�l�#'�m���
([ڭ���9�l�V]ޫZTˣ<�����[�            x������ � �            x������ � �         s  x�u�ђ�0E����tCy�ot&Co�i2�mg���%[���a�_�������]��n�u����m*Ƨ0NC�r��ǫ���x�7�@��l�w�� �틲��?�e�Ѹ$M&l����{���e���D"�I��E�u���Nӳ�޴�g]�TZSFX#N�d ��p]|-~6Mm���9���׫3�����NKS�PV>O�#����}�f��T��U���`�Q�Z�O��Md��$ت�^<�j���:�waXg���cyS�.PRU�=��Qvе�<���f����[��Q����}	�.�M[C����Tp�XC�T$�ȀT��i�c�u���lk(�fD@g�%�
9���U��?�u����ylk�a��.$V�"s�f��u�8*�BU�g���c�����C�i�x��5:L��`n��4��*�T��a+�s��H�ql�i�X��P݀�HAU��$
����sx�_<��<O��Tt|B�Bv�����|�?{��/^���g/�7��t��%��>���VtR����g
�o*�Mq,�p�s�J
#���7������q9�b� �e�e$�U��$���^��2n6VQ�l�Vj U*�^��Q�2P|V�h�!����~<��Tt��)�b��p�4���WҼ�~I���	�1^O�~��������P�P��2z����m6�Rϳ������\�̶������ø7�6���s��f�(p�P�� J�Mn5������mX��E'���v��*A�����vʈ &}��#㍒��a���"�[�\ir�C���LW����ؗoP�����/�K��V���6�Έ�!Gwh�L�m����]"�`��N�}#���q�@���������)         ^  x����n�P���]�#�8$&MQ�U)��Ԙ4ܽ`��|��ִI뢝�,&��bv�&��K��0�9U��8s�:�aSw]��TN��� W���t��ݨ��ii��tGh0��&�y�a�IVz�Y�Y�L��پ�b��4�WD�(�&[o�
A�mF*�Z�@�AT%� AT	A
�������T��H�*���CY)7)B[�Ӫ�Qt"��a�4����0�P��ڬF;��Ώ`I֐$
@P�E����D4	Q�ɻ�x]����D1&����:�{�qQp#{�ʩ=�9��e�v���y̢���1_]�a��~K�&��5E%�/�?*|n��������e�76 ��            x������ � �      !      x������ � �      #   #  x���=o�0Eg�WX��Z,��%�u�:Q�@BK?�D�	���$j����<����|A�E�́4p�,Xg	<�[T�^�j���G�n�����R�
�E
��q ��.
걮?OQ裇t�^�ު2��n��W���"}n���I���R��x�����ux��J<O�.N����xw��]�u]V郞�ܹ� B<�y��u~�#k8�{]6�e7��\'�N0w�/ӏu�ʿ�Nx6��S4���װ���,�/
���*W��S���X��H�F}jtQ~owð���$I��J�"         �   x�eQ[n� �Ƈ�
�j�R)r�!�	 Cv�ۗ$�Ua����R���S��3��.y�xv)���t ���|K"�����"�k�����H�����mGٴK�D������Lh
�]�{����>�_��5f�����!B\�Cr������q�	��\�XLwL:�y�{f�h7s��!�����<2��5%���\$�v�M�qw� Մ�Y���8.��K�zo�&��2/�A5�,q
�7̞�� ����         �  x����n�:E�ӯ��A���[ h7Ʒ�3�����v�dZ p��\�6�)��صS�N�G_���І)�������`K��)�e��������������OMh�b�<��-]ݝ)���UӽW���?��2$cedȍ�7�9�B׺�ڟ��GR�>K1�#Ker�5����7�}X"���:_O���jh�8Ɣb�k�WW홞��B�I$����4�t��/!\p��iW��S�%e���um!�le�=��������_s),�����H�_sVu��.jv"�d��`kO}I�����nS�a��T��Ϗ�NeGH8���]u��YY#�� V��4�Jk���:��cإjjŀ�{��r�����5�}�Ջ/`�f���^���mYec�9��e�/G�bZ�E{H-���%ӅQhѤ�c㇩?����P�R�� ��R(d��~t�Ow$�]1I���ݗo鉮�X����5��iV /єB4-.����H��P� �.��J�U�3��!bz��1��d�a���y���Xq�(�&�0?E�?�p�)�*�1�-��G�8s_w��ɥ�̵"&�ܨ0�mRe�� �d_����R�|��Xɰ�� ��.���:f���n�T]�t���V�qZ��QB�,��l�3�i)���m$�w�����\-��uh~�kݥm�5Wn��sz���(���Z�d^�9���B���W��������鵀\ɼGS��,��)c�B@#�/񙝀_��=ƍ�����~"���6�g.���N�xB�:n@�f́��^<s��p_��D%��q������@�#HhA�@��4�1�37��g�ab��Kc��y�0�"�����c
�g��F�S��QE��b�`�9�����-����Ҏ�q���y�����PD<J      $   o  x�}�Ɏ�8������}+�ml�2@ ����"�!	f��&�R��E�;x���!�#?i��LXX= mC����-z�l���5�-�S�)�&��?Rʽ�Ќ��`�)6�ct6����l�SE�$����˖�~x��*ϙ�}<*&�6��~�Xw/U�s6q�}͏ԑjR�Ooʫ*�'�6�ފ�=��h�,#�|A5͍��p�,WE�juo=�5�n$X��#K����p����D�O�j%�0;V9�n��jyemo�B ��#?�(a^�xLDH��'EUW;����ޝ�MϜ0f�2���:N�
)��4
[�`�ߞ&��W#��d��%YL֭��Am)E�+-ԓ�����G
��,��G^�s�k��(�اN��:vvl�˙�шuC����y�-�t}���m~zAvk	�x˫:�Lw�p-�N����ONf��Z���~��n>���U��<77�
��Dh��	�D�Pi,BD�P%�,�+l�ݨ}�~\$|�s����u��:��F�����7���7Ү7��N�tŽ`V�fl��PF�۰E�ݟ�35���2é��T� hA�o�-���w�=��Q�c�bq,G#�Op�3�D�`�m�2U���1"��@Su��ʢ}f%S��Rc�{�!�A	��ɘG���8'��1�"��Q��P��a<B���gS���
tٗ���잦�T�H���:�$N�͑�ȱ=�2\}"N �����vn�Ʃ��s��Z�üo�uC?C�%gvgs1^��ZM
j�84�ȮO�T��qfķ\=M�� �$DƄ�~�QJ"؅û���9Eͳ��W����^��M�Q��BE�����f���~Z�u����0���wD>�0�8q<���$-� !�+�`r�nh�ny�����3$�Ξ�*�Z��z�K5�)�v�/���"_	��}>�ݸ�>ᐃ?�a#ߧ���(J�.]��ۈ�������j�gHD�Hr�����z�����&�;�:�  ���JD��5�p7�n����a#7�h��}A��s��e�o ��$e�\�q�Uy��D�/��7^ݞ��(�UW�����eG���lxK��5�F��B ��/	��<�o��㏏� ?�
�     