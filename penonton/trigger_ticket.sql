-- Stored Procedure to Validate Ticket
CREATE OR REPLACE FUNCTION validate_ticket() RETURNS TRIGGER AS $$
DECLARE
  ticketNum INT;
  capacity INT;
  ticketSoldNum INT;
BEGIN
  SELECT COUNT(*) INTO ticketNum
  FROM PEMBELIAN_TIKET
  WHERE id_penonton = NEW.id_penonton
    AND id_pertandingan = NEW.id_pertandingan
  GROUP BY id_penonton;
  
  SELECT S.kapasitas INTO capacity
  FROM PERTANDINGAN P
  JOIN STADIUM S ON P.stadium = S.id_stadium
  WHERE P.id_pertandingan = NEW.id_pertandingan;
  
  SELECT COUNT(*) INTO ticketSoldNum
  FROM PEMBELIAN_TIKET
  WHERE id_pertandingan = NEW.id_pertandingan
  GROUP BY id_pertandingan;
  
  IF (ticketSoldNum >= capacity) THEN
    RAISE EXCEPTION 'Tiket untuk pertandingan ini telah habis';
  END IF;
  
  IF (ticketNum >= 5) THEN
    RAISE EXCEPTION 'Hanya dapat memesan 5 tiket untuk 1 pertandingan';
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER cek_validate_tiket 
BEFORE INSERT ON PEMBELIAN_TIKET
FOR EACH ROW EXECUTE FUNCTION validate_ticket();
