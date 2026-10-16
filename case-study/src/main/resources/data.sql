-- Demo data. Book 2 is already borrowed; member 2 owes 5,000 VND.
INSERT INTO books (id, available) VALUES (1, TRUE);
INSERT INTO books (id, available) VALUES (2, FALSE);
INSERT INTO books (id, available) VALUES (3, TRUE);
INSERT INTO members (id, unpaid_fine) VALUES (1, 0);
INSERT INTO members (id, unpaid_fine) VALUES (2, 5000);
