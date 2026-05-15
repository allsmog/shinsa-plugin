export function searchUsers(req, db) { return db.query("select * from users where email = '" + req.query.email + "'"); }
