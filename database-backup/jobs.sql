CREATE TABLE jobs (
    id integer primary key autoincrement,
    title text not null,
    isNew text not null,
    company text not null,
    companyLogoUrl text not null,
    timePosted text not null,
    timeExpired text not null,
    salary text not null,
    located text not null,
    preDescription text not null,
    fullDescription text not null,
    keywords text not null,
    applications text not null,
    jobUrl text not null
);