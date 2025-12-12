-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : ven. 12 déc. 2025 à 12:11
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `fms`
--

-- --------------------------------------------------------

--
-- Structure de la table `affectations`
--

DROP TABLE IF EXISTS `affectations`;
CREATE TABLE IF NOT EXISTS `affectations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `conducteur_id` int NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_affectation` (`vehicule_id`,`conducteur_id`,`date_debut`),
  KEY `conducteur_id` (`conducteur_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `affectations`
--

INSERT INTO `affectations` (`id`, `vehicule_id`, `conducteur_id`, `date_debut`, `date_fin`, `created_at`, `updated_at`) VALUES
(1, 2, 1, '2025-12-09', NULL, NULL, NULL),
(2, 5, 2, '2025-12-12', NULL, NULL, NULL),
(3, 6, 4, '2025-12-01', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `alertes_email`
--

DROP TABLE IF EXISTS `alertes_email`;
CREATE TABLE IF NOT EXISTS `alertes_email` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_destinataire` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `type_alerte` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'assurance, taxe circulation, entretient, visite technique [cite: 1]',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `anomalies`
--

DROP TABLE IF EXISTS `anomalies`;
CREATE TABLE IF NOT EXISTS `anomalies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `conducteur_id` int NOT NULL,
  `type_anomalie` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Mécanique, Accident, Autre',
  `description` text COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Formulaire simple pour signaler un problème [cite: 58]',
  `statut` varchar(50) COLLATE utf8mb4_general_ci DEFAULT 'Signalé' COMMENT 'Signalé, En cours, Résolu',
  `date_declaration` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `photo_path` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Possibilité d''attacher des photos [cite: 59]',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `vehicule_id` (`vehicule_id`),
  KEY `conducteur_id` (`conducteur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `assurances`
--

DROP TABLE IF EXISTS `assurances`;
CREATE TABLE IF NOT EXISTS `assurances` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `fournisseur_id` int DEFAULT NULL COMMENT 'Assureur [cite: 3]',
  `date_assurance` date NOT NULL,
  `expiration_assurance` date NOT NULL,
  `rappel_avant_jours` int NOT NULL COMMENT 'Rappel avnt (jours) [cite: 3]',
  `note` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `vehicule_id` (`vehicule_id`),
  KEY `fournisseur_id` (`fournisseur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add role', 7, 'add_role'),
(26, 'Can change role', 7, 'change_role'),
(27, 'Can delete role', 7, 'delete_role'),
(28, 'Can view role', 7, 'view_role'),
(29, 'Can add user', 8, 'add_user'),
(30, 'Can change user', 8, 'change_user'),
(31, 'Can delete user', 8, 'delete_user'),
(32, 'Can view user', 8, 'view_user'),
(33, 'Can add affectation', 9, 'add_affectation'),
(34, 'Can change affectation', 9, 'change_affectation'),
(35, 'Can delete affectation', 9, 'delete_affectation'),
(36, 'Can view affectation', 9, 'view_affectation'),
(37, 'Can add conducteur', 10, 'add_conducteur'),
(38, 'Can change conducteur', 10, 'change_conducteur'),
(39, 'Can delete conducteur', 10, 'delete_conducteur'),
(40, 'Can view conducteur', 10, 'view_conducteur'),
(41, 'Can add departement', 11, 'add_departement'),
(42, 'Can change departement', 11, 'change_departement'),
(43, 'Can delete departement', 11, 'delete_departement'),
(44, 'Can view departement', 11, 'view_departement'),
(45, 'Can add vehicule', 12, 'add_vehicule'),
(46, 'Can change vehicule', 12, 'change_vehicule'),
(47, 'Can delete vehicule', 12, 'delete_vehicule'),
(48, 'Can view vehicule', 12, 'view_vehicule'),
(49, 'Can add alerte email', 13, 'add_alerteemail'),
(50, 'Can change alerte email', 13, 'change_alerteemail'),
(51, 'Can delete alerte email', 13, 'delete_alerteemail'),
(52, 'Can view alerte email', 13, 'view_alerteemail'),
(53, 'Can add anomalie', 14, 'add_anomalie'),
(54, 'Can change anomalie', 14, 'change_anomalie'),
(55, 'Can delete anomalie', 14, 'delete_anomalie'),
(56, 'Can view anomalie', 14, 'view_anomalie'),
(57, 'Can add assurance', 15, 'add_assurance'),
(58, 'Can change assurance', 15, 'change_assurance'),
(59, 'Can delete assurance', 15, 'delete_assurance'),
(60, 'Can view assurance', 15, 'view_assurance'),
(61, 'Can add carburant', 16, 'add_carburant'),
(62, 'Can change carburant', 16, 'change_carburant'),
(63, 'Can delete carburant', 16, 'delete_carburant'),
(64, 'Can view carburant', 16, 'view_carburant'),
(65, 'Can add detail depense', 17, 'add_detaildepense'),
(66, 'Can change detail depense', 17, 'change_detaildepense'),
(67, 'Can delete detail depense', 17, 'delete_detaildepense'),
(68, 'Can view detail depense', 17, 'view_detaildepense'),
(69, 'Can add entretien', 18, 'add_entretien'),
(70, 'Can change entretien', 18, 'change_entretien'),
(71, 'Can delete entretien', 18, 'delete_entretien'),
(72, 'Can view entretien', 18, 'view_entretien'),
(73, 'Can add entretien maitre', 19, 'add_entretienmaitre'),
(74, 'Can change entretien maitre', 19, 'change_entretienmaitre'),
(75, 'Can delete entretien maitre', 19, 'delete_entretienmaitre'),
(76, 'Can view entretien maitre', 19, 'view_entretienmaitre'),
(77, 'Can add taxe circulation', 20, 'add_taxecirculation'),
(78, 'Can change taxe circulation', 20, 'change_taxecirculation'),
(79, 'Can delete taxe circulation', 20, 'delete_taxecirculation'),
(80, 'Can view taxe circulation', 20, 'view_taxecirculation'),
(81, 'Can add visite technique', 21, 'add_visitetechnique'),
(82, 'Can change visite technique', 21, 'change_visitetechnique'),
(83, 'Can delete visite technique', 21, 'delete_visitetechnique'),
(84, 'Can view visite technique', 21, 'view_visitetechnique'),
(85, 'Can add fournisseur', 22, 'add_fournisseur'),
(86, 'Can change fournisseur', 22, 'change_fournisseur'),
(87, 'Can delete fournisseur', 22, 'delete_fournisseur'),
(88, 'Can view fournisseur', 22, 'view_fournisseur'),
(89, 'Can add piece', 23, 'add_piece'),
(90, 'Can change piece', 23, 'change_piece'),
(91, 'Can delete piece', 23, 'delete_piece'),
(92, 'Can view piece', 23, 'view_piece');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1200000$k78J47qYtQCiEITpm6fJz9$l3BSa+jAYP5XH+x6CNeG6GzMNlAE/6k423um8jym1hE=', '2025-12-10 10:20:53.687692', 1, 'admin', '', '', 'admin@fms.com', 1, 1, '2025-12-10 10:20:02.933694');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `carburants`
--

DROP TABLE IF EXISTS `carburants`;
CREATE TABLE IF NOT EXISTS `carburants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `fournisseur_id` int DEFAULT NULL,
  `date_plein` datetime NOT NULL COMMENT 'Date, Heure [cite: 35]',
  `kilometrage` int NOT NULL COMMENT 'Kilométrage au moment du plein [cite: 35]',
  `quantite` decimal(8,2) NOT NULL COMMENT 'Quantité (Litres) [cite: 35]',
  `prix_unitaire` decimal(6,3) NOT NULL COMMENT 'Prix unitaire [cite: 35]',
  `station_service` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `vehicule_id` (`vehicule_id`),
  KEY `fournisseur_id` (`fournisseur_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `carburants`
--

INSERT INTO `carburants` (`id`, `vehicule_id`, `fournisseur_id`, `date_plein`, `kilometrage`, `quantite`, `prix_unitaire`, `station_service`, `created_at`, `updated_at`) VALUES
(1, 2, 4, '2025-12-11 16:13:00', 100000, 10000.00, 650.000, NULL, NULL, NULL),
(2, 6, 4, '2025-12-13 19:45:00', 10000, 10.00, 800.000, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `conducteurs`
--

DROP TABLE IF EXISTS `conducteurs`;
CREATE TABLE IF NOT EXISTS `conducteurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `prenom` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `date_naissance` date DEFAULT NULL,
  `date_embauche` date DEFAULT NULL,
  `numero_permis` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `adresse` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Adresse/quartier [cite: 2]',
  `ville` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tel1` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tel2` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_permis` (`numero_permis`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `conducteurs`
--

INSERT INTO `conducteurs` (`id`, `nom`, `prenom`, `date_naissance`, `date_embauche`, `numero_permis`, `adresse`, `ville`, `tel1`, `tel2`, `email`, `created_at`, `updated_at`) VALUES
(1, 'Kouedi Kouedi', 'Gaitan Emmanuel', '2025-12-10', '2025-12-08', 'QCELT202568', 'akwa boulevard de la république', 'DOUALA', '658956855', NULL, 'g.kouedi90@gmail.com', NULL, NULL),
(2, 'DJAMILA', 'DIALLO', '2025-12-01', '2025-12-01', 'QCELT202566', 'akwa boulevard de la république', 'DOUALA', '658956855', NULL, 'g.kouedi90@gmail.co', NULL, NULL),
(3, 'BEYAS', 'DIALLO DJAMILA', '2025-12-01', '2025-12-10', 'KCELT202568', 'akwa boulevard de la république', 'DOUALA', '658956855', NULL, 'g.kuedi90@gmail.com', NULL, NULL),
(4, 'XXZZZZZGaitan Emmanuel', 'Kouedi Kouedi', '2025-12-01', '2025-12-25', 'QCELT202511', 'Nouvelle route Nkolbisson', 'Yaoundé', '658956855', NULL, 'kouedigaitanemmanuel@gmail.com', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `departements`
--

DROP TABLE IF EXISTS `departements`;
CREATE TABLE IF NOT EXISTS `departements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `departements`
--

INSERT INTO `departements` (`id`, `nom`, `created_at`, `updated_at`) VALUES
(3, 'LOCATION', NULL, NULL),
(4, 'COMMUNICATION', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `detail_depenses`
--

DROP TABLE IF EXISTS `detail_depenses`;
CREATE TABLE IF NOT EXISTS `detail_depenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `entretien_id` int NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Description de la dépense (Pièce, Main d''oeuvre, etc.) [cite: 3]',
  `quantite` int NOT NULL,
  `cout_unitaire` decimal(10,2) NOT NULL,
  `piece_id` int DEFAULT NULL COMMENT 'Lien vers une pièce si c''est un remplacement de pièce',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `entretien_id` (`entretien_id`),
  KEY `piece_id` (`piece_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

--
-- Déchargement des données de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-12-10 21:51:29.857481', '3', 'admin admin (admin2)', 1, '[{\"added\": {}}]', 8, 2),
(2, '2025-12-10 21:51:58.054969', '4', 'admin3 admin3 (admin3)', 1, '[{\"added\": {}}]', 8, 2);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'utilisateurs', 'role'),
(8, 'utilisateurs', 'user'),
(9, 'flotte', 'affectation'),
(10, 'flotte', 'conducteur'),
(11, 'flotte', 'departement'),
(12, 'flotte', 'vehicule'),
(13, 'maintenance', 'alerteemail'),
(14, 'maintenance', 'anomalie'),
(15, 'maintenance', 'assurance'),
(16, 'maintenance', 'carburant'),
(17, 'maintenance', 'detaildepense'),
(18, 'maintenance', 'entretien'),
(19, 'maintenance', 'entretienmaitre'),
(20, 'maintenance', 'taxecirculation'),
(21, 'maintenance', 'visitetechnique'),
(22, 'fournisseurs', 'fournisseur'),
(23, 'fournisseurs', 'piece');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-12-10 10:18:28.392599'),
(2, 'auth', '0001_initial', '2025-12-10 10:18:28.913458'),
(3, 'admin', '0001_initial', '2025-12-10 10:18:29.156327'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-12-10 10:18:29.169339'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-10 10:18:29.184892'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-12-10 10:18:29.285799'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-12-10 10:18:29.337347'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-12-10 10:18:29.390777'),
(9, 'auth', '0004_alter_user_username_opts', '2025-12-10 10:18:29.406565'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-12-10 10:18:29.462666'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-12-10 10:18:29.464077'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-12-10 10:18:29.478877'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-12-10 10:18:29.529449'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-12-10 10:18:29.576929'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-12-10 10:18:29.624729'),
(16, 'auth', '0011_update_proxy_permissions', '2025-12-10 10:18:29.637986'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-12-10 10:18:29.699511'),
(18, 'flotte', '0001_initial', '2025-12-10 10:18:29.716587'),
(19, 'fournisseurs', '0001_initial', '2025-12-10 10:18:29.728654'),
(20, 'maintenance', '0001_initial', '2025-12-10 10:18:29.766035'),
(21, 'sessions', '0001_initial', '2025-12-10 10:18:29.823111'),
(22, 'utilisateurs', '0001_initial', '2025-12-10 10:18:29.833560'),
(23, 'utilisateurs', '0002_alter_user_options', '2025-12-10 10:41:32.749907');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('rafp1ieky9w2fkyf7m00udaicij5e96o', '.eJxVjMEOwiAQRP-FsyEBlrJ49O43kAUWqRqalPbU-O-2SQ86x3lvZhOB1qWGtfMcxiyuQonLbxcpvbgdID-pPSaZprbMY5SHIk_a5X3K_L6d7t9BpV739VDIO5UTqmSyN6Aosy0-lkEjaGPZMqDThpWPgHt8IWQgzRoUghOfL-K5N2k:1vTHJU:GLJ16J-AScwe-i_p5fgLqhAGhKHGYrXAjbRuwxoNs3M', '2025-12-24 10:20:52.855142'),
('7015sq4p84p68h4c6kkxvk3tw8isphbl', '.eJxVjDsOwjAQBe_iGln-O6ak5wzWZr2LA8iR4qRC3B0ipYD2zcx7iQzbWvPWaclTEWdhxOl3GwEf1HZQ7tBus8S5rcs0yl2RB-3yOhd6Xg7376BCr98aKEXlFQw2AqcUw1Cs5cgmaW80Mmn0rIhtRFWMJ8SEoSjHKaBj48T7A-G1OBg:1vTSPC:WXikm3JdubH9IwR1QjnI4sYwQ7MpOEd8lmppD0IqV2A', '2025-12-24 22:11:30.634492'),
('ra7fb57bharzogu0k4nqqsyqjm3m9iw4', '.eJxVjDsOwjAQBe_iGln-O6ak5wzWZr2LA8iR4qRC3B0ipYD2zcx7iQzbWvPWaclTEWdhxOl3GwEf1HZQ7tBus8S5rcs0yl2RB-3yOhd6Xg7376BCr98aKEXlFQw2AqcUw1Cs5cgmaW80Mmn0rIhtRFWMJ8SEoSjHKaBj48T7A-G1OBg:1vU0xY:Chn2JWVExXC1DWAgJX9nRNi1cQp2D4tIAV_gHaMloiM', '2025-12-26 11:05:16.964081');

-- --------------------------------------------------------

--
-- Structure de la table `entretiens`
--

DROP TABLE IF EXISTS `entretiens`;
CREATE TABLE IF NOT EXISTS `entretiens` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `fournisseur_id` int DEFAULT NULL,
  `entretien_maitre_id` int DEFAULT NULL COMMENT 'Plan d''entretien utilisé',
  `description` text COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Détail de l''entretien [cite: 3]',
  `date_entretien` date NOT NULL COMMENT 'Date de l''entretien [cite: 3]',
  `kilometrage` int NOT NULL COMMENT 'Kilométrage au moment de l''entretien [cite: 3]',
  `note` text COLLATE utf8mb4_general_ci,
  `depense_type` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Ex: Vidange, Réparation [cite: 39]',
  `cout_total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `vehicule_id` (`vehicule_id`),
  KEY `fournisseur_id` (`fournisseur_id`),
  KEY `entretien_maitre_id` (`entretien_maitre_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `entretien_maitres`
--

DROP TABLE IF EXISTS `entretien_maitres`;
CREATE TABLE IF NOT EXISTS `entretien_maitres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `repeter_par_date` int DEFAULT NULL COMMENT 'Répéter toutes (jours) [cite: 3]',
  `repeter_par_kilometrage` int DEFAULT NULL COMMENT 'Répéter au kilométrage (km) [cite: 3]',
  `rappel_avant_jours` int DEFAULT NULL COMMENT 'Rappel avant (jours) [cite: 3]',
  `rappel_avant_kilometrage` int DEFAULT NULL COMMENT 'Rappel avant (km) [cite: 3]',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fournisseurs`
--

DROP TABLE IF EXISTS `fournisseurs`;
CREATE TABLE IF NOT EXISTS `fournisseurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `type_activite` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'vente vehicule, location vehicule, assureur, vente pièce auto, entretien, reparation, vente carburant [cite: 1]',
  `contact` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tel1` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tel2` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ville` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `site_web` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type_fournisseur` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Type (à affiner si nécessaire) [cite: 1]',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `fournisseurs`
--

INSERT INTO `fournisseurs` (`id`, `nom`, `type_activite`, `contact`, `tel1`, `tel2`, `ville`, `site_web`, `email`, `type_fournisseur`, `created_at`, `updated_at`) VALUES
(2, 'Gaitan Emmanuel Kouedi Kouedi', 'vente_vehicule', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'DOUALA', NULL, 'g.kouedi90@gmail.com', NULL, NULL, NULL),
(4, 'Kouedi Gaitan Emmanuel', 'vente_carburant', 'Kouedi Gaitan Emmanuel', '658956855', NULL, 'DOUALA', NULL, NULL, NULL, NULL, NULL),
(5, 'LOCAKouedi Kouedi Gaitan Emmanuel', 'location_vehicule', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'Yaoundé', NULL, 'kouedigaitanemmanuel@gmail.com', NULL, NULL, NULL),
(6, 'Gaitan Emmanuel Kouedi Kouedi', 'assureur', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'DOUALA', NULL, 'g.kouedi90@gmail.com', NULL, NULL, NULL),
(7, 'Gaitan Emmanuel Kouedi Kouedi', 'vente_piece_auto', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'DOUALA', NULL, 'g.kouedi90@gmail.com', NULL, NULL, NULL),
(8, 'Gaitan Emmanuel Kouedi Kouedi', 'entretien', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'DOUALA', NULL, 'g.kouedi90@gmail.com', NULL, NULL, NULL),
(9, 'Gaitan Emmanuel Kouedi Kouedi', 'reparation', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'DOUALA', NULL, 'g.kouedi90@gmail.com', NULL, NULL, NULL),
(10, 'Gaitan Emmanuel Kouedi Kouedi', 'autre', 'Gaitan Emmanuel Kouedi Kouedi', '658956855', NULL, 'DOUALA', NULL, 'g.kouedi90@gmail.com', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `pieces`
--

DROP TABLE IF EXISTS `pieces`;
CREATE TABLE IF NOT EXISTS `pieces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fournisseur_id` int DEFAULT NULL,
  `constructeur` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Constructeur de la pièce [cite: 1]',
  `numero` varchar(150) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Numéro de la pièce [cite: 1]',
  `nom` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `prix` decimal(10,2) NOT NULL COMMENT 'Prix unitaire [cite: 1]',
  `date_prix` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fournisseur_id` (`fournisseur_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `pieces`
--

INSERT INTO `pieces` (`id`, `fournisseur_id`, `constructeur`, `numero`, `nom`, `prix`, `date_prix`, `created_at`, `updated_at`) VALUES
(1, 7, 'TOYOTA', '120689', 'Kouedi Kouedi', 15000.00, '2025-12-10', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Administrateur Système, Gestionnaire Flotte, Chauffeur/Opérateur',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `roles`
--

INSERT INTO `roles` (`id`, `nom`, `created_at`, `updated_at`) VALUES
(4, 'Administrateur Système', '2025-12-10 08:22:18', '2025-12-10 08:22:18'),
(5, 'Gestionnaire Flotte', '2025-12-10 08:22:18', '2025-12-10 08:22:18'),
(6, 'Chauffeur/Opérateur', '2025-12-10 08:22:18', '2025-12-10 08:22:18');

-- --------------------------------------------------------

--
-- Structure de la table `taxes_circulation`
--

DROP TABLE IF EXISTS `taxes_circulation`;
CREATE TABLE IF NOT EXISTS `taxes_circulation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `date_taxe_circulation` date NOT NULL,
  `expiration` date NOT NULL,
  `rappel_avant_jours` int NOT NULL COMMENT 'Rappel avant (jours) [cite: 3]',
  `note` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `vehicule_id` (`vehicule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `prenom` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'username/login',
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `fonction` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Fonction de l''utilisateur [cite: 1]',
  `role_id` int NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `remember_token` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0',
  `is_staff` tinyint(1) NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `groups_id` bigint DEFAULT NULL,
  `user_permissions_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `nom`, `prenom`, `username`, `email`, `password`, `fonction`, `role_id`, `email_verified_at`, `remember_token`, `created_at`, `updated_at`, `last_login`, `is_superuser`, `is_staff`, `is_active`, `groups_id`, `user_permissions_id`) VALUES
(1, 'System', 'Admin', 'admin', 'admin@fms.com', '$2y$12$mnNpvMkuMQhb4jgUaAOnTuDphAH8v4JU4XX787.96c140Mp1NjwC6', 'Administrateur Système', 4, NULL, NULL, '2025-12-10 07:22:18', '2025-12-10 07:22:18', NULL, 0, 0, 1, NULL, NULL),
(2, 'Administrateur', 'Administrateur', 'admin1', 'admin1@fms.com', 'pbkdf2_sha256$1200000$DzP6YbU36tbimKliwtOFWo$xyzzyFcYBQZjSS/DzIBk34GPl1qmO9hi3cqtJwrNr3U=', NULL, 4, NULL, NULL, NULL, '2025-12-12 11:05:16', '2025-12-12 11:05:17', 1, 1, 1, NULL, NULL),
(3, 'admin', 'admin', 'admin2', 'admin2@fms.com', 'pbkdf2_sha256$1200000$eqhNeYnOBLoQ2qUzR1wWeV$AjshNF7BRhCJjyNvbjfNaWeQBtohWCjHFjnxXtlXa1Q=', NULL, 5, NULL, NULL, NULL, '2025-12-10 22:10:54', '2025-12-10 22:10:54', 0, 0, 1, NULL, NULL),
(4, 'admin3', 'admin3', 'admin3', 'admin3@fms.com', 'pbkdf2_sha256$1200000$9E4RixCvFmDeQNrc0oiEkt$w8HcdDDCD3j+ehssCkJBpdBXzS2s06BjCUKXr5W8ioA=', NULL, 6, NULL, NULL, NULL, '2025-12-11 16:41:02', '2025-12-11 16:41:02', 0, 0, 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `vehicules`
--

DROP TABLE IF EXISTS `vehicules`;
CREATE TABLE IF NOT EXISTS `vehicules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `matricule` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Plaque d''immatriculation [cite: 2, 28]',
  `marque` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `modele` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `couleur` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_serie` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'N* Série [cite: 2]',
  `date_mise_circulation` date DEFAULT NULL COMMENT 'Année [cite: 2, 28]',
  `type_vehicule` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '4x4, berline, citadine, coupé, etc. [cite: 2]',
  `type_carburant` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'essence, diesel, etc. [cite: 2, 28]',
  `kilometrage_initial` int DEFAULT '0' COMMENT 'Kilométrage initial [cite: 28]',
  `actif` tinyint(1) DEFAULT '1' COMMENT 'Véhicule actif ou pas [cite: 2]',
  `departement_id` int DEFAULT NULL,
  `location_oui_non` tinyint(1) DEFAULT '0' COMMENT 'Gestion des achats/location [cite: 2]',
  `date_achat_location` date DEFAULT NULL COMMENT 'date achat/location [cite: 3]',
  `prix_achat_location` decimal(10,2) DEFAULT NULL COMMENT 'prix achat/location [cite: 3]',
  `expiration_garantie` date DEFAULT NULL,
  `prix_vente` decimal(10,2) DEFAULT NULL COMMENT 'prix vente (si revendu) [cite: 3]',
  `note` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `matricule` (`matricule`),
  UNIQUE KEY `numero_serie` (`numero_serie`),
  KEY `departement_id` (`departement_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `vehicules`
--

INSERT INTO `vehicules` (`id`, `matricule`, `marque`, `modele`, `couleur`, `numero_serie`, `date_mise_circulation`, `type_vehicule`, `type_carburant`, `kilometrage_initial`, `actif`, `departement_id`, `location_oui_non`, `date_achat_location`, `prix_achat_location`, `expiration_garantie`, `prix_vente`, `note`, `created_at`, `updated_at`) VALUES
(2, 'DDDDDDDD', 'AAA', 'QQQQROUGE', 'ROUGE', '12345678', '2025-12-10', 'CCC', 'WWW', 1000, 1, 4, 1, '2025-12-11', 10000000.00, '2025-12-16', NULL, '', NULL, NULL),
(5, 'DDDDDDDZ', 'DJAMI', 'QQQQROUGE', 'ROUGE', '12345669', NULL, 'CCC', 'DIESEL', 10000, 0, 3, 0, '2025-12-10', 100000.00, '2025-12-12', NULL, '', NULL, NULL),
(6, '16J288JJ', 'DJAMILATOU', 'BERLINE', 'ROSE', '12345664', '2025-12-13', 'CCC', 'DIESEL', 100000, 0, 4, 0, '2025-12-21', 10000000.00, '2025-12-25', NULL, '', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `visites_techniques`
--

DROP TABLE IF EXISTS `visites_techniques`;
CREATE TABLE IF NOT EXISTS `visites_techniques` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicule_id` int NOT NULL,
  `derniere_visite` date NOT NULL,
  `prochaine_visite` date NOT NULL,
  `rappel_avant_jours` int NOT NULL COMMENT 'Rappel avant (jours) [cite: 3]',
  `note` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `vehicule_id` (`vehicule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `affectations`
--
ALTER TABLE `affectations`
  ADD CONSTRAINT `affectations_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `affectations_ibfk_2` FOREIGN KEY (`conducteur_id`) REFERENCES `conducteurs` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `anomalies`
--
ALTER TABLE `anomalies`
  ADD CONSTRAINT `anomalies_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `anomalies_ibfk_2` FOREIGN KEY (`conducteur_id`) REFERENCES `conducteurs` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `assurances`
--
ALTER TABLE `assurances`
  ADD CONSTRAINT `assurances_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `assurances_ibfk_2` FOREIGN KEY (`fournisseur_id`) REFERENCES `fournisseurs` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `carburants`
--
ALTER TABLE `carburants`
  ADD CONSTRAINT `carburants_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `carburants_ibfk_2` FOREIGN KEY (`fournisseur_id`) REFERENCES `fournisseurs` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `detail_depenses`
--
ALTER TABLE `detail_depenses`
  ADD CONSTRAINT `detail_depenses_ibfk_1` FOREIGN KEY (`entretien_id`) REFERENCES `entretiens` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `detail_depenses_ibfk_2` FOREIGN KEY (`piece_id`) REFERENCES `pieces` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `entretiens`
--
ALTER TABLE `entretiens`
  ADD CONSTRAINT `entretiens_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entretiens_ibfk_2` FOREIGN KEY (`fournisseur_id`) REFERENCES `fournisseurs` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `entretiens_ibfk_3` FOREIGN KEY (`entretien_maitre_id`) REFERENCES `entretien_maitres` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `pieces`
--
ALTER TABLE `pieces`
  ADD CONSTRAINT `pieces_ibfk_1` FOREIGN KEY (`fournisseur_id`) REFERENCES `fournisseurs` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `taxes_circulation`
--
ALTER TABLE `taxes_circulation`
  ADD CONSTRAINT `taxes_circulation_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT;

--
-- Contraintes pour la table `vehicules`
--
ALTER TABLE `vehicules`
  ADD CONSTRAINT `vehicules_ibfk_1` FOREIGN KEY (`departement_id`) REFERENCES `departements` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `visites_techniques`
--
ALTER TABLE `visites_techniques`
  ADD CONSTRAINT `visites_techniques_ibfk_1` FOREIGN KEY (`vehicule_id`) REFERENCES `vehicules` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
