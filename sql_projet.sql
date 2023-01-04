-- Supprime les tables "sport" et "type_sport" s'ils existent déjà
DROP TABLE IF EXISTS sport;
DROP TABLE IF EXISTS type_sport;

-- Crée la table "type_sport"
CREATE TABLE type_sport(
    id_type_sport int AUTO_INCREMENT,
    libelle VARCHAR(100),
    PRIMARY KEY(id_type_sport)
);

-- Crée la table "sport"
CREATE TABLE sport(
    id_sport int AUTO_INCREMENT,
    nom_sport VARCHAR(100),
    prix_inscription int,
    date_limite_inscription date,
    type_sport_id int,
    image VARCHAR(100),
    nb_pratiquants int,
    PRIMARY KEY(id_sport),
    CONSTRAINT fk_id_type_sport FOREIGN KEY(type_sport_id) REFERENCES type_sport(id_type_sport)
);

INSERT INTO type_sport(id_type_sport, libelle) VALUES
(NULL,'Ballon'),
(NULL,'Raquette'),
(NULL,'Combat'),
(NULL,'Aquatique');

INSERT INTO sport(id_sport, nom_sport,prix_inscription,date_limite_inscription,type_sport_id,image,nb_pratiquants) VALUES
(NULL,'Football',80,'2020-10-19',1,'foot.jpg',15),
(NULL,'Basketball',80,'2020-10-19',1,'basket.jpg',151),
(NULL,'Tennis de table',80,'2020-10-19',2,'tennisTable.jpg',5),
(NULL,'Tennis',85,'2020-10-19',2,'tennis.jpg',20),
(NULL,'Badminton',70,'2020-10-22',2,'badminton.png',22),
(NULL,'Judo',90,'2020-10-25',3,'judo.jpg',43),
(NULL,'Boxe',72.50,'2020-10-24',3,'boxe.jpg',52),
(NULL,'Karaté',60.99,'2020-10-23',3,'karaté.png',30),
(NULL,'Natation',30.30,'2020-10-30',4,'natation.jpg',100),
(NULL,'Kanoé',125.99,'2020-10-29',4,'kanoe.jpg',99),
(NULL,'Water Polo',31.90,'2020-09-19',4,'waterPolo.jpg',25),
(NULL,'Planche à voile',230,'2020-10-19',4,'planche.jpg',30),
(NULL,'Handball',10,'2020-08-19',1,'hand.jpg',22),
(NULL,'Volleyball',25,'2020-08-19',1,'volley.jpg',55),
(NULL,'Rugby',30.80,'2020-10-19',1,'rugby.jpg',60);

ALTER TABLE sport DROP FOREIGN KEY fk_id_type_sport;

ALTER TABLE sport
ADD FOREIGN KEY (type_sport_id) REFERENCES type_sport(id_type_sport);

-- avec left join --
SELECT ts.libelle, SUM(s.prix_inscription) AS total_inscriptions
FROM type_sport ts
LEFT JOIN sport s ON ts.id_type_sport = s.type_sport_id
GROUP BY ts.id_type_sport
HAVING total_inscriptions IS NOT NULL
ORDER BY total_inscriptions DESC;

-- avec right join --
SELECT ts.libelle, AVG(s.nb_pratiquants) AS moyenne_pratiquants
FROM type_sport ts
RIGHT JOIN sport s ON ts.id_type_sport = s.type_sport_id
GROUP BY ts.id_type_sport
HAVING moyenne_pratiquants IS NOT NULL
ORDER BY moyenne_pratiquants DESC;

