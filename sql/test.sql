
-- test user data
DELETE FROM Users;
INSERT INTO Users VALUES
  ('0000000000', 'Jhon', 'Doe', 'john.doe@example.com', now(), now(), 0),
  ('1111111111', 'Jane', 'Doe', 'jane.doe@example.com', now(), now(), 0),
  ('2222222222', 'Jim', 'James', 'jim.james@4chan.org', now(), now(), 0);

DELETE FROM Events;
INSERT INTO Events VALUES
  ('aaaaaaaaaa', '1111111111', 'title', 'desc', now(), now(), now(), now(), 0);

DELETE FROM rUserToEvent;
INSERT INTO rUserToEvent VALUES
  ('0000000000', 'aaaaaaaaaa', 0, 0, 0);
