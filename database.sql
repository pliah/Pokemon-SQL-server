USE sql_intro;

CREATE TABLE trainer(
    name VARCHAR(20),
    town VARCHAR(20),
    PRIMARY KEY(name,town)
);

CREATE TABLE poke_type(
    id INT PRIMARY KEY,
    type VARCHAR(20)
);

CREATE TABLE pokemon(
    id INT PRIMARY KEY,
    name VARCHAR(20),
    type INT
    height INT,
    weight INT,
    FOREIGN KEY (type) REFERENCES poke_type(id)
 );
CREATE TABLE owned_by(
    id INT,
    name VARCHAR(20),
    town  VARCHAR(20),
    FOREIGN KEY (name,town) REFERENCES trainer(name,town),
    FOREIGN KEY (id) REFERENCES pokemon(id),
    PRIMARY KEY(id,name,town)
);

