-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Gen 08, 2025 alle 10:38
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `progetto_security`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `documents`
--

CREATE TABLE `documents` (
  `DocumentID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `filename` varchar(30) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `documents`
--

INSERT INTO `documents` (`DocumentID`, `UserID`, `filename`, `date`) VALUES
(1, 1, 'book.pdf', '2025-01-07'),
(2, 1, 'prova.pdf', '2025-01-06'),
(3, 1, 'relazione.pdf', '2025-01-06');

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `mykey` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `users`
--

INSERT INTO `users` (`ID`, `name`, `username`, `password`, `mykey`) VALUES
(1, 'Edoardo Musmeci ', 'edoardo', '$2b$12$HUpeqcXftSEPV71cyd2Ec.qiaFw8d2eg1HpCPFT7iilZlpyRSA9P6', 0x526736104a82a2b79042b2d1c956da93cff5cbd55cf6ae2aeb2ead49d1bd2abc8a14e2690ecbeddd8c3a729f3ac10390ee0d84cf1e240b1458ebbfc4);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`DocumentID`),
  ADD KEY `FK_documents_ID` (`UserID`);

--
-- Indici per le tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `documents`
--
ALTER TABLE `documents`
  MODIFY `DocumentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4013;

--
-- AUTO_INCREMENT per la tabella `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `FK_documents_ID` FOREIGN KEY (`UserID`) REFERENCES `users` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
