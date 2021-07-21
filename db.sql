CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `expense` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(100) NULL,
  `amount` FLOAT NOT NULL,
  `expense_category` VARCHAR(100) NOT NULL,
  `is_recurring` TINYINT NOT NULL DEFAULT 0,
  `date` DATE NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
);

CREATE TABLE `expense_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `income` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(100) NULL,
  `amount` FLOAT NOT NULL,
  `income_category` VARCHAR(100) NOT NULL,
  `is_recurring` TINYINT NOT NULL DEFAULT 0,
  `date` DATE NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `income_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
);

CREATE TABLE `expense_category_limit` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `amount` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_id_fk2`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`),
  CONSTRAINT `category_id_fk`
    FOREIGN KEY (`category_id`)
    REFERENCES `expense_category` (`id`)
);
