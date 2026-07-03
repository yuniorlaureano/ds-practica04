
IF OBJECT_ID('dbo.assess_detail', 'U') IS NOT NULL DROP TABLE dbo.assess_detail;
IF OBJECT_ID('dbo.vle_click_stream', 'U') IS NOT NULL DROP TABLE dbo.vle_click_stream;
IF OBJECT_ID('dbo.registrations', 'U') IS NOT NULL DROP TABLE dbo.registrations;
IF OBJECT_ID('dbo.assess_plan', 'U') IS NOT NULL DROP TABLE dbo.assess_plan;
IF OBJECT_ID('dbo.student_info', 'U') IS NOT NULL DROP TABLE dbo.student_info;
IF OBJECT_ID('dbo.vle_modules', 'U') IS NOT NULL DROP TABLE dbo.vle_modules;
IF OBJECT_ID('dbo.cursos', 'U') IS NOT NULL DROP TABLE dbo.cursos;
GO

CREATE TABLE dbo.cursos (
    code_module                 VARCHAR(10)  NOT NULL,
    code_presentation           VARCHAR(10)  NOT NULL,
    module_presentation_length  SMALLINT     NOT NULL,
    CONSTRAINT PK_cursos PRIMARY KEY (code_module, code_presentation)
);
GO

/* ------------------------------------------------------------
   vle_modules.csv - VLE sites/activities offered per course
   ------------------------------------------------------------ */
CREATE TABLE dbo.vle_modules (
    guid_site_id        UNIQUEIDENTIFIER NOT NULL,
    code_module         VARCHAR(10)      NOT NULL,
    code_presentation    VARCHAR(10)      NOT NULL,
    activity_type       VARCHAR(20)      NULL,
    week_from           TINYINT          NULL,
    week_to             TINYINT          NULL,
    CONSTRAINT PK_vle_modules PRIMARY KEY (guid_site_id, code_module, code_presentation),
    CONSTRAINT FK_vle_modules_cursos FOREIGN KEY (code_module, code_presentation)
        REFERENCES dbo.cursos (code_module, code_presentation)
);
GO

/* ------------------------------------------------------------
   assess_plan.csv - assessments defined per course
   ------------------------------------------------------------ */
CREATE TABLE dbo.assess_plan (
    code_module         VARCHAR(10)      NOT NULL,
    code_presentation   VARCHAR(10)      NOT NULL,
    guid_assess_id      UNIQUEIDENTIFIER NOT NULL,
    assessment_type     VARCHAR(10)      NULL,
    days                SMALLINT         NULL,
    weight              TINYINT          NULL,
    CONSTRAINT PK_assess_plan PRIMARY KEY (guid_assess_id),
    CONSTRAINT FK_assess_plan_cursos FOREIGN KEY (code_module, code_presentation)
        REFERENCES dbo.cursos (code_module, code_presentation)
);
GO

/* ------------------------------------------------------------
   student_info.csv - one row per student per course enrollment
   ------------------------------------------------------------ */
CREATE TABLE dbo.student_info (
    code_module            VARCHAR(10)      NOT NULL,
    code_presentation      VARCHAR(10)      NOT NULL,
    guid_student_id         UNIQUEIDENTIFIER NOT NULL,
    gender                  CHAR(1)          NULL,
    region                  VARCHAR(30)      NULL,
    highest_education       VARCHAR(40)      NULL,
    imd_band                VARCHAR(10)      NULL,
    age_band                VARCHAR(10)      NULL,
    num_of_prev_attempts    TINYINT          NULL,
    studied_credits         SMALLINT         NULL,
    disability              CHAR(1)          NULL,
    final_result            VARCHAR(20)      NULL,
    CONSTRAINT PK_student_info PRIMARY KEY (code_module, code_presentation, guid_student_id),
    CONSTRAINT UQ_student_info_guid UNIQUE (guid_student_id),
    CONSTRAINT FK_student_info_cursos FOREIGN KEY (code_module, code_presentation)
        REFERENCES dbo.cursos (code_module, code_presentation)
);
GO

/* ------------------------------------------------------------
   registrations.csv - registration/unregistration day offsets
   ------------------------------------------------------------ */
