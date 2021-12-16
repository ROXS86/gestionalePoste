DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS mansioni;
DROP TABLE IF EXISTS corsi;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cognome TEXT NOT NULL,
  nome TEXT NOT NULL,
  data_nascita TEXT NOT NULL,
  luogo_nascita TEXT NOT NULL,
  residenza TEXT NOT NULL,
  residenza_cap TEXT NOT NULL,
  residenza_via TEXT NOT NULL,
  domicilio TEXT NULL,
  domicilio_cap TEXT NULL,
  domicilio_via TEXT NULL,
  telefono TEXT NULL,
  cell TEXT NULL,
  cf TEXT NULL,
  asl TEXT NULL,
  matricola TEXT NOT NULL,
  data_assunzione TEXT NOT NULL,
  data_fine TEXT NULL,
  titolo_uno TEXT NULL,
  titolo_due TEXT NULL,
  titolo_tre TEXT NULL,
  titolo_quattro TEXT NULL

);

CREATE TABLE mansioni (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mansioni_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  descrizione TEXT NOT NULL,
  dal TEXT NOT NULL,
  al TEXT NULL,
  ufficio TEXT NULL,
  FOREIGN KEY (mansioni_id) REFERENCES user (id)
);

CREATE TABLE corsi (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  corsi_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  descrizione TEXT NOT NULL,
  dal TEXT NOT NULL,
  al TEXT NULL,
  valutazione TEXT NULL,
  data_val TEXT NULL,
  esito TEXT NULL,
  FOREIGN KEY (corsi_id) REFERENCES user (id)
);