CREATE TABLE dbo.registrations (
    guid_studente_id      UNIQUEIDENTIFIER NOT NULL,
    code_module           VARCHAR(10)      NOT NULL,
    code_presentation     VARCHAR(10)      NOT NULL,
    date_registration     SMALLINT         NULL,
    date_unregistration   SMALLINT         NULL,
    CONSTRAINT PK_registrations PRIMARY KEY (guid_studente_id, code_module, code_presentation),
    CONSTRAINT FK_registrations_cursos FOREIGN KEY (code_module, code_presentation)
        REFERENCES dbo.cursos (code_module, code_presentation),
    CONSTRAINT FK_registrations_student FOREIGN KEY (guid_studente_id)
        REFERENCES dbo.student_info (guid_student_id)
);
GO

/* ------------------------------------------------------------
   vle_click_stream.csv - clickstream fact table (VLE interactions)
   No natural key in the source file, so a surrogate id is added.
   ------------------------------------------------------------ */
CREATE TABLE dbo.vle_click_stream (
    id                BIGINT IDENTITY(1,1) NOT NULL,
    guid_student_id   UNIQUEIDENTIFIER NOT NULL,
    guid_site_id      UNIQUEIDENTIFIER NOT NULL,
    [date]            SMALLINT         NULL,
    sum_clics         SMALLINT         NULL,
    type_assign       VARCHAR(20)      NULL,
    week_from         DATE             NULL,
    weel_to           DATE             NULL,
    disability        CHAR(1)          NULL,
    modulo            VARCHAR(10)      NULL,
    week1             TINYINT          NULL,
    week2             TINYINT          NULL,
    days              SMALLINT         NULL,
    presentation      VARCHAR(10)      NULL,
    CONSTRAINT PK_vle_click_stream PRIMARY KEY (id),
    CONSTRAINT FK_vle_click_stream_student FOREIGN KEY (guid_student_id)
        REFERENCES dbo.student_info (guid_student_id),
    CONSTRAINT FK_vle_click_stream_site FOREIGN KEY (guid_site_id, modulo, presentation)
        REFERENCES dbo.vle_modules (guid_site_id, code_module, code_presentation)
);
GO

CREATE INDEX IX_vle_click_stream_student ON dbo.vle_click_stream (guid_student_id);
CREATE INDEX IX_vle_click_stream_site ON dbo.vle_click_stream (guid_site_id);
GO

/* ------------------------------------------------------------
   assess_detail.csv - assessment submissions, denormalized with a
   student-demographics snapshot at submission time. No natural key
   in the source file, so a surrogate id is added.
   ------------------------------------------------------------ */
CREATE TABLE dbo.assess_detail (
    id                      BIGINT IDENTITY(1,1) NOT NULL,
    guid_student_id         UNIQUEIDENTIFIER NOT NULL,
    guid_assess_id          UNIQUEIDENTIFIER NOT NULL,
    date_submitted          DATETIME         NULL,
    is_banked               BIT              NOT NULL DEFAULT (0),
    score                   DECIMAL(6,2)     NULL,
    assessment_type         VARCHAR(10)      NULL,
    [date]                  DATETIME         NULL,
    weight                  TINYINT          NULL,
    gender                  VARCHAR(30)      NULL,
    region                  VARCHAR(30)      NULL,
    highest_education       VARCHAR(40)      NULL,
    imd_band                VARCHAR(10)      NULL,
    age_band                VARCHAR(10)      NULL,
    num_of_prev_attempts    TINYINT          NULL,
    studied_credits         SMALLINT         NULL,
    disability              CHAR(1)          NULL,
    final_result            VARCHAR(20)      NULL,
    status                  VARCHAR(20)      NULL,
    module                  VARCHAR(10)      NULL,
    presentation            VARCHAR(10)      NULL,
    date_real_days          SMALLINT         NULL,
    id_assetcode            INT              NULL,
    CONSTRAINT PK_assess_detail PRIMARY KEY (id),
    CONSTRAINT FK_assess_detail_student FOREIGN KEY (guid_student_id)
        REFERENCES dbo.student_info (guid_student_id),
    CONSTRAINT FK_assess_detail_assess_plan FOREIGN KEY (guid_assess_id)
        REFERENCES dbo.assess_plan (guid_assess_id)
);
GO

CREATE INDEX IX_assess_detail_student ON dbo.assess_detail (guid_student_id);
CREATE INDEX IX_assess_detail_assess ON dbo.assess_detail (guid_assess_id);
GO
